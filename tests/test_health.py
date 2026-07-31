from fastapi import status
from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    "Test /health endpoint response."
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
