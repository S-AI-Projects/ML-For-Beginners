"""Typed tool dispatch refactoring example.

Label: local contract fixture, not a full MCP transport implementation.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs
separately supplied credentials/hardware and is not part of this task.

Contract:
- Explicit allowlist: add(a, b) and multiply(a, b).
- Numeric argument validation: a and b must be int/float (reject bool and str).
- add(2, 3) -> 5; multiply(2, 3) -> 6.
- Unknown tool and non-numeric argument are structured errors: {"ok": False, "error": {...}}.
- Failed tool execution stops the batch: a failed call cannot execute another tool.
- Refactor focus: extract validate_numeric_arguments into a dedicated function,
  maintaining identical contract and behavior to the baseline.
"""


def tool_add(a, b):
    return a + b


def tool_multiply(a, b):
    return a * b


ALLOWLIST = {
    "add": tool_add,
    "multiply": tool_multiply
}


def make_error(code, message):
    return {
        "ok": False,
        "error": {
            "code": code,
            "message": message
        }
    }


def make_success(result):
    return {
        "ok": True,
        "result": result
    }


# ==============================================================================
# Baseline implementation (monolithic tool lookup + validation + execution)
# ==============================================================================
def dispatch_call_baseline(call):
    """Baseline dispatcher combining allowlist, type checking, and execution."""
    if not isinstance(call, dict):
        return make_error("INVALID_FORMAT", "call must be a JSON object dictionary")

    tool_name = call.get("tool")
    if not isinstance(tool_name, str) or tool_name not in ALLOWLIST:
        return make_error("UNKNOWN_TOOL", f"tool {tool_name!r} not in allowlist")

    args = call.get("args")
    if not isinstance(args, dict):
        return make_error("INVALID_ARGUMENTS", "args must be a dictionary")

    if "a" not in args or "b" not in args:
        return make_error("MISSING_ARGUMENT", "missing required argument 'a' or 'b'")

    a = args["a"]
    b = args["b"]

    if type(a) is bool or not isinstance(a, (int, float)):
        return make_error("INVALID_TYPE", f"argument 'a' must be numeric, got {type(a).__name__}")
    if type(b) is bool or not isinstance(b, (int, float)):
        return make_error("INVALID_TYPE", f"argument 'b' must be numeric, got {type(b).__name__}")

    func = ALLOWLIST[tool_name]
    return make_success(func(a, b))


def dispatch_batch_baseline(calls):
    """Execute batch of calls using baseline dispatcher; aborts on first failure."""
    results = []
    for call in calls:
        res = dispatch_call_baseline(call)
        results.append(res)
        if not res["ok"]:
            break
    return results


# ==============================================================================
# Refactored implementation (extracted validation responsibility)
# ==============================================================================
def validate_tool_args(args):
    """Extracted responsibility: validate numeric arguments a and b."""
    if not isinstance(args, dict):
        return False, make_error("INVALID_ARGUMENTS", "args must be a dictionary")

    if "a" not in args or "b" not in args:
        return False, make_error("MISSING_ARGUMENT", "missing required argument 'a' or 'b'")

    a = args["a"]
    b = args["b"]

    if type(a) is bool or not isinstance(a, (int, float)):
        return False, make_error("INVALID_TYPE", f"argument 'a' must be numeric, got {type(a).__name__}")
    if type(b) is bool or not isinstance(b, (int, float)):
        return False, make_error("INVALID_TYPE", f"argument 'b' must be numeric, got {type(b).__name__}")

    return True, (a, b)


def dispatch_call_refactored(call):
    """Refactored dispatcher delegating argument validation to extracted function."""
    if not isinstance(call, dict):
        return make_error("INVALID_FORMAT", "call must be a JSON object dictionary")

    tool_name = call.get("tool")
    if not isinstance(tool_name, str) or tool_name not in ALLOWLIST:
        return make_error("UNKNOWN_TOOL", f"tool {tool_name!r} not in allowlist")

    is_valid, validation_res = validate_tool_args(call.get("args"))
    if not is_valid:
        return validation_res

    a, b = validation_res
    func = ALLOWLIST[tool_name]
    return make_success(func(a, b))


def dispatch_batch(calls, dispatcher=dispatch_call_refactored):
    """Execute batch of calls with fail-fast semantics; aborts on first failure."""
    results = []
    for call in calls:
        res = dispatcher(call)
        results.append(res)
        if not res["ok"]:
            break
    return results


def run_contract():
    """Run headline contract cases and verify baseline vs refactored equivalence."""
    lines = []
    lines.append("local contract fixture, not a full MCP transport implementation")

    calls = [
        {"tool": "add", "args": {"a": 2, "b": 3}},
        {"tool": "multiply", "args": {"a": 2, "b": 3}},
        {"tool": "unknown_tool", "args": {"a": 1, "b": 2}},
        {"tool": "multiply", "args": {"a": 10, "b": 20}}  # Should NOT be reached
    ]

    base_results = dispatch_batch_baseline(calls)
    refactored_results = dispatch_batch(calls)
    equiv = (base_results == refactored_results)

    lines.append("headline calls execution:")
    lines.append(f"  add(2, 3) -> {refactored_results[0]}")
    lines.append(f"  multiply(2, 3) -> {refactored_results[1]}")
    lines.append(f"  failed call -> {refactored_results[2]}")
    lines.append(f"  calls executed in batch: {len(refactored_results)} of {len(calls)} (aborted on error)")
    lines.append(f"  baseline == refactored equivalence: {equiv}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(run_contract())
