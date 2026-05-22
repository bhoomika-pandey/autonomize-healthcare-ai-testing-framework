# Autonomize Healthcare AI Testing Framework

## Overview

This project demonstrates a QA automation framework designed for testing an AI-driven healthcare platform.

The framework focuses on:

- End-to-end healthcare workflow validation
- Agent and model integration testing
- Behave BDD workflow automation
- Patient safety and clinical validation
- Privacy and cross-patient isolation testing
- AI risk classification and escalation validation
- Medical chart upload validation
- AI safety and adversarial input validation

The solution simulates a healthcare AI workflow using FastAPI mock services, Behave BDD workflows, Playwright UI automation, and Pytest-based validation layers.

The framework validates complete healthcare workflows including schema validation, AI risk classification, escalation handling, upload validation, model safety checks, privacy validation, and audit evidence generation.

---

# Tech Stack

| Area | Tool |
|---|---|
| Backend Workflow Services | FastAPI |
| API Automation | Pytest |
| BDD Workflow Automation | Behave |
| UI Workflow Automation | Playwright |
| API Requests | requests |
| Reporting | pytest-html |
| Code Quality | pre-commit, black, ruff, isort |
| Runtime | Python |
| CI/CD | GitHub Actions |
| Pipeline Compatibility | Jenkins, Azure DevOps |
| Containerization | Docker |

---

# Project Architecture

The framework is structured to support healthcare workflow orchestration, BDD automation, UI workflow validation, AI safety validation, and end-to-end workflow testing.

```text
autonomize-healthcare-ai-testing-framework/
│
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml
│
├── app/
│   ├── __init__.py
│   ├── mock_api.py
│   └── workflow_engine.py
│
├── docs/
│   ├── E2E_WORKFLOW.md
│   └── HLD_BRD_DOCUMENTATION.md
│
├── features/
│   ├── steps/
│   │   └── patient_workflow_steps.py
│   │
│   ├── environment.py
│   └── patient_intake_workflow.feature
│
├── playwright_tests/
│   └── test_patient_ui.py
│
├── test_data/
│   └── patient_database.json
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_agent_integration.py
│   ├── test_end_to_end_workflow.py
│   ├── test_health_check.py
│   ├── test_model_integration.py
│   ├── test_upload_validation.py
│   └── test_workflow_engine.py
│
├── utils/
│   ├── __init__.py
│   ├── api_client.py
│   ├── logger.py
│   └── validators.py
│
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── DEFECT_SUMMARY.md
├── Dockerfile
├── README.md
├── TEST_CASES.md
├── TEST_PRIORITIES.md
├── TEST_STRATEGY.md
├── behave.ini
├── pyproject.toml
├── pytest.ini
└── requirements.txt
```

---

# Workflow Components

The framework exposes healthcare workflow components that simulate patient processing, AI risk evaluation, validation workflows, and medical chart handling.

## 1. Patient Extraction Workflow Component

```http
GET /extract-patient/{patient_id}
```

Simulates:
- patient workflow extraction
- structured healthcare payload validation

---

## 2. AI Risk Prediction Workflow Component

```http
POST /predict-risk
```

Simulates:
- AI-driven healthcare risk evaluation
- patient risk classification workflows

---

## 3. Medical Upload Validation Workflow Component

```http
POST /upload-chart
```

Simulates:
- medical chart validation workflows
- healthcare file safety validation

---

# Mock Healthcare UI

A lightweight healthcare patient-intake UI is included to simulate complete patient workflow interactions across:

- Patient symptom submission
- AI-driven risk classification
- Medical chart upload validation
- Workflow escalation scenarios
- UI-level healthcare validation feedback

UI Endpoint:

```text
http://127.0.0.1:8000/patient-intake-ui
```

The UI is used for Playwright-based end-to-end healthcare workflow validation and user interaction testing.

# Test Coverage

The framework validates:

- End-to-end multi-stage healthcare workflow validation
- Workflow transition integrity validation
- Behave BDD workflow automation
- Clinical safety workflow validation
- High-risk escalation workflow validation
- Positive and negative API scenarios
- Agent integration validation
- Model integration validation
- Schema validation
- Nuanced patient input handling
- Contradictory symptom handling
- Ambiguous symptom handling
- Prompt injection validation
- Hallucination boundary validation
- Privacy and cross-patient isolation
- Upload validation scenarios
- Error response validation
- AI model robustness
- UI responsiveness validation
- Playwright end-to-end automation

---

# Environment Setup

Follow the steps below to configure the healthcare workflow automation environment locally.

## Clone Repository

```bash
git clone <repo_url>
cd autonomize-healthcare-ai-testing-framework
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

Install all dependencies required for workflow orchestration testing, BDD automation, UI workflow validation, and reporting.

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a local environment configuration file from the provided example:

```bash
cp .env.example .env
```

Example environment configuration:

```env
BASE_URL=http://127.0.0.1:8000
REQUEST_TIMEOUT=10
```
---

# Running Healthcare Workflow Services

Start the FastAPI-based healthcare workflow services locally before executing workflow automation and validation suites.

```bash
uvicorn app.mock_api:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Patient Intake UI:

```text
http://127.0.0.1:8000/patient-intake-ui
```

---

# Running Pytest Validation Suite

```bash
pytest -v
```

---

# Running Playwright Workflow Tests

Ensure healthcare workflow services are already running before executing Playwright workflow automation.

```bash
pytest playwright_tests -v
```

---

# Running BDD Workflow Tests

The framework uses Behave BDD workflows to validate complete healthcare workflow orchestration scenarios across patient intake, schema validation, risk classification, escalation handling, and AI safety validation.

```bash
behave
```

Primary healthcare workflow feature:

```text
features/patient_intake_workflow.feature
```

---

# Code Quality Validation

The framework includes automated code quality validation using pre-commit hooks, formatting checks, import sorting, and linting validation.

Run all configured code quality checks:

```bash
pre-commit run --all-files
```
---

# Complete Workflow Coverage

The end-to-end healthcare workflow orchestration is implemented in:

```text
app/workflow_engine.py
```

The workflow validates the complete patient journey across:

- Patient intake and workflow initiation
- Structured payload extraction and schema validation
- AI-driven risk classification and confidence validation
- Prompt-injection and AI safety validation
- High-risk escalation handling
- Medical chart upload validation
- Privacy and cross-patient isolation validation
- Workflow audit and traceability checks

---

# Workflow Validation Stages

The framework validates the following stages across the end-to-end healthcare workflow orchestration pipeline:

| Workflow Stage | Validation Scope |
|---|---|
| Patient Intake | Patient symptom submission and workflow initiation |
| Patient Extraction | Structured healthcare payload extraction and schema validation |
| Clinical Validation | DOB validation, malformed payload handling, and safety checks |
| Risk Classification | AI-driven healthcare risk prediction and confidence validation |
| Upload Validation | Medical chart upload validation and unsupported file handling |
| Workflow Escalation | High-risk workflow escalation and safety-boundary validation |
| Audit Validation | Workflow completion and response traceability validation |

# Generate Workflow Validation Report

The framework supports HTML-based workflow validation reporting for Pytest execution results.

```bash
pytest -v --html=reports/report.html
```

# CI/CD Integration

The framework integrates with GitHub Actions to automate healthcare workflow validation, BDD execution, UI workflow testing, and reporting pipelines.

Pipeline capabilities include:

- Dependency installation and environment setup
- FastAPI workflow service startup
- Automated Pytest execution
- Behave BDD workflow execution
- Playwright UI workflow automation
- HTML report generation
- Report artifact upload

The framework architecture is CI/CD compatible and supports integration with:

- GitHub Actions
- Jenkins pipelines
- Azure DevOps pipelines
- Docker-based execution environments

---

# Docker Support

The framework supports Docker-based execution for consistent healthcare workflow automation and reproducible test environments.

## Build Docker Image

```bash
docker build -t autonomize-healthcare-ai-testing-framework .
```

## Run Docker Container

```bash
docker run -p 8000:8000 autonomize-healthcare-ai-testing-framework
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```
---

# AI Safety Considerations

The framework includes dedicated AI safety and healthcare validation checks across workflow execution, model behavior, and patient data handling:

- Cross-patient data isolation
- Invalid payload handling
- Nuanced and ambiguous symptom interpretation
- Contradictory symptom testing
- Prompt injection prevention
- Hallucination boundary validation
- Supported AI output enforcement
- Confidence-score validation
- Graceful handling of malformed inputs

---

# Future Enhancements

Potential future improvements:

- Kubernetes deployment support for scalable workflow orchestration
- Authentication and role-based healthcare access validation
- Performance and load testing using JMeter
- PHI masking and sensitive healthcare data validation
- Real AI/LLM model integration
- Concurrent patient workflow execution testing
- Distributed execution support for large-scale regression suites
- Advanced healthcare workflow state management

---

# Author

Bhoomika Pandey
