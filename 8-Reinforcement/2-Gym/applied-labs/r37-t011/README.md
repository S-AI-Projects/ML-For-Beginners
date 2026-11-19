# Bounded state-chain example

This deterministic **simulation/mock** connects the lesson's state/action/reward/terminal loop to a minimal local fixture. The states are 0, 1, and terminal 2; `left` and `right` move one position and clamp at either end. Reward is 1 only when a transition enters 2. An episode stops at terminal or after five actions.

Prerequisite: Python 3 standard library and a local repository checkout. No Gym installation or external service is used.

From the repository root:

```sh
python3 8-Reinforcement/2-Gym/applied-labs/r37-t011/example.py right right
```

Expected output:

```json
{"final_state": 2, "steps": 2, "terminated": true, "total_reward": 1, "trace": [0, 1, 2]}
```

Bounded episode:

```sh
python3 8-Reinforcement/2-Gym/applied-labs/r37-t011/example.py left left left left left
```

Expected output:

```json
{"final_state": 0, "steps": 5, "terminated": false, "total_reward": 0, "trace": [0, 0, 0, 0, 0, 0]}
```

The trace represents the observations after each transition, including the initial state. This teaches bounded episode control and entry-based terminal reward only; it does not simulate CartPole physics, continuous observations, learning, or device behavior.
