# Token-budget preflight lab (R37-T041)

Checks a prompt's length against a configured budget and reports retained tokens and truncation explicitly.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## Invocation

From the repository root:

```bash
python3 6-NLP/3-Translation-Sentiment/applied-labs/r37-t041/example.py
python3 -m unittest discover -s 6-NLP/3-Translation-Sentiment/applied-labs/r37-t041 -p "test_*.py"
```

## Fixture

- Input: `"one two three four"`, budget `3`.

## Expected output

```text
tokenizer: whitespace split (teaching approximation, not a model tokenizer)
input: 'one two three four'
budget: 3
retained: ['one', 'two', 'three']
removed_count: 1
truncated: True
```

## Boundary decision

The first `budget` tokens are kept and the rest are removed.

- Exact fit (4 tokens, budget 4): not truncated, nothing removed.
- Budget 0: keeps no tokens; every token is removed.
- Empty input: nothing retained, nothing removed, not truncated.
- Negative budget: `ValueError`.

## Scope

Teaching only. It shows the budget and truncation logic with a deterministic fixture.

## Limitations

- Tokens are whitespace-separated words, a **teaching approximation**. It is not the tokenizer of any real model, so counts will differ from a production model.
- No model download, paid provider, GPU or physical device is used.
- No claim is made about real hardware, cloud-service behaviour or trained-model performance.
- The budget is not type-checked (for example, a float budget is not rejected).
