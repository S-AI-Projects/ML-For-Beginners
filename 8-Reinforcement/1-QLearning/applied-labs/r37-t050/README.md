# R37-T050: Finite-state reward trace

**Label:** toy three-state chain, not a trained Q-learning agent.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## What it is

A small, complete example of the lesson's core loop: an agent in a **state** takes an **action**, receives a **reward**, and moves to a next state. An episode stops at a **terminal** state or at a **step cap**. The example records the **trace** of one episode. It does not learn anything. It is a fixture for reading the transition rules, and for checking them with tests.

## Invocation

From the repository root:

```bash
python3 8-Reinforcement/1-QLearning/applied-labs/r37-t050/example.py
```

Run the tests from the repository root:

```bash
python3 -m unittest discover -s 8-Reinforcement/1-QLearning/applied-labs/r37-t050 -p "test_*.py"
```

## Fixture

- States are `0`, `1` and `2`. State `2` is terminal.
- Actions are `"left"` (moves -1) and `"right"` (moves +1).
- Left at state `0` stays at `0` (a wall).
- The reward is `1` only on the step that enters state `2`, otherwise `0`.
- The contract episodes are:
  - start `0`, actions `["right", "right"]`: ends at `2`, total reward `1`, end reason `terminal`, 2 steps.
  - start `0`, actions `["left"] * 10`: stops after exactly 5 steps at `0`, total reward `0`, end reason `step_cap`.

## Expected output

The CLI prints this, byte for byte:

```text
right, right (start 0):
  0 --right--> 1, reward 0
  1 --right--> 2, reward 1
  final 2, total reward 1, end terminal
left x10 (start 0):
  0 --left--> 0, reward 0
  0 --left--> 0, reward 0
  0 --left--> 0, reward 0
  0 --left--> 0, reward 0
  0 --left--> 0, reward 0
  final 0, total reward 0, end step_cap
```

## Rules

- **Transitions:** `right` adds 1, `left` subtracts 1, and the result is clamped to `0..2`.
- **Wall:** `left` at `0` stays at `0`, with reward `0`.
- **Reward on entry:** the reward is `1` only when a step enters state `2`. A step from a state that is not `2` into `2` gives `1`. Every other step gives `0`.
- **Terminal:** once the state is `2`, the episode ends. Actions after that are ignored.
- **Step cap:** at most `max_steps` steps are taken (default `5`).
- **End reasons:** `"terminal"` when the final state is `2`, even if that happens on the last allowed step. `"step_cap"` when `max_steps` steps were taken and the state is not `2`. `"actions_exhausted"` when the actions run out first.
- **Validation:** an unknown action raises `ValueError`. A state outside `0..2` raises `ValueError`, whether it is the start state or an input to `step`.

## Concept map

| Public name | Where it appears | Lesson concept | Source in the lesson |
| --- | --- | --- | --- |
| `state` (`STATES`, `TERMINAL`) | `step` input, `run_episode` start, final state | State: the situation the agent is in | "You being Mario ... at a specific position ... that's your state." |
| `action` (`ACTIONS`) | `step` input, `run_episode` input list | Action: what the agent can do in a state | "...a set of actions per state." |
| `step` | Returns `(next_state, reward, done)` | One interaction: act in a state, get a reward, move on | "By executing an action in a specified state, the agent is given a reward." |
| `reward` | Each `step`, `total_reward` | Reward: the numerical feedback for an action | "...a positive numerical score." |
| `done` | Third value from `step` | Terminal handling: the episode is over | Lesson's stop condition: "until we reach the apple." |
| `run_episode` | Runs actions from a start state | One episode (one experiment) | "...by running many experiments." |
| `trace` | Returned by `run_episode` | The agent's recorded experience: `(state, action, reward, next_state)` per step | The walk path the lesson records while the agent acts. |
| `total reward` | Returned by `run_episode` | The quantity an agent wants to maximize | "...maximize the reward..." |
| `end reason` | Returned by `run_episode` | Why the episode stopped | Lab addition. Not in the lesson. |
| `max_steps` | `run_episode` argument, default `MAX_STEPS = 5` | Step cap: a bounded episode | Lab addition. Not in the lesson. |

## How it illustrates the lesson

It makes the lesson's loop concrete on a board small enough to trace by hand: each step is a state, an action, a reward and a next state, and the trace shows the agent's experience in order. The wall and the terminal state show how transitions end, and the step cap shows a bounded episode.

## Where the simplification stops

- There is no Q-table, no Bellman update, and no learning rate or discount factor.
- There is no policy function. Actions are given as a fixed list.
- There is no exploration. Nothing chooses between actions, so no exploit-versus-explore trade-off appears.
- Transitions are deterministic, with three states and no board like Peter's world.
- The step cap and the end reasons are bookkeeping added for this lab. The lesson does not define them.

## Limitations

- Output shows the rules for this toy chain only. It says nothing about real hardware, cloud services, learning performance or trained-model performance.
- The example runs on the Python 3 standard library only. It needs no model download, paid provider, GPU or device.
- The tests check the example's behavior, not any claim about learning.
