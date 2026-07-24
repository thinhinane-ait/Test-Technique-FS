#app/api/v1/antenna.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated
from app.schemas.antenna import AntennaResponse
from app.services.antenna import AntennaService
from app.models.antenna import AntennaStatus
from app.database.dependencies import get_db


router = APIRouter(
    prefix = "/api/v1/antennas",
    tags=["Antennas"],
)


service = AntennaService()
DBSession = Annotated[Session, Depends(get_db)]

@router.get(
    "",
    response_model=list[AntennaResponse],
    summary="List Antennas"
)



def list_antennas(
    db: DBSession,
    limit: Annotated[
        int,
        Query(ge=1, le=100),
    ] = 10,

    offset: Annotated[
        int,
        Query(ge=0),
    ]=0,

    city: Annotated[
        str | None,
        Query(min_length=1,max_length=100),

    ]=None,
    
    status: Annotated[
        AntennaStatus | None,
        Query(),

    ]=None,
    )->list[AntennaResponse]: 

        return service.list_antennas(
            db,
            limit=limit,
            offset=offset,
            city=city,
            status=status,
        )