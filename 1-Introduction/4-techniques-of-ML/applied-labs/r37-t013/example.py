"""A structural rubric checker for fictional ML lifecycle scenarios.

This is a local mock exercise. It does not train a model or test a real system.
"""

from __future__ import annotations

import json
import re
from typing import Any


# Controls are explicitly tagged so the checker can perform a bounded,
# reproducible consistency check without claiming to understand prose.
ALLOWED_CONTROLS = {
    "data-quality": {"validation", "source-audit"},
    "evaluation-leakage": {"held-out-split", "deduplication"},
    "prediction-misuse": {"human-review", "input-limits"},
}
REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")
TAG = re.compile(r"^\[([a-z-]+)\]\s*(.*)$")


def _tagged_text(value: Any) -> tuple[str | None, str]:
    if not isinstance(value, str):
        return None, ""
    match = TAG.match(value.strip())
    if not match:
        return None, value.strip()
    return match.group(1), match.group(2).strip()


def check_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    """Return pass/fail/review based only on the stated structural rubric.

    Missing required content fails. A complete but unknown or mismatched
    threat/control tag is marked for human review. Explanation quality is
    deliberately outside this checker's scope.
    """
    missing = [
        field for field in REQUIRED_FIELDS
        if not isinstance(scenario.get(field), str) or not scenario[field].strip()
    ]
    if missing:
        return {"id": scenario.get("id", "(unnamed)"), "result": "FAIL", "issues": [f"missing or empty: {', '.join(missing)}"]}

    threat_tag, _ = _tagged_text(scenario["threat"])
    control_tag, _ = _tagged_text(scenario["control"])
    if threat_tag not in ALLOWED_CONTROLS:
        issue = f"unrecognized threat tag: {threat_tag or '(none)'}"
    elif control_tag not in ALLOWED_CONTROLS[threat_tag]:
        issue = f"control tag {control_tag or '(none)'} is not listed for threat {threat_tag}; review needed"
    else:
        issue = None

    if issue:
        return {"id": scenario.get("id", "(unnamed)"), "result": "REVIEW", "issues": [issue]}
    return {"id": scenario.get("id", "(unnamed)"), "result": "PASS", "issues": []}


FIXTURES = [
    {
        "id": "prepared-data",
        "lesson_section": "Data",
        "asset": "A fictional garden survey table used to prepare training examples.",
        "threat": "[data-quality] A column mix-up could label flower colors incorrectly.",
        "control": "[validation] Check column names and allowed values before splitting the table.",
        "residual_risk": "A consistent but mistaken source entry could still pass these checks.",
    },
    {
        "id": "model-evaluation",
        "lesson_section": "Evaluate the model",
        "asset": "A fictional set of labeled examples reserved for model evaluation.",
        "threat": "[evaluation-leakage] Duplicate examples in both splits could make evaluation misleading.",
        "control": "[deduplication] Remove exact duplicates before making the held-out split.",
        "residual_risk": "Near-duplicates or shared source bias may remain.",
        # Deliberately omitted asset to exercise the missing-field path.
    },
    {
        "id": "new-prediction",
        "lesson_section": "Prediction",
        "asset": "A fictional plant-care suggestion shown to a gardener.",
        "threat": "[prediction-misuse] A user might treat an uncertain suggestion as guaranteed advice.",
        "control": "[validation] Validate the input columns before prediction.",
        "residual_risk": "A user may still over-trust a plausible but incorrect suggestion.",
    },
]
# The missing-asset case is represented as a genuinely absent key in its fixture.
FIXTURES[1].pop("asset")


def main() -> None:
    print(json.dumps([check_scenario(item) for item in FIXTURES], indent=2))


if __name__ == "__main__":
    main()
