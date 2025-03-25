from fastapi import APIRouter, File, UploadFile, HTTPException
from app.core.conversion import pdf_to_excel

router = APIRouter(prefix="/convert", tags=["conversion"])

@router.post("/pdf-to-excel")
async def convert_pdf_to_excel(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="PDF required")
    data = await file.read()
    try:
        excel = pdf_to_excel(data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return StreamingResponse(BytesIO(excel), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=converted.xlsx"})

