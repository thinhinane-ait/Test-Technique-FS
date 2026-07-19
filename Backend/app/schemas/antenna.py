#app/schemas/antenna.py
from pydantic import BaseModel,ConfigDict
from app.models.antenna import AntennaStatus
from datetime import datetime
from app.schemas.intervention import InterventionSummary


class AntennaBase(BaseModel):
    name: str
    city: str
    status: AntennaStatus


class AntennaResponse(AntennaBase):
    id: int
    created_at: datetime
    latest_intervention: InterventionSummary | None = None


    model_config = ConfigDict(from_attributes=True) 
