import os
import re
import subprocess
import sys
import unittest

from example import confusion_matrix, precision_recall, worked_report, worked_rows

HERE = os.path.dirname(os.path.abspath(__file__))

# The exact worked example, written out in full. This is the regression
# fixture: it must match both the code's output and the README.
EXPECTED_OUTPUT = """y_true=[1, 1, 0, 0] y_pred=[1, 0, 1, 0]
sample true pred outcome
1 1 1 TP
2 1 0 FN
3 0 1 FP
4 0 0 TN
TP=1 FN=1 FP=1 TN=1
precision=TP/(TP+FP)=1/2=0.5
recall=TP/(TP+FN)=1/2=0.5"""


class TestRegression(unittest.TestCase):
    def test_exact_example_values(self):
        self.assertEqual(confusion_matrix([1, 1, 0, 0], [1, 0, 1, 0]), (1, 1, 1, 1))
        self.assertEqual(precision_recall([1, 1, 0, 0], [1, 0, 1, 0]), (0.5, 0.5))

    def test_worked_report_matches_expected_text(self):
        self.assertEqual(worked_report([1, 1, 0, 0], [1, 0, 1, 0]), EXPECTED_OUTPUT)

    def test_script_in_fresh_process_prints_expected_text(self):
        proc = subprocess.run(
            [sys.executable, os.path.join(HERE, "example.py")],
            capture_output=True, text=True, cwd=HERE,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), EXPECTED_OUTPUT)

    def test_readme_contains_the_same_expected_output(self):
        with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
            readme = f.read()
        blocks = re.findall(r"```text\n(.*?)\n```", readme, flags=re.S)
        self.assertIn(EXPECTED_OUTPUT, blocks)

    def test_worked_rows_trace_each_sample(self):
        self.assertEqual(
            worked_rows([1, 1, 0, 0], [1, 0, 1, 0]),
            [(1, 1, 1, "TP"), (2, 1, 0, "FN"), (3, 0, 1, "FP"), (4, 0, 0, "TN")],
        )


class TestBoundaryAndInvalid(unittest.TestCase):
    def test_single_sample(self):
        self.assertEqual(confusion_matrix([1], [1]), (1, 0, 0, 0))

    def test_no_positive_predictions_precision_zero(self):
        p, r = precision_recall([1, 1, 0, 0], [0, 0, 0, 0])
        self.assertEqual((p, r), (0.0, 0.0))

    def test_no_actual_positives_recall_zero(self):
        p, r = precision_recall([0, 0], [1, 0])
        self.assertEqual((p, r), (0.0, 0.0))

    def test_argument_order_matters(self):
        self.assertEqual(confusion_matrix([1, 1, 1], [1, 0, 0]), (1, 2, 0, 0))
        self.assertEqual(confusion_matrix([1, 0, 0], [1, 1, 1]), (1, 0, 2, 0))

    def test_invalid_inputs(self):
        for yt, yp in (([1, 0], [1]), ([], []), ([1, 2], [1, 0]), ([1, 0], [True, 0])):
            with self.assertRaises(ValueError):
                confusion_matrix(yt, yp)

    def test_deliberate_wrong_result_is_detected(self):
        self.assertNotEqual(confusion_matrix([1, 1, 0, 0], [1, 0, 1, 0]), (2, 0, 0, 2))
        self.assertNotEqual(precision_recall([1, 1, 0, 0], [1, 0, 1, 0]), (1.0, 1.0))


if __name__ == "__main__":
    unittest.main()
