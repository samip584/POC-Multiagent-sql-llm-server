import os
import operator
import functools
from enum import Enum
from config.config import settings  

from typing import Annotated, Sequence, TypedDict, List, Optional, Dict, Any

from langchain import hub
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.chains.openai_functions import create_structured_output_runnable

from langchain.agents import create_openai_tools_agent, AgentExecutor, load_tools

from langchain_openai import ChatOpenAI
from langchain_core.agents import AgentFinish
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.graph import StateGraph, END

from app.common.minio_client import minio_client

members = ["Assistant", "SQL", "Recommender"]

# Define agent capabilities for better routing
AGENT_DESCRIPTIONS = {
    "SQL": "Expert in querying the database for users, posts, places, follows, media, and timeline data. Handles questions about 'who', 'what', 'where', 'when' related to app data. Can retrieve image URLs from MinIO storage.",
    "Recommender": "Provides personalized recommendations for places to visit, users to follow, and content based on user preferences and behavior.",
    "Assistant": "General assistant for greetings, explanations, and non-database queries. Handles web search and calculations."
}

def format_media_urls(media_data: list) -> str:
    """Format media/image data with MinIO URLs for frontend rendering.
    
    Args:
        media_data: List of media records from database with external_resource_url
        
    Returns:
        Formatted string with image URLs
    """
    if not media_data:
        return "No images available."
    
    formatted = []
    for item in media_data:
        if isinstance(item, dict):
            url = item.get('external_resource_url')
            media_id = item.get('id')
        else:
            url = getattr(item, 'external_resource_url', None)
            media_id = getattr(item, 'id', None)
        
        if url:
            # Ensure URL is accessible (convert internal minio:9000 to localhost:9000 for dev)
            public_url = url.replace('minio:9000', 'localhost:9000')
            formatted.append(f"![Image {media_id}]({public_url})")
    
    return "\n".join(formatted)

def get_minio_url(key: str) -> str:
    """Get public MinIO URL for a file key.
    
    Args:
        key: S3 object key (file path in MinIO)
        
    Returns:
        Public URL accessible from frontend
    """
    url = minio_client.get_file_url(key)
    # Convert internal URL to public URL for development
    return url.replace('minio:9000', 'localhost:9000')

class AgentState(TypedDict):
  # The annotation tells the graph that new messages will always
  # be added to the current states
  messages: Annotated[Sequence[BaseMessage], operator.add]
  # The 'next' field indicates where to route to next
  next: str
  # User context
  user_id: int
  # Track query classification
  query_type: str
  # Track iteration count to prevent infinite loops
  iteration_count: int
  # Cache for intermediate results
  cached_data: Dict[str, Any]
  # Track which agents have already responded
  agents_used: Annotated[Sequence[str], operator.add]
  # Chat history for conversation context
  chat_history: List[Dict[str, str]]

class FinalResponse(BaseModel):

  response: str = Field(
      response="Final accumulated response to send the user"
  )


class GraphService:
  # Class-level cache for agents (singleton pattern)
  _instance = None
  _initialized = False
  
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(GraphService, cls).__new__(cls)
    return cls._instance
  
  def __init__(self):
    # Skip re-initialization if already done
    if GraphService._initialized:
      return
      
    print(settings.get_database_uri())
    
    db = SQLDatabase.from_uri(settings.get_database_uri())
    # Get the prompt to use - you can modify this!
    prompt = hub.pull("hwchase17/openai-functions-agent")
    os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY

    # Use temperature for more consistent responses
    self.model = ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY, temperature=0.3)
    
    # Max iterations to prevent infinite loops
    self.max_iterations = 5
    
    self.tools = load_tools(["serpapi", "llm-math"], self.model, serpapi_api_key=settings.SERPAPI_API_KEY)
    self.tools.append(TavilySearchResults(max_results=5))
    self.chat_agent = AgentExecutor(agent= create_openai_tools_agent(self.model, self.tools, prompt), tools=self.tools)
    
    # Enhanced SQL agent with better instructions
    self.sql_agent = create_sql_agent(
        self.model, 
        db=db, 
        agent_type="openai-tools",
        verbose=True,
        prefix="""You are a helpful, friendly assistant with access to a database. Talk like a real person having a conversation!

Available tables: users, posts, places, follows, media, timeline

**Schema Information**:
- posts table: id, user_id, media_id, caption, timestamp
- media table: id, external_resource_url (image URLs), meta (JSON with tags)
- users table: id, username, email, bio, avatar_url
- places table: id, name, description, latitude, longitude, address, category
- follows table: id, follower_id, following_id, timestamp
- timeline table: id, user_id, post_id, timestamp

**Your Mission**:
1. Query the database to find what the user needs
2. Respond in a warm, conversational way - like you're chatting with a friend!
3. When posts or users are mentioned, JOIN with media table to get images
4. Use casual language, contractions, and be enthusiastic
5. DON'T mention SQL queries, database operations, or technical stuff

**Image Handling**:
- Posts have images: JOIN posts with media to get external_resource_url
- User profiles have avatars: use users.avatar_url
- Return image URLs in your response - they'll be formatted automatically

**Tone Examples**:
✅ "Hey! I found 5 awesome posts for you..."
✅ "Sure thing! Alice has been posting some cool stuff lately..."
✅ "Oh nice! Here are the places you might like..."
❌ "Query executed successfully. Results: ..."
❌ "The database contains the following records..."

Remember: Be conversational, friendly, and helpful - not robotic!"""
    )
    
    # Create a fast classifier for initial routing (cheaper/faster than supervisor)
    self.classifier = self._create_classifier()
    self.supervisor_agent = self._create_supervisor()
    self.workflow = self._create_workflow()
    
    GraphService._initialized = True

  def _create_classifier(self):
    """Fast classifier to route queries directly without supervisor overhead."""
    classifier_prompt = ChatPromptTemplate.from_template(
      """Classify this user query into ONE category:
      
      Categories:
      - SQL: Questions about users, posts, places, follows, media, timeline, or any app data
      - RECOMMENDER: Requests for recommendations or suggestions
      - ASSISTANT: Greetings, general questions, calculations, web searches
      
      Query: {query}
      
      Respond with ONLY the category name (SQL, RECOMMENDER, or ASSISTANT)."""
    )
    
    return classifier_prompt | self.model
  
  def _classify_query(self, query: str) -> str:
    """Quickly classify query to route directly to the right agent."""
    try:
      result = self.classifier.invoke({"query": query})
      classification = result.content.strip().upper()
      
      # Map to agent names
      if "SQL" in classification:
        return "SQL"
      elif "RECOMMEND" in classification:
        return "Recommender"
      else:
        return "Assistant"
    except Exception as e:
      print(f"Classification error: {e}")
      # Default to SQL for data queries
      return "SQL"
  
  def summarize(self, userRequest, finalState):
    response_gen_prompt = ChatPromptTemplate.from_template('''
        **Role**: You are a warm, friendly, and conversational assistant helping a user with their questions. Talk like a helpful friend, not a robot or formal system.
        
        **Tone & Style**:
        - Use casual, natural language ("Hey!", "Sure!", "Oh, that's interesting!")
        - Be enthusiastic and positive when appropriate
        - Use contractions ("here's", "you've", "that's", "I'd")
        - Add personality with light expressions ("Great question!", "Let me help with that!", "Oh, I found some cool stuff!")
        - Speak directly to the user as if having a conversation
        - Keep it brief but friendly - no walls of text
        
        **What to NEVER do**:
        - Don't mention "workers", "agents", "SQL", "database", "supervisor", or any technical system details
        - Don't sound robotic or overly formal
        - Don't use corporate speak or jargon
        - Don't list information in a dry, mechanical way
        
        **Image Handling**:
        - ALWAYS preserve markdown image syntax ![...](...) EXACTLY as provided
        - Never modify, remove, or describe image URLs
        - Include them naturally in your response
        
        **Examples**:
        ✅ Good: "Hey! I found some awesome posts for you:\n![Image 1](http://...)\n![Image 2](http://...)\nPretty cool, right?"
        ✅ Good: "Sure thing! Here are the users you're looking for: Alice, Bob, and Charlie. They've all been pretty active lately!"
        ❌ Bad: "The SQL agent queried the database and retrieved the following results..."
        ❌ Bad: "Here is the information you requested from the database:"

        **User Request**: {userRequest}
        **Information Found**: {finalState}
        
        Respond in a friendly, conversational way (keep all image markdown intact):
    ''')

    summerizer_agent =  create_structured_output_runnable(
        FinalResponse, self.model, response_gen_prompt
    )

    return summerizer_agent.invoke({"userRequest":userRequest, "finalState":finalState})

  def _create_supervisor(self):
    system_prompt = (
      "You are an intelligent supervisor managing a conversation between specialized workers: {members}.\n\n"
      "**Agent Capabilities:**\n"
      "- SQL: {sql_desc}\n"
      "- Recommender: {rec_desc}\n"
      "- Assistant: {asst_desc}\n\n"
      "**Routing Rules:**\n"
      "1. Route to SQL for ANY question about:\n"
      "   - Users (profiles, bios, avatars, usernames)\n"
      "   - Posts (content, captions, timestamps, authors)\n"
      "   - Places (locations, details, coordinates)\n"
      "   - Follows (who follows whom, follower counts)\n"
      "   - Media (photos, images, attachments)\n"
      "   - Timeline (activity, recent posts, feeds)\n"
      "   - Keywords: 'show me', 'find', 'list', 'get', 'who', 'what posts', 'what places', 'followers', 'following'\n\n"
      "2. Route to Recommender for:\n"
      "   - Personalized suggestions\n"
      "   - 'Recommend', 'suggest', 'should I', 'best places for me'\n\n"
      "3. Route to Assistant for:\n"
      "   - General questions, greetings, explanations\n"
      "   - Web searches, calculations, general knowledge\n\n"
      "**Important:** Default to SQL for data-related queries. When in doubt about user data, choose SQL first."
    )

    options = ["FINISH"] + members

    supervisor_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("system", 
         "Given the conversation above, who should act next?\n"
         "- If the question is about app data (users, posts, places, follows, media, timeline), select SQL\n"
         "- If it's about recommendations, select Recommender\n"
         "- If it's general or already answered well, select FINISH\n"
         "- Otherwise select Assistant\n\n"
         "Select one of: {options}"),
    ]).partial(
        options=str(options), 
        members=", ".join(members),
        sql_desc=AGENT_DESCRIPTIONS["SQL"],
        rec_desc=AGENT_DESCRIPTIONS["Recommender"],
        asst_desc=AGENT_DESCRIPTIONS["Assistant"]
    )

    supervisor_functions = {
        "name": "route",
        "description": "Select the next role.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "next": {
                    "title": "Next",
                    "anyOf": [{"enum": options}],
                }
            },
            "required": ["next"],
        },
    }
    return (
        supervisor_prompt
        | self.model.bind_functions(functions=[supervisor_functions], function_call="route")
        | JsonOutputFunctionsParser()
    )

  def _create_workflow(self):
    def chat_agent_node(state, agent, name):
      try:
        result = agent.invoke({"input": state['messages'][-1].content})
        return {
          "messages": [HumanMessage(content=result["output"], name=name)],
          "agents_used": [name]
        }
      except Exception as e:
        return {
          "messages": [HumanMessage(content=f"Error: {str(e)}", name=name)],
          "agents_used": [name]
        }
    
    def sql_agent_node(state, agent, name):
      try:
        # Enhance SQL agent with user context
        user_id = state.get('user_id', 1)
        query = state['messages'][-1].content
        
        # Check cache first
        cache_key = f"sql_{user_id}_{query}"
        cached_data = state.get('cached_data', {})
        
        if cache_key in cached_data:
          return {
            "messages": [HumanMessage(content=cached_data[cache_key], name=name)],
            "agents_used": [name]
          }
        
        # Detect if query involves images/media
        needs_images = any(keyword in query.lower() for keyword in 
                          ['post', 'photo', 'image', 'picture', 'media', 'avatar', 'profile'])
        
        # Add context to help SQL agent understand it should query the database
        image_instruction = ""
        if needs_images:
          image_instruction = " When querying posts or users, make sure to JOIN with the media table and include external_resource_url field to get image URLs."
        
        enhanced_query = f"Answer this in a friendly, conversational way: {query}\n\nContext: You're helping user {user_id}. Query the database (users, posts, places, follows, media, timeline) to find what they're looking for. Be natural and casual in your response, like you're chatting with a friend.{image_instruction} Don't mention technical details like SQL queries or database operations - just give them the info they need in a warm, helpful way."
        
        result = agent.invoke(enhanced_query)
        output = result["output"]
        
        # Post-process output to ensure image URLs are in markdown format
        if needs_images and 'http' in output:
          # Extract URLs and format them as markdown images
          import re
          urls = re.findall(r'(https?://[^\s<>"]+)', output)
          for i, url in enumerate(urls, 1):
            if not f'![]({url}' in output:  # Only add markdown if not already present
              # Convert plain URLs to markdown image syntax
              output = output.replace(url, f'![Image {i}]({url})')
        
        # Update cache
        cached_data[cache_key] = output
        
        return {
          "messages": [HumanMessage(content=output, name=name)],
          "cached_data": cached_data,
          "agents_used": [name]
        }
      except Exception as e:
        return {
          "messages": [HumanMessage(content=f"Database error: {str(e)}", name=name)],
          "agents_used": [name]
        }
    
    def recommender_agent_node(state, agent, name):
      try:
        user_id = state.get('user_id', 1)
        query = state['messages'][-1].content
        
        # Use SQL results if available for better recommendations
        sql_context = ""
        for msg in state.get('messages', []):
          if hasattr(msg, 'name') and msg.name == 'SQL':
            sql_context = f"\nBased on database results: {msg.content[:500]}"  # Limit context size
            break
        
        # Enhance recommender with user context
        enhanced_query = f"Provide personalized recommendations for user {user_id}: {query}{sql_context}\nConsider their interests, past behavior, and preferences."
        
        result = agent.invoke({"input": enhanced_query})
        return {
          "messages": [HumanMessage(content=result["output"], name=name)],
          "agents_used": [name]
        }
      except Exception as e:
        return {
          "messages": [HumanMessage(content=f"Error: {str(e)}", name=name)],
          "agents_used": [name]
        }

    workflow = StateGraph(AgentState)
    workflow.add_node("Assistant", functools.partial(chat_agent_node, agent=self.chat_agent, name="Assistant"))
    workflow.add_node("SQL", functools.partial(sql_agent_node, agent=self.sql_agent, name="SQL"))
    workflow.add_node("Recommender", functools.partial(recommender_agent_node, agent=self.chat_agent, name="Recommender"))

    workflow.add_node("supervisor", self.supervisor_agent)
    
    # Add classifier node for fast initial routing
    def classifier_node(state):
      query = state['messages'][0].content
      initial_agent = self._classify_query(query)
      return {"next": initial_agent, "query_type": initial_agent.lower()}
    
    workflow.add_node("classifier", classifier_node)
    
    # Route from classifier to agents (skip supervisor for first step)
    workflow.add_conditional_edges(
      "classifier",
      lambda x: x["next"],
      {"SQL": "SQL", "Recommender": "Recommender", "Assistant": "Assistant"}
    )
    
    # Safety check: prevent infinite loops
    def should_continue(state):
      iteration = state.get('iteration_count', 0)
      if iteration >= self.max_iterations:
        return END
      return state.get('next', 'FINISH')
    
    for member in members:
      # Workers report back to supervisor
      workflow.add_edge(member, "supervisor")
  
    # The supervisor populates the "next" field in the graph state
    conditional_map = {k: k for k in members}
    conditional_map["FINISH"] = END
  
    workflow.add_conditional_edges("supervisor", should_continue, conditional_map)
    
    # Start with classifier for fast routing
    workflow.set_entry_point("classifier")

    return workflow.compile()

  async def invoke(self, input_data, user_id: int, chat_history: List[Dict[str, str]] = None):
    """Invoke the graph workflow and return final response.
    
    Args:
      input_data: User query
      user_id: User identifier
      chat_history: Previous conversation messages for context
      
    Returns:
      Final response string
    """
    if chat_history is None:
      chat_history = []
    
    # Convert chat history to LangChain messages
    history_messages = []
    for msg in chat_history:
      if msg.get('role') == 'user':
        history_messages.append(HumanMessage(content=msg.get('content', '')))
      elif msg.get('role') == 'assistant':
        history_messages.append(AIMessage(content=msg.get('content', '')))
    
    # Combine history with current question
    all_messages = history_messages + [HumanMessage(content=input_data)]
    
    initial_state = {
      "messages": all_messages,
      "user_id": user_id,
      "iteration_count": 0,
      "cached_data": {},
      "agents_used": [],
      "chat_history": chat_history
    }
    
    graphSteps = []
    
    try:
      async for s in self.workflow.astream(initial_state):
        if "__end__" not in s:
          graphSteps.append(s)
          
          # Increment iteration count
          if "supervisor" in s:
            initial_state["iteration_count"] = initial_state.get("iteration_count", 0) + 1
      
      # Return final response
      return self.summarize(input_data, graphSteps).response
        
    except Exception as e:
      error_msg = f"Graph execution error: {str(e)}"
      print(error_msg)
      return f"I encountered an error processing your request: {str(e)}"
