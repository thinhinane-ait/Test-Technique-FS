from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


client = TestClient(app)

API_KEY = settings.secret_key

headers = {
    "X-API-key": API_KEY,
}


def test_close_ticket(antenna_id):
    create_response = client.post(
        "/api/v1/interventions",
        headers=headers,
        json={
            "antenna_id": antenna_id,
            "description": "Remplacement module",
            "technician_identity": "Jean Free",
            "priority": "LOW",
        },
    )

    assert create_response.status_code == 201

    created_intervention = create_response.json()
    intervention_id = created_intervention["id"]

    close_response = client.patch(
        f"/api/v1/interventions/{intervention_id}/close",
        headers=headers,
    )

    assert close_response.status_code == 200

    data = close_response.json()

    assert data["id"] == intervention_id
    assert data["antenna_id"] == antenna_id
    assert data["ended_at"] is not None