from sqlalchemy import Column, Integer, String, JSON
from config.db import Base

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    external_resource_url = Column(String)
    meta = Column(JSON)