"""Label: toy three-state chain, not a trained Q-learning agent.

Python 3 standard library and a local checkout. The local fixture is
mandatory; any optional real-service extension needs separately
supplied credentials/hardware and is not part of this task.

Lesson concepts used here: state, action, reward, terminal state (done),
episode, step cap (bounded episode), and trace (the agent's experience).
Run with: python3 example.py
"""

STATES = (0, 1, 2)  # lesson: state, the positions the agent can be in
TERMINAL = 2  # lesson: terminal state, where the episode ends
ACTIONS = {"left": -1, "right": 1}  # lesson: action, moves the agent
MAX_STEPS = 5  # lesson: step cap, the bound on one episode


def _check_state(state):
    if state not in STATES:
        raise ValueError(f"state must be 0, 1 or 2, got {state!r}")


def step(state, action):
    """Apply one action and return (next_state, reward, done).

    Lesson concepts: state transition and reward. Moving left at state 0
    hits a wall and stays at 0. The reward is 1 only on the step that
    enters the terminal state, otherwise 0. done is True when the next
    state is terminal (lesson: terminal handling).
    """
    _check_state(state)
    if action not in ACTIONS:
        raise ValueError(f"unknown action {action!r}")
    next_state = min(max(state + ACTIONS[action], 0), TERMINAL)
    reward = 1 if next_state == TERMINAL and state != TERMINAL else 0
    return next_state, reward, next_state == TERMINAL


def run_episode(start, actions, max_steps=MAX_STEPS):
    """Run one bounded episode over a list of actions.

    Lesson concepts: episode and trace. Returns the trace (one tuple
    (state, action, reward, next_state) per step, the agent's
    experience), the final state, the total reward, and the end reason:
    "terminal", "step_cap" or "actions_exhausted". Actions after the
    episode ends are ignored.
    """
    _check_state(start)
    state, total, trace = start, 0, []
    for action in actions:
        if state == TERMINAL or len(trace) == max_steps:
            break
        next_state, reward, _ = step(state, action)
        trace.append((state, action, reward, next_state))
        total += reward
        state = next_state
    if state == TERMINAL:
        reason = "terminal"
    elif len(trace) == max_steps:
        reason = "step_cap"
    else:
        reason = "actions_exhausted"
    return trace, state, total, reason


def _print_episode(label, start, actions):
    trace, final, total, reason = run_episode(start, actions)
    print(f"{label} (start {start}):")
    for state, action, reward, next_state in trace:
        print(f"  {state} --{action}--> {next_state}, reward {reward}")
    print(f"  final {final}, total reward {total}, end {reason}")


def main():
    """Print the two contract episodes.

    Lesson concepts: a complete bounded episode (terminal reached) and a
    capped episode (step cap reached with no terminal state).
    """
    _print_episode("right, right", 0, ["right", "right"])
    _print_episode("left x10", 0, ["left"] * 10)


if __name__ == "__main__":
    main()
