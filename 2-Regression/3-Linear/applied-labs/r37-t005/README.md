# R37-T005: Regression Evaluation - Offline Service Adapter

**Label:** offline service adapter, not a remote cloud metrics service.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## What It Is

A regression metrics evaluation component placed behind a callable service interface (`RegressionEvaluationClient` and `LocalRegressionEvaluatorAdapter`). It computes:
- Mean Absolute Error (MAE): `sum(|y - y_hat|) / n`
- Root Mean Squared Error (RMSE): `sqrt(sum((y - y_hat)^2) / n)`

## Offline Adapter Pattern

The evaluation logic is isolated behind a callable interface adapter. This decouples calling code from third-party or cloud metric service implementations:
- `LocalRegressionEvaluatorAdapter`: Provides in-process, zero-latency deterministic evaluation.
- `RegressionEvaluationClient`: Consumes any adapter conforming to the `callable(truth, prediction)` protocol.

## Real-Service Behavior Not Established by this Mock

- **Network Latency & Jitter:** Network transit delays, socket connect times, and bandwidth throughput constraints.
- **Transient Failures & Retries:** Remote server timeouts, HTTP 503 service unavailable codes, exponential backoff, and retry handling.
- **Authentication & Rate Limits:** API token validation, OAuth token refresh flows, and HTTP 429 quota exhaustion.
- **Distributed Computing:** Server-side batch partitioning and multi-node GPU metric aggregation.

## Invocation

From the repository root:

```bash
python3 2-Regression/3-Linear/applied-labs/r37-t005/example.py
```

Run unit tests from the repository root:

```bash
python3 -m unittest discover -s 2-Regression/3-Linear/applied-labs/r37-t005 -p "test_*.py"
```

## Fixture and Expected Output

Fixture inputs:
- Headline: `truth=[1, 2, 3]`, `prediction=[1, 3, 2]`
- Identical: `truth=[1, 2, 3]`, `prediction=[1, 2, 3]`

Expected CLI output:

```text
offline service adapter, not a remote cloud metrics service
truth=[1, 2, 3], prediction=[1, 3, 2]:
  MAE=0.6667 (expected 2/3 = 0.6667)
  RMSE=0.8165 (expected sqrt(2/3) = 0.8165)
identical arrays [1, 2, 3]:
  MAE=0.0000, RMSE=0.0000
```

## Limitations

- Computes MAE and RMSE on local real-valued sequences; no scikit-learn models or pipelines are trained.
- No network transport, remote socket binding, or RPC protocol is implemented.
- Makes no claims about real hardware, cloud service behavior, or trained model performance.
