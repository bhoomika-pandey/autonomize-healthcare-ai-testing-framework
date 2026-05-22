import pytest

from utils.api_client import get_request
from utils.validators import (
    ValidationError,
    validate_dob_format,
    validate_patient_schema,
)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.critical
def test_extract_patient_success():

    # Validate successful patient extraction and schema integrity.

    response = get_request("/extract-patient/P123")

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2
    data = response.json()

    validate_patient_schema(data)


@pytest.mark.regression
@pytest.mark.critical
def test_extract_patient_not_found():

    # Validate missing patient record handling behavior.

    response = get_request("/extract-patient/P800")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Patient not found"


@pytest.mark.regression
def test_patient_dob_format():

    # Validate extracted patient DOB format compliance.

    response = get_request("/extract-patient/P123")

    data = response.json()

    validate_dob_format(data["dob"])


@pytest.mark.regression
@pytest.mark.critical
def test_cross_patient_data_isolation():

    # Validate patient-data isolation between healthcare records.

    response_1 = get_request("/extract-patient/P123")
    response_2 = get_request("/extract-patient/P456")

    patient_1 = response_1.json()
    patient_2 = response_2.json()

    assert patient_1["patient_id"] != patient_2["patient_id"]
    assert patient_1["name"] != patient_2["name"]


@pytest.mark.regression
def test_missing_required_patient_fields():

    # Validate detection of incomplete patient records.

    incomplete_patient = {"patient_id": "P789", "name": "Incomplete Patient"}

    with pytest.raises(ValidationError):
        validate_patient_schema(incomplete_patient)


@pytest.mark.regression
def test_invalid_dob_format_detection():

    # Validate invalid healthcare DOB format detection.

    invalid_patient = {
        "patient_id": "P999",
        "name": "Corrupted Patient",
        "dob": "12-31-1990",
        "condition": "Asthma",
    }

    with pytest.raises(ValidationError):
        validate_dob_format(invalid_patient["dob"])


@pytest.mark.regression
def test_malformed_patient_schema_detection():

    # Validate malformed healthcare schema detection logic.

    malformed_patient = {"patient_identifier": "P111", "full_name": "Wrong Schema"}

    with pytest.raises(ValidationError):
        validate_patient_schema(malformed_patient)


@pytest.mark.regression
def test_partial_extraction_failure():

    # Validate partially corrupted extraction-response handling.

    partial_patient = {
        "patient_id": "P222",
        "name": None,
        "dob": "1995-02-01",
        "condition": "Hypertension",
    }

    with pytest.raises(ValidationError):
        validate_patient_schema(partial_patient)


@pytest.mark.regression
def test_corrupted_extraction_data():

    # Validate corrupted healthcare extraction-data handling.

    corrupted_patient = {
        "patient_id": 12345,
        "name": True,
        "dob": "invalid-date",
        "condition": [],
    }

    with pytest.raises(ValidationError):
        validate_patient_schema(corrupted_patient)
