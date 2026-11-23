"""Unit tests for typed tool dispatch offline service adapter (R37-T051)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from example import LocalToolServiceAdapter, MOCK_LIMITATIONS


class TestTypedToolDispatch(unittest.TestCase):
    def setUp(self):
        self.adapter = LocalToolServiceAdapter()

    def test_add_valid_integers(self):
        res = self.adapter.dispatch({"tool": "add", "args": {"a": 2, "b": 3}})
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["tool"], "add")
        self.assertEqual(res["result"], 5)
        self.assertIsNone(res["error"])

    def test_multiply_valid_integers(self):
        res = self.adapter.dispatch({"tool": "multiply", "args": {"a": 2, "b": 3}})
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["tool"], "multiply")
        self.assertEqual(res["result"], 6)
        self.assertIsNone(res["error"])

    def test_add_floating_point(self):
        res = self.adapter.dispatch({"tool": "add", "args": {"a": 2.5, "b": 3.5}})
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["result"], 6.0)

    def test_unknown_tool_rejection(self):
        res = self.adapter.dispatch({"tool": "divide", "args": {"a": 6, "b": 2}})
        self.assertEqual(res["status"], "error")
        self.assertEqual(res["tool"], "divide")
        self.assertIsNone(res["result"])
        self.assertEqual(res["error"]["code"], "UNKNOWN_TOOL")

    def test_string_argument_a_rejection(self):
        res = self.adapter.dispatch({"tool": "add", "args": {"a": "2", "b": 3}})
        self.assertEqual(res["status"], "error")
        self.assertIsNone(res["result"])
        self.assertEqual(res["error"]["code"], "INVALID_ARGUMENT")
        self.assertIn("must be numeric", res["error"]["message"])

    def test_string_argument_b_rejection(self):
        res = self.adapter.dispatch({"tool": "multiply", "args": {"a": 2, "b": "3"}})
        self.assertEqual(res["status"], "error")
        self.assertIsNone(res["result"])
        self.assertEqual(res["error"]["code"], "INVALID_ARGUMENT")

    def test_boolean_argument_rejection(self):
        res = self.adapter.dispatch({"tool": "add", "args": {"a": True, "b": 3}})
        self.assertEqual(res["status"], "error")
        self.assertEqual(res["error"]["code"], "INVALID_ARGUMENT")

    def test_missing_argument(self):
        res = self.adapter.dispatch({"tool": "add", "args": {"a": 2}})
        self.assertEqual(res["status"], "error")
        self.assertEqual(res["error"]["code"], "MISSING_ARGUMENT")

    def test_json_string_invocation(self):
        json_call = '{"tool": "multiply", "args": {"a": 4, "b": 5}}'
        res = self.adapter.dispatch(json_call)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["result"], 20)

    def test_failed_call_halts_subsequent_execution(self):
        calls = [
            {"tool": "add", "args": {"a": 1, "b": 1}},
            {"tool": "unknown_tool", "args": {"a": 1, "b": 1}},  # Fails here
            {"tool": "multiply", "args": {"a": 10, "b": 10}},   # Must NOT execute
        ]
        results = self.adapter.execute_sequence(calls)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "success")
        self.assertEqual(results[0]["result"], 2)
        self.assertEqual(results[1]["status"], "error")
        self.assertEqual(results[1]["error"]["code"], "UNKNOWN_TOOL")
        self.assertEqual(len(self.adapter.execution_history), 1)

    def test_mock_limitations_stated(self):
        self.assertGreaterEqual(len(MOCK_LIMITATIONS), 3)

    @unittest.skip("Deliberate failure test: demonstrates framework exits non-zero on failure")
    def test_deliberate_wrong_result(self):
        res = self.adapter.dispatch({"tool": "add", "args": {"a": 2, "b": 3}})
        self.assertEqual(res["result"], 999)


if __name__ == "__main__":
    unittest.main()
