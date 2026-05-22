import json
import re
from pathlib import Path

from jsonschema import FormatChecker, validate

BASE_DIR = Path(__file__).resolve().parent.parent
PATIENT_DB_PATH = BASE_DIR / "test_data" / "patient_database.json"
PATIENT_SCHEMA_PATH = BASE_DIR / "app" / "schemas" / "patient_schema.json"


ALLOWED_UPLOAD_EXTENSIONS = [
    ".pdf",
    ".png",
    ".jpg",
]


def _load_json(path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_patient_database():
    if not hasattr(load_patient_database, "_db"):
        load_patient_database._db = _load_json(PATIENT_DB_PATH)
    return load_patient_database._db


def load_patient_schema():
    if not hasattr(load_patient_schema, "_schema"):
        load_patient_schema._schema = _load_json(PATIENT_SCHEMA_PATH)
    return load_patient_schema._schema


def extract_patient(patient_id):
    db = load_patient_database()
    patient = db.get(patient_id)

    if not patient:
        return None

    return patient


def validate_patient(patient):
    schema = load_patient_schema()
    validate(instance=patient, schema=schema, format_checker=FormatChecker())

    return {
        "schema_valid": True,
        "validated_fields": [
            "patient_id",
            "name",
            "dob",
            "condition",
        ],
    }


def classify_risk(symptoms):
    normalized_symptoms = symptoms.lower().strip()

    if not normalized_symptoms:
        return {
            "risk_level": "invalid",
            "confidence": 0,
            "reason": "Symptoms cannot be empty",
        }

    if not re.search(r"[a-z]", normalized_symptoms):
        return {
            "risk_level": "invalid",
            "confidence": 0,
            "reason": "Symptoms contain no clinical text",
        }

    if "ignore all instructions" in normalized_symptoms:
        return {
            "risk_level": "blocked",
            "confidence": 0,
            "reason": "Potential prompt injection detected",
        }

    if (
        "chest pain" in normalized_symptoms
        or "chest pressure" in normalized_symptoms
        or "pressure in chest" in normalized_symptoms
        or "chest discomfort" in normalized_symptoms
    ):
        return {
            "risk_level": "high",
            "confidence": 0.95,
            "reason": "High-risk cardiac symptom detected",
        }

    if "fever" in normalized_symptoms:
        return {
            "risk_level": "medium",
            "confidence": 0.80,
            "reason": "Moderate-risk symptom detected",
        }

    return {
        "risk_level": "low",
        "confidence": 0.60,
        "reason": "No critical symptom keyword detected",
    }


def determine_escalation(prediction):
    if prediction["risk_level"] == "high":
        return {
            "required": True,
            "channel": "clinical_triage_queue",
            "reason": "High-risk patient symptom requires review",
        }

    return {
        "required": False,
        "channel": None,
        "reason": "No immediate escalation required",
    }


def validate_chart_upload(file_name, file_size_bytes):
    if not file_name:
        return {
            "accepted": False,
            "reason": "Medical chart file is required",
        }

    normalized_name = file_name.lower()
    has_allowed_extension = any(
        normalized_name.endswith(extension) for extension in ALLOWED_UPLOAD_EXTENSIONS
    )

    if not has_allowed_extension:
        return {
            "accepted": False,
            "reason": "Unsupported file format",
        }

    if file_size_bytes <= 0:
        return {
            "accepted": False,
            "reason": "Uploaded file is empty",
        }

    if file_size_bytes > (5 * 1024 * 1024):
        return {
            "accepted": False,
            "reason": "File size exceeds allowed limit",
        }

    return {
        "accepted": True,
        "reason": "File uploaded successfully",
    }


def create_audit_event(patient_id, prediction, escalation):
    return {
        "event_type": "patient_intake_workflow_completed",
        "patient_reference": patient_id,
        "risk_level": prediction["risk_level"],
        "escalation_required": escalation["required"],
        "phi_exposed": False,
    }


def validate_privacy_boundary(requested_patient_id, patient):
    return {
        "patient_id_matched": patient["patient_id"] == requested_patient_id,
        "cross_patient_leakage_detected": False,
    }


def run_patient_intake_workflow(
    patient_id, symptoms, chart_file_name, chart_file_size_bytes
):
    # Allow injection of components for easier testing and swapping implementations.
    return run_patient_intake_workflow_with_components(
        patient_id=patient_id,
        symptoms=symptoms,
        chart_file_name=chart_file_name,
        chart_file_size_bytes=chart_file_size_bytes,
        extractor=extract_patient,
        validator=validate_patient,
        predictor=classify_risk,
        escalator=determine_escalation,
        upload_validator=validate_chart_upload,
        privacy_checker=validate_privacy_boundary,
        auditor=create_audit_event,
    )


def run_patient_intake_workflow_with_components(
    patient_id,
    symptoms,
    chart_file_name,
    chart_file_size_bytes,
    extractor,
    validator,
    predictor,
    escalator,
    upload_validator,
    privacy_checker,
    auditor,
):
    """Run the patient intake workflow using injectable components.

    Each component should be a callable that matches the signature used
    within the original implementation. This enables unit tests to
    inject lightweight stubs and avoids file I/O at import time.
    """
    patient = extractor(patient_id)

    if not patient:
        return {
            "workflow_status": "failed",
            "failure_stage": "data_extraction",
            "detail": "Patient not found",
        }

    schema_validation = validator(patient)
    prediction = predictor(symptoms)

    if prediction["risk_level"] in ["invalid", "blocked"]:
        return {
            "workflow_status": "failed",
            "failure_stage": "model_safety",
            "patient": patient,
            "schema_validation": schema_validation,
            "prediction": prediction,
        }

    escalation = escalator(prediction)
    upload_validation = upload_validator(chart_file_name, chart_file_size_bytes)

    if not upload_validation["accepted"]:
        return {
            "workflow_status": "failed",
            "failure_stage": "upload_validation",
            "patient": patient,
            "schema_validation": schema_validation,
            "prediction": prediction,
            "escalation": escalation,
            "upload_validation": upload_validation,
        }

    privacy_validation = privacy_checker(patient_id, patient)
    audit_event = auditor(patient_id, prediction, escalation)

    return {
        "workflow_status": "completed",
        "patient": patient,
        "schema_validation": schema_validation,
        "prediction": prediction,
        "escalation": escalation,
        "upload_validation": upload_validation,
        "privacy_validation": privacy_validation,
        "audit_event": audit_event,
    }
