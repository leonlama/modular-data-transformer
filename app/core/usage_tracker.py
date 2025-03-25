from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.usage import UsageLog
from app.models.user import User

def check_and_increment_usage(db: Session, user: User, endpoint: str):
    # Define the period (last 30 days) for usage tracking
    period_start = datetime.utcnow() - timedelta(days=30)
    usage_count = (
        db.query(UsageLog)
        .filter(UsageLog.user_id == user.api_key)
        .filter(UsageLog.timestamp >= period_start)
        .count()
    )
    
    if usage_count >= user.monthly_limit:
        raise Exception("Monthly limit exceeded")
    
    # Log this usage
    log_entry = UsageLog(user_id=user.api_key, endpoint=endpoint)
    db.add(log_entry)
    db.commit()
