from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
import json
import pandas as pd
from io import BytesIO
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db
from app.core.usage_tracker import check_and_increment_usage
from app.models.user import User
from app.tasks import json_to_csv_task
import base64

router = APIRouter(prefix="/convert", tags=["conversion"])

@router.post("/json-to-csv", response_class=Response)
async def json_to_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "json-to-csv")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    # Typically application/json
    if file.content_type != "application/json":
        raise HTTPException(status_code=415, detail="JSON file required")
    contents = await file.read()
    try:
        data = json.loads(contents)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"JSON parse error: {e}")

    # data can be a dict or list. Let's assume a list of dicts
    if isinstance(data, dict):
        # Possibly wrap in a list
        data = [data]
    if not isinstance(data, list):
        raise HTTPException(status_code=422, detail="Expected JSON array or object")

    try:
        df = pd.DataFrame(data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"DataFrame creation error: {e}")

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=converted.csv"}
    )

@router.post("/json-to-csv-async")
async def json_to_csv_async(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "json-to-csv-async")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    if file.content_type != "application/json":
        raise HTTPException(status_code=415, detail="JSON file required")

    contents = await file.read()

    # Enqueue Celery task
    encoded = base64.b64encode(contents).decode("utf-8")
    task = json_to_csv_task.delay(encoded)
    return {"task_id": task.id, "status": "queued"}
