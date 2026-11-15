"""Structural rubric checker for risk scenarios (standard library only).

Each fictional scenario has: lesson_section, asset, threat, control,
residual_risk. The checker verifies STRUCTURE ONLY. A human must judge whether
the explanations are any good; passing here does not mean a scenario is
correct, realistic or well argued.

Scenario shape:
    {"lesson_section": str, "asset": str,
     "threat": {"id": str, "description": str},
     "control": {"description": str, "mitigates": str},   # a threat id
     "residual_risk": {"level": "low"|"medium"|"high", "note": str}}

Result: {"status": "pass"|"fail"|"review", "problems": [...], "flags": [...]}
    fail   - a required field is missing/blank/invalid (problems lists them)
    review - structure is complete, but control.mitigates does not match
             threat.id, so a human should look (flags lists it)
    pass   - complete and internally consistent
If there are problems the status is "fail" even when a flag also exists.

Two implementations with the SAME contract:
    check_scenario_baseline - one function doing everything (the baseline)
    check_scenario          - the refactor: the responsibility "find structural
                              problems" is extracted into find_structural_problems
The tests prove both give identical results on the fixture and on mutations.

Simulation: fictional scenarios, no real system, no trained model.
"""

LEVELS = ("low", "medium", "high")


def _blank(v):
    return not isinstance(v, str) or v.strip() == ""


# ---------------------------------------------------------------- baseline
def check_scenario_baseline(s):
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


# ------------------------------------------------- refactor: extracted part
def find_structural_problems(s):
    """The extracted responsibility: list the missing/invalid fields."""
    problems = []
    if _blank(s.get("lesson_section")):
        problems.append("missing lesson_section")
    if _blank(s.get("asset")):
        problems.append("missing asset")

    threat = s.get("threat")
    if not isinstance(threat, dict):
        problems.append("missing threat")
    else:
        if _blank(threat.get("id")):
            problems.append("missing threat.id")
        if _blank(threat.get("description")):
            problems.append("missing threat.description")

    control = s.get("control")
    if not isinstance(control, dict):
        problems.append("missing control")
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
    return problems


def check_scenario(s):
    if not isinstance(s, dict):
        raise ValueError("scenario must be a dict")
    problems = find_structural_problems(s)
    flags = []
    threat, control = s.get("threat"), s.get("control")
    if isinstance(threat, dict) and isinstance(control, dict):
        if not _blank(threat.get("id")) and not _blank(control.get("mitigates")):
            if control["mitigates"] != threat["id"]:
                flags.append(
                    f"control mitigates {control['mitigates']!r}, not threat {threat['id']!r}: needs human review"
                )
    status = "fail" if problems else ("review" if flags else "pass")
    return {"status": status, "problems": problems, "flags": flags}


# ------------------------------------------------------------------ fixture
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

if __name__ == "__main__":
    for name, scenario in SCENARIOS.items():
        r = check_scenario(scenario)
        print(f"{name}: status={r['status']} problems={r['problems']} flags={r['flags']}")
