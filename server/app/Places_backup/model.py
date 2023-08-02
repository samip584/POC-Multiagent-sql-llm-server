from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base, engine


class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)
    title = Column(String)