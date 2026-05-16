from utils.api_client import get_request

def test_health_check():

    response = get_request("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"