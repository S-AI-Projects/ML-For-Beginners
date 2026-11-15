# R37-T037: Worked example of a confusion matrix, precision and recall

Standard-library Python only. No model, download, GPU or paid service.

## Run
```
python3 4-Classification/1-Introduction/applied-labs/r37-t037/example.py
python3 -m unittest discover -s 4-Classification/1-Introduction/applied-labs/r37-t037 -p "test_*.py"
```

## Worked example: input to output
Input: `y_true=[1,1,0,0]`, `y_pred=[1,0,1,0]` (1 = positive, 0 = negative;
argument order is always `(y_true, y_pred)`).

1. Compare each pair: a true 1 predicted 1 is **TP**, a true 1 predicted 0 is
   **FN**, a true 0 predicted 1 is **FP**, a true 0 predicted 0 is **TN**.
2. Count: TP=1, FN=1, FP=1, TN=1.
3. precision = TP / (TP + FP) = 1 / 2 = 0.5
4. recall = TP / (TP + FN) = 1 / 2 = 0.5

Exact output of `example.py` (this block is checked by the regression test):

```text
y_true=[1, 1, 0, 0] y_pred=[1, 0, 1, 0]
sample true pred outcome
1 1 1 TP
2 1 0 FN
3 0 1 FP
4 0 0 TN
TP=1 FN=1 FP=1 TN=1
precision=TP/(TP+FP)=1/2=0.5
recall=TP/(TP+FN)=1/2=0.5
```

## Zero-denominator policy
If the classifier never predicts positive, TP + FP = 0 and precision would be
0/0. Policy: return **0.0**. Recall follows the same rule when there are no
actual positives (TP + FN = 0). Example: `y_true=[1,1,0,0]`,
`y_pred=[0,0,0,0]` gives precision=0.0, recall=0.0.

## Regression test
`test_example.py` runs this exact example in a fresh process and requires its
output to equal the block above, and the block above to equal the README's.
Changing the code, or the README text, makes the test fail.

## Limits (simulation)
Labels are hand-written, not from a trained model, so this shows how the
numbers are computed, not how any real classifier performs. It handles one
positive class against the rest. Class balance is not handled: with very few
positives these numbers are unstable.
