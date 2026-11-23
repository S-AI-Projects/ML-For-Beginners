"""
R37-T060: Security-Scenario Rubric Checker
Runnable concept example evaluating fictional machine learning security scenarios
structured as asset, threat, control, and residual_risk fields.
"""

from typing import Dict, Any, List, Optional


THREAT_CONTROL_MAPPINGS = {
    "poisoning": [
        "data", "dataset", "hash", "rbac", "sanitization", "validation",
        "ingestion", "pipeline", "integrity", "provenance"
    ],
    "inversion": [
        "privacy", "differential", "rate", "throttling", "noise",
        "query", "api", "perturbation", "extraction"
    ],
    "extraction": [
        "privacy", "differential", "rate", "throttling", "noise",
        "query", "api", "watermarking"
    ],
    "evasion": [
        "adversarial", "input", "validation", "filtering", "preprocessing",
        "robustness", "rate"
    ],
    "leakage": [
        "masking", "anonymization", "encryption", "differential", "retention"
    ],
}


FICTIONAL_SCENARIOS = {
    "complete_valid_scenario": {
        "asset": "Customer transaction training dataset for credit fraud detection",
        "threat": "Data poisoning via unauthorized injection of mislabeled records",
        "control": "Cryptographic hash verification and strict RBAC on training data ingestion pipelines",
        "residual_risk": "Low; insider threat with authorized write access remains auditable via immutable logs",
    },
    "missing_asset_scenario": {
        "asset": "",  # Missing asset
        "threat": "Adversarial evasion attacks against deployed inference endpoint",
        "control": "Input validation and adversarial perturbation filtering at the API gateway",
        "residual_risk": "Moderate; novel perturbation strategies may degrade precision",
    },
    "unrelated_control_scenario": {
        "asset": "Proprietary model weights and neural architecture parameters",
        "threat": "Model inversion and data extraction attacks via public query API",
        "control": "Implement scheduled database backup encryption at rest",  # Unrelated to API inversion
        "residual_risk": "High; public query endpoint remains exposed to high-frequency inversion queries",
    },
}


class SecurityRubricChecker:
    """
    Automated rubric checker for ML security scenarios.
    Human review evaluates contextual nuance and quality of explanation;
    this checker verifies structural completeness, field presence, and threat-control alignment.
    """

    REQUIRED_FIELDS = ["asset", "threat", "control", "residual_risk"]

    @staticmethod
    def evaluate(scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a scenario against the security rubric.
        Returns a dict with 'status' ('pass', 'fail', 'flagged_for_review') and 'reason'.
        """
        # 1. Structural check for required fields
        for field in SecurityRubricChecker.REQUIRED_FIELDS:
            val = scenario.get(field)
            if val is None or not str(val).strip():
                return {
                    "status": "fail",
                    "reason": f"Missing or empty required field: {field}",
                    "field": field,
                }

        asset = str(scenario["asset"]).strip()
        threat = str(scenario["threat"]).strip().lower()
        control = str(scenario["control"]).strip().lower()
        residual_risk = str(scenario["residual_risk"]).strip()

        # 2. Threat-Control relevance alignment
        threat_tokens = threat.split()
        matched_categories = []
        for cat, keywords in THREAT_CONTROL_MAPPINGS.items():
            if cat in threat:
                matched_categories.append((cat, keywords))

        if matched_categories:
            aligned = False
            for cat, keywords in matched_categories:
                if any(kw in control for kw in keywords):
                    aligned = True
                    break
            if not aligned:
                return {
                    "status": "flagged_for_review",
                    "reason": "Control appears unrelated to named threat category; requires human review",
                    "threat": threat,
                    "control": control,
                }

        # 3. Passed structural rubric
        return {
            "status": "pass",
            "reason": "Scenario meets structural rubric criteria; explanation subject to human review",
            "details": {
                "asset_defined": True,
                "threat_defined": True,
                "control_aligned": True,
                "residual_risk_recorded": True,
            },
        }

    @classmethod
    def evaluate_all(cls, scenarios: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        return {name: cls.evaluate(sc) for name, sc in scenarios.items()}


if __name__ == "__main__":
    results = SecurityRubricChecker.evaluate_all(FICTIONAL_SCENARIOS)
    for name, res in results.items():
        print(f"Scenario: {name} -> Status: {res['status']} ({res['reason']})")
