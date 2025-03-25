# app/main.py
from fastapi import FastAPI
from app.routers import pdf_converter

app = FastAPI(title="Modular Data Transformer")
app.include_router(pdf_converter.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Modular Data Transformer API!"}

