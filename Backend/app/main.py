#backend/app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import antenna, intervention
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

@app.get("/")
def root():
    return {
        "message": settings.app_name
    }

app.include_router(antenna.router)
app.include_router(intervention.router)