from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base, engine


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    media_id = Column(Integer, ForeignKey('media.id'))
    
    # Relationships
    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="posts")