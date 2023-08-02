from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.orm import relationship
from config.db import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(BigInteger)
    longitude = Column(Float)
    latitude = Column(Float)
    idp_id = Column(Integer)
    
    # Relationships
    timelines = relationship("Timeline", back_populates="user")
    posts = relationship("Post", back_populates="user")

    # Assuming a bidirectional relationship for follows
    # This will retrieve all the follows where this user is the source
    followed = relationship(
        "Follow",
        back_populates="source_user",
        foreign_keys="[Follow.source_user_id]"
    )

    
    # This will retrieve all the follows where this user is the destination
    followers = relationship(
        "Follow",
        back_populates="destination_user",
        foreign_keys="[Follow.destination_user_id]"
    )
