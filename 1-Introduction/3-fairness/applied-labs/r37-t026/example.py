"""
r37-t026: Allowlisted Action Policy — Worked Example with Checks
================================================================
Lesson context: 1-Introduction/3-fairness/README.md
  "Building Machine Learning solutions with responsible AI"

This module evaluates proposed actions against an explicit allowed-tool set
and per-tool argument schema before any execution.

Contract requirements:
- Allowed `read` with a valid path passes and calls the stub executor.
- Unknown `delete` tool and a missing required argument are rejected.
- Rejected actions raise PolicyViolation and NEVER reach the stub executor.
- Focus: Publish a worked input-to-output explanation and execute the exact
  example as a regression test.

Input-to-Output Worked Trace:
1. Input: tool="read", args={"path": "/data/sample.txt"}
   - Step 1: Check tool in ALLOWLIST -> "read" in {"read", "write"} -> PASS
   - Step 2: Check schema -> required "path" present -> PASS
   - Step 3: Forward to stub_executor -> "[stub] executed read with args {'path': '/data/sample.txt'}"
2. Input: tool="delete", args={"path": "/data/sample.txt"}
   - Step 1: Check tool in ALLOWLIST -> "delete" not in {"read", "write"} -> REJECT
   - Step 2: PolicyViolation("unknown tool 'delete'") raised. Executor call count: 0.
3. Input: tool="read", args={}
   - Step 1: Check tool in ALLOWLIST -> "read" in {"read", "write"} -> PASS
   - Step 2: Check schema -> required "path" missing -> REJECT
   - Step 3: PolicyViolation("missing required argument 'path'") raised. Executor call count: 0.

NOTE: Simulation/mock behavior using small local fixtures.
No model download, paid provider, GPU, or physical device is required.
"""

from typing import Any, Dict, List, Optional


class PolicyViolation(Exception):
    """Raised when an action violates the allowlist policy or argument schema."""
    pass


ALLOWLIST: Dict[str, Dict[str, Any]] = {
    "read": {
        "required_args": ["path"],
    },
    "write": {
        "required_args": ["path", "content"],
    },
}

_stub_executor_call_log: List[Dict[str, Any]] = []


def stub_executor(tool_name: str, args: Dict[str, Any]) -> str:
    """Mock stub executor that records calls for allowed actions only."""
    _stub_executor_call_log.append({"tool": tool_name, "args": args})
    return f"[stub] executed {tool_name} with args {args}"


def get_executor_call_count() -> int:
    return len(_stub_executor_call_log)


def clear_executor_calls() -> None:
    _stub_executor_call_log.clear()


def evaluate_and_execute(tool_name: str, args: Dict[str, Any], allowlist: Optional[Dict[str, Any]] = None) -> str:
    """
    Evaluates action against allowlist and required arguments before execution.
    Rejected actions never reach stub_executor.
    """
    if allowlist is None:
        allowlist = ALLOWLIST

    # Step 1: Tool allowlist check
    if tool_name not in allowlist:
        raise PolicyViolation(f"unknown tool '{tool_name}' — not in allowlist.")

    # Step 2: Schema validation
    required_args = allowlist[tool_name].get("required_args", [])
    for req in required_args:
        if req not in args:
            raise PolicyViolation(f"missing required argument '{req}' for tool '{tool_name}'.")

    # Step 3: Execution
    return stub_executor(tool_name, args)


def run_worked_example():
    """Runs the worked input-to-output example and prints each evaluation step."""
    clear_executor_calls()
    print("=== Worked Example: Allowlisted Action Policy ===")

    # Scenario 1: Allowed read
    print("\n1. Evaluating allowed read:")
    res1 = evaluate_and_execute("read", {"path": "/data/sample.txt"})
    print(f"   Outcome: SUCCESS -> {res1}")
    print(f"   Executor call count: {get_executor_call_count()}")

    # Scenario 2: Unknown delete tool
    print("\n2. Evaluating unknown delete tool:")
    try:
        evaluate_and_execute("delete", {"path": "/data/sample.txt"})
    except PolicyViolation as e:
        print(f"   Outcome: REJECTED -> {e}")
    print(f"   Executor call count: {get_executor_call_count()} (unchanged)")

    # Scenario 3: Missing required argument
    print("\n3. Evaluating missing required argument:")
    try:
        evaluate_and_execute("read", {})
    except PolicyViolation as e:
        print(f"   Outcome: REJECTED -> {e}")
    print(f"   Executor call count: {get_executor_call_count()} (unchanged)")


if __name__ == "__main__":
    run_worked_example()
