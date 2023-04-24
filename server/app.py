from fastapi import FastAPI
from config.db import Base, engine
from app.User.router import user_router

app = FastAPI()

__app_name__ = "SQL_LLM_Server"
__version__ = "0.0.1"

@app.get("/")
async def root():
    return {"app": __app_name__, "version": __version__}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(user_router)

__all__ = ["app"]
