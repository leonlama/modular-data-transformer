from fastapi import APIRouter, File, UploadFile, HTTPException
import pandas as pd
from io import BytesIO

router = APIRouter(prefix="/convert", tags=["conversion"])

@router.post("/csv-to-json")
async def convert_csv_to_json(file: UploadFile = File(...)):
    if file.content_type not in ("text/csv", "application/csv"):
        raise HTTPException(status_code=415, detail="CSV required")
    contents = await file.read()
    try:
        df = pd.read_csv(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"CSV parse error: {e}")
    return df.to_dict(orient="records")
