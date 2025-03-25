# app/core/init_db.py
from app.core.database import Base, engine
from app.models.usage import UsageLog
from app.models.user import User

def init_db():
    print("init_db function called!")
    Base.metadata.create_all(bind=engine)
