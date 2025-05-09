# app/main.py
import os
from fastapi import FastAPI
from app.core.init_db import init_db
from app.routers import pdf_converter, csv_converter, excel_converter, xml_converter, json_converter, account

app = FastAPI(title="Modular Data Transformer")

@app.on_event("startup")
def on_startup():
    print("DB init!")
    init_db()

app.include_router(pdf_converter.router)
app.include_router(csv_converter.router)
app.include_router(excel_converter.router)
app.include_router(xml_converter.router)
app.include_router(json_converter.router)
app.include_router(account.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Modular Data Transformer API!"}

@app.get("/ping")
def ping():
    return {"status": "OK"}

@app.get("/env")
def read_env():
    return {"REDIS_URL": os.environ.get("REDIS_URL")}
