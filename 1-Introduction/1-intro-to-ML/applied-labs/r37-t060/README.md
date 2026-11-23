# Applied Lab R37-T060: Security-Scenario Rubric Checker

## Overview
This applied lab extends [Introduction to Machine Learning](../../README.md) by introducing a security scenario analysis schema and an automated rubric checker. In real-world machine learning deployments, understanding the threat surface—including datasets, model weights, and inference APIs—is crucial from day one.

## Scenario Schema
Each security scenario is structured as:
- **`asset`**: The machine learning asset requiring protection (e.g., training datasets, model weights, inference endpoints).
- **`threat`**: The adversarial threat or failure mode (e.g., data poisoning, model inversion, evasion attacks).
- **`control`**: The technical or organizational safeguard implemented (e.g., hash validation, differential privacy, rate limiting).
- **`residual_risk`**: The assessed remaining risk post-control implementation.

## Rubric Assessment Rules
1. **Pass (`pass`)**: All required fields (`asset`, `threat`, `control`, `residual_risk`) are non-empty and the control is structurally aligned with the threat category.
2. **Fail (`fail`)**: Any required field (such as `asset`) is missing or empty.
3. **Flagged for Review (`flagged_for_review`)**: All fields are present, but the specified control appears structurally unrelated to the identified threat category, requiring human expert review.
4. **Human Review Scope**: The automated checker evaluates structural compliance and threat-control alignment; final judgment of nuanced justifications remains with human assessors.

## Scope and Limitations
- Lightweight Python 3 standard library implementation.
- Keyword and heuristic structural taxonomy; no cloud API, credentials, or heavy neural models needed.

## Testing & Verification
Run the automated test suite:
```bash
python3 -m unittest discover -s 1-Introduction/1-intro-to-ML/applied-labs/r37-t060 -p "test_*.py" -v
```
Expected output:
```text
Ran 6 tests in 0.000s
OK
```
