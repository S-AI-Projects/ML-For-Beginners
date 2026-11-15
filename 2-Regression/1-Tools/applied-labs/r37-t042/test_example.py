import math
import unittest
from unittest import mock

import example

# (tool, a, b, expected): expected values are written by hand.
TABLE = [
    ("add", 2, 3, 5),
    ("multiply", 2, 3, 6),
    ("add", -1, 1.5, 0.5),
    ("multiply", 0, 7, 0),
    ("add", 0, 0, 0),
    ("multiply", 2.5, 4, 10.0),
]

# Independent calculations, not built on the dispatcher.
INDEPENDENT = {
    "add": lambda a, b: sum([a, b]),
    "multiply": lambda a, b: math.prod([a, b]),
}


def _call(tool, a=None, b=None):
    return {"tool": tool, "args": {"a": a, "b": b}}


class DispatchTests(unittest.TestCase):
    def test_add_2_3(self):
        result = example.dispatch({"tool": "add", "args": {"a": 2, "b": 3}})
        self.assertEqual(result, {"ok": True, "result": 5})

    def test_multiply_2_3(self):
        call = {"tool": "multiply", "args": {"a": 2, "b": 3}}
        self.assertEqual(example.dispatch(call), {"ok": True, "result": 6})

    def test_table_matches_expected_and_independent_calculation(self):
        for tool, a, b, expected in TABLE:
            with self.subTest(tool=tool, a=a, b=b):
                call = {"tool": tool, "args": {"a": a, "b": b}}
                result = example.dispatch(call)
                self.assertEqual(result, {"ok": True, "result": expected})
                self.assertEqual(result["result"], INDEPENDENT[tool](a, b))

    def test_unknown_tool(self):
        result = example.dispatch(_call("subtract", 2, 3))
        self.assertFalse(result["ok"])
        error = result["error"]
        self.assertEqual(error["code"], "unknown_tool")
        self.assertIsInstance(error["message"], str)
        self.assertTrue(error["message"])

    def test_non_string_tool_is_unknown_tool(self):
        result = example.dispatch({"tool": ["add"], "args": {"a": 1, "b": 1}})
        self.assertEqual(result["error"]["code"], "unknown_tool")

    def test_string_argument_is_invalid(self):
        result = example.dispatch(_call("add", "a", 3))
        self.assertFalse(result["ok"])
        error = result["error"]
        self.assertEqual(error["code"], "invalid_argument")
        self.assertIsInstance(error["message"], str)
        self.assertTrue(error["message"])

    def test_bool_and_none_are_not_numeric(self):
        bad_values = [True, False, None]
        for value in bad_values:
            for position in ("a", "b"):
                with self.subTest(value=value, position=position):
                    args = {"a": 1, "b": 1}
                    args[position] = value
                    result = example.dispatch({"tool": "add", "args": args})
                    code = result["error"]["code"]
                    self.assertEqual(code, "invalid_argument")

    def test_missing_and_extra_args_are_invalid(self):
        cases = [
            {"tool": "add", "args": {"a": 1}},
            {"tool": "add", "args": {"a": 1, "b": 2, "c": 3}},
            {"tool": "add"},
            {"tool": "add", "args": [1, 2]},
        ]
        for call in cases:
            with self.subTest(call=call):
                result = example.dispatch(call)
                self.assertEqual(result["error"]["code"], "invalid_argument")

    def test_failed_call_stops_later_calls(self):
        seen = []
        real_add = example.ALLOWED_TOOLS["add"]

        def counting_add(a, b):
            seen.append((a, b))
            return real_add(a, b)

        calls = [
            _call("add", 1, 1),
            _call("add", "x", 1),
            _call("add", 2, 2),
        ]
        with mock.patch.dict(example.ALLOWED_TOOLS, {"add": counting_add}):
            results = example.dispatch_all(calls)

        self.assertEqual(seen, [(1, 1)])  # third call never executed
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], {"ok": True, "result": 2})
        self.assertEqual(results[1]["error"]["code"], "invalid_argument")
        self.assertEqual(results[2]["error"]["code"], "not_executed")

    def test_unknown_tool_stops_later_calls(self):
        seen = []
        real_add = example.ALLOWED_TOOLS["add"]

        def counting_add(a, b):
            seen.append((a, b))
            return real_add(a, b)

        calls = [_call("nope", 1, 1), _call("add", 2, 2)]
        with mock.patch.dict(example.ALLOWED_TOOLS, {"add": counting_add}):
            results = example.dispatch_all(calls)

        self.assertEqual(seen, [])
        self.assertEqual(results[0]["error"]["code"], "unknown_tool")
        self.assertEqual(results[1]["error"]["code"], "not_executed")


if __name__ == "__main__":
    unittest.main()
