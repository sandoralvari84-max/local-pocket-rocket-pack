# Data science / ML — advanced / academic layer (mentor-curated, round 2)

Builds on data-science-101.md.

## Statistical inference
- Frequentist vs Bayesian: p-values and confidence intervals vs posterior distributions and credible intervals; priors.
- Estimation: maximum likelihood (MLE), method of moments; bias, variance, consistency, efficiency of estimators.
- Testing pitfalls: a p-value is P(data | H0), not P(H0); multiple-comparisons inflation (Bonferroni, FDR/Benjamini–Hochberg); statistical power and required sample size; effect size vs significance.

## Experimental & causal
- RCTs are the gold standard for causation; randomisation balances confounders.
- Observational causal inference: confounding, colliders, DAGs; approaches — matching, propensity scores, difference-in-differences, instrumental variables, regression discontinuity.
- "Correlation ≠ causation"; Simpson's paradox; selection and survivorship bias.

## Machine learning theory
- Bias–variance decomposition; underfitting vs overfitting; regularisation L1 (sparse/Lasso) and L2 (Ridge); early stopping.
- Optimisation: gradient descent (batch/stochastic/mini-batch), learning rate, convexity; loss functions per task.
- Validation: k-fold, stratified, time-series (no leakage from future); nested CV for model selection + evaluation.
- Ensembles: bagging (random forests) reduces variance; boosting (gradient boosting) reduces bias; stacking.

## Deep learning
- Backpropagation and the chain rule; architectures — CNNs (vision), RNN/LSTM (sequence), Transformers (attention, now dominant).
- Regularisation: dropout, batch/layer norm, data augmentation, weight decay; vanishing/exploding gradients.
- Transfer learning and fine-tuning; watch compute, data needs and overfitting on small sets.

## Evaluation & ethics
- Imbalanced data: use precision/recall, F1, PR-AUC, not accuracy; calibration of probabilities.
- Fairness: disparate impact, group vs individual fairness, trade-offs; document data lineage and limitations (model cards, datasheets).
- MLOps: reproducibility, feature stores, monitoring for data/concept drift, versioning.

## Sources (authoritative)
- "An Introduction to Statistical Learning" (ISLR, free) — https://www.statlearning.com/
- "The Elements of Statistical Learning" (ESL, free) — https://hastie.su.domains/ElemStatLearn/
- scikit-learn user guide — https://scikit-learn.org/stable/user_guide.html
- Google ML Crash Course — https://developers.google.com/machine-learning
