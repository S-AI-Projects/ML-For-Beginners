"""Typed tool dispatch: compare two approaches (R37-T042).

Label: this is a local contract fixture, not a full MCP transport
implementation.

Prerequisite: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs separately
supplied credentials/hardware and is not part of this task.
"""

import json
import sys

ALLOWED_TOOLS = {
    "add": lambda a, b: a + b,
    "multiply": lambda a, b: a * b,
}

FIXTURE = [
    {"tool": "add", "args": {"a": 2, "b": 3}},
    {"tool": "multiply", "args": {"a": 2, "b": 3}},
    {"tool": "add", "args": {"a": "a", "b": 3}},
    {"tool": "multiply", "args": {"a": 2, "b": 3}},
]


def _error(code, message):
    return {"ok": False, "error": {"code": code, "message": message}}


def _is_number(value):
    # bool is a subclass of int, so it must be excluded explicitly
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def dispatch(call):
    """Run one JSON-style tool call through the allowlist."""
    if not isinstance(call, dict):
        return _error("invalid_argument", "call must be an object")
    tool = call.get("tool")
    if not isinstance(tool, str) or tool not in ALLOWED_TOOLS:
        return _error("unknown_tool", f"unknown tool: {tool!r}")
    args = call.get("args")
    if not isinstance(args, dict) or set(args) != {"a", "b"}:
        return _error("invalid_argument", "args must be exactly {a, b}")
    for name in ("a", "b"):
        if not _is_number(args[name]):
            msg = f"argument {name!r} must be a number"
            return _error("invalid_argument", msg)
    return {"ok": True, "result": ALLOWED_TOOLS[tool](args["a"], args["b"])}


def dispatch_all(calls):
    """Run calls in order; stop at the first structured error."""
    results = []
    failed = False
    for call in calls:
        if failed:
            results.append(
                _error("not_executed", "not run: an earlier call failed")
            )
            continue
        result = dispatch(call)
        results.append(result)
        failed = not result["ok"]
    return results


def main():
    print("Local contract fixture, not a full MCP transport implementation.")
    print(json.dumps(FIXTURE, indent=2))
    print(json.dumps(dispatch_all(FIXTURE), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
