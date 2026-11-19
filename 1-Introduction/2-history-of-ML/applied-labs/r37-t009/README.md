# R37-T009: Security-Scenario Rubric - Evaluation Experiment

**Label:** fictional scenarios, structural rubric only, not a security assessment.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## What It Is

A structural rubric checker for cybersecurity and risk management scenarios tied to the historical origins of machine learning (Dartmouth 1956 workshop archives, early perceptron training data, and expert system heuristics).

Each scenario encodes four fields:
1. `asset`: The sensitive system component, data, or artifact.
2. `threat`: The named security hazard or unauthorized action.
3. `control`: The preventative, detective, or mitigative mechanism.
4. `residual_risk`: The remaining exposure after control implementation.

## Rubric Rules

- **Pass:** All four fields are non-empty and the control is recognized as directly addressing the named threat.
- **Fail:** Any field is missing or whitespace-only (e.g. empty asset names "asset" in failure reason).
- **Review:** All fields are populated, but the control is not recognized as addressing the specific threat (e.g., monitor calibration for data exfiltration). Human review is flagged.

## Evaluation Experiment

The evaluation experiment compares three input configurations:
- **Configuration 1 (Single Scenario, n=1):** Pure passing baseline. Automated decision rate: 100%, Review rate: 0%.
- **Configuration 2 (Standard Three, n=3):** 1 Pass, 1 Fail, 1 Review. Automated rate: 66.7%, Review rate: 33.3%.
- **Configuration 3 (Extended Suite, n=5):** 2 Pass, 2 Fail, 1 Review. Automated rate: 80.0%, Review rate: 20.0%.

**Observed Trade-off:** Expanding scenario coverage increases structural screening efficiency, while keeping manual human audit overhead bounded to genuinely anomalous threat-control mismatches.

## Invocation

From the repository root:

```bash
python3 1-Introduction/2-history-of-ML/applied-labs/r37-t009/example.py
```

Run unit tests from the repository root:

```bash
python3 -m unittest discover -s 1-Introduction/2-history-of-ML/applied-labs/r37-t009 -p "test_*.py"
```

## Fixture and Expected Output

Expected CLI output:

```text
fictional scenarios, structural rubric only, not a security assessment
scenario 1: status=pass, reason=scenario meets all structural rubric requirements
scenario 2: status=fail, reason=missing or empty required field: 'asset'
scenario 3: status=review, reason=control 'periodic workstation display monitor recalibration' is unrelated to named threat 'exfiltration of expert system decision heuristics'; human review required
evaluation experiment across configurations:
  config_1_single: n=1, counts={'pass': 1, 'fail': 0, 'review': 0}, automated_rate=1.00, review_rate=0.00
  config_2_standard_three: n=3, counts={'pass': 1, 'fail': 1, 'review': 1}, automated_rate=0.67, review_rate=0.33
  config_3_extended_five: n=5, counts={'pass': 2, 'fail': 2, 'review': 1}, automated_rate=0.80, review_rate=0.20
```

## Limitations

- Fictional historical scenarios and structural rubric only; not a formal ISO 27001 or NIST risk assessment.
- Semantic relatedness is checked against an explicit allowlist mapping; no LLM semantic reasoning is used.
- Makes no claims about real hardware, cloud service behavior, or model accuracy.
