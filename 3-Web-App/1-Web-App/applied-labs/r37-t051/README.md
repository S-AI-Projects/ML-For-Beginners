# Applied Lab R37-T051: Typed Tool Dispatch — Offline Service Adapter

## Overview

This lab extends [Build a Web App to use a ML Model](../../README.md) by introducing an explicit typed tool dispatch contract. In production machine learning web applications and tool-calling agent systems (such as MCP or OpenAI function calling), web requests invoke discrete backend tools. This lab implements a deterministic offline service adapter that enforces:
- An explicit allowlist of tools (`add`, `multiply`).
- Strict schema validation for numeric arguments (`a`, `b`).
- Structured response and error envelopes.
- Fail-fast sequential execution (a failed call halts downstream execution).

## Contract Specification

### Allowed Tools
- `add(a, b)`: Returns $a + b$
- `multiply(a, b)`: Returns $a \times b$

### Argument Types
- `a`: Numeric (`int` or `float`)
- `b`: Numeric (`int` or `float`)
- Strings, booleans, and null values are rejected with structured error code `INVALID_ARGUMENT`.

### Envelopes

#### Success Envelope
```json
{
  "status": "success",
  "tool": "add",
  "result": 5,
  "error": null
}
```

#### Error Envelope
```json
{
  "status": "error",
  "tool": "divide",
  "result": null,
  "error": {
    "code": "UNKNOWN_TOOL",
    "message": "Tool 'divide' is not in the explicit allowlist: ['add', 'multiply']"
  }
}
```

## Mock Limitations

This implementation is a local contract fixture and **does not** establish:
1. Real transport framing (e.g. MCP JSON-RPC, WebSockets, REST HTTP endpoints).
2. Network latency, socket timeouts, or retry backoff.
3. Multi-tenant authentication, token authorization, or rate limiting.
4. Asynchronous task queueing or distributed worker execution.
5. Physical hardware, GPU acceleration, or cloud service availability.

## Running the Code and Tests

### Run Example
```bash
python3 3-Web-App/1-Web-App/applied-labs/r37-t051/example.py
```

### Run Unit Tests
```bash
python3 -m unittest discover -s 3-Web-App/1-Web-App/applied-labs/r37-t051 -p "test_*.py" -v
```
