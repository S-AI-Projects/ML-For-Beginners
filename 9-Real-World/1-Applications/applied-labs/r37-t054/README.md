# Applied Lab R37-T054: Security-Scenario Rubric — Invariant and State Trace

## Overview

This lab extends [Postscript: Machine learning in the real world](../../README.md) by introducing a security scenario rubric checker with step-by-step state tracing.

Deploying machine learning models in production exposes assets to adversarial attacks, training data poisoning, model inversion, and unauthorized access. This lab provides a structured, automated rubric checker evaluating four key fields:
1. `asset`: The protected resource or data artifact.
2. `threat`: The specific threat classification.
3. `control`: The preventative or detective security mechanism.
4. `residual_risk`: The remaining risk level after control implementation.

## Rubric Checks & State Traces

1. **Step 1 (Ingest)**: Verifies valid dictionary schema.
2. **Step 2 (Presence Check)**: Verifies no required field is missing or whitespace-only; missing `asset` triggers immediate failure.
3. **Step 3 (Relevance Heuristic)**: Verifies the proposed `control` addresses the named `threat`. Unrelated controls are flagged for human review.
4. **Step 4 (Final Verdict)**: Asserts the state invariant linking intermediate states to the final verdict.

## Fixture Outcomes

- **Complete Scenario**: Status `passed` (e.g. data poisoning mitigated by data provenance tracking and sanitization).
- **Missing Asset**: Status `failed` (asset field is empty or missing).
- **Unrelated Control**: Status `flagged_for_review` (e.g. physical padlock applied against data poisoning).

## Running Tests

```bash
python3 -m unittest discover -s 9-Real-World/1-Applications/applied-labs/r37-t054 -p "test_*.py" -v
```
