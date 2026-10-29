
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_pipe_with_inspections():
    response = client.get("/pipes/PIPE-1001")

    assert response.status_code == 200

    data = response.json()

    assert data["pipe_id"] == "PIPE-1001"
    assert data["material"] == "Carbon Steel"
    assert len(data["inspections"]) == 3


def test_unknown_pipe_returns_404():
    response = client.get("/pipes/PIPE-9999")

    assert response.status_code == 404


def test_invalid_inspection_result_returns_422():
    response = client.post(
        "/pipes/PIPE-1001/inspections",
        json={
            "inspection_type": "Weld Inspection",
            "result": "Unknown"
        }
    )

    assert response.status_code == 422
