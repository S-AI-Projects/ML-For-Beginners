# Bounded conversation memory: worked example with checks

Label: local teaching fixture, not a real chat-model memory implementation

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## What this lab is

This lab is **not ARIMA** and does **no forecasting**. It is a small standalone analogy for ordered observations kept in a fixed-size window: a bounded memory that stores at most three string records, oldest first, and hands callers a copy of what it holds.

## Exact invocation

Run from the repository root:

```bash
python3 7-TimeSeries/2-ARIMA/applied-labs/r37-t043/example.py
python3 -m unittest discover -s 7-TimeSeries/2-ARIMA/applied-labs/r37-t043 -p "test_*.py"
```

## Fixture

- `BoundedMemory` in `example.py` has a fixed capacity of 3 (`CAPACITY = 3`).
- `add(record)` appends a record; if the memory then holds more than 3, the oldest record is removed.
- `records()` returns a new list (a shallow copy) of the stored records.
- Records are plain strings in this fixture.

## Retention policy, order and ownership

- **Retention:** at most 3 records. Adding a 4th evicts only the oldest.
- **Order:** arrival order, oldest first.
- **Ownership:** `records()` returns a shallow copy. Callers can append, remove or clear their copy without changing the stored memory.
- **Limitation:** because the records are immutable strings, the copy fully protects the memory. If records were mutable objects, a caller could still change an object it reached through the copy. This lab does not deep-copy, and that limitation is intentional for this fixture.

## Worked example: input to output

The table follows the same steps as the CLI. Stored memory is shown after each step.

| Step | Input | Stored memory after step | Note |
| --- | --- | --- | --- |
| 1 | add `A` | `[A]` | |
| 2 | add `B` | `[A,B]` | |
| 3 | add `C` | `[A,B,C]` | Exactly 3 records; nothing evicted |
| 4 | add `D` | `[B,C,D]` | `A` (the oldest) is evicted |
| 5 | take the returned list, then append `X`, remove `B`, clear it | `[B,C,D]` | The returned copy becomes `[]`; stored memory is unchanged |

Expected output of `example.py` (exactly what the CLI prints):

```text
add A -> [A]
add B -> [A,B]
add C -> [A,B,C]
add D -> [B,C,D]
mutate returned list -> copy []
stored memory -> [B,C,D]
```

## Checks

`test_example.py` covers:

- the worked example above (A, B, C, D, then mutation of the copy) gives `["B", "C", "D"]`;
- an empty memory returns `[]`;
- 1 to 3 records are retained in order;
- exactly 3 records evict nothing;
- a 4th record evicts only the oldest;
- a longer stream keeps only the last 3;
- appending, removing or clearing the returned list leaves the stored memory unchanged;
- two calls return independent copies;
- arrival order is preserved.

## How this relates to the lesson

The lesson text says autoregressive models "look 'back' in time to analyze previous values in your data", and that these previous values are called lags. This lab shares that one idea: it looks at ordered past values in arrival order.

The lesson text does not talk about fixed-size windows. The "keep only the last three" rule is therefore a standalone analogy, not something the lesson teaches.

## Where the simplifications stop

- No values, timestamps or statistics are stored. Records are just strings.
- There is no differencing, no fitting, and no forecasting. ARIMA is not implemented.
- Capacity is fixed at 3, with no configuration and no input validation beyond the stated contract.
- The copy is shallow. Deep copying or immutable containers would be needed for mutable records.
- This is a local teaching fixture, not a real chat-model memory implementation. It says nothing about real chat models, real hardware, cloud services or trained-model performance.
