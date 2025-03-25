# app/models/usage.py
from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class UsageLog(Base):
    __tablename__ = "usage_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # or store their API key
    endpoint = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
