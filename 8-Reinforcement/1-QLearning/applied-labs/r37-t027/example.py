"""
r37-t027: Finite-State Reward Trace — Evaluation Experiment
=============================================================
Lesson context: 8-Reinforcement/1-QLearning/README.md
  "Introduction to Reinforcement Learning and Q-Learning"

Simulates a 3-state chain environment with states {0, 1, 2}.
Actions: "left", "right".
Transitions:
  - From state 0:
      "left"  -> remains in state 0 (bounded)
      "right" -> moves to state 1
  - From state 1:
      "left"  -> moves to state 0
      "right" -> moves to state 2
  - State 2 is terminal:
      Reward = 1 only on entry into terminal state 2.
      Any subsequent action in terminal state yields 0 reward and stays in state 2.

Step Cap:
  Episodes are capped at a configurable step cap (default: 5 steps).

Contract Requirements:
- From state 0, action sequence ["right", "right"] ends at state 2 with total reward 1.
- Repeated "left" actions from state 0 end at the step cap with reward 0.
- Compare three small controlled configurations (e.g. step caps 2, 5, 10, or policy variants).
- Report correctness and observed trade-offs without claiming real-world model accuracy.

NOTE: Simulation/mock behavior using small local fixtures.
No model download, paid provider, GPU, or physical device is required.
"""

from typing import Any, Dict, List, Tuple


class ThreeStateChainEnv:
    """Deterministic 3-state environment: states 0, 1, 2 (terminal=2)."""

    def __init__(self, step_cap: int = 5):
        self.step_cap = step_cap
        self.state = 0
        self.steps_taken = 0
        self.done = False

    def reset(self, start_state: int = 0) -> int:
        self.state = start_state
        self.steps_taken = 0
        self.done = False
        return self.state

    def step(self, action: str) -> Tuple[int, int, bool, Dict[str, Any]]:
        """
        Takes an action ('left' or 'right').
        Returns: (next_state, reward, done, info)
        """
        if self.done:
            return self.state, 0, True, {"reason": "already_terminated"}

        self.steps_taken += 1
        prev_state = self.state
        reward = 0

        if action == "right":
            if self.state < 2:
                self.state += 1
        elif action == "left":
            if self.state > 0:
                self.state -= 1
        else:
            raise ValueError(f"Invalid action: '{action}'. Must be 'left' or 'right'.")

        # Reward 1 only on entry into terminal state 2
        if prev_state != 2 and self.state == 2:
            reward = 1
            self.done = True

        if self.steps_taken >= self.step_cap:
            self.done = True

        return self.state, reward, self.done, {
            "steps": self.steps_taken,
            "capped": (self.steps_taken >= self.step_cap and self.state != 2)
        }


def run_episode(actions: List[str], step_cap: int = 5, start_state: int = 0) -> Dict[str, Any]:
    """Runs a sequence of actions in the environment and returns a full trace."""
    env = ThreeStateChainEnv(step_cap=step_cap)
    state = env.reset(start_state=start_state)
    trace = [state]
    rewards = []

    for a in actions:
        if env.done:
            break
        state, r, done, _ = env.step(a)
        trace.append(state)
        rewards.append(r)

    return {
        "final_state": env.state,
        "total_reward": sum(rewards),
        "steps_taken": env.steps_taken,
        "is_terminal": (env.state == 2),
        "state_trace": trace,
        "reward_trace": rewards,
    }


def compare_three_configurations() -> Dict[str, Any]:
    """
    Compares three controlled configurations:
      Config 1: step_cap = 1 (insufficient budget for reaching terminal state from 0)
      Config 2: step_cap = 2 (minimal budget to reach terminal state with optimal policy)
      Config 3: step_cap = 5 (flexible budget allowing sub-optimal exploration)
    """
    action_seq_optimal = ["right", "right"]
    action_seq_exploring = ["right", "left", "right", "right"]
    action_seq_suboptimal = ["left", "left", "left", "left", "left"]

    results = {
        "config_cap_1": {
            "step_cap": 1,
            "optimal_seq": run_episode(action_seq_optimal, step_cap=1),
            "trade_off": "Truncates before reaching terminal state; reward=0; fails on insufficient budget.",
        },
        "config_cap_2": {
            "step_cap": 2,
            "optimal_seq": run_episode(action_seq_optimal, step_cap=2),
            "trade_off": "Succeeds on exact minimal optimal path; reward=1; zero margin for exploration.",
        },
        "config_cap_5": {
            "step_cap": 5,
            "optimal_seq": run_episode(action_seq_optimal, step_cap=5),
            "exploring_seq": run_episode(action_seq_exploring, step_cap=5),
            "looping_seq": run_episode(action_seq_suboptimal, step_cap=5),
            "trade_off": "Tolerates exploratory moves while still capping infinite loops safely at step 5.",
        },
    }
    return results


def run_demo():
    print("=== Finite-State Reward Trace Demo ===")
    ep1 = run_episode(["right", "right"], step_cap=5)
    print(f"Optimal ['right', 'right'] from 0: Final state={ep1['final_state']}, Total reward={ep1['total_reward']}, Steps={ep1['steps_taken']}")
    assert ep1["final_state"] == 2 and ep1["total_reward"] == 1

    ep2 = run_episode(["left"] * 10, step_cap=5)
    print(f"Repeated 'left' from 0: Final state={ep2['final_state']}, Total reward={ep2['total_reward']}, Steps={ep2['steps_taken']}")
    assert ep2["final_state"] == 0 and ep2["total_reward"] == 0 and ep2["steps_taken"] == 5

    print("\n=== Configurations Comparison ===")
    comparison = compare_three_configurations()
    for name, cfg in comparison.items():
        print(f"{name} (cap={cfg['step_cap']}): {cfg['trade_off']}")


if __name__ == "__main__":
    run_demo()
