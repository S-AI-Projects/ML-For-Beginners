# R37-T032: Confusion matrix, precision and recall (boundary cases)

Standard-library Python only. No model, download, GPU or paid service.

## Run
```
python3 example.py
python3 -m unittest discover -s 4-Classification/3-Classifiers-2/applied-labs/r37-t032 -p "test_*.py"
```

## Fixture and expected output
`y_true=[1,1,0,0]`, `y_pred=[1,0,1,0]` ->
`TP=1 FN=1 FP=1 TN=1`, `precision=0.5 recall=0.5`

## Cases covered
| Kind | Input (y_true, y_pred) | Result |
|---|---|---|
| Smallest valid | `[1]`, `[1]` | TP=1, others 0 |
| Boundary: no positive predictions | `[1,1,0,0]`, `[0,0,0,0]` | precision=0.0 (TP+FP=0) |
| Boundary: no actual positives | `[0,0]`, `[1,0]` | recall=0.0 (TP+FN=0) |
| Invalid | length mismatch, empty, labels not 0/1 (incl. `True`) | `ValueError` |

## Boundary decision
precision = TP/(TP+FP) is 0/0 when the model never predicts positive.
Policy: return **0.0** (not NaN, not an exception). recall = TP/(TP+FN)
follows the same rule. Other libraries may choose differently.

## Limits (simulation)
Labels are hand-written, not from a trained model. This shows how the metrics
are computed, not how any real classifier performs. Argument order is
`(y_true, y_pred)`; swapping them swaps FP and FN. Class balance is not
handled: with very few positives these numbers are unstable.

## Relation to the lesson

The lesson prints a classification report with precision and recall per
cuisine (for example Linear SVC, chinese: precision 0.71, recall 0.67) but
never shows how those numbers are computed. For each cuisine, the report
treats that cuisine as the positive class (1) and all others as negative (0).
This example computes the counts TP, FN, FP and TN for one such binary case
and derives precision and recall from them. Labels are passed as
(y_true, y_pred), the same order as the lesson's y_test and y_pred; swapping
them swaps FN and FP.

## Where the simplification stops

The labels here are hand-written, not predictions from a trained model, so
nothing here says how well a real classifier performs. It handles one
positive class against the rest, while the lesson has five cuisines and
also reports f1-score and accuracy, which are not computed here. Class
balance is not handled: the lesson's test set is roughly balanced (support
227 to 254 per cuisine), but with a rare positive class precision and
recall would be much less stable.
