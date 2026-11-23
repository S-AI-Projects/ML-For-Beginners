# Applied Lab R37-T059: Finite-State Reward Trace & Scenario Assessment

## Overview
This applied lab extends [Introduction to Reinforcement Learning and Q-Learning](../../README.md) by introducing a minimal, deterministic 3-state Markov chain environment with bounded episodes, explicit terminal handling, and applied scenario assessments.

## Environment Specification
- **State Space**: $S = \{0, 1, 2\}$, starting at state $s_0 = 0$.
- **Terminal State**: $s = 2$. Reaching state 2 terminates the episode immediately.
- **Action Space**: $A = \{\text{'left'}, \text{'right'}\}$.
- **Transitions**:
  - `right`: $\min(2, s + 1)$
  - `left`: $\max(0, s - 1)$ (clamped lower boundary at state 0)
- **Reward Function**:
  $$R(s, a, s') = \begin{cases} 1 & \text{if } s \neq 2 \text{ and } s' = 2 \\ 0 & \text{otherwise} \end{cases}$$
- **Episode Cap**: Maximum 5 steps per episode.

## Scenarios
1. **Goal Path (`['right', 'right']`)**:
   - $0 \xrightarrow{\text{right}} 1$ (reward 0) $\xrightarrow{\text{right}} 2$ (reward 1, terminal).
   - Terminates in 2 steps with total reward 1 (`terminated_by_goal=True`).
2. **Boundary Timeout (`['left'] * 5`)**:
   - Stays clamped at state 0 for 5 consecutive steps.
   - Terminates at step cap 5 with total reward 0 (`terminated_by_cap=True`).

## Applied Scenario Assessment Questions
1. **Predict Output**: What are the final state, step count, and total reward when executing `['right', 'right']` from state 0?
   - *Rationale & Expected*: State 2, 2 steps, total reward 1. Verified via `check_q1_prediction()`.
2. **Diagnose Failure**: Why does executing repeated `left` actions from state 0 yield 0 reward?
   - *Rationale & Diagnosis*: The agent is clamped at state 0 and exhausts the 5-step cap before reaching state 2. Verified via `check_q2_diagnosis()`.
3. **Choose Boundary Policy**: How should transitions below 0 be handled?
   - *Rationale & Policy*: `clamp_at_zero` enforces bounded Markov state invariants without illegal wrap-around or undefined states. Verified via `check_q3_boundary_policy()`.

## Scope and Limitations
- Pure Python 3 standard library simulation (no external dependencies, GPU, or cloud API required).
- Deterministic transitions designed for exact trace analysis and unit verification.

## Testing & Verification
Execute the test suite:
```bash
python3 -m unittest discover -s 8-Reinforcement/1-QLearning/applied-labs/r37-t059 -p "test_*.py" -v
```
Expected output:
```text
Ran 8 tests in 0.000s
OK
```
