from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from .service import ChatBotService

chat_bot_router = APIRouter(prefix="/chat-bot", tags=["chat-bot"])
chat_bot_service = ChatBotService()

class AskRequest(BaseModel):
    question: str
    user_id: Optional[int] = None

@chat_bot_router.post("/ask")
async def ask_question(request: AskRequest):
  """Ask a question to the chatbot."""
  user_id = request.user_id if request.user_id is not None else 1
  result = await chat_bot_service.ask_question(request.question, user_id)
  return result

__all__ = ["chat_bot_router"]
