from fastapi import APIRouter, Body
from .service import MediaService

media_router = APIRouter(prefix="/media", tags=["media"])

@media_router.post("/generate")
async def generateMedia():
  media_service = MediaService()  # Create an instance of ChatBotService
  
  media_service.generateMedia('abhi.jpg', 'frankie.jpg', 'output.jpg')
  
  return {"response": {}}

__all__ = ["media_router"]
