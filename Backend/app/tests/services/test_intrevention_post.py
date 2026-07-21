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

def test_create_intervention_success():
    response = client.post(
        "/api/v1/intervention",
        headers=header,
        json={
            "antenna_id":1,
            "description": "Remplacement module",
            "technician_identity": 'Jean Free',
            "priority":"LOW"
        }
    )
    assert response.status_code == 200

    data = response.json()

    assert data["antenna_id"] == 1 
    assert data["description"] == "Remplacement module"


def test_create_intervention_duplicate_active():

    response1 = client.post(
        '/api/v1/intervention',
        headers=header,
        json={
            "antenna_id":1,
            "description": "Remplacement module",
            "technician_identity": 'Jean Free',
            "priority":"LOW"
        }
    )
    assert response1.status_code == 200

    # Deuxième création
    response2 = client.post(
        "/api/v1/intervention",
        headers=header,
        json={
            "antenna_id":1,
            "description":"Deuxième intervention",
            "technician_identity":"Jean Free",
            "priority":"LOW"
        }
    )
    assert response2.status_code == 409


def test_create_intervention_without_api_key():
    response = client.post(
        "/api/v1/intervention",
        json={
            "antenna_id":1,
            "description": "Remplacement module",
            "technician_identity": 'Jean Free',
            "priority":"LOW"
        }
    )
    assert response.status_code == 403
    