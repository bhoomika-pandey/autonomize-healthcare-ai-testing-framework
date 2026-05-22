# HLD and BRD: Healthcare Agentic Testing Workflow

## Business Requirement

The testing framework validates a healthcare AI workflow with emphasis on
clinical safety, patient data integrity, privacy, and model-output reliability.
The goal is not to build a production agentic platform. The goal is to simulate
the responsibilities of multiple healthcare agents and prove that the complete
patient journey is testable through API, UI, BDD, and CI automation.

## In-Scope Workflow

The complete workflow covers:

1. Patient data retrieval from a mocked healthcare source system.
2. Data extraction and schema validation.
3. Clinical symptom submission.
4. AI risk classification.
5. Model safety checks for unsafe or adversarial input.
6. Escalation decision for high-risk symptoms.
7. Medical chart upload validation.
8. Privacy boundary validation.
9. Audit event generation.

## High-Level Architecture

```text
Patient/Test Data Source
    -> Workflow Engine
        -> Data Extraction Responsibility
        -> Schema Validation Responsibility
        -> Risk Classification Responsibility
        -> Model Safety Responsibility
        -> Escalation Responsibility
        -> Upload Validation Responsibility
        -> Privacy and Audit Responsibility
    -> API, BDD, Pytest, and Playwright Test Layers
    -> CI Report Artifacts
```

## Component Responsibilities

| Component | Responsibility |
|---|---|
| `app/mock_api.py` | Mock FastAPI service and UI endpoint used by automation. |
| `app/workflow_engine.py` | Lightweight orchestration for the complete patient workflow. |
| `app/schemas/patient_schema.json` | Contract for extracted patient data validation. |
| `features/` | Behave BDD acceptance scenarios written in business-readable language. |
| `tests/test_end_to_end_workflow.py` | Pytest validation of the complete workflow. |
| `playwright_tests/` | UI automation for patient symptom submission and upload behavior. |
| `test_data/` | Controlled mock healthcare data. |
| `reports/` | Test execution reports generated locally or in CI. |

## Why This Is Not Overengineered

The framework models multiple agent responsibilities, but implements them as
lightweight workflow functions. This keeps the assignment focused on QA
validation, patient safety, BDD coverage, and CI-ready automation instead of
building a production-grade multi-agent application.

## Acceptance Criteria

- The workflow validates more than one agent responsibility.
- High-risk symptoms trigger escalation.
- Patient schema validation is enforced.
- Prompt injection is blocked before workflow completion.
- Upload validation participates in the end-to-end workflow.
- Audit and privacy checks are represented in the workflow result.
- Behave scenarios describe the full workflow in business-readable language.
- Pytest and Playwright automation remain executable in CI.

