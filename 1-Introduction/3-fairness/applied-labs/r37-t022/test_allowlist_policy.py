"""
Unit tests for r37-t022: allowlisted action policy — compare two approaches.

Run with:
    python3 -m unittest discover -s 1-Introduction/3-fairness/applied-labs/r37-t022 -p "test_*.py" -v

Test classes
------------
TestNormalCase              — allowed action reaches executor
TestBoundaryUnknownTool     — unknown tool is rejected before executor
TestBoundaryMissingArg      — known tool with missing arg is rejected before executor
TestExecutorNotReachedOnReject — executor call log stays empty for all rejections
TestApproachComparison      — Approach A and Approach B agree on identical inputs
TestDeliberateFailure       — @skip demo that exits non-zero when skip removed
"""

import unittest

from example import (
    ALLOWLIST,
    PolicyViolation,
    clear_executor_log,
    evaluate_action,
    evaluate_action_via_table,
    get_executor_calls,
)


class TestNormalCase(unittest.TestCase):
    """Allowed read_file with a valid path must reach the executor."""

    def setUp(self):
        clear_executor_log()

    def test_allowed_read_returns_result(self):
        result = evaluate_action("read_file", {"path": "/data/report.csv"})
        self.assertIn("read_file", result)

    def test_executor_called_exactly_once(self):
        evaluate_action("read_file", {"path": "/data/report.csv"})
        calls = get_executor_calls()
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["tool"], "read_file")

    def test_allowed_list_directory(self):
        result = evaluate_action("list_directory", {"path": "/data/"})
        self.assertIn("list_directory", result)

    def test_allowed_write_file(self):
        result = evaluate_action("write_file", {"path": "/out.txt", "content": "hello"})
        self.assertIn("write_file", result)


class TestBoundaryUnknownTool(unittest.TestCase):
    """Unknown tool must raise PolicyViolation; executor must not be called."""

    def setUp(self):
        clear_executor_log()

    def test_delete_raises_policy_violation(self):
        with self.assertRaises(PolicyViolation):
            evaluate_action("delete_file", {"path": "/data/report.csv"})

    def test_executor_not_called_for_unknown_tool(self):
        try:
            evaluate_action("delete_file", {"path": "/data/report.csv"})
        except PolicyViolation:
            pass
        self.assertEqual(get_executor_calls(), [],
                         "Executor must NOT be called for rejected actions")

    def test_violation_message_mentions_unknown_tool(self):
        with self.assertRaises(PolicyViolation) as ctx:
            evaluate_action("run_shell", {})
        self.assertIn("unknown tool", str(ctx.exception))

    def test_empty_tool_name_rejected(self):
        with self.assertRaises(PolicyViolation):
            evaluate_action("", {})


class TestBoundaryMissingArg(unittest.TestCase):
    """Known tool with a missing required arg must raise PolicyViolation."""

    def setUp(self):
        clear_executor_log()

    def test_read_file_missing_path_raises(self):
        with self.assertRaises(PolicyViolation):
            evaluate_action("read_file", {})

    def test_write_file_missing_content_raises(self):
        with self.assertRaises(PolicyViolation):
            evaluate_action("write_file", {"path": "/out.txt"})  # 'content' missing

    def test_write_file_missing_path_raises(self):
        with self.assertRaises(PolicyViolation):
            evaluate_action("write_file", {"content": "hello"})  # 'path' missing

    def test_executor_not_called_for_missing_arg(self):
        try:
            evaluate_action("read_file", {})
        except PolicyViolation:
            pass
        self.assertEqual(get_executor_calls(), [],
                         "Executor must NOT be called when required arg is missing")

    def test_violation_message_mentions_missing_arg(self):
        with self.assertRaises(PolicyViolation) as ctx:
            evaluate_action("read_file", {})
        self.assertIn("missing required argument", str(ctx.exception))


class TestExecutorNotReachedOnReject(unittest.TestCase):
    """
    Core contract: rejected actions NEVER reach the stub executor.
    Runs multiple rejections and asserts the executor log stays empty.
    """

    def setUp(self):
        clear_executor_log()

    def test_all_rejections_leave_executor_clean(self):
        rejections = [
            ("delete_file",  {"path": "/x"}),   # unknown tool
            ("read_file",    {}),                # missing 'path'
            ("write_file",   {"path": "/x"}),   # missing 'content'
            ("unknown_cmd",  {"a": "b"}),        # unknown tool
        ]
        for tool, args in rejections:
            try:
                evaluate_action(tool, args)
            except PolicyViolation:
                pass
        self.assertEqual(get_executor_calls(), [],
                         "Executor must remain empty after all rejections")


class TestApproachComparison(unittest.TestCase):
    """
    Approach A (direct validation logic) and Approach B (table look-up)
    must agree on identical inputs.
    """

    def _verdict_a(self, tool, args):
        try:
            evaluate_action(tool, args)
            return "ALLOW"
        except PolicyViolation:
            return "REJECT"

    def _verdict_b(self, tool, args):
        result = evaluate_action_via_table(tool, args)
        return "ALLOW" if result == "ALLOW" else "REJECT"

    def test_allowed_read_both_agree(self):
        tool, args = "read_file", {"path": "/data/report.csv"}
        self.assertEqual(self._verdict_a(tool, args), self._verdict_b(tool, args))
        self.assertEqual(self._verdict_a(tool, args), "ALLOW")

    def test_unknown_delete_both_agree(self):
        tool, args = "delete_file", {"path": "/data/report.csv"}
        self.assertEqual(self._verdict_a(tool, args), self._verdict_b(tool, args))
        self.assertEqual(self._verdict_a(tool, args), "REJECT")

    def test_missing_arg_both_agree(self):
        tool, args = "read_file", {}
        self.assertEqual(self._verdict_a(tool, args), self._verdict_b(tool, args))
        self.assertEqual(self._verdict_a(tool, args), "REJECT")

    def test_allowed_list_directory_both_agree(self):
        tool, args = "list_directory", {"path": "/data/"}
        self.assertEqual(self._verdict_a(tool, args), self._verdict_b(tool, args))
        self.assertEqual(self._verdict_a(tool, args), "ALLOW")


class TestDeliberateFailure(unittest.TestCase):
    """
    This test is intentionally designed to FAIL to demonstrate the framework
    exits non-zero on assertion failure.

    Remove the @skip decorator and run:
        python3 -m unittest \
            1-Introduction/3-fairness/applied-labs/r37-t022/test_allowlist_policy.py \
            TestDeliberateFailure.test_wrong_verdict_DEMO_FAIL
    Expected: FAIL, exit code 1
    """

    @unittest.skip(
        "Deliberate-failure demo — remove @skip to confirm non-zero exit on failure."
    )
    def test_wrong_verdict_DEMO_FAIL(self):
        """
        Asserts that an unknown tool returns 'ALLOW' — which is intentionally wrong.
        Without @skip this WILL fail, proving the suite catches mistakes.
        """
        clear_executor_log()
        try:
            evaluate_action("delete_file", {"path": "/x"})
            verdict = "ALLOW"
        except PolicyViolation:
            verdict = "REJECT"
        # Deliberately wrong assertion: delete_file must be REJECT, not ALLOW
        self.assertEqual(verdict, "ALLOW",
                         "DEMO: This failure is intentional. 'delete_file' must be REJECT.")


if __name__ == "__main__":
    unittest.main()

