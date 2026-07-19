from sqlalchemy.orm import Session
from app.models.intervention import Intervention
from sqlalchemy import select




class InterventionRepository():


    def get_last_intervention_by_antenna_ids(
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