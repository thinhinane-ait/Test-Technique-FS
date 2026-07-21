from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.services.intervention import InterventionService
from app.schemas.intervention import InterventionResponse, InterventionCreate
from typing import Annotated





router = APIRouter(
    prefix = "/api/v1",
    tags=["interventions"],
)

def get_db():
    db = SessionLocal()

    try : 
        yield db
    
    finally: 
        db.close()

service = InterventionService()
DBSession = Annotated[Session, Depends(get_db)]

@router.post(
    "/intervention",
    response_model=InterventionResponse,
    summary="Create intervention"
)
def create_intervention(
     intervention:InterventionCreate,
     db: DBSession
):
    return service.create_intervention(
        db,
        intervention
    )