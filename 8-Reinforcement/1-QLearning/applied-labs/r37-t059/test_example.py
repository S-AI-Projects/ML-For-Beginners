"""
Unit tests for R37-T059: Finite-State Reward Trace & Scenario Assessment
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from example import (
    ThreeStateChainEnv,
    APPLIED_QUESTIONS,
    check_q1_prediction,
    check_q2_diagnosis,
    check_q3_boundary_policy,
)


class TestThreeStateChainEnv(unittest.TestCase):

    def setUp(self):
        self.env = ThreeStateChainEnv(max_steps=5, start_state=0)

    def test_goal_path_right_right(self):
        """From state 0, ['right', 'right'] ends at terminal state 2 with total reward 1."""
        res = self.env.run_episode(["right", "right"])
        self.assertEqual(res["final_state"], 2)
        self.assertEqual(res["total_reward"], 1)
        self.assertEqual(res["step_count"], 2)
        self.assertTrue(res["terminated_by_goal"])
        self.assertFalse(res["terminated_by_cap"])
        self.assertTrue(res["done"])

    def test_repeated_left_hits_step_cap(self):
        """Repeated 'left' from state 0 stays at 0 and ends at step cap 5 with reward 0."""
        res = self.env.run_episode(["left"] * 5)
        self.assertEqual(res["final_state"], 0)
        self.assertEqual(res["total_reward"], 0)
        self.assertEqual(res["step_count"], 5)
        self.assertFalse(res["terminated_by_goal"])
        self.assertTrue(res["terminated_by_cap"])
        self.assertTrue(res["done"])

    def test_single_right_intermediate(self):
        """A single 'right' reaches state 1 with 0 reward and not done."""
        next_state, reward, done, info = self.env.step("right")
        self.assertEqual(next_state, 1)
        self.assertEqual(reward, 0)
        self.assertFalse(done)
        self.assertEqual(info["reason"], "in_progress")

    def test_oscillation_until_cap(self):
        """Oscillating between states 0 and 1 stops at step cap 5."""
        res = self.env.run_episode(["right", "left", "right", "left", "right"])
        self.assertEqual(res["step_count"], 5)
        self.assertEqual(res["total_reward"], 0)
        self.assertEqual(res["final_state"], 1)
        self.assertTrue(res["terminated_by_cap"])

    def test_q1_prediction_check(self):
        """Executable check for Q1: output prediction matches ground truth."""
        valid_pred = {
            "final_state": 2,
            "step_count": 2,
            "total_reward": 1,
            "terminated_by_goal": True,
        }
        self.assertTrue(check_q1_prediction(valid_pred))

        invalid_pred = {
            "final_state": 1,
            "step_count": 2,
            "total_reward": 0,
            "terminated_by_goal": False,
        }
        self.assertFalse(check_q1_prediction(invalid_pred))

    def test_q2_failure_diagnosis_check(self):
        """Executable check for Q2: diagnosis flags clamped boundary timeout."""
        is_diag, reason = check_q2_diagnosis(["left"] * 5)
        self.assertTrue(is_diag)
        self.assertEqual(reason, "clamped_boundary_timeout")

        is_diag_success, reason_success = check_q2_diagnosis(["right", "right"])
        self.assertFalse(is_diag_success)
        self.assertEqual(reason_success, "goal_reached_not_failure")

    def test_q3_boundary_policy_check(self):
        """Executable check for Q3: verifies clamp_at_zero as boundary policy."""
        self.assertTrue(check_q3_boundary_policy("clamp_at_zero"))
        self.assertFalse(check_q3_boundary_policy("wrap_around"))
        self.assertFalse(check_q3_boundary_policy("teleport_to_goal"))

    def test_deliberate_failure_detection(self):
        """Verifies that deliberate assertion mismatches cause test failures."""
        env = ThreeStateChainEnv()
        res = env.run_episode(["right", "right"])
        with self.assertRaises(AssertionError):
            self.assertEqual(res["total_reward"], 999, "Deliberate wrong reward must fail")


if __name__ == "__main__":
    unittest.main()
