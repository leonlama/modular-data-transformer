# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, unique=True, index=True)
    # For usage limit
    monthly_limit = Column(Integer, default=50)
