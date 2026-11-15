# R37-T040: Structural rubric checker with three applied questions

Standard-library Python only. No model, download, GPU or paid service.

**The checker verifies structure only.** It checks that fields are present and
that the control points at the named threat. A human must judge whether the
explanations are sound. Passing does not mean a scenario is correct.

## Run
```
python3 1-Introduction/4-techniques-of-ML/applied-labs/r37-t040/example.py
python3 -m unittest discover -s 1-Introduction/4-techniques-of-ML/applied-labs/r37-t040 -p "test_*.py"
```

## Fixture and expected output
```text
complete: status=pass problems=[] flags=[]
no_asset: status=fail problems=['missing asset'] flags=[]
unrelated_control: status=review problems=[] flags=["control mitigates 'T9', not threat 'T3': needs human review"]
Q1 (predict an output): check=OK
Q2 (diagnose a failure): check=OK
Q3 (choose a boundary policy): check=OK
```

| Status | Meaning |
|---|---|
| pass | all fields present, control mitigates the named threat |
| fail | a field is missing, blank or invalid |
| review | structure complete, but the control targets a different threat |

## Three applied questions (each has an executable check)

**Q1 (predict an output).** What status does the `unrelated_control`
scenario get? **Answer: `review`.** Rationale: no field is missing, but the
control mitigates `T9` while the threat is `T3`, so one flag is raised.

**Q2 (diagnose a failure).** An author wrote `asset = ['Customer survey data']`
and gets "missing asset". Why? **Answer:** the checker needs a non-blank
string, and a list is not a string, so it counts as missing; use a string.
Rationale: `_blank()` treats non-strings and empty strings as missing.

**Q3 (choose a boundary policy).** A scenario has a missing asset AND a control
aimed at the wrong threat: `fail` or `review`? **Answer: `fail`**, with the flag
still listed. Rationale: an incomplete scenario cannot be reviewed
meaningfully, and keeping the flag means the second issue is not lost. This is
a design choice; the check confirms the code implements it.

Each `check` in `QUESTIONS` runs the real code and the tests require it to
pass, so a wrong answer or a code change that breaks it makes the tests fail.

## Limits (simulation)
Fictional scenarios, no real system. The rubric cannot tell whether a control
really works or whether a risk level is sensible; it only matches threat ids.
