from behave import given, then, when

from app.workflow_engine import extract_patient


@given('patient "{patient_id}" exists in the healthcare source system')
def step_patient_exists(context, patient_id):
    context.patient_id = patient_id
    context.patient = extract_patient(patient_id)

    assert context.patient is not None


@when(
    'the complete patient workflow runs with symptoms "{symptoms}" '
    'and chart "{chart_file_name}"'
)
def step_run_complete_workflow(context, symptoms, chart_file_name):
    context.workflow_result = context.run_patient_intake_workflow(
        patient_id=context.patient_id,
        symptoms=symptoms,
        chart_file_name=chart_file_name,
        chart_file_size_bytes=2048,
    )


@when(
    'the complete patient workflow runs with empty symptoms and chart "{chart_file_name}"'
)
def step_run_complete_workflow_empty_symptoms(context, chart_file_name):
    context.workflow_result = context.run_patient_intake_workflow(
        patient_id=context.patient_id,
        symptoms="",
        chart_file_name=chart_file_name,
        chart_file_size_bytes=2048,
    )


@when('the complete patient workflow runs for missing patient "{patient_id}"')
def step_run_missing_patient_workflow(context, patient_id):
    context.patient_id = patient_id
    context.workflow_result = context.run_patient_intake_workflow(
        patient_id=patient_id,
        symptoms="Severe chest pain",
        chart_file_name="chart.pdf",
        chart_file_size_bytes=2048,
    )


@then("the workflow should complete successfully")
def step_workflow_completed(context):
    assert context.workflow_result["workflow_status"] == "completed"


@then("the extracted patient schema should be valid")
def step_schema_valid(context):
    schema_validation = context.workflow_result["schema_validation"]

    assert schema_validation["schema_valid"] is True
    assert "patient_id" in schema_validation["validated_fields"]


@then('the model should classify the patient as "{risk_level}" risk')
def step_model_risk(context, risk_level):
    prediction = context.workflow_result["prediction"]

    assert prediction["risk_level"] == risk_level
    assert 0 <= prediction["confidence"] <= 1


@then("the workflow should trigger clinical escalation")
def step_escalation_required(context):
    escalation = context.workflow_result["escalation"]

    assert escalation["required"] is True
    assert escalation["channel"] == "clinical_triage_queue"


@then("the medical chart upload should be accepted")
def step_upload_accepted(context):
    upload_validation = context.workflow_result["upload_validation"]

    assert upload_validation["accepted"] is True


@then("an audit event should be recorded")
def step_audit_event(context):
    audit_event = context.workflow_result["audit_event"]

    assert audit_event["event_type"] == "patient_intake_workflow_completed"
    assert audit_event["patient_reference"] == context.patient_id
    assert audit_event["phi_exposed"] is False


@then("no cross-patient data leakage should be detected")
def step_privacy_boundary(context):
    privacy_validation = context.workflow_result["privacy_validation"]

    assert privacy_validation["patient_id_matched"] is True
    assert privacy_validation["cross_patient_leakage_detected"] is False


@then('the workflow should fail at the "{failure_stage}" stage')
def step_workflow_failed_at_stage(context, failure_stage):
    assert context.workflow_result["workflow_status"] == "failed"
    assert context.workflow_result["failure_stage"] == failure_stage


@then('the model safety reason should be "{expected_reason}"')
def step_model_safety_reason(context, expected_reason):
    prediction = context.workflow_result["prediction"]

    assert prediction["reason"] == expected_reason


@then('the upload validation reason should be "{expected_reason}"')
def step_upload_validation_reason(context, expected_reason):
    upload_validation = context.workflow_result["upload_validation"]

    assert upload_validation["reason"] == expected_reason


@then('the workflow failure detail should be "{expected_detail}"')
def step_workflow_failure_detail(context, expected_detail):
    assert context.workflow_result["detail"] == expected_detail
