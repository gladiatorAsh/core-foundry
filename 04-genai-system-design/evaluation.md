# Evaluating LLM systems

> "If you can't measure it, you can't ship it." Evaluation is the most common Staff differentiator in LLM design rounds.

## Layers of evaluation

1. **Component evals:** retrieval (recall@k, MRR, nDCG), classifiers/routers (precision/recall), extractors (field-level F1, exact match).
2. **End-to-end offline evals:** a **golden dataset** of realistic inputs with reference answers or rubrics, run on every change.
3. **Online evals:** user feedback, behavioral signals, A/B tests, sampled human review, production LLM-judge sampling.

## Building the golden set

- Start with 50–200 examples from real logs (de-identified), stratified by intent, difficulty, language, and risk.
- Include adversarial cases: unanswerable questions, prompt injections, out-of-scope requests, ambiguous queries.
- Label with domain experts; store expected sources (for retrieval eval) plus a rubric or reference answer.
- Grow it continuously: **every production failure becomes a test case.**
- Version it; keep a held-out slice you don't tune prompts against.

## Metrics for RAG answers

| Metric | Question it answers |
|---|---|
| Context recall / retrieval recall@k | Did we retrieve the evidence needed? |
| Context precision | How much of what we retrieved was relevant? |
| **Faithfulness / groundedness** | Is every claim supported by the retrieved context? |
| Answer relevance | Does it address the question? |
| Correctness | Does it match the reference answer? |
| Citation accuracy | Do the cited sources support the cited sentences? |
| Abstention quality | Does it say "I don't know" when it should (and only then)? |

Tools that implement these: Ragas, DeepEval, TruLens, Azure AI Foundry evaluations, OpenAI Evals, promptfoo, LangSmith, Braintrust.

## LLM-as-judge

- **Pairwise** comparison (A vs B) is more reliable than absolute 1–10 scores. Use **binary or 3-point rubrics** with specific criteria.
- Known biases: position bias (randomize order), verbosity bias, self-preference (the judge favors its own family's outputs).
- **Calibrate against humans:** measure agreement (Cohen's kappa / % agreement) on 100+ items before trusting it.
- Ask for reasoning before the verdict; use a strong judge model; keep the judge prompt versioned.
- Use cheap deterministic checks first (JSON valid, citations present, regex for forbidden content).

## Online signals

Thumbs up/down (sparse, biased), copy/paste events, follow-up reformulations, escalation to a human, task completion,
session abandonment, and **deflection rate** (support). Guardrails: latency, cost/request, safety-flag rate.

## Release process

- Eval gate in CI: block deploys if key metrics regress beyond a threshold (with confidence intervals; small sets are noisy).
- Changes that require the gate: prompt edits, model version upgrades, retrieval config, chunking, tool schemas.
- Shadow traffic for new models → A/B on a small % → ramp.

## Benchmarks (for context, not product decisions)

MMLU and HumanEval are largely saturated. More current references: MMLU-Pro, GPQA (graduate-level QA),
SWE-bench Verified (real GitHub issues), LiveCodeBench, τ-bench (agents), Chatbot Arena (human preference Elo).
Public benchmarks rarely predict performance on *your* task, so build your own evals.
