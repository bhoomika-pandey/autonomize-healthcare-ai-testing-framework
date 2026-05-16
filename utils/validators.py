def validate_patient_schema(data):

    required_fields = [
        "patient_id",
        "name",
        "dob",
        "diagnosis"
    ]

    for field in required_fields:

        assert field in data, f"{field} is missing"

    assert isinstance(data["patient_id"], str)
    assert isinstance(data["name"], str)
    assert isinstance(data["dob"], str)
    assert isinstance(data["diagnosis"], str)