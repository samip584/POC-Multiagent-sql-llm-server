from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from config.db import Base, engine
from config.config import validate_settings

validate_settings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.chatbot.router import chat_bot_router
from app.User.router import user_router

from app.common.exceptions import add_exception_handlers

app = FastAPI()

__app_name__ = "MultiAgent_SQL_LLM_Server"
__version__ = "0.0.1"

# Import models to register them with SQLAlchemy (needed for migrations)
from app.User.model import User
from app.Post.model import Post
from app.Media.model import Media
from app.Timeline.model import Timeline
from app.Follow.model import Follow
from app.Places.model import Place


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],  # Replace with actual frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Initialize Routes
@app.get("/")
async def root():
    return {"app": __app_name__, "version": __version__}

@app.get("/health")
async def health_check():
    # Basic health check - could add DB ping, etc.
    return {"status": "healthy"}


app.include_router(chat_bot_router)
app.include_router(user_router)

add_exception_handlers(app)

__all__ = ["app"]

