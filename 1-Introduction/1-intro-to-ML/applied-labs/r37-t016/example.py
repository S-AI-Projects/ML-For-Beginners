"""A local, structural rubric checker for fictional machine-learning scenarios."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


FIXTURE_PATH = Path(__file__).with_name("fixtures.json")
REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")

# These simple pairs make this fixture checker deterministic. They do not
# establish that a control is effective in a real system.
CONTROL_THREATS = {
    "restrict record access": {"unauthorized record access"},
    "validate incoming measurements": {"tampered weather measurements"},
    "review label quality": {"incorrect sentiment labels"},
}


def check_fields(scenario: dict[str, Any]) -> list[str]:
    """Return structural completeness errors for one scenario."""
    errors = []
    for field in REQUIRED_FIELDS:
        value = scenario.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing or empty {field}")
    return errors


def evaluate_scenario(scenario: dict[str, Any]) -> dict[str, str]:
    """Check completeness and the fixture's stated threat/control pairing."""
    errors = check_fields(scenario)
    if errors:
        return {"id": str(scenario.get("id", "unknown")), "status": "fail", "detail": "; ".join(errors)}

    threat = scenario["threat"].strip().lower()
    control = scenario["control"].strip().lower()
    expected_threats = CONTROL_THREATS.get(control)
    if expected_threats is None or threat not in expected_threats:
        return {
            "id": str(scenario.get("id", "unknown")),
            "status": "review",
            "detail": "control is not linked to the named threat in this local rubric",
        }
    return {"id": str(scenario.get("id", "unknown")), "status": "pass", "detail": "complete; stated control matches threat"}


def evaluate(scenarios: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Evaluate a list, with per-scenario logic delegated to check_fields."""
    return [evaluate_scenario(scenario) for scenario in scenarios]


def load_fixture() -> list[dict[str, Any]]:
    with FIXTURE_PATH.open(encoding="utf-8") as fixture_file:
        return json.load(fixture_file)


def main() -> None:
    print(json.dumps(evaluate(load_fixture()), indent=2))


if __name__ == "__main__":
    main()
