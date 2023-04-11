from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

class Follow(Base):
    __tablename__ = 'follow'

    id = Column(Integer, primary_key=True)
    source_user_id = Column(Integer, ForeignKey('users.id'))
    destination_user_id = Column(Integer, ForeignKey('users.id'))