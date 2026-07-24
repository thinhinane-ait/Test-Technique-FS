#app/services/antenna.py
from sqlalchemy.orm import Session
from app.models.antenna import  AntennaStatus
from app.repositories.antenna import AntennaRepository
from app.repositories.intervention import InterventionRepository
from app.schemas.antenna import AntennaResponse

class AntennaService():
    
    def __init__(self):
        self.antenna_repository = AntennaRepository()
        self.intervention_repository = InterventionRepository()

    def list_antennas(
            self,
            db: Session,
            *,
            limit: int,
            offset: int,
            city: str | None = None,
            status: AntennaStatus | None = None,
    )-> list[AntennaResponse]:
              
              antennas =self.antenna_repository.get_antennas(
                    db,
                    limit=limit,
                    offset=offset,
                    city=city,
                    status=status,
              )

              antenna_ids = [antenna.id for antenna in antennas]

              latest_interventions = (
                        self.intervention_repository
                        .get_last_intervention_by_antenna_ids(
                        db,
                        antenna_ids,
                        )
                  )

              latest_by_antenna_id = {
                    intervention.antenna_id: intervention 
                    for intervention in latest_interventions
              }
              return [
                    AntennaResponse(
                          id=antenna.id,
                          name=antenna.name,
                          city=antenna.city,
                          status=antenna.status,
                          created_at=antenna.created_at,
                          latest_intervention=latest_by_antenna_id.get(antenna.id)

                    )
                    for antenna in antennas
              ]