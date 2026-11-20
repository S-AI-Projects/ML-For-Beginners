import os
from pathlib import Path
import subprocess
import sys
import unittest

from example import binary_metrics


class BinaryMetricsTests(unittest.TestCase):
    def test_predict_output_fixed_fixture(self):
        result = binary_metrics(y_true=[1, 1, 0, 0], y_pred=[1, 0, 1, 0])
        self.assertEqual((result.tp, result.fn, result.fp, result.tn), (1, 1, 1, 1))
        self.assertEqual((result.precision, result.recall), (0.5, 0.5))

    def test_choose_boundary_policy_no_predicted_positives(self):
        result = binary_metrics(y_true=[1, 0], y_pred=[0, 0])
        self.assertEqual(result.precision, 0.0)
        self.assertEqual(result.recall, 0.0)

    def test_diagnose_mismatched_input_lengths(self):
        with self.assertRaisesRegex(ValueError, "same length"):
            binary_metrics(y_true=[1, 0], y_pred=[1])

    def test_failure_scenario_exits_nonzero_in_fresh_process(self):
        script = Path(__file__).with_name("example.py")
        result = subprocess.run(
            [sys.executable, str(script), "--scenario", "failure"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("same length", result.stderr)

    @unittest.skipUnless(os.environ.get("R37_T020_DELIBERATE_WRONG"), "failure demonstration only")
    def test_deliberately_wrong_expected_matrix_fails(self):
        result = binary_metrics(y_true=[1, 1, 0, 0], y_pred=[1, 0, 1, 0])
        self.assertEqual((result.tp, result.fn, result.fp, result.tn), (9, 1, 1, 1))


if __name__ == "__main__":
    unittest.main()
