# create_user.py
import sys
from app.core.init_db import init_db
from app.core.database import SessionLocal
from app.models.user import User

def create_user(api_key: str, monthly_limit: int = 50):
    db = SessionLocal()
    new_user = User(api_key=api_key, monthly_limit=monthly_limit)
    db.add(new_user)
    db.commit()
    db.close()
    print(f"User created with api_key={api_key} monthly_limit={monthly_limit}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_user.py <api_key> [monthly_limit]")
        sys.exit(1)

    init_db()
    key = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    create_user(key, limit)

