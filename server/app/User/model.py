from sqlalchemy import Column, Integer, String, Float, BigInteger
from config.db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(BigInteger)
    longitude = Column(Float)
    latitude = Column(Float)
    idp_id = Column(Integer)
