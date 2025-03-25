from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
import xmltodict
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db
from app.core.usage_tracker import check_and_increment_usage
from app.models.user import User
from app.tasks import xml_to_json_task

router = APIRouter(prefix="/convert", tags=["conversion"])

@router.post("/xml-to-json")
async def xml_to_json(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "xml-to-json")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    # Typically text/xml or application/xml
    if file.content_type not in ("text/xml", "application/xml"):
        raise HTTPException(status_code=415, detail="XML file required")

    contents = await file.read()
    try:
        parsed = xmltodict.parse(contents)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"XML parse error: {e}")

    return parsed

@router.post("/xml-to-json-async")
async def xml_to_json_async(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "xml-to-json-async")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    if file.content_type not in ("text/xml", "application/xml"):
        raise HTTPException(status_code=415, detail="XML file required")

    contents = await file.read()

    # Enqueue Celery task
    task = xml_to_json_task.delay(contents)
    return {"task_id": task.id, "status": "queued"}
