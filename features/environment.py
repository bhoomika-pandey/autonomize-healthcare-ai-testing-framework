from app.workflow_engine import run_patient_intake_workflow


def before_scenario(context, scenario):
    context.run_patient_intake_workflow = run_patient_intake_workflow
    context.workflow_result = None
