from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import pytest

from app.database.session import SessionLocal
from app.models.intervention import Intervention

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_interventions():
    db = SessionLocal()

    print("Avant nettoyage :", db.query(Intervention).count())

    db.query(Intervention).delete()
    db.commit()

    print("Après nettoyage :", db.query(Intervention).count())

    yield

    db.close()



API_KEY = settings.secret_key

header = {
    "X-API-key":API_KEY
}

def test_close_ticket():

    # Création intervention active
    create_response = client.post(
        "/api/v1/intervention",
        headers=header,
        json={
            "antenna_id": 1,
            "description": "Remplacement module",
            "technician_identity": "Jean Free",
            "priority": "LOW"
        }
    )
 
    assert create_response.status_code == 200
    print("CREATE STATUS :", create_response.status_code)
    print("CREATE BODY :", create_response.json())

    intervention = create_response.json()

    intervention_id = intervention["id"]


    # Fermeture intervention
    response = client.patch(
    f"/api/v1/intervention/{intervention_id}/close",
    headers=header,
)

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200

    data = response.json()

    assert data["ended_at"] is not None