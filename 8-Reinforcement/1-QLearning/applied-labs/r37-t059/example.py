"""
R37-T059: Finite-State Reward Trace & Scenario Assessment
Simulates a three-state chain with actions left/right, terminal state 2,
and reward 1 only on entry into terminal; caps an episode at 5 steps.
"""

from typing import List, Dict, Any, Tuple


class ThreeStateChainEnv:
    """
    Three-state chain environment (states 0, 1, 2).
    - States: 0 (start), 1, 2 (terminal)
    - Actions: 'left', 'right'
    - Transitions:
        'left' at state 0 stays at 0 (clamped boundary)
        'left' at state 1 moves to 0
        'right' at state 0 moves to 1
        'right' at state 1 moves to 2 (terminal)
    - Reward: 1 only upon entering terminal state 2, 0 otherwise
    - Step cap: 5 steps maximum per episode
    """

    def __init__(self, max_steps: int = 5, start_state: int = 0):
        self.max_steps = max_steps
        self.start_state = start_state
        self.state = start_state
        self.step_count = 0
        self.done = False

    def reset(self) -> int:
        self.state = self.start_state
        self.step_count = 0
        self.done = False
        return self.state

    def step(self, action: str) -> Tuple[int, int, bool, Dict[str, Any]]:
        if self.done:
            return self.state, 0, True, {"reason": "already_terminated"}

        action = action.strip().lower()
        if action not in ("left", "right"):
            raise ValueError(f"Invalid action: {action}. Must be 'left' or 'right'.")

        self.step_count += 1
        prev_state = self.state

        if action == "right":
            next_state = min(2, prev_state + 1)
        elif action == "left":
            next_state = max(0, prev_state - 1)
        else:
            next_state = prev_state

        reward = 1 if (prev_state != 2 and next_state == 2) else 0

        if next_state == 2:
            self.done = True
            reason = "terminal_state_reached"
        elif self.step_count >= self.max_steps:
            self.done = True
            reason = "step_cap_exceeded"
        else:
            reason = "in_progress"

        self.state = next_state
        info = {
            "step": self.step_count,
            "prev_state": prev_state,
            "action": action,
            "next_state": next_state,
            "reward": reward,
            "reason": reason,
        }
        return next_state, reward, self.done, info

    def run_episode(self, actions: List[str]) -> Dict[str, Any]:
        self.reset()
        trace = []
        total_reward = 0

        for act in actions:
            if self.done:
                break
            nxt, rew, done, info = self.step(act)
            total_reward += rew
            trace.append(info)

        return {
            "start_state": self.start_state,
            "final_state": self.state,
            "total_reward": total_reward,
            "step_count": self.step_count,
            "terminated_by_goal": (self.state == 2),
            "terminated_by_cap": (self.step_count >= self.max_steps and self.state != 2),
            "done": self.done,
            "trace": trace,
        }


# ==============================================================================
# Applied Questions: Scenario Assessment & Executable Checks
# ==============================================================================

APPLIED_QUESTIONS = {
    "Q1_predict_output": {
        "question": "What is the final state, step count, and total reward when executing ['right', 'right'] from state 0?",
        "expected_answer": {
            "final_state": 2,
            "step_count": 2,
            "total_reward": 1,
            "terminated_by_goal": True,
        },
        "rationale": (
            "From state 0, the first 'right' transitions to state 1 (reward 0). "
            "The second 'right' transitions from state 1 to terminal state 2, awarding reward 1 "
            "and ending the episode after 2 steps."
        ),
    },
    "Q2_diagnose_failure": {
        "question": "Why does an agent executing repeated 'left' actions from state 0 fail to collect any reward?",
        "expected_diagnosis": "clamped_boundary_timeout",
        "rationale": (
            "At state 0, executing 'left' clamps the agent at state 0 without progress. "
            "Because the terminal state is 2, the agent remains at state 0 until the 5-step cap is "
            "exhausted, terminating with 0 reward and terminated_by_cap=True."
        ),
    },
    "Q3_boundary_policy": {
        "question": "Which boundary policy prevents teleportation and ensures deterministic state transitions at state 0?",
        "valid_policy": "clamp_at_zero",
        "rationale": (
            "Clamping state transitions (max(0, state - 1)) ensures state invariants are preserved "
            "without illegal wrap-arounds into terminal reward states or undefined state spaces."
        ),
    },
}


def check_q1_prediction(predicted: Dict[str, Any]) -> bool:
    """Verifies that predicted output matches actual simulation of ['right', 'right']."""
    env = ThreeStateChainEnv()
    result = env.run_episode(["right", "right"])
    expected = APPLIED_QUESTIONS["Q1_predict_output"]["expected_answer"]

    for k, v in expected.items():
        if predicted.get(k) != v:
            return False
        if result.get(k) != v:
            return False
    return True


def check_q2_diagnosis(actions: List[str]) -> Tuple[bool, str]:
    """
    Executes an action sequence and verifies failure diagnosis
    (e.g., clamped boundary timeout vs goal termination).
    """
    env = ThreeStateChainEnv()
    result = env.run_episode(actions)

    if result["total_reward"] == 0 and result["terminated_by_cap"] and result["final_state"] == 0:
        return True, "clamped_boundary_timeout"
    elif result["terminated_by_goal"]:
        return False, "goal_reached_not_failure"
    else:
        return False, "unknown_termination"


def check_q3_boundary_policy(policy_name: str) -> bool:
    """Checks whether chosen boundary policy satisfies state safety."""
    valid_policies = {"clamp_at_zero"}
    return policy_name in valid_policies


if __name__ == "__main__":
    env = ThreeStateChainEnv()
    res1 = env.run_episode(["right", "right"])
    print("Normal run ['right', 'right']:", res1)
    res2 = env.run_episode(["left"] * 5)
    print("Repeated left run:", res2)
