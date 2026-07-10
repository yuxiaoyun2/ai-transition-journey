from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_document():
    response = client.get("/documents")

    assert response.status_code == 200

    assert response.headers["content-type"].startswith("application/json")

    assert "items" in response.json()
