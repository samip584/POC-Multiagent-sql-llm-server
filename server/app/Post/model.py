from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    media_id = Column(Integer, ForeignKey('media.id'))