# R37-T039: Comparing three token budgets on the same text

Standard-library Python only. No model, download, GPU or paid service.

**Teaching approximation:** tokens are the pieces of `str.split()`. This is
NOT the tokenizer of any real model; real tokenizers use sub-word pieces, so
real token counts differ.

## Run
```
python3 6-NLP/1-Introduction-to-NLP/applied-labs/r37-t039/example.py
python3 -m unittest discover -s 6-NLP/1-Introduction-to-NLP/applied-labs/r37-t039 -p "test_*.py"
```

## Contract
Budget 3 with `"one two three four"` retains `['one', 'two', 'three']` and
removes 1 token. Empty input retains none. A negative budget raises
`ValueError`.

## Experiment: three budgets, one fixed text
Text: `"the room was clean and quiet"` (6 whitespace tokens). Budgets 2, 4, 8.

```text
contract: retained=['one', 'two', 'three'] removed_count=1 truncated=True
text='the room was clean and quiet' (whitespace tokens: teaching approximation)
budget retained removed coverage budget_used
2 2 4 0.333 1.000
4 4 2 0.667 1.000
8 6 0 1.000 0.750
```

Metrics: `retained` (tokens kept, a stand-in for cost), `removed`,
`coverage` = retained / total tokens (1.0 for empty text), and
`budget_used` = retained / budget (0.0 when budget is 0).

## Correctness and observed trade-off
- Correctness: the tests check the exact rows above, that retained tokens are
  always the first ones in order, and that retained + removed = total.
- Trade-off: a smaller budget keeps fewer tokens (less to process) but lowers
  coverage (budget 2 keeps a third of the text). A budget larger than the
  text (8) removes nothing but leaves 25% of the budget unused. The tests
  confirm coverage never decreases as the budget grows.

## Limits (simulation)
One fixed hand-written text, whitespace tokens and made-up budgets. The
numbers show how the calculation behaves, not real model token counts,
costs, speed or accuracy.
