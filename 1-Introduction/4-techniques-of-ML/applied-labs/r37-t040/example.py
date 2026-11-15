"""Structural rubric checker for risk scenarios, plus three applied questions.

The checker verifies STRUCTURE ONLY. A human must judge whether the
explanations are sound; passing here does not mean a scenario is correct,
realistic or well argued.

Scenario shape:
    {"lesson_section": str, "asset": str,
     "threat": {"id": str, "description": str},
     "control": {"description": str, "mitigates": str},   # a threat id
     "residual_risk": {"level": "low"|"medium"|"high", "note": str}}

Result: {"status": "pass"|"fail"|"review", "problems": [...], "flags": [...]}
    fail   - a required field is missing/blank/invalid
    review - structure complete, but control.mitigates != threat.id
    pass   - complete and internally consistent
Boundary policy: if there are problems the status is "fail" even when a flag
also exists (the flag is still listed).

Simulation: fictional scenarios, no real system, no trained model.
"""

LEVELS = ("low", "medium", "high")


def _blank(v):
    return not isinstance(v, str) or v.strip() == ""


def check_scenario(s):
    if not isinstance(s, dict):
        raise ValueError("scenario must be a dict")
    problems, flags = [], []

    if _blank(s.get("lesson_section")):
        problems.append("missing lesson_section")
    if _blank(s.get("asset")):
        problems.append("missing asset")

    threat = s.get("threat")
    if not isinstance(threat, dict):
        problems.append("missing threat")
        threat = {}
    else:
        if _blank(threat.get("id")):
            problems.append("missing threat.id")
        if _blank(threat.get("description")):
            problems.append("missing threat.description")

    control = s.get("control")
    if not isinstance(control, dict):
        problems.append("missing control")
        control = {}
    else:
        if _blank(control.get("description")):
            problems.append("missing control.description")
        if _blank(control.get("mitigates")):
            problems.append("missing control.mitigates")

    risk = s.get("residual_risk")
    if not isinstance(risk, dict):
        problems.append("missing residual_risk")
    else:
        if risk.get("level") not in LEVELS:
            problems.append("invalid residual_risk.level")
        if _blank(risk.get("note")):
            problems.append("missing residual_risk.note")

    if not _blank(threat.get("id")) and not _blank(control.get("mitigates")):
        if control["mitigates"] != threat["id"]:
            flags.append(
                f"control mitigates {control['mitigates']!r}, not threat {threat['id']!r}: needs human review"
            )

    status = "fail" if problems else ("review" if flags else "pass")
    return {"status": status, "problems": problems, "flags": flags}


# NOTE: edit lesson_section to match real headings in the lesson README.
SCENARIOS = {
    "complete": {
        "lesson_section": "Preparing your data",
        "asset": "Customer survey data used to train a model",
        "threat": {"id": "T1", "description": "Personal details leak from the training file"},
        "control": {"description": "Remove names and emails before training", "mitigates": "T1"},
        "residual_risk": {"level": "low", "note": "Rare combinations of answers could still identify someone"},
    },
    "no_asset": {
        "lesson_section": "Training your model",
        "asset": "",
        "threat": {"id": "T2", "description": "A mislabeled batch skews the model"},
        "control": {"description": "Spot-check a sample of labels", "mitigates": "T2"},
        "residual_risk": {"level": "medium", "note": "Spot checks miss some errors"},
    },
    "unrelated_control": {
        "lesson_section": "Evaluating your model",
        "asset": "Test set used to report accuracy",
        "threat": {"id": "T3", "description": "Test rows leak into the training set"},
        "control": {"description": "Add a darker colour theme to the chart", "mitigates": "T9"},
        "residual_risk": {"level": "high", "note": "Leakage would make the score look better than it is"},
    },
}


# ------------------------------------------------------------ applied questions
def _diagnosis_scenario():
    s = dict(SCENARIOS["complete"])
    s["asset"] = ["Customer survey data"]  # the author wrote a list, not a string
    return s


def _both_problem_and_flag():
    s = dict(SCENARIOS["unrelated_control"])
    s["asset"] = ""
    return s


QUESTIONS = [
    {
        "id": "Q1",
        "kind": "predict an output",
        "prompt": "What status does check_scenario give the 'unrelated_control' scenario?",
        "answer": "review",
        "rationale": (
            "Every field is present, so there are no problems. But control.mitigates is 'T9' "
            "while the threat id is 'T3', so one flag is raised. No problems plus a flag means 'review'."
        ),
        "check": lambda: check_scenario(SCENARIOS["unrelated_control"])["status"] == "review",
    },
    {
        "id": "Q2",
        "kind": "diagnose a failure",
        "prompt": (
            "An author wrote asset = ['Customer survey data'] (a list) and the checker says "
            "'missing asset'. Why, and how is it fixed?"
        ),
        "answer": "The checker requires a non-blank string; a list is not a string, so it counts as missing. Use a string.",
        "rationale": (
            "_blank() treats anything that is not a str, or a str that is empty after strip(), as missing. "
            "Replacing the list with the string 'Customer survey data' makes the scenario pass."
        ),
        "check": lambda: (
            check_scenario(_diagnosis_scenario())["problems"] == ["missing asset"]
            and check_scenario({**_diagnosis_scenario(), "asset": "Customer survey data"})["status"] == "pass"
        ),
    },
    {
        "id": "Q3",
        "kind": "choose a boundary policy",
        "prompt": (
            "A scenario has BOTH a missing asset and a control aimed at the wrong threat. "
            "Should the status be 'fail' or 'review'?"
        ),
        "answer": "fail (problems take precedence over flags); the flag is still listed.",
        "rationale": (
            "An incomplete scenario cannot be reviewed meaningfully, so the missing field must be fixed first. "
            "Keeping the flag in the output means the second issue is not lost. This is a design choice; "
            "the check confirms the code implements it."
        ),
        "check": lambda: (
            check_scenario(_both_problem_and_flag())["status"] == "fail"
            and len(check_scenario(_both_problem_and_flag())["flags"]) == 1
        ),
    },
]

if __name__ == "__main__":
    for name, scenario in SCENARIOS.items():
        r = check_scenario(scenario)
        print(f"{name}: status={r['status']} problems={r['problems']} flags={r['flags']}")
    for q in QUESTIONS:
        print(f"{q['id']} ({q['kind']}): check={'OK' if q['check']() else 'FAILED'}")
