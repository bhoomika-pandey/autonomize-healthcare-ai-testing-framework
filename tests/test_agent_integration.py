from utils.api_client import get_request
from utils.validators import validate_patient_schema


def test_extract_patient_success():

    response = get_request("/extract-patient/P123")

    assert response.status_code == 200

    data = response.json()

    validate_patient_schema(data)

    assert data["patient_id"] == "P123"

def test_extract_patient_not_found():

    response = get_request("/extract-patient/P999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Patient record not found"

def test_patient_dob_format():

    response = get_request("/extract-patient/P123")

    data = response.json()

    dob = data["dob"]

    assert len(dob) == 10
    assert "-" in dob