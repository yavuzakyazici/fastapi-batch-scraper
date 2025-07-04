from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=False )
    password = Column(String(255))
    is_active = Column(Integer)

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255))
    timestamp = Column(String(100))
    status_code = Column(Integer)