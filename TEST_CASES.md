# TEST CASES

# Overview

This document contains detailed test cases for validating the AI healthcare testing framework.

The test suite covers:
- Agent Integration Testing
- Model Integration Testing
- Upload Validation
- Privacy & Patient Safety Validation

---

# TEST CASE 1 — Patient Extraction Success

| Field | Value |
|---|---|
| Test Case ID | TC_AGENT_001 |
| Scenario | Validate successful patient extraction |
| Priority | P1 |
| Severity | High |

## Preconditions
- FastAPI server is running
- Patient record exists

## Steps
1. Send GET request to:
   `/extract-patient/P123`
2. Capture API response
3. Validate response schema

## Expected Result
- Status code should be `200`
- Required patient fields should exist
- Patient data should match expected structure

## Pass Criteria
- All validations pass successfully

---

# TEST CASE 2 — Patient Not Found

| Field | Value |
|---|---|
| Test Case ID | TC_AGENT_002 |
| Scenario | Validate missing patient handling |
| Priority | P1 |
| Severity | High |

## Preconditions
- FastAPI server is running

## Steps
1. Send GET request to:
   `/extract-patient/P999`
2. Capture API response

## Expected Result
- Status code should be `404`
- Error message:
  `Patient record not found`

## Pass Criteria
- API gracefully handles invalid patient ID

---

# TEST CASE 3 — High Risk Classification

| Field | Value |
|---|---|
| Test Case ID | TC_MODEL_001 |
| Scenario | Validate high-risk symptom classification |
| Priority | P0 |
| Severity | Critical |

## Preconditions
- FastAPI server is running

## Steps
1. Send POST request to:
   `/predict-risk`
2. Use payload:

```json
{
  "symptoms": "Severe chest pain"
}
```

3. Capture API response

## Expected Result
- Status code should be `200`
- Risk level should be `high`

## Pass Criteria
- High-risk symptoms classified correctly

---

# TEST CASE 4 — Empty Symptoms Validation

| Field | Value |
|---|---|
| Test Case ID | TC_MODEL_002 |
| Scenario | Validate empty symptom handling |
| Priority | P1 |
| Severity | High |

## Preconditions
- FastAPI server is running

## Steps
1. Send POST request to:
   `/predict-risk`
2. Use payload:

```json
{
  "symptoms": ""
}
```

3. Capture API response

## Expected Result
- Status code should be `400`
- Error message:
  `Symptoms cannot be empty`

## Pass Criteria
- API rejects invalid symptom input

---

# TEST CASE 5 — Nuanced Patient Symptoms

| Field | Value |
|---|---|
| Test Case ID | TC_MODEL_003 |
| Scenario | Validate nuanced symptom interpretation |
| Priority | P1 |
| Severity | High |

## Preconditions
- FastAPI server is running

## Steps
1. Send POST request to:
   `/predict-risk`
2. Use payload:

```json
{
  "symptoms": "Experiencing pressure in chest while breathing"
}
```

3. Capture API response

## Expected Result
- Status code should be `200`
- Risk level should be:
  `high` or `medium`

## Pass Criteria
- AI model handles semantic variation gracefully

---

# TEST CASE 6 — Contradictory Symptoms

| Field | Value |
|---|---|
| Test Case ID | TC_MODEL_004 |
| Scenario | Validate contradictory symptom handling |
| Priority | P1 |
| Severity | High |

## Preconditions
- FastAPI server is running

## Steps
1. Send POST request to:
   `/predict-risk`
2. Use payload:

```json
{
  "symptoms": "I feel okay overall but also severe chest pain"
}
```

3. Capture API response

## Expected Result
- Status code should be `200`
- Risk level should remain valid

## Pass Criteria
- System handles conflicting symptoms safely

---

# TEST CASE 7 — Cross-Patient Data Isolation

| Field | Value |
|---|---|
| Test Case ID | TC_PRIVACY_001 |
| Scenario | Validate patient data isolation |
| Priority | P0 |
| Severity | Critical |

## Preconditions
- FastAPI server is running

## Steps
1. Retrieve patient:
   `P123`
2. Retrieve patient:
   `P456`
3. Compare returned patient data

## Expected Result
- Patient records should remain isolated
- No cross-patient leakage should occur

## Pass Criteria
- Patient identifiers and names remain unique

---

# TEST CASE 8 — Invalid File Upload

| Field | Value |
|---|---|
| Test Case ID | TC_UPLOAD_001 |
| Scenario | Validate unsupported upload format |
| Priority | P2 |
| Severity | Medium |

## Preconditions
- FastAPI server is running

## Steps
1. Upload file:
   `malware.exe`
2. Send request to:
   `/upload-chart`

## Expected Result
- Status code should be `400`
- Clear validation message should appear

## Pass Criteria
- Unsupported file types are blocked successfully

---

# Regression Testing Recommendations

The following areas should always be included in regression cycles:
- Risk classification validation
- Privacy and data isolation
- Upload validation
- Schema validation
- Error handling
- AI semantic robustness

---

# Suggested Future Test Cases

Potential future enhancements:
- Authentication validation
- Authorization testing
- PHI masking validation
- Audit log verification
- Load and performance testing
- Prompt injection testing
- Real AI model validation