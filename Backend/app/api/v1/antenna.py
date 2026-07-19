from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from typing import Annotated
from app.schemas.antenna import AntennaResponse

router = APIRouter(
    prefix = "/antennas",
    tags=["Antennas"],
)



DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get(
    "",
    response_model=list[AntennaResponse]
)