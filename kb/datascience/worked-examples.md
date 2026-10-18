# Data science — worked examples (mentor-curated, round 3: reasoning by example)

Method: restate → retrieve facts → reason in steps → check → concise answer.

## Example 1 — "Our fraud model is 98% accurate. Is it good?"
- Restate: judge a fraud classifier reported only by accuracy.
- Facts (foundations › model evaluation; advanced.md › Evaluation): on imbalanced data accuracy misleads; use precision/recall/F1/PR-AUC.
- Steps:
  1. Fraud is rare — say 2% of transactions. A model that labels everything "legit" is 98% accurate and catches zero fraud.
  2. So accuracy alone tells us almost nothing here; the classes are imbalanced.
  3. Ask for precision (of flagged, how many were fraud) and recall (of actual fraud, how much was caught), plus PR-AUC; choose the threshold by the cost of a miss vs a false alarm.
- Check: the reasoning shows why 98% can be worthless; recommends the right metrics; matches the KB.
- Answer: Not necessarily — with rare fraud, 98% accuracy can mean it catches nothing. Judge it on precision, recall and PR-AUC, and set the threshold by the business cost of misses vs false alarms.

## Example 2 — "The model scores great in training but poorly on new data. Why, and what do I do?"
- Restate: diagnose and fix a train-vs-new-data performance gap.
- Facts (advanced.md › Machine learning theory): overfitting; bias–variance; regularisation, cross-validation, more data.
- Steps:
  1. A large train-good / test-bad gap is overfitting (high variance) — the model memorised noise.
  2. Fixes: regularise (L1/L2), reduce model complexity, get more/representative data, use early stopping.
  3. Validate honestly with cross-validation; ensure no leakage (fit scalers/encoders on training folds only).
- Check: symptom (gap) → named cause (overfitting) → standard remedies; consistent with the KB.
- Answer: It's overfitting. Add regularisation, simplify the model or add data, use cross-validation, and check for leakage — then re-evaluate on a held-out set.
