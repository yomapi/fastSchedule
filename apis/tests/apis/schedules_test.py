from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_find_schedule_with_limit():
    response = client.get("/api/v1/schedule/")
    assert response.status_code == 200
    response_dict = response.json()
    assert isinstance(response_dict["count"], int)
    assert isinstance(response_dict["data"], list)
