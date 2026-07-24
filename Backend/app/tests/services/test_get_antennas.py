from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_antennas(antenna_id):
    response = client.get("/api/v1/antennas")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert any(
        antenna["id"] == antenna_id
        for antenna in data
    )


def test_get_antennas_with_filters(antenna_id):
    response = client.get(
        "/api/v1/antennas",
        params={
            "city": "Paris",
            "status": "UP",
            "limit": 10,
            "offset": 0,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert any(
        antenna["id"] == antenna_id
        and antenna["city"] == "Paris"
        and antenna["status"] == "UP"
        for antenna in data
    )