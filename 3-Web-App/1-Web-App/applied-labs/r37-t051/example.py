"""Typed tool dispatch — offline service adapter for 3-Web-App/1-Web-App.

This module provides a deterministic local contract fixture for tool dispatching.
It validates tool names against an explicit allowlist and validates argument types
before executing local arithmetic operations.
"""

import json
from typing import Any, Callable, Dict, List, Optional, Union

ALLOWED_TOOLS: Dict[str, Callable[[float, float], float]] = {
    "add": lambda a, b: a + b,
    "multiply": lambda a, b: a * b,
}

MOCK_LIMITATIONS: List[str] = [
    "No network latency, socket transport, or connection retries.",
    "No distributed serialization framing (e.g. MCP JSON-RPC, REST, gRPC).",
    "No authentication, authorization, or tenant rate-limiting.",
    "Synchronous execution only; does not establish asynchronous task queues.",
    "Local in-memory computation only; does not establish remote worker failure modes.",
]


class ToolServiceAdapter:
    """Callable interface for tool dispatch services."""

    def __call__(self, call_payload: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        return self.dispatch(call_payload)

    def dispatch(self, call_payload: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement dispatch.")


class LocalToolServiceAdapter(ToolServiceAdapter):
    """Deterministic local service adapter with typed dispatch and allowlist checks."""

    def __init__(self, allowed_tools: Optional[Dict[str, Callable[[float, float], float]]] = None):
        self.allowed_tools = allowed_tools if allowed_tools is not None else dict(ALLOWED_TOOLS)
        self.execution_history: List[Dict[str, Any]] = []

    def dispatch(self, call_payload: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Dispatches a single tool call through validation and execution."""
        # 1. Parse payload if JSON string
        if isinstance(call_payload, str):
            try:
                payload = json.loads(call_payload)
            except Exception as e:
                return {
                    "status": "error",
                    "tool": None,
                    "result": None,
                    "error": {
                        "code": "INVALID_JSON",
                        "message": f"Malformed JSON payload: {str(e)}",
                    },
                }
        elif isinstance(call_payload, dict):
            payload = call_payload
        else:
            return {
                "status": "error",
                "tool": None,
                "result": None,
                "error": {
                    "code": "INVALID_PAYLOAD_TYPE",
                    "message": "Payload must be a JSON string or dict",
                },
            }

        tool_name = payload.get("tool")
        args = payload.get("args")

        # 2. Allowlist verification
        if not tool_name or tool_name not in self.allowed_tools:
            return {
                "status": "error",
                "tool": tool_name,
                "result": None,
                "error": {
                    "code": "UNKNOWN_TOOL",
                    "message": f"Tool '{tool_name}' is not in the explicit allowlist: {sorted(list(self.allowed_tools.keys()))}",
                },
            }

        # 3. Arguments schema verification
        if not isinstance(args, dict):
            return {
                "status": "error",
                "tool": tool_name,
                "result": None,
                "error": {
                    "code": "INVALID_ARGUMENTS_FORMAT",
                    "message": "'args' field must be an object/dict",
                },
            }

        if "a" not in args or "b" not in args:
            return {
                "status": "error",
                "tool": tool_name,
                "result": None,
                "error": {
                    "code": "MISSING_ARGUMENT",
                    "message": "Arguments 'a' and 'b' are required",
                },
            }

        a_val = args["a"]
        b_val = args["b"]

        # Note: In Python, bool is a subclass of int (isinstance(True, int) == True).
        # We explicitly disallow booleans as numeric arguments.
        if isinstance(a_val, bool) or not isinstance(a_val, (int, float)):
            return {
                "status": "error",
                "tool": tool_name,
                "result": None,
                "error": {
                    "code": "INVALID_ARGUMENT",
                    "message": f"Argument 'a' must be numeric (int/float), got {type(a_val).__name__}",
                },
            }

        if isinstance(b_val, bool) or not isinstance(b_val, (int, float)):
            return {
                "status": "error",
                "tool": tool_name,
                "result": None,
                "error": {
                    "code": "INVALID_ARGUMENT",
                    "message": f"Argument 'b' must be numeric (int/float), got {type(b_val).__name__}",
                },
            }

        # 4. Safe execution
        func = self.allowed_tools[tool_name]
        try:
            result = func(a_val, b_val)
            record = {
                "status": "success",
                "tool": tool_name,
                "result": result,
                "error": None,
            }
            self.execution_history.append(record)
            return record
        except Exception as ex:
            return {
                "status": "error",
                "tool": tool_name,
                "result": None,
                "error": {
                    "code": "EXECUTION_FAILURE",
                    "message": f"Tool execution failed: {str(ex)}",
                },
            }

    def execute_sequence(self, calls: List[Union[str, Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Executes a sequential list of calls.
        
        A failed call immediately halts execution; subsequent tools are not executed.
        """
        results: List[Dict[str, Any]] = []
        for call in calls:
            res = self.dispatch(call)
            results.append(res)
            if res["status"] != "success":
                # A failed call cannot execute another tool
                break
        return results


def run_demo() -> Dict[str, Any]:
    """Runs standard contract cases: add(2,3) -> 5; multiply(2,3) -> 6."""
    adapter = LocalToolServiceAdapter()
    res_add = adapter.dispatch({"tool": "add", "args": {"a": 2, "b": 3}})
    res_mul = adapter.dispatch({"tool": "multiply", "args": {"a": 2, "b": 3}})
    res_err_tool = adapter.dispatch({"tool": "divide", "args": {"a": 6, "b": 2}})
    res_err_arg = adapter.dispatch({"tool": "add", "args": {"a": "2", "b": 3}})
    return {
        "add": res_add,
        "multiply": res_mul,
        "unknown_tool": res_err_tool,
        "string_arg": res_err_arg,
    }


if __name__ == "__main__":
    demo = run_demo()
    print(json.dumps(demo, indent=2))
