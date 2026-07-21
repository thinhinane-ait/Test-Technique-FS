##app/v1/intervention.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.services.intervention import InterventionService
from app.schemas.intervention import InterventionResponse, InterventionCreate
from typing import Annotated
from app.core.security import verify_api_key


router = APIRouter(
    prefix = "/api/v1",
    tags=["interventions"],
    dependencies=[Depends(verify_api_key)],
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



@router.patch("/intervention/{intervention_id}/close",
              response_model=InterventionResponse,
    summary="Close intervention")

def close_intervention(
    intervention_id : int,
    db:DBSession
): 
    return service.close_intervention(
        db,
        intervention_id
    )