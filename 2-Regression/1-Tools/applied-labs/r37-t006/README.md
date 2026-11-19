# R37-T006: Typed Tool Dispatch - Refactor the Teaching Example

**Label:** local contract fixture, not a full MCP transport implementation.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## What It Is

A typed JSON tool dispatcher enforcing:
- Explicit allowlist: `add(a, b)` and `multiply(a, b)`.
- Numeric argument validation: `a` and `b` must be real numbers (`int`/`float`, rejecting `bool` and `str`).
- Structured error handling: returning `{"ok": False, "error": {"code": ..., "message": ...}}`.
- Fail-fast batch execution: if a call fails, subsequent calls in the batch cannot execute.

## Refactoring and Responsibility Extraction

- **Baseline (`dispatch_call_baseline`):** Monolithic handler performing tool allowlist lookup, schema/type validation, and execution.
- **Extracted Responsibility (`validate_tool_args`):** Dedicated argument validator checking dictionary structure, required keys (`a`, `b`), and strict numeric types.
- **Refactored Dispatcher (`dispatch_call_refactored`):** Coordinates tool allowlist resolution, delegates argument validation to `validate_tool_args`, and invokes the tool.
- **Equivalence:** Before/after behavioral equivalence is proven on all valid calls and failure cases.

## Invocation

From the repository root:

```bash
python3 2-Regression/1-Tools/applied-labs/r37-t006/example.py
```

Run unit tests from the repository root:

```bash
python3 -m unittest discover -s 2-Regression/1-Tools/applied-labs/r37-t006 -p "test_*.py"
```

## Fixture and Expected Output

Fixture calls:
- `add(2, 3)` -> `5` (`ok: True`)
- `multiply(2, 3)` -> `6` (`ok: True`)
- Unknown tool `unknown_tool` -> `ok: False`, code `UNKNOWN_TOOL`
- String argument `a="2"` -> `ok: False`, code `INVALID_TYPE`

Expected CLI output:

```text
local contract fixture, not a full MCP transport implementation
headline calls execution:
  add(2, 3) -> {'ok': True, 'result': 5}
  multiply(2, 3) -> {'ok': True, 'result': 6}
  failed call -> {'ok': False, 'error': {'code': 'UNKNOWN_TOOL', 'message': "tool 'unknown_tool' not in allowlist"}}
  calls executed in batch: 3 of 4 (aborted on error)
  baseline == refactored equivalence: True
```

## Limitations

- Local function dispatch fixture only; does not implement MCP JSON-RPC protocol framing or stdio transport.
- Tools are restricted to binary arithmetic (`add`, `multiply`).
- Makes no claims about real hardware, cloud service behavior, or trained model performance.
