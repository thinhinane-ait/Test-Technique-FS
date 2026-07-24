#backend/app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import antenna, intervention

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
     description="""
    API de gestion des antennes et des interventions.

    Fonctionnalités :
    - Consultation des antennes
    - Création d'interventions
    - Contrôle des interventions actives
    """
)

@app.get("/")
def root():
    return {
        "message": settings.app_name
    }

app.include_router(antenna.router)
app.include_router(intervention.router)