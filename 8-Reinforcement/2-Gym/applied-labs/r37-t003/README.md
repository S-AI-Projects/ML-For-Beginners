# R37-T003: Finite-State Reward Trace - Compare Two Approaches

**Label:** toy three-state chain, not a trained Q-learning or Gym physics agent.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## What It Is

A small, deterministic simulation of a discrete three-state chain:
- States: `0`, `1`, `2` (state `2` is terminal).
- Actions: `"left"` (-1) and `"right"` (+1). Left at state 0 stays at 0 (a wall).
- Reward: `1` only on the transition entering state `2`, otherwise `0`.
- Episode cap: at most 5 steps.

## Comparison of Two Approaches

This lab compares two distinct computational approaches over identical inputs:
1. **Approach A (Direct Simulation):** Step-by-step stateful transition execution via `step(state, action)` recording a transition trace.
2. **Approach B (Independent Calculation & Canonical Table):** Closed-form analytical transition calculator and explicit expected-result lookup table (`EXPECTED_TABLE`).

Both approaches yield identical results across all test cases.

## Invocation

From the repository root:

```bash
python3 8-Reinforcement/2-Gym/applied-labs/r37-t003/example.py
```

Run unit tests from the repository root:

```bash
python3 -m unittest discover -s 8-Reinforcement/2-Gym/applied-labs/r37-t003 -p "test_*.py"
```

## Fixture and Expected Output

Fixture episodes:
- Start 0, actions `["right", "right"]` -> ends at 2, total reward 1, end reason `"terminal"`.
- Start 0, actions `["left"] * 10` -> ends at 0, total reward 0, end reason `"step_cap"`.

Expected CLI output:

```text
toy three-state chain, not a trained Q-learning or Gym physics agent
start 0, actions ['right', 'right']:
  direct: final=2, reward=1, end=terminal
  independent: final=2, reward=1, end=terminal
  approaches agree: True
start 0, actions ['left'] * 10:
  direct: final=0, reward=0, end=step_cap
  independent: final=0, reward=0, end=step_cap
  approaches agree: True
```

## Limitations

- The environment has 3 discrete states; no continuous state physics, pole balancing, or cart dynamics.
- No Q-table, policy network, or reinforcement learning updates.
- Makes no claims about real hardware, cloud services, or trained agent performance.
