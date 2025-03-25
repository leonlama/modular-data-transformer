# app/main.py
from fastapi import FastAPI
from app.routers import pdf_converter, csv_converter, excel_converter, xml_converter, json_converter

app = FastAPI(title="Modular Data Transformer")
app.include_router(pdf_converter.router)
app.include_router(csv_converter.router)
app.include_router(excel_converter.router)
app.include_router(xml_converter.router)
app.include_router(json_converter.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Modular Data Transformer API!"}
