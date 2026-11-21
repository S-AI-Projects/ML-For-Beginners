"""
r37-t022: Allowlisted Action Policy — Compare Two Approaches
=============================================================
Lesson context: 1-Introduction/3-fairness/README.md
  "Building Machine Learning solutions with responsible AI"

This example demonstrates a minimal allowlisted action policy that evaluates
proposed actions against an explicit allowed-tool set and per-tool argument
schema BEFORE any execution. Rejected actions never reach the stub executor.

Connection to the lesson
------------------------
The fairness lesson stresses that AI systems must be reliable, safe, and
accountable. A concrete way to enforce those principles at the action layer
is to gate every tool call through an explicit policy check:

  1. Is the tool in the allowlist?          → if not, REJECT immediately
  2. Are all required arguments present?    → if not, REJECT immediately
  3. Only if both checks pass              → forward to executor

This mirrors the lesson's "reliability and safety" principle: unexpected or
out-of-scope actions are refused before they can cause harm.

Where the simplification stops
-------------------------------
The lesson discusses system-wide responsible-AI practices (fairness metrics,
RAI dashboard, bias detection). This lab isolates just one enforcement
mechanism — argument-schema validation — using hard-coded fixtures and a
stub executor. No model, cloud call, or external service is involved.

NOTE: All behaviour here is simulation/mock. The "executor" is a stub that
records calls; it is never invoked for rejected actions.

Allowlist schema format
-----------------------
ALLOWLIST = {
    "<tool_name>": {
        "required_args": [<list of required argument keys>]
    },
    ...
}

Validation order
----------------
1. Tool-name check   → PolicyViolation("unknown tool")
2. Required-arg check → PolicyViolation("missing required argument")
3. Pass              → executor is called
"""

# ---------------------------------------------------------------------------
# Policy types
# ---------------------------------------------------------------------------

class PolicyViolation(Exception):
    """Raised when an action is rejected by the policy checker."""


# ---------------------------------------------------------------------------
# Allowlist definition (explicit expected-result table — Approach A)
# ---------------------------------------------------------------------------

ALLOWLIST = {
    "read_file": {
        "required_args": ["path"],
    },
    "write_file": {
        "required_args": ["path", "content"],
    },
    "list_directory": {
        "required_args": ["path"],
    },
}

# Explicit expected-result table for comparison (Approach B)
# Same inputs as the fixtures below — independent calculation.
EXPECTED_RESULTS_TABLE = [
    # (tool_name,       args,                           expected_outcome)
    ("read_file",       {"path": "/data/report.csv"},   "ALLOW"),
    ("delete_file",     {"path": "/data/report.csv"},   "REJECT: unknown tool"),
    ("read_file",       {},                             "REJECT: missing required argument 'path'"),
    ("write_file",      {"path": "/out.txt"},            "REJECT: missing required argument 'content'"),
    ("list_directory",  {"path": "/data/"},             "ALLOW"),
]


# ---------------------------------------------------------------------------
# Stub executor — only reached for allowed actions
# ---------------------------------------------------------------------------

_executor_call_log = []   # records every action that reaches the executor


def stub_executor(tool_name, args):
    """
    Simulated tool executor (mock).
    Records the call and returns a fake success result.
    Never called for rejected actions.
    """
    _executor_call_log.append({"tool": tool_name, "args": args})
    return f"[stub] executed '{tool_name}' with args {args}"


def get_executor_calls():
    """Return a copy of the executor call log."""
    return list(_executor_call_log)


def clear_executor_log():
    _executor_call_log.clear()


# ---------------------------------------------------------------------------
# Policy checker (Approach A — direct implementation)
# ---------------------------------------------------------------------------

def evaluate_action(tool_name, args, allowlist=None):
    """
    Evaluate a proposed action against the allowlist policy.

    Validation order
    ----------------
    1. Check tool_name is in the allowlist → PolicyViolation if not.
    2. Check all required_args are present → PolicyViolation if any missing.
    3. Forward to stub_executor and return its result.

    Parameters
    ----------
    tool_name : str   Name of the tool being requested.
    args      : dict  Arguments supplied by the caller.
    allowlist : dict  Policy schema (defaults to module-level ALLOWLIST).

    Returns
    -------
    str   Result from stub_executor on success.

    Raises
    ------
    PolicyViolation  On any policy breach (rejected actions never execute).
    """
    if allowlist is None:
        allowlist = ALLOWLIST

    # --- Step 1: tool-name check ---
    if tool_name not in allowlist:
        raise PolicyViolation(
            f"unknown tool '{tool_name}' — not in allowlist. "
            f"Allowed tools: {sorted(allowlist.keys())}"
        )

    # --- Step 2: required-argument check ---
    required = allowlist[tool_name].get("required_args", [])
    for arg in required:
        if arg not in args:
            raise PolicyViolation(
                f"missing required argument '{arg}' for tool '{tool_name}'. "
                f"Required: {required}, provided keys: {sorted(args.keys())}"
            )

    # --- Step 3: execute (only allowed actions reach here) ---
    return stub_executor(tool_name, args)


# ---------------------------------------------------------------------------
# Approach B — independent look-up against the expected-results table
# ---------------------------------------------------------------------------

def evaluate_action_via_table(tool_name, args):
    """
    Alternative policy check: compare against the explicit EXPECTED_RESULTS_TABLE.

    Uses the same inputs as evaluate_action() but derives the verdict from a
    pre-computed table rather than running the validation logic again.
    This provides an independent cross-check of Approach A.

    Returns
    -------
    str   "ALLOW" or "REJECT: <reason>" matching the table entry.

    Raises
    ------
    KeyError  If the (tool_name, frozenset(args)) pair is not in the table.
    """
    frozen_args = frozenset(args.items())
    for t, a, outcome in EXPECTED_RESULTS_TABLE:
        if t == tool_name and frozenset(a.items()) == frozen_args:
            return outcome
    raise KeyError(
        f"No table entry for tool='{tool_name}', args={args}. "
        "Add a row to EXPECTED_RESULTS_TABLE."
    )


# ---------------------------------------------------------------------------
# Demo scenarios
# ---------------------------------------------------------------------------

def run_normal_case():
    """
    Normal case: read_file with a valid path.
    Policy: tool known ✓, required arg 'path' present ✓ → ALLOW.
    """
    print("=== Normal case: allowed read_file ===")
    clear_executor_log()
    result = evaluate_action("read_file", {"path": "/data/report.csv"})
    print(f"  Result : {result}")
    print(f"  Executor calls: {get_executor_calls()}")


def run_boundary_unknown_tool():
    """
    Boundary case: tool not in allowlist → REJECT at step 1.
    Executor is never called.
    """
    print("\n=== Boundary case: unknown tool 'delete_file' ===")
    clear_executor_log()
    try:
        evaluate_action("delete_file", {"path": "/data/report.csv"})
    except PolicyViolation as exc:
        print(f"  PolicyViolation (expected): {exc}")
    print(f"  Executor calls (must be empty): {get_executor_calls()}")


def run_boundary_missing_arg():
    """
    Boundary case: tool is known but required argument is absent → REJECT at step 2.
    Executor is never called.
    """
    print("\n=== Boundary case: missing required argument ===")
    clear_executor_log()
    try:
        evaluate_action("read_file", {})   # 'path' is missing
    except PolicyViolation as exc:
        print(f"  PolicyViolation (expected): {exc}")
    print(f"  Executor calls (must be empty): {get_executor_calls()}")


def run_comparison_approaches():
    """
    Compare Approach A (direct logic) with Approach B (table look-up)
    using identical inputs.
    """
    print("\n=== Comparison: Approach A vs Approach B ===")
    test_cases = [
        ("read_file",    {"path": "/data/report.csv"}),
        ("delete_file",  {"path": "/data/report.csv"}),
        ("read_file",    {}),
    ]
    for tool, args in test_cases:
        # Approach A
        try:
            evaluate_action(tool, args)
            verdict_a = "ALLOW"
        except PolicyViolation as exc:
            verdict_a = f"REJECT: {str(exc).split('—')[0].strip()}"

        # Approach B (table)
        try:
            verdict_b = evaluate_action_via_table(tool, args)
        except KeyError:
            verdict_b = "NOT IN TABLE"

        match = "✓" if (
            (verdict_a == "ALLOW" and verdict_b == "ALLOW") or
            (verdict_a.startswith("REJECT") and verdict_b.startswith("REJECT"))
        ) else "✗ MISMATCH"
        print(f"  tool={tool!r:15} args_keys={sorted(args)!s:15} A={verdict_a[:30]!r:32} B={verdict_b[:30]!r:32} {match}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_normal_case()
    run_boundary_unknown_tool()
    run_boundary_missing_arg()
    run_comparison_approaches()

