"""
Unit tests for r37-t026: allowlisted action policy — worked example with checks.

Run with:
    python3 -m unittest discover -s 1-Introduction/3-fairness/applied-labs/r37-t026 -p "test_*.py" -v
"""

import unittest

from example import (
    ALLOWLIST,
    PolicyViolation,
    clear_executor_calls,
    evaluate_and_execute,
    get_executor_call_count,
)


class TestAllowlistedActionPolicyRegression(unittest.TestCase):
    """
    Regression test executing the exact worked example.
    """

    def setUp(self):
        clear_executor_calls()

    def test_allowed_read_with_valid_path_passes(self):
        res = evaluate_and_execute("read", {"path": "/data/sample.txt"})
        self.assertIn("executed read", res)
        self.assertEqual(get_executor_call_count(), 1)

    def test_unknown_delete_tool_is_rejected(self):
        with self.assertRaises(PolicyViolation) as ctx:
            evaluate_and_execute("delete", {"path": "/data/sample.txt"})
        self.assertIn("unknown tool", str(ctx.exception))
        self.assertEqual(get_executor_call_count(), 0, "Rejected delete must never reach executor")

    def test_missing_required_argument_is_rejected(self):
        with self.assertRaises(PolicyViolation) as ctx:
            evaluate_and_execute("read", {})
        self.assertIn("missing required argument", str(ctx.exception))
        self.assertEqual(get_executor_call_count(), 0, "Missing arg must never reach executor")

    def test_rejected_actions_never_reach_stub_executor(self):
        # Fire multiple invalid actions in sequence
        actions = [
            ("delete", {"path": "/path"}),
            ("drop_table", {"name": "users"}),
            ("read", {}),
            ("write", {"path": "/path"}),  # missing content
        ]
        for tool, args in actions:
            with self.assertRaises(PolicyViolation):
                evaluate_and_execute(tool, args)

        self.assertEqual(get_executor_call_count(), 0, "Executor must remain untouched")


class TestDeliberateFailure(unittest.TestCase):
    """
    Framework check: deliberate wrong expected result causes test to fail,
    demonstrating the framework exits non-zero on failure.
    """

    @unittest.skip("Deliberate failure demo: remove skip to verify non-zero exit")
    def test_deliberate_wrong_executor_call_DEMO_FAIL(self):
        # Intentionally wrong assertion
        self.assertEqual(get_executor_call_count(), 99, "DEMO: intentional failure")


if __name__ == "__main__":
    unittest.main()
