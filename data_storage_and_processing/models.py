from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "user"
 
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())