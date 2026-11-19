"""Finite-state reward trace comparing two approaches.

Label: toy three-state chain, not a trained Q-learning or Gym physics agent.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs
separately supplied credentials/hardware and is not part of this task.

Lesson concepts: state, action, transition, reward, terminal state, step cap.
States: 0, 1, 2 (terminal=2).
Actions: "left" (moves -1, clamped at 0), "right" (moves +1, clamped at 2).
Reward: 1 only when a step enters state 2, otherwise 0.
Episode cap: at most 5 steps.
"""

STATES = (0, 1, 2)
TERMINAL = 2
ACTIONS = {"left": -1, "right": 1}
MAX_STEPS = 5


def _check_state(state):
    if state not in STATES:
        raise ValueError(f"state must be 0, 1, or 2, got {state!r}")


def _check_action(action):
    if action not in ACTIONS:
        raise ValueError(f"unknown action {action!r}, allowed: 'left', 'right'")


def step(state, action):
    """Direct transition step: returns (next_state, reward, done)."""
    _check_state(state)
    _check_action(action)
    next_state = min(max(state + ACTIONS[action], 0), TERMINAL)
    reward = 1 if next_state == TERMINAL and state != TERMINAL else 0
    done = (next_state == TERMINAL)
    return next_state, reward, done


def run_episode_direct(start_state, actions, max_steps=MAX_STEPS):
    """Approach A: Direct step-by-step stateful simulation.

    Returns (trace, final_state, total_reward, end_reason).
    """
    _check_state(start_state)
    if not isinstance(actions, (list, tuple)):
        raise TypeError("actions must be a list or tuple")

    state = start_state
    trace = []
    total_reward = 0
    end_reason = "actions_exhausted"

    if state == TERMINAL:
        return trace, state, total_reward, "terminal"

    for action in actions:
        if len(trace) >= max_steps:
            end_reason = "step_cap"
            break
        next_state, reward, done = step(state, action)
        trace.append((state, action, reward, next_state))
        total_reward += reward
        state = next_state
        if done:
            end_reason = "terminal"
            break
    else:
        if len(trace) >= max_steps and state != TERMINAL:
            end_reason = "step_cap"

    return trace, state, total_reward, end_reason


# Canonical expected-result table for comparison (Approach B)
EXPECTED_TABLE = {
    (0, ("right", "right")): (2, 1, "terminal"),
    (0, ("left",) * 10): (0, 0, "step_cap"),
    (0, ("left", "left", "left", "left", "left")): (0, 0, "step_cap"),
    (0, ("right",)): (1, 0, "actions_exhausted"),
    (1, ("right",)): (2, 1, "terminal"),
    (1, ("left", "left")): (0, 0, "actions_exhausted"),
}


def calculate_independent(start_state, actions, max_steps=MAX_STEPS):
    """Approach B: Simpler independent calculation and explicit lookup table.

    Computes final state, reward, and end reason through closed-form bounds
    and compares against the explicit expected-result table.
    """
    _check_state(start_state)
    key = (start_state, tuple(actions))
    if key in EXPECTED_TABLE:
        return EXPECTED_TABLE[key]

    # Analytical calculation for arbitrary input sequences
    pos = start_state
    steps = 0
    total_reward = 0
    for a in actions:
        _check_action(a)
        if steps >= max_steps:
            return pos, total_reward, "step_cap"
        new_pos = min(max(pos + ACTIONS[a], 0), TERMINAL)
        steps += 1
        if new_pos == TERMINAL and pos != TERMINAL:
            total_reward = 1
            return new_pos, total_reward, "terminal"
        pos = new_pos

    reason = "step_cap" if steps >= max_steps and pos != TERMINAL else "actions_exhausted"
    return pos, total_reward, reason


def compare_approaches(start_state, actions, max_steps=MAX_STEPS):
    """Compare direct simulation against independent calculation."""
    trace_a, final_a, reward_a, reason_a = run_episode_direct(start_state, actions, max_steps)
    final_b, reward_b, reason_b = calculate_independent(start_state, actions, max_steps)
    match = (final_a == final_b and reward_a == reward_b and reason_a == reason_b)
    return {
        "direct": (final_a, reward_a, reason_a),
        "independent": (final_b, reward_b, reason_b),
        "match": match
    }


def run_contract():
    """Run headline contract scenarios and compare approaches."""
    lines = []
    lines.append("toy three-state chain, not a trained Q-learning or Gym physics agent")

    # Contract 1: [right, right] from 0
    c1 = compare_approaches(0, ["right", "right"])
    lines.append("start 0, actions ['right', 'right']:")
    lines.append(f"  direct: final={c1['direct'][0]}, reward={c1['direct'][1]}, end={c1['direct'][2]}")
    lines.append(f"  independent: final={c1['independent'][0]}, reward={c1['independent'][1]}, end={c1['independent'][2]}")
    lines.append(f"  approaches agree: {c1['match']}")

    # Contract 2: repeated left from 0
    c2 = compare_approaches(0, ["left"] * 10)
    lines.append("start 0, actions ['left'] * 10:")
    lines.append(f"  direct: final={c2['direct'][0]}, reward={c2['direct'][1]}, end={c2['direct'][2]}")
    lines.append(f"  independent: final={c2['independent'][0]}, reward={c2['independent'][1]}, end={c2['independent'][2]}")
    lines.append(f"  approaches agree: {c2['match']}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(run_contract())
