# End-to-End Patient Workflow

## Primary Flow

1. Patient record is retrieved from the healthcare source system.
2. Extracted patient data is validated against the patient schema.
3. Patient symptom text is submitted for model classification.
4. Model safety checks reject unsafe prompt-injection attempts.
5. Risk model returns a supported risk level and confidence score.
6. High-risk classification triggers clinical escalation.
7. Medical chart upload is validated for file type and size.
8. Privacy checks confirm the requested patient remains isolated.
9. Audit event records the workflow outcome without exposing PHI.

## Automation Coverage

| Layer | Coverage |
|---|---|
| Behave | Business-readable complete workflow scenarios. |
| Pytest | API and workflow assertions with strict pass/fail checks. |
| Playwright | Patient-facing UI symptom and upload interactions. |
| CI | Automated execution and report publishing. |

## Critical Edge Cases

- Missing patient ID.
- Empty symptom input.
- Prompt-injection input.
- Contradictory symptom phrasing with severe clinical indicators.
- Unsupported chart file type.
- Empty chart upload.
- Oversized chart upload.
- Cross-patient data leakage.
- Missing audit event.
- High-risk classification without escalation.

