"""Structural rubric checker for fictional ML risk scenarios.

This is a local mock exercise. It does not run an ML model or assess whether
an explanation is factually or ethically adequate.
"""

import argparse
import json
from pathlib import Path

REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")

# Deliberately small vocabulary for this teaching fixture. Compatibility is a
# review cue, not a semantic or security judgment.
THREAT_CONTROL_TERMS = {
    "disclosure": ("restrict access", "encrypt"),
    "poisoned": ("provenance", "quarantine"),
    "inject instructions": ("sanitize", "isolate", "review input"),
}


def evaluate(scenario):
    """Return PASS, FAIL, or REVIEW using only the stated structural rubric."""
    missing = [field for field in REQUIRED_FIELDS if not str(scenario.get(field, "")).strip()]
    if missing:
        return {"name": scenario.get("name", "unnamed"), "status": "FAIL", "reason": "missing " + ", ".join(missing)}

    threat = scenario["threat"].lower()
    control = scenario["control"].lower()
    for threat_term, relevant_controls in THREAT_CONTROL_TERMS.items():
        if threat_term in threat and not any(term in control for term in relevant_controls):
            return {"name": scenario.get("name", "unnamed"), "status": "REVIEW", "reason": "control not matched to named threat by the fixture rubric"}

    return {"name": scenario.get("name", "unnamed"), "status": "PASS", "reason": "required fields present and no fixture mismatch detected"}


def load_fixtures(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, choices=(1, 2, 3), default=3,
                        help="check the first N controlled fixture rows (default: 3)")
    parser.add_argument("--fixtures", default=str(Path(__file__).with_name("fixtures.json")))
    args = parser.parse_args()
    outcomes = [evaluate(row) for row in load_fixtures(args.fixtures)[:args.size]]
    print(json.dumps({"checked": len(outcomes), "outcomes": outcomes}, indent=2))


if __name__ == "__main__":
    main()
