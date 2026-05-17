# Autonomize Healthcare AI Testing Framework

## Overview

This project demonstrates a QA automation framework designed for testing an AI-driven healthcare platform.

The framework focuses on:

- Agent Integration Testing
- Model Integration Testing
- Patient Safety Validation
- Privacy & Data Isolation Testing
- Upload Validation Scenarios
- Risk-Based Testing

The solution simulates a healthcare AI system using FastAPI mock services and validates system behavior using pytest automation.

---

# Tech Stack

| Area | Tool |
|---|---|
| Backend Mock APIs | FastAPI |
| API Automation | Pytest |
| UI Automation | Playwright |
| API Requests | requests |
| Reporting | pytest-html |
| Runtime | Python |
| CI/CD Ready | GitHub Actions |
| Pipeline Compatibility | Jenkins, Azure DevOps |
| Containerization | Docker |

---

# Project Structure

```text
autonomize-healthcare-ai-testing-framework/
│
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml
│
├── app/
│   ├── __init__.py
│   └── mock_api.py
│
├── tests/
│   ├── __init__.py
│   ├── test_health_check.py
│   ├── test_agent_integration.py
│   ├── test_model_integration.py
│   └── test_upload_validation.py
│
├── playwright_tests/
│   └── test_patient_ui.py
│
├── utils/
│   ├── __init__.py
│   ├── api_client.py
│   └── validators.py
│
├── test_data/
│
├── reports/
│
├── README.md
├── TEST_STRATEGY.md
├── TEST_CASES.md
├── DEFECT_SUMMARY.md
├── TEST_PRIORITIES.md
├── requirements.txt
├── pytest.ini
├── Dockerfile
├── .dockerignore
└── .gitignore
```

---

# APIs Implemented

## 1. Patient Extraction API

```http
GET /extract-patient/{patient_id}
```

Simulates:
- healthcare agent extraction
- structured patient data retrieval

---

## 2. AI Risk Prediction API

```http
POST /predict-risk
```

Simulates:
- AI model integration
- symptom risk classification

---

## 3. Upload Validation API

```http
POST /upload-chart
```

Simulates:
- medical chart upload validation
- incorrect file format handling

---

# Mock Healthcare UI

A lightweight healthcare patient-intake UI is included to simulate:

- Patient symptom submission
- AI risk prediction workflows
- Medical chart upload interactions
- UI error-message validation

UI Endpoint:

```text
http://127.0.0.1:8000/patient-intake-ui
```

The UI is used for Playwright-based end-to-end automation testing.

# Test Coverage

The framework validates:

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

# Setup Instructions

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

```bash
pip install -r requirements.txt
```

---

# Running FastAPI Server

```bash
uvicorn app.mock_api:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Running FastAPI Server

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

# Running API Tests

```bash
pytest -v
```

---

# Running Playwright Tests

Ensure FastAPI server is already running.

```bash
pytest playwright_tests -v
```

---

# Generate HTML Report

```bash
pytest -v --html=reports/report.html
```

# CI/CD Integration

The framework is integrated with GitHub Actions for automated test execution.

Pipeline capabilities include:
- Dependency installation
- FastAPI server startup
- Automated pytest execution
- HTML report generation
- Report artifact upload

The framework architecture is CI/CD compatible and can also be integrated with:
- Jenkins pipelines
- Azure DevOps pipelines
- Docker-based execution environments

---

# Docker Support

The framework supports Docker-based execution for consistent runtime environments.

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

Additional validations included:

- Cross-patient data isolation
- Invalid payload handling
- Nuanced symptom interpretation
- Contradictory symptom testing
- Ambiguous symptom handling
- Prompt injection prevention
- Hallucination boundary validation
- Supported AI output enforcement
- Confidence-score validation
- Graceful handling of malformed inputs

---

# Future Enhancements

Potential future improvements:

- Kubernetes deployment manifests for scalable orchestration
- Authentication & authorization validation
- Performance testing using JMeter
- PHI masking validation
- Real AI model integration
- Advanced healthcare workflow orchestration
- Load testing for concurrent patient workflows
- Distributed execution support for large-scale regression suites

---

# Author

Bhoomika Pandey