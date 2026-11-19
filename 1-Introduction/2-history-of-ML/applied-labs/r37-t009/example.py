"""Security-scenario structural rubric checker and evaluation experiment.

Label: fictional scenarios, structural rubric only, not a security assessment.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs
separately supplied credentials/hardware and is not part of this task.

Contract:
- Three fictional scenarios tied to "History of machine learning":
  1. Complete scenario passes.
  2. Scenario without an asset fails.
  3. Control unrelated to named threat is flagged for review.
- Encodes: asset, threat, control, residual_risk.
- Human review judges explanation; checker verifies structural rubric.
- Focus: Compare three controlled configurations / input sizes using a metric
  appropriate to this contract, reporting correctness and trade-offs.
"""

REQUIRED_FIELDS = ("asset", "threat", "control", "residual_risk")

# Threat to approved related controls mapping for historical ML contexts
THREAT_CONTROL_MAP = {
    "unauthorized modification of historical Dartmouth conference proceedings": {
        "cryptographic checksums and immutable version control for proceedings",
        "dual-custody signing for archival publications"
    },
    "adversarial poisoning of early perceptron training samples": {
        "input sanity filtering and historical training data provenance audits",
        "statistical outlier clipping for training inputs"
    },
    "exfiltration of expert system decision heuristics": {
        "role-based access control and encrypted storage for rule engines",
        "access logging and token-based authentication for inference APIs"
    }
}

SCENARIOS = {
    "scenario_1_pass": {
        "name": "Dartmouth 1956 Proceedings Archival",
        "asset": "Dartmouth 1956 workshop proposal and conference transcripts",
        "threat": "unauthorized modification of historical Dartmouth conference proceedings",
        "control": "cryptographic checksums and immutable version control for proceedings",
        "residual_risk": "compromise of cryptographic signing keys requiring manual recovery"
    },
    "scenario_2_fail": {
        "name": "Early Perceptron Training Data",
        "asset": "",  # Empty asset: fails rubric
        "threat": "adversarial poisoning of early perceptron training samples",
        "control": "input sanity filtering and historical training data provenance audits",
        "residual_risk": "subtle poisoning within nominal sensor thresholds"
    },
    "scenario_3_review": {
        "name": "Expert System Rule Base Protection",
        "asset": "proprietary medical diagnosis expert system decision heuristics",
        "threat": "exfiltration of expert system decision heuristics",
        "control": "periodic workstation display monitor recalibration",  # Unrelated control: flagged for review
        "residual_risk": "unauthorized exfiltration remains unmitigated by monitor calibration"
    }
}


def control_addresses_threat(control, threat):
    """Check whether control is semantically recognized as addressing threat."""
    allowed = THREAT_CONTROL_MAP.get(threat, set())
    return control in allowed


def check_scenario(scenario):
    """Evaluate scenario against structural rubric.

    Returns dict with keys 'status' ('pass' | 'fail' | 'review') and 'reason'.
    """
    if not isinstance(scenario, dict):
        raise TypeError(f"scenario must be a dict, got {type(scenario).__name__}")

    # Step 1: Check presence and non-emptiness of required fields
    for field in REQUIRED_FIELDS:
        val = scenario.get(field)
        if val is None or not isinstance(val, str) or len(val.strip()) == 0:
            return {
                "status": "fail",
                "reason": f"missing or empty required field: {field!r}"
            }

    threat = scenario["threat"]
    control = scenario["control"]

    # Step 2: Check threat-control relatedness
    if not control_addresses_threat(control, threat):
        return {
            "status": "review",
            "reason": f"control {control!r} is unrelated to named threat {threat!r}; human review required"
        }

    return {
        "status": "pass",
        "reason": "scenario meets all structural rubric requirements"
    }


def run_experiment():
    """Evaluation experiment comparing three small controlled configurations."""
    configs = {
        "config_1_single": [SCENARIOS["scenario_1_pass"]],
        "config_2_standard_three": [
            SCENARIOS["scenario_1_pass"],
            SCENARIOS["scenario_2_fail"],
            SCENARIOS["scenario_3_review"]
        ],
        "config_3_extended_five": [
            SCENARIOS["scenario_1_pass"],
            SCENARIOS["scenario_2_fail"],
            SCENARIOS["scenario_3_review"],
            {
                "asset": "Perceptron hardware wiring schematics",
                "threat": "adversarial poisoning of early perceptron training samples",
                "control": "statistical outlier clipping for training inputs",
                "residual_risk": "extreme non-Gaussian distribution noise"
            },
            {
                "asset": "1960s ELIZA rule scripts",
                "threat": "exfiltration of expert system decision heuristics",
                "control": "",  # missing control
                "residual_risk": "unrestricted rule leakage"
            }
        ]
    }

    metrics = {}
    for name, suite in configs.items():
        results = [check_scenario(s) for s in suite]
        counts = {
            "pass": sum(1 for r in results if r["status"] == "pass"),
            "fail": sum(1 for r in results if r["status"] == "fail"),
            "review": sum(1 for r in results if r["status"] == "review")
        }
        total = len(suite)
        automated_decision_rate = (counts["pass"] + counts["fail"]) / total
        review_flag_rate = counts["review"] / total
        metrics[name] = {
            "total": total,
            "counts": counts,
            "automated_rate": automated_decision_rate,
            "review_rate": review_flag_rate
        }
    return metrics


def run_contract():
    """Run contract checks and evaluation experiment."""
    lines = []
    lines.append("fictional scenarios, structural rubric only, not a security assessment")

    r1 = check_scenario(SCENARIOS["scenario_1_pass"])
    lines.append(f"scenario 1: status={r1['status']}, reason={r1['reason']}")

    r2 = check_scenario(SCENARIOS["scenario_2_fail"])
    lines.append(f"scenario 2: status={r2['status']}, reason={r2['reason']}")

    r3 = check_scenario(SCENARIOS["scenario_3_review"])
    lines.append(f"scenario 3: status={r3['status']}, reason={r3['reason']}")

    lines.append("evaluation experiment across configurations:")
    metrics = run_experiment()
    for name, m in metrics.items():
        lines.append(f"  {name}: n={m['total']}, counts={m['counts']}, automated_rate={m['automated_rate']:.2f}, review_rate={m['review_rate']:.2f}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(run_contract())
