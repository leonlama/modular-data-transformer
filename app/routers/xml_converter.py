from fastapi import APIRouter, File, UploadFile, HTTPException
import xmltodict

router = APIRouter(prefix="/convert", tags=["conversion"])

@router.post("/xml-to-json")
async def xml_to_json(file: UploadFile = File(...)):
    # Typically text/xml or application/xml
    if file.content_type not in ("text/xml", "application/xml"):
        raise HTTPException(status_code=415, detail="XML file required")

    contents = await file.read()
    try:
        parsed = xmltodict.parse(contents)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"XML parse error: {e}")

    return parsed
