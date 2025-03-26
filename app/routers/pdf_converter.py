from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.core.conversion import pdf_to_excel
from io import BytesIO
import base64
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db
from app.core.usage_tracker import check_and_increment_usage
from app.models.user import User
from app.tasks import pdf_to_excel_task

router = APIRouter(prefix="/convert", tags=["conversion"])

@router.post(
    "/pdf-to-excel",
    response_class=StreamingResponse,
    responses={200: {"content": {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}}}},
)
async def convert_pdf_to_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check rate limit and log usage for this endpoint
    try:
        check_and_increment_usage(db, user, "pdf-to-excel")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="PDF required")
    data = await file.read()
    try:
        excel = pdf_to_excel(data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return StreamingResponse(
        BytesIO(excel),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=converted.xlsx"},
    )

@router.post("/pdf-to-excel-async")
async def pdf_to_excel_async(
    file: UploadFile = File(...),
    db = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        check_and_increment_usage(db, user, "pdf-to-excel-async")
    except Exception as e:
        raise HTTPException(status_code=429, detail=str(e))

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="PDF file required")

    contents = await file.read()
    encoded = base64.b64encode(contents).decode("utf-8")
    task = pdf_to_excel_task.delay(encoded)
    return {"task_id": task.id, "status": "queued"}
