import pytest

from app.workflow_engine import run_patient_intake_workflow


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.critical
def test_complete_high_risk_patient_intake_workflow(
    valid_workflow_payload
):

    # Validate the full patient-safety workflow across agent responsibilities.

    result = run_patient_intake_workflow(**valid_workflow_payload)

    assert result["workflow_status"] == "completed"

    assert (
        result["patient"]["patient_id"]
        == valid_workflow_payload["patient_id"]
    )
    assert result["schema_validation"]["schema_valid"] is True

    assert result["prediction"]["risk_level"] == "high"
    assert result["prediction"]["confidence"] >= 0.90

    assert result["escalation"]["required"] is True
    assert result["escalation"]["channel"] == "clinical_triage_queue"

    assert result["upload_validation"]["accepted"] is True

    assert (
        result["privacy_validation"]
        ["cross_patient_leakage_detected"]
        is False
    )
    assert result["audit_event"]["phi_exposed"] is False


@pytest.mark.regression
@pytest.mark.critical
def test_workflow_blocks_prompt_injection_before_escalation(
    prompt_injection_workflow_payload
):

    # Validate that model-safety guardrails stop unsafe workflow progression.

    result = run_patient_intake_workflow(
        **prompt_injection_workflow_payload
    )

    assert result["workflow_status"] == "failed"
    assert result["failure_stage"] == "model_safety"
    assert (
        result["prediction"]["reason"]
        == "Potential prompt injection detected"
    )
    assert "escalation" not in result


@pytest.mark.regression
def test_complete_workflow_api_endpoint(
    test_client,
    valid_workflow_payload
):

    # Validate the workflow is exposed through the mock platform API.

    response = test_client.post(
        "/workflow/patient-intake",
        json=valid_workflow_payload
    )

    assert response.status_code == 200

    data = response.json()
    assert data["workflow_status"] == "completed"
    assert data["prediction"]["risk_level"] == "high"
    assert data["escalation"]["required"] is True
    assert data["audit_event"]["phi_exposed"] is False


@pytest.mark.regression
def test_workflow_rejects_invalid_chart_upload(valid_workflow_payload):

    # Validate invalid chart uploads stop workflow completion.

    invalid_payload = {
        **valid_workflow_payload,
        "chart_file_name": "malware.exe"
    }

    result = run_patient_intake_workflow(**invalid_payload)

    assert result["workflow_status"] == "failed"
    assert result["failure_stage"] == "upload_validation"
    assert result["upload_validation"]["accepted"] is False
    assert result["upload_validation"]["reason"] == "Unsupported file format"
