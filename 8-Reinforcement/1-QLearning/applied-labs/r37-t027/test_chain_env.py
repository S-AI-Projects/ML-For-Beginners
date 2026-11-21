"""
Unit tests for r37-t027: finite-state reward trace — evaluation experiment.

Run with:
    python3 -m unittest discover -s 8-Reinforcement/1-QLearning/applied-labs/r37-t027 -p "test_*.py" -v
"""

import unittest

from example import (
    ThreeStateChainEnv,
    compare_three_configurations,
    run_episode,
)


class TestFiniteStateChainContract(unittest.TestCase):
    """
    Contract requirements:
    - From state 0, [right, right] ends at 2 with total reward 1
    - Repeated left ends at the step cap with reward 0
    - Reward 1 only on entry into terminal state 2
    """

    def test_right_right_reaches_terminal_state_with_reward_1(self):
        res = run_episode(["right", "right"], step_cap=5, start_state=0)
        self.assertEqual(res["final_state"], 2)
        self.assertEqual(res["total_reward"], 1)
        self.assertEqual(res["steps_taken"], 2)
        self.assertTrue(res["is_terminal"])
        self.assertEqual(res["state_trace"], [0, 1, 2])
        self.assertEqual(res["reward_trace"], [0, 1])

    def test_repeated_left_ends_at_step_cap_with_reward_0(self):
        # 10 'left' actions with step cap 5
        actions = ["left"] * 10
        res = run_episode(actions, step_cap=5, start_state=0)
        self.assertEqual(res["final_state"], 0)
        self.assertEqual(res["total_reward"], 0)
        self.assertEqual(res["steps_taken"], 5)
        self.assertFalse(res["is_terminal"])
        self.assertEqual(res["reward_trace"], [0, 0, 0, 0, 0])

    def test_reward_given_only_on_entry(self):
        env = ThreeStateChainEnv(step_cap=10)
        env.reset(start_state=1)
        # Move into 2 -> reward 1
        s, r, done, _ = env.step("right")
        self.assertEqual(s, 2)
        self.assertEqual(r, 1)
        self.assertTrue(done)
        # Attempt another step after terminal -> reward 0
        s2, r2, done2, _ = env.step("right")
        self.assertEqual(r2, 0)
        self.assertTrue(done2)


class TestControlledConfigurationsComparison(unittest.TestCase):
    """
    Verify three controlled configurations and report trade-offs.
    """

    def test_configurations_comparison(self):
        comparison = compare_three_configurations()
        self.assertIn("config_cap_1", comparison)
        self.assertIn("config_cap_2", comparison)
        self.assertIn("config_cap_5", comparison)

        # Cap 1 cannot reach terminal state
        self.assertEqual(comparison["config_cap_1"]["optimal_seq"]["total_reward"], 0)
        # Cap 2 reaches terminal state
        self.assertEqual(comparison["config_cap_2"]["optimal_seq"]["total_reward"], 1)
        # Cap 5 reaches terminal state with exploration
        self.assertEqual(comparison["config_cap_5"]["exploring_seq"]["total_reward"], 1)


class TestInputValidation(unittest.TestCase):
    """Invalid action raises ValueError."""

    def test_invalid_action_raises(self):
        env = ThreeStateChainEnv()
        with self.assertRaises(ValueError):
            env.step("jump")


class TestDeliberateFailure(unittest.TestCase):
    """
    Framework check: deliberate wrong expected result causes test to fail,
    demonstrating the framework exits non-zero on failure.
    """

    @unittest.skip("Deliberate failure demo: remove skip to verify non-zero exit")
    def test_deliberate_wrong_reward_DEMO_FAIL(self):
        res = run_episode(["right", "right"], step_cap=5)
        # Intentionally wrong expected reward (99 instead of 1)
        self.assertEqual(res["total_reward"], 99, "DEMO: intentional failure")


if __name__ == "__main__":
    unittest.main()
