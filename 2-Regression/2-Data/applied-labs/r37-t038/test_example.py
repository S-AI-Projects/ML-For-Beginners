import math
import unittest

from example import DEMO_CASES, evaluate_batch, mae_rmse


class TestMetrics(unittest.TestCase):
    def test_contract_example(self):
        mae, rmse = mae_rmse([1, 2, 3], [1, 3, 2])
        self.assertAlmostEqual(mae, 2 / 3)
        self.assertAlmostEqual(rmse, math.sqrt(2 / 3))

    def test_identical_arrays_give_zero(self):
        self.assertEqual(mae_rmse([1, 2, 3], [1, 2, 3]), (0.0, 0.0))

    def test_single_pair_and_floats(self):
        self.assertEqual(mae_rmse([5], [8]), (3.0, 3.0))
        mae, rmse = mae_rmse([0.5, 1.5], [1.0, 1.0])
        self.assertAlmostEqual(mae, 0.5)
        self.assertAlmostEqual(rmse, 0.5)

    def test_rmse_is_at_least_mae(self):
        mae, rmse = mae_rmse([0, 0, 0, 0], [0, 0, 0, 10])
        self.assertEqual(mae, 2.5)
        self.assertGreater(rmse, mae)  # one big error hurts RMSE more

    def test_units_follow_the_data(self):
        # same errors expressed in other units: both metrics scale by the same factor
        a = mae_rmse([1, 2, 3], [1, 3, 2])
        b = mae_rmse([1000, 2000, 3000], [1000, 3000, 2000])
        self.assertAlmostEqual(b[0], a[0] * 1000)
        self.assertAlmostEqual(b[1], a[1] * 1000)


class TestInvalidAndRecovery(unittest.TestCase):
    def test_length_mismatch(self):
        with self.assertRaisesRegex(ValueError, "length mismatch"):
            mae_rmse([1, 2, 3], [1, 2])

    def test_empty(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            mae_rmse([], [])

    def test_missing_values(self):
        with self.assertRaisesRegex(ValueError, r"prediction\[1\] is missing"):
            mae_rmse([1, 2, 3], [1, None, 2])
        with self.assertRaisesRegex(ValueError, r"truth\[0\] is not finite"):
            mae_rmse([float("nan"), 2], [1, 2])

    def test_non_numbers_and_bools(self):
        for t, p in (([1, "2"], [1, 2]), ([1, 2], [True, 2]), ([1, 2], [float("inf"), 2])):
            with self.assertRaises(ValueError):
                mae_rmse(t, p)

    def test_recovers_on_next_valid_input(self):
        with self.assertRaises(ValueError):
            mae_rmse([1, 2, 3], [1, None, 2])
        mae, rmse = mae_rmse([1, 2, 3], [1, 3, 2])  # same function, valid input
        self.assertAlmostEqual(mae, 2 / 3)
        self.assertAlmostEqual(rmse, math.sqrt(2 / 3))

    def test_batch_reports_error_and_continues(self):
        r = evaluate_batch(DEMO_CASES)
        self.assertEqual([x["ok"] for x in r], [True, False, True, True, False, False])
        self.assertIn("missing", r[1]["error"])
        self.assertEqual((r[0]["mae"], r[0]["rmse"]), (r[2]["mae"], r[2]["rmse"]))  # before == after the error
        self.assertEqual((r[3]["mae"], r[3]["rmse"]), (0.0, 0.0))

    def test_deliberate_wrong_result_is_detected(self):
        mae, rmse = mae_rmse([1, 2, 3], [1, 3, 2])
        self.assertNotAlmostEqual(mae, 1.0)
        self.assertNotAlmostEqual(rmse, 2 / 3)  # RMSE is sqrt(2/3), not 2/3


if __name__ == "__main__":
    unittest.main()
