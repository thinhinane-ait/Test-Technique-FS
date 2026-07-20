#app/schemas/intervention.py

from pydantic import BaseModel, ConfigDict
from app.models.intervention import InterventionPriority
from datetime import datetime

class InterventionSummary(BaseModel):
    id: int
    description: str
    technician_identity: str
    priority: InterventionPriority
    created_at: datetime
    ended_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True,extra="forbid")
