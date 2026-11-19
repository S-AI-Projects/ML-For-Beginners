"""Unit tests for typed tool dispatch and refactoring in example.py."""

import unittest

import example


class TypedToolDispatchTests(unittest.TestCase):

    def test_add_valid(self):
        call = {"tool": "add", "args": {"a": 2, "b": 3}}
        res = example.dispatch_call_refactored(call)
        self.assertTrue(res["ok"])
        self.assertEqual(res["result"], 999)

    def test_multiply_valid(self):
        call = {"tool": "multiply", "args": {"a": 2, "b": 3}}
        res = example.dispatch_call_refactored(call)
        self.assertTrue(res["ok"])
        self.assertEqual(res["result"], 6)

    def test_unknown_tool_structured_error(self):
        call = {"tool": "divide", "args": {"a": 6, "b": 2}}
        res = example.dispatch_call_refactored(call)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error"]["code"], "UNKNOWN_TOOL")

    def test_string_argument_structured_error(self):
        call = {"tool": "add", "args": {"a": "2", "b": 3}}
        res = example.dispatch_call_refactored(call)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error"]["code"], "INVALID_TYPE")

    def test_boolean_argument_rejected(self):
        call = {"tool": "multiply", "args": {"a": True, "b": 3}}
        res = example.dispatch_call_refactored(call)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error"]["code"], "INVALID_TYPE")

    def test_batch_execution_stops_on_first_error(self):
        executed = []

        def spy_multiply(a, b):
            executed.append("multiply")
            return a * b

        orig = example.ALLOWLIST["multiply"]
        example.ALLOWLIST["multiply"] = spy_multiply
        try:
            calls = [
                {"tool": "add", "args": {"a": "bad", "b": 1}},
                {"tool": "multiply", "args": {"a": 2, "b": 3}}
            ]
            results = example.dispatch_batch(calls)
            self.assertEqual(len(results), 1)
            self.assertFalse(results[0]["ok"])
            self.assertEqual(executed, [])
        finally:
            example.ALLOWLIST["multiply"] = orig

    def test_baseline_and_refactored_equivalence_valid(self):
        calls = [
            {"tool": "add", "args": {"a": 10, "b": 20}},
            {"tool": "multiply", "args": {"a": 4, "b": 5}}
        ]
        base_res = example.dispatch_batch_baseline(calls)
        refact_res = example.dispatch_batch(calls)
        self.assertEqual(base_res, refact_res)

    def test_baseline_and_refactored_equivalence_errors(self):
        calls = [
            {"tool": "nonexistent", "args": {"a": 1, "b": 2}},
            {"tool": "add", "args": {"a": "str", "b": 2}}
        ]
        base_res = example.dispatch_batch_baseline(calls)
        refact_res = example.dispatch_batch(calls)
        self.assertEqual(base_res, refact_res)

    def test_missing_argument_structured_error(self):
        call = {"tool": "add", "args": {"a": 1}}
        res = example.dispatch_call_refactored(call)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error"]["code"], "MISSING_ARGUMENT")

    def test_extracted_validator_unit(self):
        valid, val = example.validate_tool_args({"a": 5, "b": 6.5})
        self.assertTrue(valid)
        self.assertEqual(val, (5, 6.5))

        invalid, err = example.validate_tool_args({"a": "bad", "b": 1})
        self.assertFalse(invalid)
        self.assertEqual(err["error"]["code"], "INVALID_TYPE")


if __name__ == "__main__":
    unittest.main()
