# app/core/init_db.py
from app.core.database import Base, engine
from app.models.usage import UsageLog

def init_db():
    Base.metadata.create_all(bind=engine)
