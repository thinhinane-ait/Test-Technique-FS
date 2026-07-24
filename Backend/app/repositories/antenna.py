#app.repositories.antenna.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.antenna import Antenna, AntennaStatus


class AntennaRepository():
    def __init__(self):
        pass
    ### get list antennas
    def get_antennas(
            self,
            db: Session,
            *,
            limit: int,
            offset: int,
            city: str | None = None,
            status: AntennaStatus | None = None,

    )-> list[Antenna]:
        statement = select(Antenna)

        if city is not None: 
            statement = statement.where(
                Antenna.city.ilike(city)
            )
        
        if status is not None:
            statement = statement.where(
                Antenna.status == status
                )
        
        statement = (
            statement
            .order_by(Antenna.id)
            .offset(offset)
            .limit(limit)

        )

        return list(db.scalars(statement).all())
     
    def get_antenna_by_id(
            self,
            db: Session,
            antenna_id: int,
    ) -> Antenna | None: 
        statement = (
            select(Antenna)
            .where(Antenna.id == antenna_id)
        )
        return db.scalar(statement)
    
    def update_status_antenna_id(
            self,
            db: Session,
            antenna: Antenna,
            status: AntennaStatus
    )-> Antenna: 
        antenna.status = status
        return antenna
        