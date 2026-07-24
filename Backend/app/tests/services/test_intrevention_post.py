from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


client = TestClient(app)

API_KEY = settings.secret_key

headers = {
    "X-API-key": API_KEY,
}


def test_create_intervention_success(antenna_id):
    response = client.post(
        "/api/v1/interventions",
        headers=headers,
        json={
            "antenna_id": antenna_id,
            "description": "Remplacement module",
            "technician_identity": "Jean Free",
            "priority": "LOW",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["antenna_id"] == antenna_id
    assert data["description"] == "Remplacement module"
    assert data["technician_identity"] == "Jean Free"
    assert data["priority"] == "LOW"
    assert data["ended_at"] is None


def test_create_intervention_duplicate_active(antenna_id):
    response1 = client.post(
        "/api/v1/interventions",
        headers=headers,
        json={
            "antenna_id": antenna_id,
            "description": "Remplacement module",
            "technician_identity": "Jean Free",
            "priority": "LOW",
        },
    )

    assert response1.status_code == 201

    response2 = client.post(
        "/api/v1/interventions",
        headers=headers,
        json={
            "antenna_id": antenna_id,
            "description": "Deuxième intervention",
            "technician_identity": "Jean Free",
            "priority": "LOW",
        },
    )

    assert response2.status_code == 409


def test_create_intervention_without_api_key(antenna_id):
    response = client.post(
        "/api/v1/interventions",
        json={
            "antenna_id": antenna_id,
            "description": "Remplacement module",
            "technician_identity": "Jean Free",
            "priority": "LOW",
        },
    )

    assert response.status_code == 403