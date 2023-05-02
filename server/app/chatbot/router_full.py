from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional, List, Dict

from .service import ChatBotService

chat_bot_router = APIRouter(prefix="/chat-bot", tags=["chat-bot"])

chat_bot_service = ChatBotService()  # Create an instance of ChatBotService

class AskRequest(BaseModel):
    question: str
    user_id: Optional[int] = None
    include_images: Optional[bool] = True  # New field for image metadata
    chat_history: Optional[List[Dict[str, str]]] = []  # Chat history for context

class ImageMetadata(BaseModel):
    url: str
    alt: str

class ChatResponse(BaseModel):
    text: str
    images: List[ImageMetadata] = []
    has_images: bool = False
    user_id: int

@chat_bot_router.post("/ask", response_model=ChatResponse)
async def ask_question(request: AskRequest):
  """
  Ask a question to the chatbot.
  
  Returns structured response with:
  - text: The response text (may include markdown image syntax)
  - images: Array of image objects with url and alt text for easy frontend rendering
  - has_images: Boolean indicating if images are present
  - user_id: The user who asked the question
  """
  # Use user_id if provided, otherwise default to 1
  user_id = request.user_id if request.user_id is not None else 1
  
  result = await chat_bot_service.ask_question(
    request.question, 
    user_id,
    include_image_metadata=request.include_images,
    chat_history=request.chat_history or []
  )
  
  # Add user_id to response
  result['user_id'] = user_id
  
  return result

@chat_bot_router.post("/ask/simple")
async def ask_question_simple(request: AskRequest):
  """
  Ask a question to the chatbot (simple text response - backward compatible).
  
  Returns just the response text as a string.
  """
  user_id = request.user_id if request.user_id is not None else 1
  
  result = await chat_bot_service.ask_question(
    request.question, 
    user_id,
    include_image_metadata=False,
    chat_history=request.chat_history or []
  )
  
  return {"response": result.get("response", result.get("text", "")), "user_id": user_id}

__all__ = ["chat_bot_router"]
