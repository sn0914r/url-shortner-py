from fastapi import FastAPI
from app.core.database import check_db_connection

app = FastAPI(title="URL Shortener API")

@app.on_event("startup")
async def startup_event():
    await check_db_connection()

@app.get("/health")
async def health_check():
    return {"status": "ok"}