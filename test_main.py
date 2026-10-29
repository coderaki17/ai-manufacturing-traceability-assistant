
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_existing_pipe():
    response = client.get("/pipes/PIPE-1001")

    assert response.status_code == 200
    assert response.json()["pipe_id"] == "PIPE-1001"
    assert response.json()["quality_status"] == "Passed"


def test_missing_pipe():
    response = client.get("/pipes/PIPE-9999")

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Pipe PIPE-9999 was not found"
    )


def test_pipe_id_is_case_insensitive():
    response = client.get("/pipes/pipe-1001")

    assert response.status_code == 200
    assert response.json()["pipe_id"] == "PIPE-1001"
