from app.schemas.antenna import AntennaBase
from app.models.antenna import AntennaStatus
import pytest 
from pydantic import ValidationError

def test_antenna_base():
        antenna = AntennaBase(
            name = "67482_111",
            city='Bas-Rhin',
            status = AntennaStatus.UP
        )
        assert antenna.name == "67482_111"
        assert antenna.city == "Bas-Rhin"
        assert antenna.status == AntennaStatus.UP


 ### Verifier qu'une erreur est leve si le name est absent 

def test_missing_name():
    with pytest.raises(ValidationError):
        AntennaBase(
            city="Paris",
            status=AntennaStatus.UP
        )

 ### Verifier qu'une erreur est leve si le city est absent 

def test_missing_city():
    with pytest.raises(ValidationError):
        AntennaBase(
            name="75482_111",
            status=AntennaStatus.UP
        )

### Verifier qu'une erreur est leve si le status est ivalide

def test_validation_status():
    with pytest.raises(ValidationError):
        AntennaBase(
            name = "67482_111",
            city='Bas-Rhin',
            status="Test"
        )




# python -m pytest app/tests/schemas/test_antenna.py -v