# Probability and statistics

## Core rules

- Bayes: `P(A|B) = P(B|A)·P(A) / P(B)`. Expect the base-rate question: a test 99% sensitive, 95% specific, prevalence 1% →
  P(disease | positive) = 0.99·0.01 / (0.99·0.01 + 0.05·0.99) ≈ **16.7%**.
- Linearity of expectation (works even for dependent variables). Var(aX + b) = a²Var(X). Var(X+Y) = Var X + Var Y + 2Cov(X,Y).
- Law of total probability/expectation: E[X] = E[E[X|Y]].

## Distributions

| Distribution | Use | Mean / variance |
|---|---|---|
| Bernoulli(p) | One trial | p / p(1−p) |
| Binomial(n, p) | Successes in n trials | np / np(1−p) |
| Geometric(p) | Trials until first success | 1/p / (1−p)/p² |
| Poisson(λ) | Counts of rare events per interval | λ / λ |
| Exponential(λ) | Time between Poisson events (memoryless) | 1/λ / 1/λ² |
| Normal(μ, σ²) | Sums of many effects (CLT) | μ / σ² |
| Uniform(a, b) | – | (a+b)/2 / (b−a)²/12 |

**CLT:** the sample mean of i.i.d. variables with finite variance → Normal(μ, σ²/n) as n grows. Standard error = σ/√n.

## Estimation

- **MLE:** choose parameters maximizing the likelihood of the data. (MSE ↔ Gaussian noise MLE; cross-entropy ↔ Bernoulli/categorical MLE.)
- **MAP:** MLE + a prior → regularization (Gaussian prior = L2, Laplace = L1).
- Bias vs variance of estimators; unbiased sample variance divides by n−1 (Bessel's correction).

## Hypothesis testing (A/B tests)

- Null H₀ (no difference). **p-value** = P(data at least this extreme | H₀), *not* P(H₀ | data).
- α (type I, false positive rate, usually 0.05); β (type II); **power** = 1 − β (usually 0.8).
- Two-proportion z-test for conversion rates; t-test for means; Mann–Whitney for skewed data; chi-square for categorical; bootstrap when unsure.
- 95% CI: "if we repeated the experiment many times, 95% of such intervals would contain the true value."
- Multiple testing: Bonferroni (conservative), Benjamini–Hochberg (controls false discovery rate).
- Practical vs statistical significance: with huge samples, tiny useless effects become "significant".

## Classic interview puzzles (practice the reasoning, out loud)

1. Expected number of coin flips to get two heads in a row → **6**.
2. Probability at least two of 23 people share a birthday → **≈ 50.7%**.
3. Sample uniformly from a stream of unknown length → **reservoir sampling** (keep item i with probability k/i).
4. Monty Hall → switching wins with probability **2/3**.
5. Expected value of the max of two dice → 161/36 ≈ **4.47**.
6. Generate a fair bit from a biased coin → flip twice; HT → 0, TH → 1, else repeat (von Neumann).
7. A/B test shows +2% with p = 0.04 after peeking daily → inflated false-positive risk; use sequential testing or a fixed horizon.
8. Simpson's paradox: a treatment better in every subgroup can look worse in aggregate because of confounded group sizes.
