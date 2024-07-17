from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict

from .service import UserService
from config.db import get_db

user_router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()

@user_router.get("/", response_model=List[Dict])
def get_all_users(db: Session = Depends(get_db)):
    """Get all users from the database."""
    users = user_service.get_all_users(db)
    return users

@user_router.get("/{user_id}", response_model=Dict)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID."""
    user = user_service.get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

__all__ = ["user_router"]
