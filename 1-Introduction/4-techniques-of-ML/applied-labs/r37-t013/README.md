# R37-T013: scenario rubric checker

This local Python 3 standard-library exercise connects three fictional cases to
the lesson's **Data**, **Evaluate the model**, and **Prediction** sections. Each
complete answer states an `asset`, a tagged `threat`, a tagged `control`, and a
`residual_risk`. The checker fails missing or blank fields and marks unknown or
unmatched threat/control tags for human review. The tag table is an explicit
structural rubric, not a natural-language security analysis.

## Run it

From the repository root, run:

```sh
python3 1-Introduction/4-techniques-of-ML/applied-labs/r37-t013/example.py
python3 -m unittest discover -s 1-Introduction/4-techniques-of-ML/applied-labs/r37-t013 -p "test_*.py"
```

Prerequisites: Python 3 standard library and a local checkout. No model, network
service, credentials, GPU, or physical device is used.

## Fixtures and expected output

The inputs are local mock narratives in `example.py`:

1. **prepared-data** (Data): a garden survey table; its data-quality threat and
   validation control are an allowed pair, so the result is `PASS`.
2. **model-evaluation** (Evaluate the model): a held-out labeled set; the
   fixture intentionally omits its asset, so the result is `FAIL`.
3. **new-prediction** (Prediction): a plant-care suggestion; its
   `prediction-misuse` threat is paired with a data validation control, so the
   result is `REVIEW`.

Expected output from `example.py`:

```json
[
  {"id": "prepared-data", "result": "PASS", "issues": []},
  {"id": "model-evaluation", "result": "FAIL", "issues": ["missing or empty: asset"]},
  {"id": "new-prediction", "result": "REVIEW", "issues": ["control tag validation is not listed for threat prediction-misuse; review needed"]}
]
```

The tests compare the direct implementation with this independently written
expected-result table on the same fixture inputs. The checker only checks
presence and a declared tag pairing. Human review must judge each explanation,
the appropriateness and effectiveness of a control, and whether residual risk is
acceptable. The stories and controls are simulations/mock examples; they do
not establish real hardware or cloud behavior, or trained-model performance.
