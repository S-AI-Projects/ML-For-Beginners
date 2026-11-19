"""Unit tests for finite-state reward trace in example.py."""

import unittest

import example


class StateChainTests(unittest.TestCase):

    def test_right_right_ends_at_terminal_with_reward_1(self):
        trace, final_state, total_reward, end_reason = example.run_episode_direct(
            0, ["right", "right"]
        )
        self.assertEqual(final_state, 2)
        self.assertEqual(total_reward, 2)
        self.assertEqual(end_reason, "terminal")
        self.assertEqual(len(trace), 2)
        self.assertEqual(trace, [(0, "right", 0, 1), (1, "right", 1, 2)])

    def test_repeated_left_ends_at_step_cap_with_reward_0(self):
        trace, final_state, total_reward, end_reason = example.run_episode_direct(
            0, ["left"] * 10
        )
        self.assertEqual(final_state, 0)
        self.assertEqual(total_reward, 0)
        self.assertEqual(end_reason, "step_cap")
        self.assertEqual(len(trace), 5)

    def test_compare_approaches_right_right(self):
        comparison = example.compare_approaches(0, ["right", "right"])
        self.assertTrue(comparison["match"])
        self.assertEqual(comparison["direct"], (2, 1, "terminal"))
        self.assertEqual(comparison["independent"], (2, 1, "terminal"))

    def test_compare_approaches_repeated_left(self):
        comparison = example.compare_approaches(0, ["left"] * 10)
        self.assertTrue(comparison["match"])
        self.assertEqual(comparison["direct"], (0, 0, "step_cap"))
        self.assertEqual(comparison["independent"], (0, 0, "step_cap"))

    def test_compare_approaches_mixed_actions(self):
        actions = ["right", "left", "right", "right"]
        comparison = example.compare_approaches(0, actions)
        self.assertTrue(comparison["match"])
        self.assertEqual(comparison["direct"], (2, 1, "terminal"))

    def test_wall_at_zero(self):
        next_state, reward, done = example.step(0, "left")
        self.assertEqual((next_state, reward, done), (0, 0, False))

    def test_reward_only_on_entry_into_terminal(self):
        # Stepping into 1 gives 0
        s1, r1, d1 = example.step(0, "right")
        self.assertEqual((s1, r1, d1), (1, 0, False))
        # Stepping from 1 into 2 gives reward 1 and done True
        s2, r2, d2 = example.step(1, "right")
        self.assertEqual((s2, r2, d2), (2, 1, True))

    def test_actions_after_terminal_ignored(self):
        trace, final_state, total_reward, end_reason = example.run_episode_direct(
            0, ["right", "right", "left", "right"]
        )
        self.assertEqual(final_state, 2)
        self.assertEqual(total_reward, 2)
        self.assertEqual(end_reason, "terminal")
        self.assertEqual(len(trace), 2)

    def test_invalid_action_raises(self):
        with self.assertRaises(ValueError):
            example.step(0, "jump")

    def test_invalid_state_raises(self):
        with self.assertRaises(ValueError):
            example.step(3, "left")
        with self.assertRaises(ValueError):
            example.step(-1, "right")


if __name__ == "__main__":
    unittest.main()
