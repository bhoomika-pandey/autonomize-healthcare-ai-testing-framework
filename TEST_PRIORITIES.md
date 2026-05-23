# Risk-Based Test Prioritization

The following prioritization model identifies high-risk healthcare workflow scenarios, AI safety validations, orchestration failures, and patient-safety-sensitive workflows based on severity and business impact.

| Healthcare Workflow Scenario | Severity | Priority |
|---|---|---|
| Cross-patient data leakage | Critical | P0 |
| Incorrect healthcare risk classification | Critical | P0 |
| Workflow orchestration and transition integrity failure | Critical | P0 |
| High-risk escalation workflow failure | Critical | P0 |
| Prompt injection vulnerability | Critical | P0 |
| Hallucination boundary violation | Critical | P0 |
| Missing patient records | High | P1 |
| Empty symptoms submission | High | P1 |
| No file selected upload warning | High | P1 |
| Oversized file upload handling | High | P1 |
| End-to-end workflow interruption | High | P1 |
| Workflow sequencing inconsistency | High | P1 |
| Invalid upload handling | Medium | P2 |
| Successful chart upload | Medium | P2 |
| Ambiguous symptom handling | Medium | P2 |
| Workflow response inconsistency | Medium | P2 |
| UI error messaging | Low | P3 |
| Minor UI responsiveness issues | Low | P3 |

## Priority Legend

| Priority | Description |
|---|---|
| P0 | Critical healthcare workflow failures with severe patient-safety or compliance impact |
| P1 | High-risk workflow failures affecting orchestration continuity, validation integrity, or user workflows |
| P2 | Medium-risk validation failures with limited workflow impact |
| P3 | Low-risk usability or non-blocking workflow issues |