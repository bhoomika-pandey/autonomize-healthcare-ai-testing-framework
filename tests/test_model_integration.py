import requests
from utils.api_client import post_request, get_request

BASE_URL = "http://127.0.0.1:8000"

def test_high_risk_prediction():
    payload = {
        "symptoms": "Severe chest pain"
    }
    response = post_request(
        "/predict-risk",
        payload
    )

    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "high"

def test_low_risk_prediction():
    payload = {
        "symptoms": "Mild headache"
    }
    response = post_request(
        "/predict-risk",
        payload
    )

    data = response.json()
    assert data["risk_level"] == "low"

def test_empty_symptoms():
    payload = {
        "symptoms": ""
    }
    response = post_request(
        "/predict-risk",
        payload
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Symptoms cannot be empty"

def test_nuanced_patient_input():
    payload = {
        "symptoms": "I feel chest pressure and breathing difficulty"
    }
    response = post_request(
        "/predict-risk",
        payload
    )

    data = response.json()
    assert data["risk_level"] in [
        "high",
        "medium"
    ]

def test_semantic_varaiation_input():
    payload = {
        "symptoms": "Experiencing pressure in chest while breathing"
    }
    response = post_request(
        "/predict-risk",
        payload
    )

    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] in [
        "high",
        "medium"
    ]

def test_contradictory_symptoms():
    payload = {
        "symptoms":(
            "I feel okay overall "
            "but also severe chest pain"
        )
    }
    response = post_request(
        "/predict-risk",
        payload
    )

    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] in [
        "high",
        "medium"
    ]

def test_garbage_input():
    payload = {
        "symptoms": "@@@###$$$12345"
    }
    response = post_request(
        "/predict-risk",
        payload
    )

    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "medium"

def test_missing_symptom_field():
    payload = {}
    response = requests.post(
        f"{BASE_URL}/predict-risk",
        json=payload
    )

    assert response.status_code == 422

def test_cross_patient_data_isolation():
    response_1 = get_request(
        "/extract-patient/P123"
    )
    response_2 = get_request(
        "/extract-patient/P456"
    )

    patient_1 = response_1.json()
    patient_2 = response_2.json()

    assert patient_1["patient_id"] != patient_2["patient_id"]
    assert patient_1["name"] != patient_2["name"]

def test_prediction_response_structure():
    payload = {
        "symptoms": "Chest pain"
    }
    response = post_request(
        "/predict-risk",
        payload
    )

    data = response.json()

    assert "risk_level" in data
    assert data["risk_level"] in [
        "high",
        "medium",
        "low"
    ]