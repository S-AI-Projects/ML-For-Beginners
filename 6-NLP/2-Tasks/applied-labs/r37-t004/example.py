"""Cosine-similarity lookup with intermediate state trace and invariants.

Label: local vector test double, not an NLP embedding service.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs
separately supplied credentials/hardware and is not part of this task.

Contract:
- [1, 0] vs [1, 0] gives 1.0.
- [1, 0] vs [0, 1] gives 0.0.
- A zero vector returns the documented undefined-result sentinel: None.
- Trace records intermediate states: dot product, norms, norm product, zero check.
- Invariant: when norms are non-zero, similarity * norm_u * norm_v == dot product
  and -1.0 <= similarity <= 1.0 (Cauchy-Schwarz).
"""

import math

UNDEFINED_SENTINEL = None


def validate_vector(v, name="vector"):
    """Ensure vector is non-empty list or tuple of numeric values."""
    if not isinstance(v, (list, tuple)):
        raise TypeError(f"{name} must be a list or tuple, got {type(v).__name__}")
    if len(v) == 0:
        raise ValueError(f"{name} cannot be empty")
    for x in v:
        if type(x) is bool or not isinstance(x, (int, float)):
            raise TypeError(f"elements in {name} must be numeric, got {x!r}")
        if math.isnan(x) or math.isinf(x):
            raise ValueError(f"elements in {name} must be finite real numbers, got {x!r}")


def cosine_similarity_with_trace(u, v):
    """Compute cosine similarity between u and v, returning (similarity, trace)."""
    validate_vector(u, "u")
    validate_vector(v, "v")
    if len(u) != len(v):
        raise ValueError(f"vectors must have equal dimensions, got {len(u)} and {len(v)}")

    trace = {}

    # Step 1: dot product
    dot = sum(ui * vi for ui, vi in zip(u, v))
    trace["step1_dot"] = dot

    # Step 2: norm of u
    norm_u = math.sqrt(sum(ui * ui for ui in u))
    trace["step2_norm_u"] = norm_u

    # Step 3: norm of v
    norm_v = math.sqrt(sum(vi * vi for vi in v))
    trace["step3_norm_v"] = norm_v

    # Step 4: norm product
    norm_prod = norm_u * norm_v
    trace["step4_norm_product"] = norm_prod

    # Step 5: zero vector check
    is_zero = (norm_u == 0.0 or norm_v == 0.0)
    trace["step5_zero_vector"] = is_zero

    # Step 6: similarity calculation
    if is_zero:
        similarity = UNDEFINED_SENTINEL
    else:
        sim_val = dot / norm_prod
        # Clamp minor floating precision noise to [-1.0, 1.0]
        similarity = max(-1.0, min(1.0, sim_val))
    trace["step6_similarity"] = similarity

    return similarity, trace


def check_trace_invariant(trace):
    """Check mathematical invariant connecting intermediate state to final output."""
    if trace["step5_zero_vector"]:
        return trace["step6_similarity"] is UNDEFINED_SENTINEL

    sim = trace["step6_similarity"]
    dot = trace["step1_dot"]
    norm_prod = trace["step4_norm_product"]

    # Invariant 1: sim * norm_prod == dot (within numerical tolerance)
    reconstructed_dot = sim * norm_prod
    diff = abs(reconstructed_dot - dot)
    if diff > 1e-9:
        return False

    # Invariant 2: -1.0 <= sim <= 1.0 (Cauchy-Schwarz inequality)
    if not (-1.0 <= sim <= 1.0):
        return False

    return True


def run_contract():
    """Run headline contract cases and print traces."""
    lines = []
    lines.append("local vector test double, not an NLP embedding service")

    # Contract 1: [1, 0] vs [1, 0]
    sim1, trace1 = cosine_similarity_with_trace([1, 0], [1, 0])
    lines.append(f"[1, 0] vs [1, 0] -> similarity={sim1:.4f}, invariant={check_trace_invariant(trace1)}")

    # Contract 2: [1, 0] vs [0, 1]
    sim2, trace2 = cosine_similarity_with_trace([1, 0], [0, 1])
    lines.append(f"[1, 0] vs [0, 1] -> similarity={sim2:.4f}, invariant={check_trace_invariant(trace2)}")

    # Contract 3: zero vector [0, 0] vs [1, 0]
    sim3, trace3 = cosine_similarity_with_trace([0, 0], [1, 0])
    lines.append(f"[0, 0] vs [1, 0] -> similarity={sim3} (undefined sentinel), invariant={check_trace_invariant(trace3)}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(run_contract())
