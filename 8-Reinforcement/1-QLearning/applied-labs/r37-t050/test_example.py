"""Unit tests for the toy three-state chain in example.py."""

import unittest

import example


class ChainTests(unittest.TestCase):

    def test_right_right_reaches_terminal(self):
        trace, final, total, reason = example.run_episode(
            0, ["right", "right"])
        self.assertEqual(trace, [(0, "right", 0, 1), (1, "right", 1, 2)])
        self.assertEqual(final, 2)
        self.assertEqual(total, 1)
        self.assertEqual(reason, "terminal")
        self.assertEqual(len(trace), 2)

    def test_ten_lefts_stop_at_step_cap(self):
        trace, final, total, reason = example.run_episode(0, ["left"] * 10)
        self.assertEqual(len(trace), 5)
        self.assertEqual(final, 0)
        self.assertEqual(total, 0)
        self.assertEqual(reason, "step_cap")

    def test_left_at_zero_stays_at_zero(self):
        self.assertEqual(example.step(0, "left"), (0, 0, False))

    def test_reward_only_when_entering_terminal(self):
        self.assertEqual(example.step(0, "right"), (1, 0, False))
        self.assertEqual(example.step(1, "right"), (2, 1, True))
        self.assertEqual(example.step(1, "left"), (0, 0, False))

    def test_start_at_terminal_takes_no_steps(self):
        self.assertEqual(
            example.run_episode(2, ["left"]), ([], 2, 0, "terminal"))

    def test_terminal_on_step_five_beats_step_cap(self):
        actions = ["left", "right", "left", "right", "right"]
        trace, final, total, reason = example.run_episode(0, actions)
        self.assertEqual(len(trace), 5)
        self.assertEqual(final, 2)
        self.assertEqual(total, 1)
        self.assertEqual(reason, "terminal")

    def test_actions_exhausted_before_cap(self):
        trace, final, total, reason = example.run_episode(0, ["right"])
        self.assertEqual(trace, [(0, "right", 0, 1)])
        self.assertEqual(final, 1)
        self.assertEqual(total, 0)
        self.assertEqual(reason, "actions_exhausted")

    def test_actions_after_end_are_ignored(self):
        trace, final, total, reason = example.run_episode(
            0, ["right", "right", "jump"])
        self.assertEqual(len(trace), 2)
        self.assertEqual(final, 2)
        self.assertEqual(reason, "terminal")

    def test_unknown_action_raises(self):
        with self.assertRaises(ValueError):
            example.step(0, "jump")
        with self.assertRaises(ValueError):
            example.run_episode(0, ["jump"])

    def test_bad_start_state_raises(self):
        with self.assertRaises(ValueError):
            example.run_episode(3, ["right"])
        with self.assertRaises(ValueError):
            example.run_episode(-1, ["right"])
        with self.assertRaises(ValueError):
            example.step(5, "right")


if __name__ == "__main__":
    unittest.main()
