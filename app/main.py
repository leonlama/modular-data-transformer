# app/main.py
from fastapi import FastAPI
from app.routers import pdf_converter
from app.routers.csv_converter import router as csv_router

app = FastAPI(title="Modular Data Transformer")
app.include_router(pdf_converter.router)
app.include_router(csv_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Modular Data Transformer API!"}
