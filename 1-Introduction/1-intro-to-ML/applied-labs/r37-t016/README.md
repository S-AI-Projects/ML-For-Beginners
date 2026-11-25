# R37-T016: local scenario rubric checker

This small applied example connects the lesson's **Why data quality matters** and **Examples of applied ML** sections to fictional scenarios. Learners state an asset, threat, control, control rationale, and residual risk. The checker verifies that the four rubric fields (asset, threat, control, and residual risk) are present and that the control name is paired with the stated threat in this deliberately small fixture rubric. It does not score the control rationale.

This illustrates that data quality and the risks around an ML application deserve explicit thought. The fixture's fixed threat/control mapping is only a structural teaching aid: it does not judge the explanation, prove a control is effective, or represent real healthcare, weather systems, hardware, cloud services, or trained models. Human review judges the control rationale; the checker deliberately leaves that explanation to people.

## Run the local fixture

Prerequisite: Python 3 standard library and a local repository checkout. From the repository root:

```bash
python3 1-Introduction/1-intro-to-ML/applied-labs/r37-t016/example.py
```

The input is `fixtures.json`. It contains three fictional cases; expected and actual statuses are, in order, `pass`, `fail` (asset missing), and `review` (control not linked to the named threat). Output:

```json
[
  {"id": "clinic-records", "status": "pass", "detail": "complete; stated control matches threat"},
  {"id": "weather-feed-missing-asset", "status": "fail", "detail": "missing or empty asset"},
  {"id": "sentiment-control-review", "status": "review", "detail": "control is not linked to the named threat in this local rubric"}
]
```

Run the unit tests from the repository root:

```bash
python3 -m unittest discover -s 1-Introduction/1-intro-to-ML/applied-labs/r37-t016 -p "test_*.py"
```

The baseline evaluator is frozen in the tests. `check_fields` is the extracted responsibility; the equivalence test verifies the same results for all fixture cases. Tests also cover blank/empty boundary values and include a deliberate wrong-result assertion check so assertion failure behavior is exercised.
