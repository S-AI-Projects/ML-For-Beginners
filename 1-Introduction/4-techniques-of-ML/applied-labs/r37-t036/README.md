# R37-T036: Structural rubric checker for risk scenarios

Standard-library Python only. No model, download, GPU or paid service.

**The checker verifies structure only.** It checks that fields are present and
that the control points at the named threat. A human must judge whether the
explanations are sound. Passing does not mean a scenario is correct.

## Run
```
python3 1-Introduction/4-techniques-of-ML/applied-labs/r37-t036/example.py
python3 -m unittest discover -s 1-Introduction/4-techniques-of-ML/applied-labs/r37-t036 -p "test_*.py"
```

## Fixture and expected output
Three fictional scenarios (asset, threat, control, residual risk):

```
complete: status=pass problems=[] flags=[]
no_asset: status=fail problems=['missing asset'] flags=[]
unrelated_control: status=review problems=[] flags=["control mitigates 'T9', not threat 'T3': needs human review"]
```

| Status | Meaning |
|---|---|
| pass | all fields present, control mitigates the named threat |
| fail | a field is missing, blank or invalid (e.g. no asset) |
| review | structure complete, but the control targets a different threat |

## Baseline, then one extracted responsibility
`check_scenario_baseline` does everything in one function. `check_scenario`
has the same contract, with the responsibility "find structural problems"
extracted into `find_structural_problems`. The tests prove both return
identical results on the fixture and on every single-field deletion or
blanking of it.

## Limits (simulation)
Fictional scenarios, no real system. The rubric cannot tell whether a control
really works or whether a risk level is sensible; it only matches threat ids.
