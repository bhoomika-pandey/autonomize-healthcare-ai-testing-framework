import pytest
from utils.api_client import get_request

@pytest.mark.smoke
@pytest.mark.regression
def test_health_check():
    response = get_request("/health")

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2

    data = response.json()

    assert data["status"] == "healthy"