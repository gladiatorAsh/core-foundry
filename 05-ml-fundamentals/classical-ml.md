# Classical ML

## Bias–variance trade-off

Expected error = bias² + variance + irreducible noise. **High bias** (underfitting): train and val errors are both high,
so use a more complex model or more features. **High variance** (overfitting): low train error, high val error, so
use more data, regularization, a simpler model, or ensembling (bagging cuts variance; boosting cuts bias).

## Regularization

- **L2 (ridge):** penalty λΣw²; shrinks weights smoothly; equivalent to a Gaussian prior (MAP).
- **L1 (lasso):** penalty λΣ|w|; drives weights to exactly zero, so it does feature selection; Laplace prior.
- **Elastic net:** both; handles correlated features better than L1 alone.
- Others: early stopping, dropout, data augmentation, weight decay (≈ L2 for SGD; decoupled in AdamW).

## Linear and logistic regression

- Linear: minimize MSE; closed form `w = (XᵀX)⁻¹Xᵀy` (O(d³)), or gradient descent at scale. Assumes linearity, independent errors, homoscedasticity.
- Logistic: `p = σ(wᵀx)`; minimize **log loss** (cross-entropy), which is convex; outputs are calibrated-ish probabilities.
  Coefficients are log-odds: e^w = the odds ratio per unit change.
- Multiclass: softmax regression. Multicollinearity inflates coefficient variance (it matters for interpretation, less for prediction).

## Decision trees and ensembles

- Trees split to maximize impurity reduction (Gini or entropy for classification; variance for regression). Interpretable, handle
  non-linearity and mixed types, overfit easily.
- **Random forest (bagging):** many deep trees on bootstrap samples + random feature subsets; averaging reduces variance; robust baseline.
- **Gradient boosting (XGBoost, LightGBM, CatBoost):** shallow trees added sequentially, each fitting the **negative gradient**
  (residuals) of the loss; learning rate + number of trees + depth control overfitting. **The default for tabular data.**
- Feature importance: gain-based (biased toward high-cardinality features) vs permutation importance vs **SHAP** (consistent, local + global).

## SVM, k-NN, Naive Bayes

- SVM: max-margin hyperplane; hinge loss; kernels (RBF) for non-linear boundaries; scales poorly beyond ~100K samples.
- k-NN: no training; prediction cost O(n·d) (use ANN indexes); suffers from the curse of dimensionality; scale features.
- Naive Bayes: assumes conditional independence of features; fast, strong for text baselines.

## Unsupervised

- **k-means:** minimize within-cluster squared distance; choose k via elbow/silhouette; sensitive to init (k-means++) and scale; spherical clusters only.
- DBSCAN: density-based; finds arbitrary shapes and outliers; struggles with varying density.
- Hierarchical clustering: dendrogram; O(n²) memory.
- **PCA:** project onto the top eigenvectors of the covariance matrix (via SVD); linear; maximize retained variance. t-SNE/UMAP for visualization only.
- Anomaly detection: isolation forest, autoencoder reconstruction error, statistical thresholds.

## Feature engineering and data issues

- Scaling (standardize for linear/distance models; trees don't care). Log-transform skewed features.
- Categorical: one-hot (low cardinality), target encoding (with out-of-fold to avoid leakage), hashing trick, learned embeddings.
- Missing values: impute + a missingness indicator; trees (XGBoost) handle missing values natively.
- **Leakage:** features that encode the label or future information (e.g. "account closed date" for churn). Split by time; build features point-in-time.
- **Imbalance:** class weights, resampling (SMOTE rarely helps in production), threshold tuning, the right metric (PR-AUC).
- **Calibration:** Platt scaling (logistic fit on scores), isotonic regression; check reliability diagrams.

## Cross-validation

k-fold for i.i.d. data; **stratified** for imbalanced classes; **grouped** when samples share an entity (same user in train
and val = leakage); **time-series split** (rolling/expanding window) for temporal data.

## Loss functions to know

MSE (Gaussian noise; sensitive to outliers), MAE (robust; median), Huber (both), log loss / cross-entropy, hinge,
focal loss (down-weights easy examples in imbalanced detection), pinball/quantile loss (prediction intervals, asymmetric costs),
contrastive/triplet/InfoNCE (embeddings), pairwise/listwise ranking losses (RankNet, LambdaRank).
