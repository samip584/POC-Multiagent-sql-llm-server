from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base, engine


class Follow(Base):
    __tablename__ = 'follow'

    id = Column(Integer, primary_key=True)
    source_user_id = Column(Integer, ForeignKey('users.id'))
    destination_user_id = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    source_user = relationship("User", foreign_keys=[source_user_id], back_populates="followed")
    destination_user = relationship("User", foreign_keys=[destination_user_id], back_populates="followers")