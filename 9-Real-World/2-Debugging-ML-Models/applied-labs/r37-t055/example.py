"""Allowlisted action policy — evaluation experiment for 9-Real-World/2-Debugging-ML-Models."""

from typing import Any, Dict, List, Optional, Set

MOCK_LIMITATIONS = [
    "Simulates filesystem read in-memory; does not access physical OS filesystem or cloud blob storage.",
    "Does not execute real shell commands or network sockets.",
    "Static schema dictionary; does not implement dynamic JSON-Schema / Pydantic compiler.",
    "Single-tenant policy verification; does not establish cryptographic session authentication.",
]

# Explicit set of permitted tools and their mandatory argument schemas
ALLOWED_ACTION_SCHEMAS: Dict[str, Dict[str, type]] = {
    "read": {"path": str},
    "inspect": {"model_name": str},
}

# Simulated local storage fixture
MOCK_FILE_STORAGE = {
    "model_config.json": '{"model_type": "LogisticRegression", "n_features": 4}',
    "dataset_summary.txt": "Dataset contains 1000 rows with 4 numeric features.",
}


def evaluate_and_execute_action(action: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates proposed actions against explicit allowed-tool set and schema before execution.
    
    1. Rejects unknown tools with code 'DISALLOWED_ACTION'.
    2. Rejects schema violations (missing or invalid args) with code 'SCHEMA_VIOLATION' before execution.
    3. Executes allowed actions successfully.
    """
    if not isinstance(action, dict):
        return {
            "status": "rejected",
            "executed": False,
            "tool": None,
            "result": None,
            "error": {"code": "INVALID_ACTION_PAYLOAD", "message": "Action must be a dictionary."},
        }

    tool_name = action.get("tool")
    args = action.get("args")

    # 1. Allowlist check
    if not tool_name or tool_name not in ALLOWED_ACTION_SCHEMAS:
        return {
            "status": "rejected",
            "executed": False,
            "tool": tool_name,
            "result": None,
            "error": {
                "code": "DISALLOWED_ACTION",
                "message": f"Tool '{tool_name}' is not in the explicit allowlist: {sorted(list(ALLOWED_ACTION_SCHEMAS.keys()))}.",
            },
        }

    # 2. Schema check
    schema = ALLOWED_ACTION_SCHEMAS[tool_name]
    if not isinstance(args, dict):
        return {
            "status": "rejected",
            "executed": False,
            "tool": tool_name,
            "result": None,
            "error": {
                "code": "SCHEMA_VIOLATION",
                "message": "'args' field must be a dictionary.",
            },
        }

    for expected_arg, expected_type in schema.items():
        if expected_arg not in args:
            return {
                "status": "rejected",
                "executed": False,
                "tool": tool_name,
                "result": None,
                "error": {
                    "code": "SCHEMA_VIOLATION",
                    "message": f"Missing mandatory argument '{expected_arg}' for tool '{tool_name}'.",
                },
            }
        val = args[expected_arg]
        if not isinstance(val, expected_type) or (isinstance(val, str) and not val.strip()):
            return {
                "status": "rejected",
                "executed": False,
                "tool": tool_name,
                "result": None,
                "error": {
                    "code": "SCHEMA_VIOLATION",
                    "message": f"Argument '{expected_arg}' must be of type {expected_type.__name__} (non-empty).",
                },
            }

    # 3. Execution phase (only reached if policy passes)
    if tool_name == "read":
        path = args["path"].strip()
        content = MOCK_FILE_STORAGE.get(path, f"[File '{path}' loaded from mock storage]")
        return {
            "status": "success",
            "executed": True,
            "tool": tool_name,
            "result": {"path": path, "content": content},
            "error": None,
        }
    elif tool_name == "inspect":
        model_name = args["model_name"].strip()
        return {
            "status": "success",
            "executed": True,
            "tool": tool_name,
            "result": {"model_name": model_name, "status": "verified"},
            "error": None,
        }

    return {
        "status": "rejected",
        "executed": False,
        "tool": tool_name,
        "result": None,
        "error": {"code": "INTERNAL_DISPATCH_ERROR", "message": "Unhandled tool."},
    }


def run_evaluation_experiment(test_actions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Runs a systematic evaluation experiment across proposed actions."""
    results = []
    total = len(test_actions)
    allowed_count = 0
    rejected_count = 0

    for act in test_actions:
        res = evaluate_and_execute_action(act)
        results.append({"action": act, "evaluation": res})
        if res["status"] == "success":
            allowed_count += 1
        else:
            rejected_count += 1

    return {
        "total_evaluated": total,
        "allowed_count": allowed_count,
        "rejected_count": rejected_count,
        "rejection_rate": (rejected_count / total) if total > 0 else 0.0,
        "evaluations": results,
    }


def get_experiment_matrix() -> List[Dict[str, Any]]:
    return [
        {"tool": "read", "args": {"path": "model_config.json"}},
        {"tool": "delete", "args": {"path": "model.bin"}},
        {"tool": "read", "args": {}},
        {"tool": "read", "args": {"path": ""}},
        {"tool": "inspect", "args": {"model_name": "classifier_v1"}},
        {"tool": "write", "args": {"path": "hack.py", "content": "rm -rf"}},
    ]


if __name__ == "__main__":
    import json
    exp = run_evaluation_experiment(get_experiment_matrix())
    print(json.dumps(exp, indent=2))
