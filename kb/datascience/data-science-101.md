# Data science — 101 (mentor-curated seed, round 1)

## Statistics foundations
- Descriptive: mean, median, mode, variance, standard deviation, percentiles.
- Distributions: normal, binomial, Poisson; the Central Limit Theorem underlies much inference.
- Inference: hypothesis tests, p-values, confidence intervals; a p-value is not the probability the hypothesis is true.
- Correlation is not causation; watch for confounders and selection bias.

## Machine learning types
- Supervised: learn from labelled data — regression (continuous) and classification (categories).
- Unsupervised: find structure — clustering (k-means), dimensionality reduction (PCA).
- Reinforcement: learn by reward from interacting with an environment.

## Common algorithms
- Linear & logistic regression; decision trees; random forests; gradient boosting (XGBoost/LightGBM).
- k-nearest neighbours; support vector machines; k-means; neural networks for complex/large data.
- Start simple (a baseline) before reaching for complex models.

## Model evaluation
- Split train/validation/test; use cross-validation; never evaluate on data used for training.
- Classification metrics: accuracy, precision, recall, F1, ROC-AUC (accuracy misleads on imbalanced data).
- Regression metrics: MAE, RMSE, R².
- Bias–variance trade-off: underfitting (too simple) vs overfitting (memorising noise); use regularisation.

## Data pipeline
- Collect → clean (missing values, outliers, types) → explore (EDA) → feature engineering → model → evaluate → deploy → monitor.
- Most effort is cleaning and preparation; garbage in, garbage out.
- Prevent leakage: fit scalers/encoders on training data only.

## Ethics
- Bias in data produces biased models; test across groups; document data sources and limits.
- Respect privacy and consent; anonymise; follow data-protection law (e.g. GDPR).
- Be transparent about uncertainty and intended use.

## Sources (authoritative)
- scikit-learn documentation & user guide — https://scikit-learn.org/stable/
- pandas documentation — https://pandas.pydata.org/docs/
- An Introduction to Statistical Learning (free) — https://www.statlearning.com/
- Google Machine Learning Crash Course — https://developers.google.com/machine-learning/crash-course
