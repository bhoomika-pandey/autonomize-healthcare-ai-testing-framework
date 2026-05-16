from datetime import datetime
from jsonschema import validate

patient_schema = {
    "type": "object",
    "properties": {
        "patient_id": {"type": "string"},
        "name": {"type": "string"},
        "dob": {"type": "string"},
        "condition": {"type": "string"}
    },
    "required": [
        "patient_id",
        "name",
        "dob",
        "condition"
    ]
}

def validate_patient_schema(data):
    validate(
        instance=data,
        schema=patient_schema
    )

def validate_dob_format(dob):
    datetime.strptime(dob, "%Y-%m-%d")