#app.repositories.antenna.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.antenna import Antenna, AntennaStatus


class AntennaRepository():
    
    def get_antenna(
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
                Antenna.status.ilike(status)
                )
        
        statement = (
            statement
            .order_by(Antenna.id)
            .offset(offset)
            .limit(limit)

        )

        return list(db.scalars(statement).all())
