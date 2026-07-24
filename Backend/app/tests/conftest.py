import pytest

from app.database.session import SessionLocal
from app.models.antenna import Antenna, AntennaStatus
from app.models.intervention import Intervention


@pytest.fixture
def antenna_id():
    db = SessionLocal()

    antenna = Antenna(
        name="Antenne test",
        city="Paris",
        status=AntennaStatus.UP,
    )

    db.add(antenna)
    db.commit()
    db.refresh(antenna)

    created_id = antenna.id

    yield created_id

    db.query(Intervention).filter(
        Intervention.antenna_id == created_id
    ).delete()

    db.delete(antenna)
    db.commit()
    db.close()