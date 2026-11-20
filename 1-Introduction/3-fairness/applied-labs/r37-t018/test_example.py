import json
from pathlib import Path
import subprocess
import sys
import unittest

from example import FIXTURE_ACTIONS, run_actions, validate_action


class PolicyGateTests(unittest.TestCase):
    def test_allowed_read_with_valid_fixture_path_reaches_executor(self):
        calls = []

        def recording_executor(tool, arguments):
            calls.append((tool, arguments))
            return "local fixture result"

        action = {"tool": "read", "arguments": {"path": "fixture/impact-summary.txt"}}
        result = run_actions([action], executor=recording_executor)
        self.assertEqual(result["trace"][0]["status"], "allowed")
        self.assertTrue(result["trace"][0]["executor_called"])
        self.assertEqual(calls, [("read", {"path": "fixture/impact-summary.txt"})])

    def test_unknown_delete_tool_is_rejected_before_executor(self):
        calls = []
        action = {"tool": "delete", "arguments": {"path": "fixture/impact-summary.txt"}}
        result = run_actions([action], executor=lambda *args: calls.append(args))
        self.assertEqual(result["trace"][0]["error"], "tool 'delete' is not allowed")
        self.assertFalse(result["trace"][0]["executor_called"])
        self.assertEqual(calls, [])

    def test_missing_path_is_refused_then_next_valid_input_recovers(self):
        calls = []
        actions = [
            {"tool": "read", "arguments": {}},
            {"tool": "read", "arguments": {"path": "fixture/impact-summary.txt"}},
        ]
        result = run_actions(actions, executor=lambda tool, args: calls.append((tool, args)) or "recovered")
        self.assertEqual([row["status"] for row in result["trace"]], ["rejected", "allowed"])
        self.assertEqual(result["trace"][0]["error"], "missing required argument: path")
        self.assertFalse(result["trace"][0]["executor_called"])
        self.assertEqual(result["trace"][1]["result"], "recovered")
        self.assertEqual(calls, [("read", {"path": "fixture/impact-summary.txt"})])

    def test_boundary_and_invalid_fixture_paths_are_rejected(self):
        for action, expected_error in (
            ({"tool": "read", "arguments": {"path": ""}}, "argument 'path' must be a non-empty string"),
            ({"tool": "read", "arguments": {"path": "fixture/missing.txt"}}, "fixture path not found: fixture/missing.txt"),
        ):
            with self.subTest(action=action):
                self.assertEqual(validate_action(action), expected_error)

    def test_command_line_trace_matches_expected_fixture(self):
        script = Path(__file__).with_name("example.py")
        completed = subprocess.run(
            [sys.executable, str(script)], capture_output=True, text=True, check=True
        )
        actual = json.loads(completed.stdout)
        self.assertEqual(actual, run_actions(FIXTURE_ACTIONS))
        self.assertEqual(actual["executor_calls"], ["read"])
        self.assertEqual(
            [item["status"] for item in actual["trace"]],
            ["rejected", "rejected", "allowed"],
        )


if __name__ == "__main__":
    unittest.main()
