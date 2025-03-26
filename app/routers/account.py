from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db
from app.models.user import User
from celery_app import celery_app

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

@router.get("/task-status/{task_id}")
def get_task_status(task_id: str, user: User = Depends(get_current_user)):
    result = celery_app.AsyncResult(task_id)
    return {
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
