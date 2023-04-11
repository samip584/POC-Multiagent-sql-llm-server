from sqlalchemy import Column, Integer, String, Float
from config.db import Base

class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)
    title = Column(String)