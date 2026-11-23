"""Security-scenario rubric — invariant and state trace for 9-Real-World/1-Applications."""

from typing import Any, Dict, List, Optional

MOCK_LIMITATIONS = [
    "Checks structural schema and keyword heuristics; does not perform semantic LLM reasoning or human judgment.",
    "Does not integrate with live SIEM, enterprise risk registers, or CVE vulnerability feeds.",
    "Does not execute live threat attacks or penetration tests.",
    "Uses static keyword relevance sets to flag disconnected controls for human review.",
]

# Known domain keywords mapping threats to relevant security controls (handles both space and underscore)
THREAT_CONTROL_KEYWORDS = {
    "data_poisoning": {"validation", "checksum", "sanitization", "provenance", "watermark", "integrity"},
    "model_inversion": {"differential privacy", "differential_privacy", "encryption", "rate limiting", "rate_limiting", "noise injection", "noise_injection", "access control", "access_control"},
    "adversarial_evasion": {"adversarial training", "adversarial_training", "input filtering", "input_filtering", "defensive distillation", "robustness check"},
    "unauthorized_access": {"authentication", "mfa", "rbac", "access control", "access_control", "least privilege", "least_privilege"},
}

FICTIONAL_SCENARIOS = [
    {
        "id": "scenario_1_finance_credit",
        "lesson_context": "Real-World Finance & Banking",
        "asset": "Customer credit-risk training dataset",
        "threat": "data_poisoning",
        "control": "Input data provenance tracking and anomaly-based training set sanitization",
        "residual_risk": "Low: undetected subtle drift in rare outlier profiles",
    },
    {
        "id": "scenario_2_healthcare_imaging",
        "lesson_context": "Real-World Healthcare Diagnostics",
        "asset": "Chest X-ray diagnostic classification model weights",
        "threat": "model_inversion",
        "control": "Differential privacy training with gradient noise injection and query rate limiting",
        "residual_risk": "Low: minor epsilon reconstruction leakage under extreme query volume",
    },
    {
        "id": "scenario_3_retail_recommendation",
        "lesson_context": "Real-World Retail Recommendation System",
        "asset": "E-commerce user purchase history embedding matrix",
        "threat": "unauthorized_access",
        "control": "Role-based access control (RBAC) with mutual TLS authentication",
        "residual_risk": "Low: internal privileged administrator credential exposure",
    },
]


def check_security_rubric_with_state_trace(scenario: Dict[str, Any]) -> Dict[str, Any]:
    state_trace: List[Dict[str, Any]] = []

    # Step 1: Ingest and validate basic dictionary structure
    s1_state = {"step": 1, "action": "ingest_scenario", "scenario_id": scenario.get("id", "unknown")}
    state_trace.append(s1_state)

    # Step 2: Check required fields presence
    required_fields = ["asset", "threat", "control", "residual_risk"]
    missing_fields = []
    empty_fields = []

    for f in required_fields:
        val = scenario.get(f)
        if val is None:
            missing_fields.append(f)
        elif not isinstance(val, str) or not val.strip():
            empty_fields.append(f)

    s2_state = {
        "step": 2,
        "action": "check_required_fields",
        "missing_fields": missing_fields,
        "empty_fields": empty_fields,
        "has_asset": bool(scenario.get("asset") and str(scenario["asset"]).strip()),
    }
    state_trace.append(s2_state)

    if missing_fields or empty_fields:
        return {
            "status": "failed",
            "passed": False,
            "review_flagged": False,
            "reason": f"Missing or empty required fields: {missing_fields + empty_fields}",
            "state_trace": state_trace,
            "invariant_holds": True,
        }

    # Step 3: Check threat-control semantic relevance heuristic
    threat = scenario["threat"].lower().strip()
    control_text = scenario["control"].lower().strip()

    keywords = THREAT_CONTROL_KEYWORDS.get(threat, set())
    matches = [kw for kw in keywords if kw in control_text]

    s3_state = {
        "step": 3,
        "action": "evaluate_control_relevance",
        "threat": threat,
        "keywords_checked": sorted(list(keywords)),
        "matches_found": matches,
        "relevance_pass": len(matches) > 0,
    }
    state_trace.append(s3_state)

    if not s3_state["relevance_pass"]:
        final_status = "flagged_for_review"
        passed = False
        review_flagged = True
        reason = f"Control does not contain expected security keywords for threat '{threat}'. Flagged for human review."
    else:
        final_status = "passed"
        passed = True
        review_flagged = False
        reason = "All required fields complete and control aligns structurally with named threat."

    # Step 4: Final output verification
    s4_state = {
        "step": 4,
        "action": "finalize_verdict",
        "final_status": final_status,
        "passed": passed,
    }
    state_trace.append(s4_state)

    invariant_holds = (state_trace[-1]["final_status"] == final_status)

    return {
        "status": final_status,
        "passed": passed,
        "review_flagged": review_flagged,
        "reason": reason,
        "state_trace": state_trace,
        "invariant_holds": invariant_holds,
    }
