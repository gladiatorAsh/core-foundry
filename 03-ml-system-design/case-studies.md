# ML system design case studies

Each outline: **objective & label → data/features → model → serving → evaluation → gotchas**. Rehearse two per week.

---

## 1. Video / content recommendations (YouTube, Netflix home)
- **Objective:** long-term satisfaction; proxy = expected watch time / completed views, with penalties for hides/dislikes.
- **Candidates:** two-tower model (user tower: history, context; item tower: content + engagement) with ANN retrieval;
  plus co-watch, subscriptions, trending, and fresh-content sources.
- **Ranker:** multi-task deep model predicting P(click), E[watch time], P(like), P(dislike) → weighted score.
- **Re-rank:** diversity (no 5 videos of the same creator), freshness, dedupe, policy filters.
- **Eval:** offline Recall@k (candidates), NDCG (ranker); online watch time per user, retention, satisfaction surveys.
- **Gotchas:** feedback loops/popularity bias (exploration), cold-start creators, position bias, clickbait.

## 2. Search ranking (e-commerce or web)
- **Objective:** relevance + conversion; labels from clicks/purchases (biased) + human relevance judgments.
- **Pipeline:** query understanding (spell correction, intent, entity extraction) → retrieval (BM25 + dense vectors,
  hybrid) → learning-to-rank (LambdaMART / cross-encoder for top-k) → business re-rank.
- **Eval:** NDCG@10 on judged sets; online CTR, conversion, zero-result rate, reformulation rate; interleaving.
- **Gotchas:** position bias in click labels (inverse propensity weighting), tail queries, latency of cross-encoders.

## 3. Ads click-through rate (CTR) prediction
- **Objective:** calibrated P(click) (and P(conversion)) because the **auction uses it**: expected value = bid × pCTR.
- **Model:** logistic regression with feature crosses → wide & deep / DCN / DLRM; huge sparse categorical embeddings.
- **Data:** billions of impressions/day, so **negative down-sampling** + recalibration; near-real-time training (freshness matters).
- **Eval:** log loss, calibration (normalized cross-entropy), AUC; online revenue, advertiser ROI, user experience guardrails.
- **Gotchas:** calibration drift, delayed conversions, privacy changes (fewer cross-site signals), new ads cold start.

## 4. Social feed ranking (Facebook/LinkedIn/Instagram)
- **Objective:** meaningful interactions; weighted sum of predicted actions (like, comment, share, dwell, hide/report as negatives).
- **Inventory:** posts from connections + recommended (unconnected) content; candidate sourcing per source with quotas.
- **Model:** multi-task, multi-label deep model; features on author affinity, content type, recency, past engagement.
- **Gotchas:** integrity signals (misinformation, bait), creator fairness, time-decay, notification/feed interplay.

## 5. Fraud detection (payments)
- **Objective:** minimize fraud loss + false-decline cost (each false decline loses a customer's revenue).
- **Labels:** chargebacks (delayed 30–90 days), manual review outcomes.
- **Features:** velocity (txns per card/device/IP in windows), device fingerprint, geo mismatch, merchant risk, graph
  features (shared devices/cards across accounts).
- **Model:** GBDT (strong on tabular data, explainable) + graph model for rings; rules engine for known patterns.
- **Serving:** real-time score < 100 ms in the payment path; thresholds → approve / step-up auth / review / decline.
- **Eval:** PR-AUC, recall at a fixed false-positive rate, dollar-weighted metrics; backtests on time-split data.
- **Gotchas:** adversarial adaptation (retrain often, monitor drift), label delay, extreme imbalance, explainability for disputes.

## 6. Harmful content detection (integrity)
- **Objective:** catch policy-violating content with high precision at action thresholds; reduce prevalence (views of violating content).
- **Model:** multimodal (text + image + video) classifiers, fine-tuned foundation models; LLMs for policy reasoning
  on borderline cases; hash matching (PhotoDNA-style) for known bad content.
- **Pipeline:** pre-upload/at-upload scoring → auto-action above high threshold → human review queue for the uncertain band → appeals.
- **Eval:** precision/recall per policy and per language, **prevalence** measured via sampled human labeling, reviewer agreement.
- **Gotchas:** label noise and policy changes, low-resource languages, adversarial obfuscation, reviewer wellbeing.

## 7. ETA / delivery time prediction (Uber, DoorDash)
- **Objective:** accurate ETA with an asymmetric cost (late is worse than early) → quantile regression / pinball loss.
- **Features:** route graph travel times, real-time traffic, restaurant prep time history, courier supply, weather, time of day.
- **Model:** GBDT or deep model correcting a routing-engine baseline (predict the residual).
- **Eval:** MAE, P90 error, % within ±5 min; online: customer cancellations, support contacts.

## 8. "People You May Know" / friend recommendations
- **Candidates:** friends-of-friends (graph walks), shared contexts (school, workplace, contacts upload), embeddings.
- **Ranker:** P(request sent) × P(accepted). Optimize for **accepted** connections, not requests.
- **Gotchas:** privacy (don't leak sensitive connections), graph computation at scale (precompute 2-hop neighbors), fatigue.

---

### Practice prompts (no outline; do these cold)

Design: notification ranking (send/no-send + timing) · Spotify playlist generation · Airbnb search ranking ·
duplicate listing detection · LinkedIn job recommendations · query autocomplete with ML · spam email filter ·
App Store search · Ads budget pacing · Image search (text → image with CLIP-style embeddings).
