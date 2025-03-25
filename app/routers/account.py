from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db
from app.models.user import User

router = APIRouter(prefix="/account", tags=["account"])

@router.get("/usage")
def get_usage(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Possibly reset monthly usage if needed, to reflect any new month
    user.reset_monthly_usage_if_needed()
    db.commit()

    return {
        "monthly_usage": user.monthly_usage,
        "monthly_limit": user.monthly_limit
    }
