from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.core.conversion import pdf_to_excel
from io import BytesIO
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db
from app.core.usage_tracker import check_and_increment_usage
from app.models.user import User

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
