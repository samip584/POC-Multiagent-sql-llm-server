from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from config.db import Base, engine


class Timeline(Base):
    __tablename__ = 'timelines'

    id = Column(Integer, primary_key=True)
    start_timestamp = Column(Integer)
    end_timestamp = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    places_id = Column(JSON)
    
    # Relationship
    user = relationship("User", back_populates="timelines")