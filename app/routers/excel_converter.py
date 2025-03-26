from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
import pandas as pd
from io import BytesIO
import base64
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db
from app.core.usage_tracker import check_and_increment_usage
from app.models.user import User
from app.tasks import excel_to_csv_task, excel_to_json_task

router = APIRouter(prefix="/convert", tags=["conversion"])

@router.post("/excel-to-csv", response_class=Response)
async def excel_to_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "excel-to-csv")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    # Accept .xls or .xlsx
    if file.content_type not in (
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ):
        raise HTTPException(status_code=415, detail="Excel file required")

    contents = await file.read()
    try:
        df = pd.read_excel(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Excel parse error: {e}")

    csv_bytes = df.to_csv(index=False).encode("utf-8")

    # Return as a downloadable CSV
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=converted.csv"}
    )

@router.post("/excel-to-csv-async")
async def excel_to_csv_async(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "excel-to-csv-async")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    if file.content_type not in (
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ):
        raise HTTPException(status_code=415, detail="Excel file required")

    contents = await file.read()
    
    # Encode contents as base64 string
    encoded_contents = base64.b64encode(contents).decode("utf-8")

    # Enqueue Celery task with encoded contents
    task = excel_to_csv_task.delay(encoded_contents)
    return {"task_id": task.id, "status": "queued"}

@router.post("/excel-to-json")
async def excel_to_json(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "excel-to-json")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    if file.content_type not in (
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ):
        raise HTTPException(status_code=415, detail="Excel file required")

    contents = await file.read()
    try:
        df = pd.read_excel(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Excel parse error: {e}")

    # Return as JSON
    return df.to_dict(orient="records")

@router.post("/excel-to-json-async")
async def excel_to_json_async(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "excel-to-json-async")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    if file.content_type not in (
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ):
        raise HTTPException(status_code=415, detail="Excel file required")

    contents = await file.read()

    # Encode contents as base64 string
    encoded_contents = base64.b64encode(contents).decode("utf-8")

    # Enqueue Celery task with encoded contents
    task = excel_to_json_task.delay(encoded_contents)
    return {"task_id": task.id, "status": "queued"}
