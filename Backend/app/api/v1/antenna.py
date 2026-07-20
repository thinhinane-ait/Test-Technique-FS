from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from typing import Annotated
from app.schemas.antenna import AntennaResponse
from app.services.antenna import AntennaService

router = APIRouter(
    prefix = "/v1/antenna",
    tags=["Antennas"],
)


def get_db():
    db = SessionLocal()

    try : 
        yield db
    
    finally: 
        db.close()

service = AntennaService()
DBSession = Annotated[Session, Depends(get_db)]

@router.get(
    "",
    response_model=list[AntennaResponse],
)



def list_antennas(db: DBSession):
    return service.list_antennas(
        db,
        limit=100,
        offset=0,
    )