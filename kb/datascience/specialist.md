# Data science — specialist layer (the statistics models get wrong)

The precise definitions and fallacies that trip up both people and language models.

## p-values and significance (most-misstated topic in stats)
- A p-value is **P(data at least this extreme | null hypothesis true)** — NOT the probability the null is true, and
  NOT the probability your result is due to chance. Models state this wrong constantly.
- p < 0.05 is an arbitrary convention, not a law. "Not significant" ≠ "no effect" (could be low power).
- **Multiple comparisons**: testing 20 hypotheses at α=0.05 yields ~1 false positive by chance. Correct with
  Bonferroni (conservative) or Benjamini–Hochberg FDR. p-hacking = trying until something is "significant".
- Statistical significance ≠ practical importance; always report effect size and confidence intervals.

## Causation
- Correlation ≠ causation; a confounder can drive both variables. RCTs establish causation by randomisation.
- **Simpson's paradox**: a trend in subgroups can reverse when combined — aggregation can lie.
- **Base-rate fallacy**: a 99%-accurate test for a 1-in-1000 condition yields mostly false positives (PPV ≈ 9%).
- Selection/survivorship bias: conclusions from a non-random sample (e.g. only survivors) are invalid.

## Modelling pitfalls
- **Data leakage** is the #1 cause of "amazing" models that fail in production: fitting scalers/encoders on the full
  dataset, using future information, or target leakage. Fit only on training folds.
- Cross-validation must respect structure: use **time-series split** for temporal data (no shuffling), group-k-fold
  when rows share an entity. Random k-fold on time series leaks the future.
- **Accuracy misleads on imbalanced data** — a 99%-negative dataset scores 99% by predicting "negative" always. Use
  precision/recall/F1, and PR-AUC over ROC-AUC when positives are rare. Check probability calibration, not just ranking.
- Bias–variance: underfit (high bias) vs overfit (high variance); regularisation, more data, or simpler models fix
  overfitting. More features ≠ better (curse of dimensionality).

## Misconceptions to reject
- "Correlation of 0 means independent" — only for linear relationships; non-linear dependence can have r≈0.
- "Big data fixes bias" — a large biased sample is still biased, just more confidently wrong.

## Sources
- "An Introduction to Statistical Learning" (free) — https://www.statlearning.com/ ; ASA statement on p-values.
- "The Elements of Statistical Learning" — https://hastie.su.domains/ElemStatLearn/
