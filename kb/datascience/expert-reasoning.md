# Data science — expert reasoning layer (how a data-science expert thinks)

The core discipline is skepticism about your own result. Most "findings" are leakage, bias, or noise until proven otherwise.
Teach the habit of trying to break your own conclusion before anyone else does.

## Framing method (before any model)
- Start from the decision the analysis will drive. A number nobody acts on is waste; know the action and its cost of error.
- Define the target and the unit of analysis precisely; most disputes are definitional, not statistical.
- Pick the metric for the business cost, not convenience: imbalanced classes → precision/recall/PR-AUC, not accuracy.

## Validation method (the skill that separates experts)
- Split before you look. Any decision made after seeing the test set contaminates it. Keep a truly held-out set for the end.
- Leakage is the #1 killer: a feature that encodes the target (or the future). Ask of every feature "would I have this at prediction time?"
- Cross-validate to estimate variance, not to pick the lucky fold. Respect structure: time-series → forward chaining; grouped data → group-aware folds.
- A result that vanishes on fresh data was never real. Reproduce end-to-end from raw before believing it.

### Worked case — "our model is 99% accurate!"
- Reflex: suspect leakage or imbalance before celebrating. 99% on a 99:1 class split is the dumb baseline.
- Check: class balance (predict-majority baseline), then feature importances for a feature that smells like the target, then a strict time/group split.
- Common culprit: an ID or timestamp proxy, or preprocessing (scaling/imputation) fit on the whole set before splitting. Refit inside the fold.
- Verify on data from a later period the model never touched; if it holds there, believe it.

## Causal vs correlational
- Observational data answers "associated with", not "causes". Confounders, selection bias, and reverse causation lurk everywhere.
- To claim causation you need an experiment (A/B) or a credible identification strategy — and you name the assumption it rests on.
- A/B: fix the hypothesis, the metric, the sample size and the stopping rule BEFORE running; peeking inflates false positives.

## The meta-rule
An expert reports the uncertainty, not just the point estimate, and states what would change their mind. "p<0.05" without an
effect size, a confidence interval, and a leakage check is not evidence. Calibrated doubt is the expertise.
