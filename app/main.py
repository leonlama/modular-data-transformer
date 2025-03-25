# app/main.py
from fastapi import FastAPI

app = FastAPI(title="Modular Data Transformer")

@app.get("/")
def root():
    return {"message": "Welcome to the Modular Data Transformer API!"}

