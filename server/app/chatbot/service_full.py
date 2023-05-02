from typing import List, Dict
from .graph import GraphService
from .media_utils import format_response_with_images

class ChatBotService:
  """Service class for handling chatbot operations."""

  def __init__(self):
    """Initialize the ChatBotService with GraphService."""
    self.graphService = GraphService()

  async def ask_question(self, question: str, user_id: int, include_image_metadata: bool = True, chat_history: List[Dict[str, str]] = None) -> dict:
    """Process a user question using the graph service and return the response.
    
    Args:
      question: User's question
      user_id: User identifier
      include_image_metadata: If True, returns structured response with separate image URLs
      chat_history: Previous conversation messages for context
      
    Returns:
      Response dict with text and optionally image metadata
    """
    if chat_history is None:
      chat_history = []
    
    output = await self.graphService.invoke(question, user_id, chat_history)
    
    if include_image_metadata:
      # Return structured response with separate image array for frontend
      return format_response_with_images(output, convert_urls=True)
    else:
      # Return simple text response (backward compatible)
      return {"response": output}


