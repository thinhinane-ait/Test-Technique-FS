#app/schemas/intervention.py

from pydantic import BaseModel, ConfigDict
from app.models.intervention import InterventionPriority
from datetime import datetime

class InterventionBase(BaseModel):
    antenna_id: int
    description: str
    technician_identity: str
    priority: InterventionPriority

class InterventionCreate(InterventionBase):
    pass

class InterventionResponse(InterventionBase):
    id: int
    created_at: datetime
    ended_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True,extra="forbid") 

class InterventionSummary(BaseModel):
    id: int
    description: str
    technician_identity: str
    priority: InterventionPriority
    created_at: datetime
    ended_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True,extra="forbid")
     



