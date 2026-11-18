# R37-T046: structural rubric checker for fictional scenarios

**Label:** fictional scenarios, structural rubric only, not a security assessment.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## Run it

From the repository root:

```bash
python3 -m unittest discover -s 1-Introduction/2-history-of-ML/applied-labs/r37-t046 -p "test_*.py"
python3 1-Introduction/2-history-of-ML/applied-labs/r37-t046/example.py
```

The first command runs the tests (exit code 0 on success). The second prints the fixture results.

## Fixture

Three fictional scenarios, all tied to the lesson section `1980s Expert systems` (a real heading in the lesson README):

- **Scenario 1:** asset "loan-triage rule base (fictional)", threat "unauthorized rule edit", control "access control on rule base".
- **Scenario 2:** same threat and a related control, but no `asset` field.
- **Scenario 3:** asset "triage inference engine (fictional)", threat "conflicting rules", control "scheduled rule review" (not related to that threat).

Each scenario has the fields `section`, `asset`, `threat`, `control`, `residual_risk`. The full data is in `example.py` (`SCENARIOS`), and `work/R37-T046/inputs.txt` records it.

## Expected output

```text
scenario 1: pass
  reasons: all fields present; control related to threat
scenario 2: fail
  reasons: missing or empty field: asset
scenario 3: review
  reasons: control not related to threat: scheduled rule review
baseline == refactored: True
```

This matches the real output saved in `work/R37-T046/example_output.txt`.

## Rubric

- **fail:** a required field is missing or empty (or whitespace only). Missing fields are checked first, so a scenario with a missing field is "fail" even when its control is also unrelated.
- **review:** all fields are present, but the control is not in the fixed `RELATED_CONTROLS` table for the threat. This flags the scenario for a person to read; it does not fail it.
- **pass:** all fields are present and the control is related to the threat.

Human review judges the explanation; the checker only verifies structure. It never decides whether a residual risk is accurate, whether a control works, or whether the scenario is realistic.

## Baseline and refactor

- `check_scenario_baseline` is the complete, self-contained checker. It checks fields and relatedness inline.
- `check_scenario` has the same contract. It extracts one responsibility, the relatedness test, into `control_addresses_threat(control, threat)`.
- Equivalence is tested in `test_example.py`: both functions return identical results on all three fixture scenarios and on extra cases (empty and whitespace fields, `None` values, an unknown threat, an unrelated control, a missing section). The CLI also prints `baseline == refactored`.
- `control_addresses_threat` is tested on its own: a related pair (True), an unrelated pair (False), and an unknown threat (False).

## How this relates to the lesson

The lesson describes expert systems in the 1980s as hybrids: a rules engine that holds business rules, and an inference engine that uses those rules to deduce new facts. This lab uses a fixed rule table in the same spirit, mapping each threat to the controls related to it. The table is a small, hand-written stand-in for domain knowledge, which is also how the lesson describes these systems.

## Where the simplifications stop

- The threat-to-control table is fixed and hand-written, and it has three threats. Real expert systems hold far larger rule bases and reason over them, which this lab does not model.
- Relatedness is a lookup, not inference. The checker never reasons about why a control matters.
- The "fictional" scenarios are invented for teaching. They are not evidence about any system.

## Limitations

- The checker verifies structure and internal consistency only. It is not a security assessment.
- A "pass" means the fields are filled in and the control is in the table. It does not mean the control is effective or the residual risk is correct.
- A "review" is a prompt for human judgement, not a finding.
- No claim is made about real hardware, cloud services, real security effectiveness, or trained-model performance.
- Stdlib only. No model download, paid provider, GPU or device is used.
