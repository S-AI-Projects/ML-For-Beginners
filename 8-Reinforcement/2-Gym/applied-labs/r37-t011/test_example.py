import unittest

from example import run_episode


class EpisodeTests(unittest.TestCase):
    def test_right_right_reaches_terminal_with_entry_reward(self):
        self.assertEqual(run_episode(["right", "right"]), {
            "final_state": 2, "total_reward": 1, "steps": 2,
            "terminated": True, "trace": [0, 1, 2]})

    def test_left_repeats_to_step_cap_without_reward(self):
        self.assertEqual(run_episode(["left"] * 5), {
            "final_state": 0, "total_reward": 0, "steps": 5,
            "terminated": False, "trace": [0, 0, 0, 0, 0, 0]})

    def test_stops_when_terminal_is_entered(self):
        self.assertEqual(run_episode(["right", "right", "left"])["steps"], 2)

    def test_empty_episode_is_bounded_at_zero_steps(self):
        self.assertEqual(run_episode([]), {
            "final_state": 0, "total_reward": 0, "steps": 0,
            "terminated": False, "trace": [0]})

    def test_left_clamps_at_zero_and_reward_is_only_on_entry(self):
        self.assertEqual(run_episode(["left", "right", "right"]), {
            "final_state": 2, "total_reward": 1, "steps": 3,
            "terminated": True, "trace": [0, 0, 1, 2]})

    def test_terminal_start_takes_no_actions(self):
        self.assertEqual(run_episode(["left"], start_state=2), {
            "final_state": 2, "total_reward": 0, "steps": 0,
            "terminated": True, "trace": [2]})

    def test_invalid_action_fails(self):
        with self.assertRaises(ValueError):
            run_episode(["up"])

    def test_more_than_five_actions_fails(self):
        with self.assertRaises(ValueError):
            run_episode(["left"] * 6)

    def test_invalid_start_state_fails(self):
        with self.assertRaises(ValueError):
            run_episode([], start_state=3)


if __name__ == "__main__":
    unittest.main()
