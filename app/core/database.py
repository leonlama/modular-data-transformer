# app/core/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# For demonstration, store it in the project root (not recommended in production)
DB_URL = "sqlite:///./usage.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All models that inherit from Base must be imported before Base.metadata.create_all()
# is called, otherwise SQLAlchemy won't register them
Base = declarative_base()
