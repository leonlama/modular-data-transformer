from datetime import datetime
from sqlalchemy.orm import Session
from app.models.usage import UsageLog
from app.models.user import User

def check_and_increment_usage(db: Session, user: User, endpoint: str):
    # 1) Possibly reset monthly usage
    user.reset_monthly_usage_if_needed()
    db.commit()  # commit so the user's usage_reset_date is up to date

    # 2) Check if usage is at or above limit
    if user.monthly_usage >= user.monthly_limit:
        raise Exception("Monthly limit exceeded")

    # 3) Increment usage
    user.monthly_usage += 1
    db.commit()

    # 4) Log in usage_log for auditing
    record = UsageLog(user_id=user.api_key, endpoint=endpoint)
    db.add(record)
    db.commit()
