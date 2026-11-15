# R37-T042: Typed tool dispatch, compare two approaches

> This is a **local contract fixture, not a full MCP transport implementation**.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## Invocation

Run from the repository root:

```bash
python3 2-Regression/1-Tools/applied-labs/r37-t042/example.py
python3 -m unittest discover -s 2-Regression/1-Tools/applied-labs/r37-t042 -p "test_*.py"
```

## Fixture

`example.py` dispatches JSON-style tool calls through an explicit allowlist:

- `add(a, b)` and `multiply(a, b)` only.
- Call shape: `{"tool": "add", "args": {"a": 2, "b": 3}}`.
- Success envelope: `{"ok": true, "result": 5}`.
- Error envelope: `{"ok": false, "error": {"code": "...", "message": "..."}}`.
- Error codes: `unknown_tool`, `invalid_argument`, and `not_executed`.
- Numeric arguments are `int` or `float`. `bool` and `None` are rejected. Missing or extra args are rejected.

The CLI runs a fixture of four calls. The second call is valid, the third has a string argument `"a"`, and the fourth is valid but must not run.

## Expected output

Output of `python3 2-Regression/1-Tools/applied-labs/r37-t042/example.py`, exit code 0:

```text
Local contract fixture, not a full MCP transport implementation.
[
  {
    "tool": "add",
    "args": {
      "a": 2,
      "b": 3
    }
  },
  {
    "tool": "multiply",
    "args": {
      "a": 2,
      "b": 3
    }
  },
  {
    "tool": "add",
    "args": {
      "a": "a",
      "b": 3
    }
  },
  {
    "tool": "multiply",
    "args": {
      "a": 2,
      "b": 3
    }
  }
]
[
  {
    "ok": true,
    "result": 5
  },
  {
    "ok": true,
    "result": 6
  },
  {
    "ok": false,
    "error": {
      "code": "invalid_argument",
      "message": "argument 'a' must be a number"
    }
  },
  {
    "ok": false,
    "error": {
      "code": "not_executed",
      "message": "not run: an earlier call failed"
    }
  }
]
```

## Interpretation: a list of calls stops at the first structured error

`dispatch_all` runs calls in order. When one call returns a structured error, every later call is reported as `not_executed` and is never run. In the fixture, the string argument on call 3 stops the run, so call 4 (a valid `multiply`) is reported but not executed.

## How it illustrates the lesson

| Concept | Where it appears |
| --- | --- |
| Tool name | `tool` field, checked against `ALLOWED_TOOLS` |
| Argument schema | `args` must be exactly `{a, b}`, each numeric |
| Dispatch | `dispatch` looks up the allowlisted function and calls it |
| Error envelope | `ok: false` with `code` and `message` |

The lab compares the direct dispatcher with an independent calculation (`sum`, `math.prod`) and an explicit expected-result table, using identical inputs (`test_example.py`).

## Where the simplifications stop

- There is no transport. Calls are Python dicts, not JSON-RPC or MCP messages.
- The allowlist is a plain dict of lambdas, with no discovery, versioning, or permissions.
- Validation covers only the two numeric arguments `a` and `b`. There is no general schema language.
- `not_executed` is a code local to this fixture, not a standard error code.
- Errors are returned as values. There are no exceptions, timeouts, or retries.
- Nothing here measures real hardware, cloud services, or trained-model performance.

## Limitations

- Local contract fixture only. It is not a full MCP transport implementation.
- Stdlib only. Tests use `unittest`.
- Argument validation is deliberately narrow: `int` and `float` only, with `bool` and `None` excluded.
- The lab does not cover concurrency, cancellation, or partial results from a failed batch.
