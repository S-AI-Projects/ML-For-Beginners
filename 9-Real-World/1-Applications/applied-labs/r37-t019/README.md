# Local scenario rubric example

This fictional exercise connects to the lesson's sections on **Predicting student behavior**, **Personalizing the customer journey**, and **Hospital readmission management**. Each row states an asset, threat, control, and residual risk. The checker reports `PASS` when all four fields are non-empty, `FAIL` when a field is missing, and `REVIEW` when a tiny fixture vocabulary does not connect the named threat with the control.

The compatibility vocabulary is a teaching mock, not natural-language understanding. Human review judges whether the explanation is sound. This example illustrates recording scenario evidence and stating why a control is relevant; it does not assess model behavior, real risks, or real-world model accuracy. Fictional text fixtures replace any real student, customer, or patient data. Python 3 standard library is the only prerequisite; no model, service, credentials, or hardware is used.

From the repository root, run:

```sh
python3 9-Real-World/1-Applications/applied-labs/r37-t019/example.py
python3 -m unittest discover -s 9-Real-World/1-Applications/applied-labs/r37-t019 -p "test_*.py"
```

The example command emits this result:

```json
{
  "checked": 3,
  "outcomes": [
    {
      "name": "fictional-education-progress",
      "status": "PASS",
      "reason": "required fields present and no fixture mismatch detected"
    },
    {
      "name": "fictional-retail-recommendations",
      "status": "FAIL",
      "reason": "missing asset"
    },
    {
      "name": "fictional-health-readmission",
      "status": "REVIEW",
      "reason": "control not matched to named threat by the fixture rubric"
    }
  ]
}
```

## Controlled input-size comparison

`--size N` checks the first N rows of the fixed fixture, so each run changes only the number of rows. The contract metric is exact status agreement with the fixture's expected decisions (not elapsed time or model accuracy). Results are 1/1 (100%) at size 1, 2/2 (100%) at size 2, and 3/3 (100%) at size 3. Increasing size exposes more rubric outcomes but also exposes more cases that need human interpretation; the `REVIEW` outcome is intentionally not an automated judgment.

For example:

```sh
python3 9-Real-World/1-Applications/applied-labs/r37-t019/example.py --size 1
```

Expected compact result: `checked` is `1`, and the only outcome is `fictional-education-progress: PASS`. The full fixture is [`fixtures.json`](fixtures.json), and the structural checks are in [`test_example.py`](test_example.py).
