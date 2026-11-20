# R37-T018: validate before executing

This worked example applies the lesson's themes of safety, transparency, and accountability to a tiny local action gate. It checks an explicit tool allow-list and the selected tool's argument schema before calling a stub executor. It refuses an unknown `delete` tool, refuses `read` when its required `path` is missing, and then recovers on the next valid `read` input.

## Prerequisites and invocation

Use Python 3 and its standard library from a local repository checkout. From the repository root, run:

```bash
python3 1-Introduction/3-fairness/applied-labs/r37-t018/example.py
python3 -m unittest discover -s 1-Introduction/3-fairness/applied-labs/r37-t018 -p "test_*.py"
```

The fixture sequence is intentionally ordered so the refusal and recovery are visible:

1. `delete(path="fixture/impact-summary.txt")` is refused because `delete` is not allowed.
2. `read()` is refused because the required `path` argument is missing.
3. `read(path="fixture/impact-summary.txt")` is allowed and returns the embedded fixture text.

Expected output:

```json
{
  "trace": [
    {
      "action": {"tool": "delete", "arguments": {"path": "fixture/impact-summary.txt"}},
      "status": "rejected",
      "error": "tool 'delete' is not allowed",
      "executor_called": false
    },
    {
      "action": {"tool": "read", "arguments": {}},
      "status": "rejected",
      "error": "missing required argument: path",
      "executor_called": false
    },
    {
      "action": {"tool": "read", "arguments": {"path": "fixture/impact-summary.txt"}},
      "status": "allowed",
      "result": "Synthetic review note: document intended use, affected people, and risks.",
      "executor_called": true
    }
  ],
  "executor_calls": ["read"]
}
```

The refusal trace shows the validation order: tool membership first, then argument shape and required fields, then fixture-path validity. Only after all checks pass does the executor run. This deterministic example uses a simulated fixture and a stub executor that reads embedded text; it does not perform filesystem operations, call a cloud service, or execute a real tool. It illustrates input validation and refusal handling only, not the security of a production tool system or any model behavior.
