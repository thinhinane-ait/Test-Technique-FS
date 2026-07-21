#app/repositories/invention.py
from sqlalchemy.orm import Session
from app.models.intervention import Intervention
from app.models.antenna import AntennaStatus
from app.schemas.intervention import InterventionCreate
from app.repositories.antenna import AntennaRepository
from sqlalchemy import select
from datetime import datetime
from fastapi import HTTPException

class InterventionRepository():

    def __init__(self):
        self.antenna_repository = AntennaRepository()

    
    def get_last_intervention_by_antenna_ids(
            self,
            db: Session,
            antenna_ids: list[int],
    )-> list[Intervention]:
        if not antenna_ids:
            return[]
        
        statement = (
            select(Intervention)
            .where(Intervention.antenna_id.in_(antenna_ids))
            .distinct(Intervention.antenna_id)
            .order_by(
                Intervention.antenna_id,
                Intervention.created_at.desc(),
                Intervention.id.desc()
            )
        )

        return list(db.scalars(statement).all())
    
    def create_new_intervention(
            self,
            db: Session,
            intervention: InterventionCreate
    ) -> Intervention:
                db_intervention = Intervention(
                  antenna_id= intervention.antenna_id,
                  description= intervention.description,
                  technician_identity= intervention.technician_identity,
                  priority= intervention.priority
                )
                db.add(db_intervention)
                return db_intervention




        
        
