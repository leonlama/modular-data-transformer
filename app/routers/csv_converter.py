from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
import pandas as pd
from io import BytesIO
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db
from app.core.usage_tracker import check_and_increment_usage
from app.models.user import User
from app.tasks import csv_to_json_task, csv_to_excel_task
import base64

router = APIRouter(prefix="/convert", tags=["conversion"])

@router.post("/csv-to-json")
async def convert_csv_to_json(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "csv-to-json")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    if file.content_type not in ("text/csv", "application/csv"):
        raise HTTPException(status_code=415, detail="CSV required")
    contents = await file.read()
    try:
        df = pd.read_csv(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"CSV parse error: {e}")
    return df.to_dict(orient="records")

@router.post("/csv-to-json-async")
async def convert_csv_to_json_async(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "csv-to-json-async")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    if file.content_type not in ("text/csv", "application/csv"):
        raise HTTPException(status_code=415, detail="CSV required")

    contents = await file.read()
    encoded = base64.b64encode(contents).decode("utf-8")
    task = csv_to_json_task.delay(encoded)
    return {"task_id": task.id, "status": "queued"}

@router.post("/csv-to-excel")
async def csv_to_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "csv-to-excel")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    if file.content_type not in ("text/csv", "application/csv"):
        raise HTTPException(status_code=415, detail="CSV required")
    contents = await file.read()

    try:
        df = pd.read_csv(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"CSV parse error: {e}")

    # Convert to Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=converted.xlsx"},
    )

@router.post("/csv-to-excel-async")
async def csv_to_excel_async(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "csv-to-excel-async")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    if file.content_type not in ("text/csv", "application/csv"):
        raise HTTPException(status_code=415, detail="CSV required")

    contents = await file.read()
    
    # Base64 encode contents before sending to Celery
    encoded = base64.b64encode(contents).decode("utf-8")
    task = csv_to_excel_task.delay(encoded)
    return {"task_id": task.id, "status": "queued"}
