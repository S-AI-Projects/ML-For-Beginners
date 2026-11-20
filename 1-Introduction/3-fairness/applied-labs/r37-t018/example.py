"""Demonstrate an allow-list and argument-schema gate before tool execution.

This is a local simulation. The stub reads only an embedded fixture; it does
not access the filesystem, a cloud service, or any external tool.
"""

import json


ALLOWED_TOOL_SCHEMAS = {
    "read": {
        "required": ("path",),
        "optional": (),
    }
}

# The path is a simulated fixture key, not a path opened on the host machine.
FIXTURE_FILES = {
    "fixture/impact-summary.txt": (
        "Synthetic review note: document intended use, affected people, and risks."
    )
}

# First two actions are deliberately refused; the third demonstrates recovery.
FIXTURE_ACTIONS = [
    {"tool": "delete", "arguments": {"path": "fixture/impact-summary.txt"}},
    {"tool": "read", "arguments": {}},
    {"tool": "read", "arguments": {"path": "fixture/impact-summary.txt"}},
]


def validate_action(action):
    """Return a refusal message, or None when tool and arguments are valid."""
    if not isinstance(action, dict):
        return "action must be an object"
    if set(action) != {"tool", "arguments"}:
        return "action must contain exactly 'tool' and 'arguments'"

    tool = action["tool"]
    if not isinstance(tool, str) or tool not in ALLOWED_TOOL_SCHEMAS:
        return "tool {!r} is not allowed".format(tool)

    arguments = action["arguments"]
    if not isinstance(arguments, dict):
        return "arguments must be an object"

    schema = ALLOWED_TOOL_SCHEMAS[tool]
    allowed_arguments = set(schema["required"]) | set(schema["optional"])
    unexpected = set(arguments) - allowed_arguments
    if unexpected:
        return "unexpected argument(s): {}".format(", ".join(sorted(unexpected)))

    missing = set(schema["required"]) - set(arguments)
    if missing:
        return "missing required argument: {}".format(", ".join(sorted(missing)))

    path = arguments["path"]
    if not isinstance(path, str) or not path.strip():
        return "argument 'path' must be a non-empty string"
    if path not in FIXTURE_FILES:
        return "fixture path not found: {}".format(path)

    return None


def stub_executor(tool, arguments):
    """Return local fixture data for the one allowed simulated tool."""
    if tool == "read":
        return FIXTURE_FILES[arguments["path"]]
    raise AssertionError("the policy gate must block tools without an executor")


def run_actions(actions, executor=stub_executor):
    """Validate each action before calling the supplied local executor stub."""
    trace = []
    executor_calls = []

    for action in actions:
        refusal = validate_action(action)
        if refusal is not None:
            trace.append({
                "action": action,
                "status": "rejected",
                "error": refusal,
                "executor_called": False,
            })
            continue

        tool = action["tool"]
        executor_calls.append(tool)
        result = executor(tool, action["arguments"])
        trace.append({
            "action": action,
            "status": "allowed",
            "result": result,
            "executor_called": True,
        })

    return {"trace": trace, "executor_calls": executor_calls}


if __name__ == "__main__":
    print(json.dumps(run_actions(FIXTURE_ACTIONS), indent=2))
