from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
import xmltodict
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db
from app.core.usage_tracker import check_and_increment_usage
from app.models.user import User

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
