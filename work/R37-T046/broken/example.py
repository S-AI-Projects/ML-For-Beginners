"""Structural rubric checker for fictional security scenarios.

Teaching example for 1-Introduction/2-history-of-ML, section
"1980s Expert systems".

fictional scenarios, structural rubric only, not a security assessment

Python 3 standard library and a local checkout. The local fixture is
mandatory; any optional real-service extension needs separately supplied
credentials/hardware and is not part of this task.
"""

SECTION = "1980s Expert systems"
REQUIRED_FIELDS = ("section", "asset", "threat", "control", "residual_risk")

# Fixed local table: threat -> controls related to that threat.
RELATED_CONTROLS = {
    "unauthorized rule edit": (
        "access control on rule base",
        "change review log",
    ),
    "conflicting rules": (
        "rule conflict check",
        "rule priority ordering",
    ),
    "stale rule set": (
        "scheduled rule review",
        "rule version history",
    ),
}

# Three fictional scenarios; scenario 2 has no asset on purpose.
SCENARIOS = [
    {
        "section": SECTION,
        "asset": "loan-triage rule base (fictional)",
        "threat": "unauthorized rule edit",
        "control": "access control on rule base",
        "residual_risk": "insider with valid credentials",
    },
    {
        "section": SECTION,
        "threat": "unauthorized rule edit",
        "control": "change review log",
        "residual_risk": "review log is read only after an incident",
    },
    {
        "section": SECTION,
        "asset": "triage inference engine (fictional)",
        "threat": "conflicting rules",
        "control": "scheduled rule review",
        "residual_risk": "conflicts found only at review time",
    },
]


def control_addresses_threat(control, threat):
    """Return True when the control is listed as related to the threat."""
    return control in RELATED_CONTROLS.get(threat, ())


def check_scenario_baseline(scenario):
    """Return the structural status and reasons for one scenario."""
    missing = []
    for name in REQUIRED_FIELDS:
        value = scenario.get(name)
        if not isinstance(value, str) or not value.strip():
            missing.append(name)
    if missing:
        reasons = ["missing or empty field: " + name for name in missing]
        return {"status": "fail", "reasons": reasons}
    related = scenario["control"] in RELATED_CONTROLS.get(
        scenario["threat"], ()
    )
    if not related:
        reason = "control not related to threat: " + scenario["control"]
        return {"status": "review", "reasons": [reason]}
    reasons = ["all fields present", "control related to threat"]
    return {"status": "pass", "reasons": reasons}


def check_scenario(scenario):
    """Same contract as check_scenario_baseline, relatedness extracted."""
    missing = []
    for name in REQUIRED_FIELDS:
        value = scenario.get(name)
        if not isinstance(value, str) or not value.strip():
            missing.append(name)
    if missing:
        reasons = ["missing or empty field: " + name for name in missing]
        return {"status": "fail", "reasons": reasons}
    if not control_addresses_threat(scenario["control"], scenario["threat"]):
        reason = "control not related to threat: " + scenario["control"]
        return {"status": "review", "reasons": [reason]}
    reasons = ["all fields present", "control related to threat"]
    return {"status": "pass", "reasons": reasons}


def main():
    same = True
    for index, scenario in enumerate(SCENARIOS, start=1):
        result = check_scenario(scenario)
        print(f"scenario {index}: {result['status']}")
        print("  reasons: " + "; ".join(result["reasons"]))
        if check_scenario_baseline(scenario) != result:
            same = False
    print(f"baseline == refactored: {same}")


if __name__ == "__main__":
    main()
