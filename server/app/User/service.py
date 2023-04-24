from sqlalchemy.orm import Session
from .model import User
from typing import List, Dict

class UserService:
    """Service class for handling user operations."""

    def get_all_users(self, db: Session) -> List[Dict]:
        """Retrieve all users from the database."""
        users = db.query(User).all()
        return [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            }
            for user in users
        ]

    def get_user_by_id(self, user_id: int, db: Session) -> Dict:
        """Retrieve a specific user by ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            }
        return None
