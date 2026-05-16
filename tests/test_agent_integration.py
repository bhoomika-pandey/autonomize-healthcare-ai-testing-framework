import pytest
from utils.api_client import get_request
from utils.validators import (
    validate_patient_schema, 
    validate_dob_format
)

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.critical
def test_extract_patient_success():
    response = get_request("/extract-patient/P123")

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2
    data = response.json()

    validate_patient_schema(data)


@pytest.mark.regression
@pytest.mark.critical
def test_extract_patient_not_found():
    response = get_request("/extract-patient/P999")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Patient record not found"


@pytest.mark.regression
def test_patient_dob_format():
    response = get_request("/extract-patient/P123")

    data = response.json()

    validate_dob_format(data["dob"])