# Metrics and experimentation

## Offline metrics

| Task | Metrics | Notes |
|---|---|---|
| Binary classification | Precision, recall, F1, ROC-AUC, **PR-AUC**, log loss, calibration (reliability curve, ECE) | Imbalanced data → PR-AUC; ads/bidding need **calibrated** probabilities |
| Ranking / recommendation | **NDCG@k**, MAP, MRR, Recall@k, Hit rate | Recall@k for candidate generation; NDCG for the ranker |
| Regression | MAE, RMSE, MAPE | RMSE punishes large errors; MAPE breaks near 0 |
| Retrieval (RAG) | Recall@k, MRR, nDCG, context precision | Measure retrieval separately from generation |
| Generation | Task success, faithfulness/groundedness, LLM-as-judge rubric scores, pairwise win rate, BLEU/ROUGE (weak) | See [../04-genai-system-design/evaluation.md](../04-genai-system-design/evaluation.md) |

**Precision vs recall:** precision = TP / (TP + FP) ("of what we flagged, how much was right");
recall = TP / (TP + FN) ("of what was there, how much we caught"). Fraud review queues are capacity-limited, so
optimize precision at the queue size. Medical screening favors recall.

**ROC-AUC** = the probability a random positive scores above a random negative. It's insensitive to class
imbalance, which hides poor precision on rare positives.

## Online metrics

- **North star** (e.g. long-term retention, revenue) is slow, so use **driver metrics** (sessions, watch time, CTR).
- **Guardrails** must not regress: latency, crash rate, unsubscribes, hides/reports, revenue for non-revenue tests.
- Watch for metric gaming: optimizing CTR increases clickbait; optimizing watch time can hurt satisfaction.

## A/B testing essentials

- **Randomization unit:** user (most common), session, request, or cluster (for network effects).
- **Sample size** grows with variance and shrinks with the square of the minimum detectable effect (MDE):
  n per arm ≈ 16 σ² / δ² for α = 0.05, power = 0.8.
- **Duration:** at least 1–2 full weekly cycles; watch for **novelty/primacy** effects.
- **Pitfalls:** peeking (inflates false positives; use sequential testing), multiple comparisons, **sample ratio
  mismatch** (SRM: check the traffic split first), interference between treatment and control (marketplaces,
  social networks: use cluster or switchback designs), Simpson's paradox.
- **Variance reduction:** CUPED (regress on a pre-period metric), stratification.
- **Interleaving** (for ranking): blend results from A and B in one list; far more sensitive than A/B for ranker comparisons.
- **Offline–online gap:** offline gains may not transfer because of distribution shift, position bias, feedback
  loops, or a bad proxy metric. Use **counterfactual evaluation** (inverse propensity scoring) with logged exploration data.

## Monitoring in production

- **Data drift** (input distribution, e.g. PSI or KL divergence), **concept drift** (P(y|x) changes), **prediction drift**.
- Data quality: nulls, schema changes, feature freshness, upstream outages.
- Model performance once labels arrive; slice by segment (country, device, new users).
- Retraining triggers: schedule plus drift thresholds; always gate with offline eval + canary.
