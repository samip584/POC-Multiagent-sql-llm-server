from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from config.db import Base, engine


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    external_resource_url = Column(String)
    meta = Column(JSON)
    
    # Relationships
    posts = relationship("Post", back_populates="media")