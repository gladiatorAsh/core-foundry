# ML system design framework

| Time | Step | Key questions |
|---|---|---|
| 0–7 | **1. Clarify the business goal** | What are we optimizing for the business (engagement, revenue, safety, cost)? Constraints: latency, scale, privacy, cold start. What's the non-ML baseline? |
| 7–12 | **2. Frame as an ML problem** | Input → output. Classification, regression, ranking, retrieval, generation? Choose the **label** and the **proxy** carefully, and say why the proxy is OK. |
| 12–20 | **3. Data** | Sources, labels (implicit vs explicit, human labeling), volume, freshness, bias, leakage, privacy. Train/val/test split (by **time** for most production problems). |
| 20–28 | **4. Features & model** | Features (user, item, context, cross); embeddings; start simple (logistic regression / GBDT) → deep model (two-tower, DLRM-style, transformer). Justify each step up in complexity. |
| 28–38 | **5. Serving architecture** | Candidate generation → ranking → re-ranking (business rules, diversity). Online vs batch inference; feature store (online/offline consistency); latency budget per stage. |
| 38–48 | **6. Evaluation** | Offline metrics that correlate with the online goal; online A/B test design; guardrail metrics. |
| 48–60 | **7. Deploy & monitor** | Shadow → canary → A/B; data/prediction drift; retraining cadence; feedback loops; failure fallbacks. |

## Things Staff candidates say (that others don't)

- "Before ML: what's the heuristic baseline, and how much better do we need to be to justify the complexity?"
- "The label is *watched 30s+*, not *clicked*, because clicks reward clickbait."
- "I'll split by time, not randomly, to avoid leaking future behavior."
- "Training-serving skew is the most common silent failure, so features come from one feature store definition."
- "Our model changes what users see, which changes our training data (a feedback loop). I'd keep an
  exploration slice (e.g. 1–5% randomized) to get unbiased data."
- "Offline AUC improved but online engagement didn't. Here's how I'd debug that."

## The multi-stage ranking funnel (memorize this diagram)

```
Billions of items
   │  Candidate generation (recall): two-tower ANN, collaborative filtering, graph, popular/trending, rules
   ▼  ~1,000s
Lightweight ranker (optional): small model / GBDT
   ▼  ~100s
Heavy ranker (precision): deep model on rich features, multi-task (click, like, share, dwell, hide)
   ▼  ~10s–100
Re-ranking / policy: diversity, freshness, dedupe, fairness, business rules, ads blending
   ▼
User
```

## Feature store and freshness

- **Batch features** (daily aggregates) vs **streaming features** (last 30 min of activity) vs **request-time features** (context).
- The online store (low-latency KV) serves inference; the offline store (warehouse) holds point-in-time correct training data.
- **Point-in-time joins** prevent label leakage: training features must be computed as of the event time.

## Handling common constraints

| Constraint | Techniques |
|---|---|
| Cold start (new users/items) | Content features, popularity priors, exploration, onboarding questions |
| Class imbalance (fraud) | Re-weighting, focal loss, down-sampling negatives (then **recalibrate** probabilities), PR-AUC not ROC-AUC |
| Latency | Two-stage funnel, caching embeddings, distillation, quantization, precomputed candidates |
| Label delay (chargebacks in 60 days) | Proxy labels, delayed-feedback models, train on matured windows |
| Privacy | Minimize features, aggregate, differential privacy, on-device inference, federated learning |
| Feedback loops / position bias | Exploration traffic, position as a feature at training (set to fixed at serving), inverse propensity weighting |
