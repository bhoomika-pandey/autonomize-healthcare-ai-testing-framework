import json
from datetime import datetime
from pathlib import Path

from jsonschema import FormatChecker, validate

BASE_DIR = Path(__file__).resolve().parent.parent
PATIENT_SCHEMA_PATH = BASE_DIR / "app" / "schemas" / "patient_schema.json"


with PATIENT_SCHEMA_PATH.open("r", encoding="utf-8") as file:
    patient_schema = json.load(file)


class ValidationError(Exception):
    """Custom validation error for schema and format checks."""


def validate_patient_schema(data):
    """Validate `data` against the patient schema.

    Raises:
        ValidationError: if schema validation fails.
    """
    try:
        validate(instance=data, schema=patient_schema, format_checker=FormatChecker())
    except Exception as exc:
        raise ValidationError(str(exc))


def validate_dob_format(dob):
    """Validate DOB format 'YYYY-MM-DD'.

    Raises:
        ValidationError: if DOB parsing fails.
    """
    try:
        datetime.strptime(dob, "%Y-%m-%d")
    except Exception as exc:
        raise ValidationError(str(exc))
