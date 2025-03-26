from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from io import BytesIO
import base64
import pandas as pd

from app.core.auth import get_current_user, get_db
from app.core.usage_tracker import check_and_increment_usage
from app.models.user import User
from app.tasks import excel_to_csv_task, excel_to_json_task, pdf_to_excel_task

router = APIRouter(prefix="/convert", tags=["conversion"])

# Excel → CSV (async)
@router.post("/excel-to-csv-async")
async def excel_to_csv_async(file: UploadFile = File(...),
                             db: Session = Depends(get_db),
                             user: User = Depends(get_current_user)):
    check_and_increment_usage(db, user, "excel-to-csv-async")
    if file.content_type not in (
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ):
        raise HTTPException(status_code=415, detail="Excel file required")

    contents = await file.read()
    encoded = base64.b64encode(contents).decode("utf-8")
    task = excel_to_csv_task.delay(encoded)
    return {"task_id": task.id, "status": "queued"}

# Excel → JSON (async)
@router.post("/excel-to-json-async")
async def excel_to_json_async(file: UploadFile = File(...),
                              db: Session = Depends(get_db),
                              user: User = Depends(get_current_user)):
    check_and_increment_usage(db, user, "excel-to-json-async")
    if file.content_type not in (
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ):
        raise HTTPException(status_code=415, detail="Excel file required")

    contents = await file.read()
    encoded = base64.b64encode(contents).decode("utf-8")
    task = excel_to_json_task.delay(encoded)
    return {"task_id": task.id, "status": "queued"}

# PDF → Excel (async)
@router.post("/pdf-to-excel-async")
async def pdf_to_excel_async(file: UploadFile = File(...),
                             db: Session = Depends(get_db),
                             user: User = Depends(get_current_user)):
    check_and_increment_usage(db, user, "pdf-to-excel-async")
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="PDF file required")

    contents = await file.read()
    encoded = base64.b64encode(contents).decode("utf-8")
    task = pdf_to_excel_task.delay(encoded)
    return {"task_id": task.id, "status": "queued"}
