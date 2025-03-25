from fastapi import APIRouter, File, UploadFile, HTTPException
import json
import pandas as pd
from io import BytesIO
from fastapi.responses import Response

router = APIRouter(prefix="/convert", tags=["conversion"])

@router.post("/json-to-csv", response_class=Response)
async def json_to_csv(file: UploadFile = File(...)):
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
