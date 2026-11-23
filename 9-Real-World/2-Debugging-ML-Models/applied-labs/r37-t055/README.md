# Applied Lab R37-T055: Allowlisted Action Policy — Evaluation Experiment

## Overview

This lab extends [Postscript: Model Debugging in Machine Learning using Responsible AI dashboard components](../../README.md) by introducing an allowlisted action policy evaluator and empirical experimentation harness.

Autonomous model debugging systems and agentic assistants often propose administrative or debugging actions. Executing unverified actions can cause catastrophic side effects (e.g. arbitrary file deletion or unsanctioned code execution). This lab provides:
- Pre-execution validation against an explicit allowlist of permitted tools (`read`, `inspect`).
- Schema validation checking argument types and non-empty string constraints.
- An empirical evaluation experiment measuring allowance and rejection rates across diverse action payloads.

## Policy Matrix & Outcomes

| Proposed Action | Args | Validation Verdict | Execution Status | Error Code |
| :--- | :--- | :--- | :--- | :--- |
| `read` | `{"path": "model_config.json"}` | **Allowed** | Executed | `None` |
| `delete` | `{"path": "model.bin"}` | **Rejected** | Halted | `DISALLOWED_ACTION` |
| `read` | `{}` (missing path) | **Rejected** | Halted | `SCHEMA_VIOLATION` |
| `read` | `{"path": " "}` (empty) | **Rejected** | Halted | `SCHEMA_VIOLATION` |
| `inspect` | `{"model_name": "classifier_v1"}` | **Allowed** | Executed | `None` |
| `write` | `{"path": "hack.py", ...}` | **Rejected** | Halted | `DISALLOWED_ACTION` |

## Running Tests

```bash
python3 -m unittest discover -s 9-Real-World/2-Debugging-ML-Models/applied-labs/r37-t055 -p "test_*.py" -v
```
