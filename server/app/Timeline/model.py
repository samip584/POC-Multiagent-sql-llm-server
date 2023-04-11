from sqlalchemy import Column, Integer, ForeignKey, JSON
from config.db import Base

class Timeline(Base):
    __tablename__ = 'timelines'

    id = Column(Integer, primary_key=True)
    start_timestamp = Column(Integer)
    end_timestamp = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    places_id = Column(JSON)