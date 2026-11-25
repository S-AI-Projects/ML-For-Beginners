"""Small deterministic chain simulation for the CartPole Gym lesson concepts."""
from __future__ import annotations

import argparse
import json
from typing import Iterable

TERMINAL_STATE = 2
MAX_STEPS = 5


def run_episode(actions: Iterable[str], start_state: int = 0) -> dict[str, object]:
    """Run a three-state mock environment; reward 1 only when entering state 2."""
    if type(start_state) is not int or start_state not in (0, 1, TERMINAL_STATE):
        raise ValueError("start_state must be 0, 1, or terminal state 2")
    state = start_state
    total_reward = 0
    trace = [state]
    action_list = list(actions)
    if len(action_list) > MAX_STEPS:
        raise ValueError("at most five actions are allowed")
    if any(action not in ("left", "right") for action in action_list):
        raise ValueError("actions must be 'left' or 'right'")
    for action in action_list:
        if state == TERMINAL_STATE:
            break
        state = max(0, min(TERMINAL_STATE, state + (1 if action == "right" else -1)))
        reward = int(state == TERMINAL_STATE)
        total_reward += reward
        trace.append(state)
        if state == TERMINAL_STATE:
            break
    return {"final_state": state, "total_reward": total_reward, "steps": len(trace) - 1,
            "terminated": state == TERMINAL_STATE, "trace": trace}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a deterministic three-state mock episode.")
    parser.add_argument("actions", nargs="*", choices=("left", "right"), help="actions, up to five")
    args = parser.parse_args()
    print(json.dumps(run_episode(args.actions), sort_keys=True))


if __name__ == "__main__":
    main()
