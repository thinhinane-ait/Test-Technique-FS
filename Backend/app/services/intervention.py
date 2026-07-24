#app/services/intervention.py
from app.repositories.intervention import InterventionRepository
from sqlalchemy.orm import Session
from app.schemas.intervention import InterventionCreate
from app.models.intervention import Intervention
from app.models.antenna import AntennaStatus
from app.repositories.antenna import AntennaRepository
from fastapi import HTTPException

class InterventionService:

    def __init__(self):
        self.intervention_repository = InterventionRepository()
        self.antenna_repository = AntennaRepository()

    def create_intervention(
            self,
            db: Session,
            intervention: InterventionCreate,
    )-> Intervention:
        ##get antenna 
        antenna = self.antenna_repository.get_antenna_by_id(
            db,
            intervention.antenna_id,
        )
        if antenna is None: 

             raise HTTPException(
                    status_code=404,
                    detail="L'antenne n'existe pas"
                )
        ### get last intervention pour antenne specifique
        
        active_intervention = self.intervention_repository.get_active_intervention_by_antenna_id(
            db,
            intervention.antenna_id
        )

        ### vérifier si `ended_at` IS NULL
        if active_intervention: 
             raise HTTPException(
                    status_code=409,
                    detail=f"Une intervention est déja en cours pour cette {intervention.antenna_id}"
                )
        
        ### Creer une nouvelle intervention pour l'antenne 
        new_intervention = self.intervention_repository.create_new_intervention(
            db,
            intervention
        )
        self.antenna_repository.update_status_antenna_id(
                db,
                antenna,
                AntennaStatus.DOWN,
            )
        db.commit()
        db.refresh(new_intervention)
        return new_intervention

    
    def close_intervention(
            self,
            db: Session,
            intervention_id: int
    )-> Intervention:
        
        ### Véréfier l'existance de l'intervention

        intervention = self.intervention_repository.get_intervention_by_id(
            db,
            intervention_id
        )

        if intervention is None:

            raise HTTPException(
                status_code=404,
                detail="Aucune intervention en cours"
            )
        
        if intervention.ended_at is not None:
            raise HTTPException(
                status_code=409,
                detail="L'intervention est déjà clôturée"
            )
        
        closed_intervention = self.intervention_repository.close_intervention(
                intervention
            )
        
        antenna = self.antenna_repository.get_antenna_by_id(
            db,
            intervention.antenna_id
        )
        
        self.antenna_repository.update_status_antenna_id(
                db,
                antenna,
                AntennaStatus.UP,
            )
        
        db.commit()
        db.refresh(closed_intervention)

        return closed_intervention
        





        