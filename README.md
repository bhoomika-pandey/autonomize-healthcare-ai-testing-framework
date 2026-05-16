# Healthcare AI Testing Framework

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
| Automation Framework | Pytest |
| API Requests | requests |
| Reporting | pytest-html |
| Runtime | Python |
| CI/CD Ready | GitHub Actions |
| Pipeline Compatibility | Jenkins, Azure DevOps |

---

# Project Structure

```text
autonomize-healthcare-ai-testing-framework/
│
├── app/
├── tests/
├── utils/
├── test_data/
├── reports/
│
├── README.md
├── TEST_STRATEGY.md
├── TEST_CASES.md
├── DEFECT_SUMMARY.md
└── requirements.txt
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

# Test Coverage

The framework validates:

- Positive and negative API scenarios
- Schema validation
- Nuanced patient input handling
- Contradictory symptom handling
- Privacy and cross-patient isolation
- Upload validation scenarios
- Error response validation
- AI model robustness

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

# Running Tests

```bash
pytest -v
```

---

# Generate HTML Report

```bash
pytest -v --html=reports/report.html
```

---

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

# AI Safety Considerations

Additional validations included:

- Cross-patient data isolation
- Invalid payload handling
- Nuanced symptom interpretation
- Contradictory symptom testing
- Graceful handling of malformed inputs

---

# Future Enhancements

Potential future improvements:

- Playwright-based UI automation
- Docker containerization
- Jenkins pipeline integration
- Azure DevOps pipeline integration
- Authentication & authorization validation
- Performance testing using JMeter
- Real AI model integration
- Prompt injection testing
- PHI masking validation

---

# Author

Bhoomika Pandey