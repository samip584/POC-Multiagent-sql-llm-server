from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from config.config import settings

class ChatBotService:
  """Service class for handling chatbot operations."""

  def __init__(self):
    """Initialize the ChatBotService."""
    self.model = ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY, temperature=0.3)
    self.db = SQLDatabase.from_uri(settings.get_database_uri())

  async def ask_question(self, question: str, user_id: int) -> dict:
    """Process a user question and return the response.
    
    Args:
      question: User's question
      user_id: User identifier
      
    Returns:
      Response dict with text
    """
    # Simple response for now
    response = f"Received question: {question} from user {user_id}"
    return {"response": response}


