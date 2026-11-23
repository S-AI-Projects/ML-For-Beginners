"""Unit tests for allowlisted action policy evaluation experiment (R37-T055)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from example import (
    evaluate_and_execute_action,
    run_evaluation_experiment,
    get_experiment_matrix,
    MOCK_LIMITATIONS,
)


class TestAllowlistedActionPolicy(unittest.TestCase):
    def test_allowed_read_with_valid_path_succeeds(self):
        # Allowed read with a valid path succeeds
        action = {"tool": "read", "args": {"path": "model_config.json"}}
        res = evaluate_and_execute_action(action)
        self.assertEqual(res["status"], "success")
        self.assertTrue(res["executed"])
        self.assertEqual(res["tool"], "read")
        self.assertIsNotNone(res["result"])
        self.assertIsNone(res["error"])

    def test_unknown_tool_delete_is_rejected(self):
        # Unknown tool delete is rejected
        action = {"tool": "delete", "args": {"path": "model.bin"}}
        res = evaluate_and_execute_action(action)
        self.assertEqual(res["status"], "rejected")
        self.assertFalse(res["executed"])
        self.assertEqual(res["tool"], "delete")
        self.assertIsNone(res["result"])
        self.assertEqual(res["error"]["code"], "DISALLOWED_ACTION")
        self.assertIn("not in the explicit allowlist", res["error"]["message"])

    def test_read_without_path_argument_rejected_before_execution(self):
        # read without path argument is rejected before execution
        action = {"tool": "read", "args": {}}
        res = evaluate_and_execute_action(action)
        self.assertEqual(res["status"], "rejected")
        self.assertFalse(res["executed"])
        self.assertEqual(res["error"]["code"], "SCHEMA_VIOLATION")
        self.assertIn("Missing mandatory argument 'path'", res["error"]["message"])

    def test_empty_path_string_rejected(self):
        action = {"tool": "read", "args": {"path": "   "}}
        res = evaluate_and_execute_action(action)
        self.assertEqual(res["status"], "rejected")
        self.assertFalse(res["executed"])
        self.assertEqual(res["error"]["code"], "SCHEMA_VIOLATION")

    def test_allowed_inspect_tool_succeeds(self):
        action = {"tool": "inspect", "args": {"model_name": "sentiment_net"}}
        res = evaluate_and_execute_action(action)
        self.assertEqual(res["status"], "success")
        self.assertTrue(res["executed"])

    def test_evaluation_experiment_matrix(self):
        matrix = get_experiment_matrix()
        exp = run_evaluation_experiment(matrix)
        self.assertEqual(exp["total_evaluated"], 6)
        self.assertEqual(exp["allowed_count"], 2)
        self.assertEqual(exp["rejected_count"], 4)
        self.assertAlmostEqual(exp["rejection_rate"], 4 / 6)

    def test_mock_limitations_documented(self):
        self.assertGreaterEqual(len(MOCK_LIMITATIONS), 3)

    @unittest.skip("Deliberate failure test: demonstrates framework exits non-zero on failure")
    def test_deliberate_wrong_result(self):
        action = {"tool": "read", "args": {"path": "model_config.json"}}
        res = evaluate_and_execute_action(action)
        self.assertEqual(res["status"], "rejected")


if __name__ == "__main__":
    unittest.main()
