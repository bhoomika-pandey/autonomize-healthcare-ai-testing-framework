import requests

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():

    response = requests.get(f"{BASE_URL}/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Healthcare AI Testing API is running"