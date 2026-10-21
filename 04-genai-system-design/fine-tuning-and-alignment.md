# Fine-tuning and alignment

## Decision ladder (say this in order)

1. **Prompt engineering:** clear instructions, examples (few-shot), structured outputs.
2. **RAG:** when the gap is *knowledge* (private or fresh facts).
3. **Fine-tuning:** when the gap is *behavior*: consistent format/style, domain jargon, a narrow task at lower
   cost/latency with a smaller model, or tool-calling reliability. Needs hundreds to thousands of high-quality examples and an eval set.
4. **Pre-training / continued pre-training:** very large domain corpora (code, biomedical); rarely justified for applied teams.

Fine-tuning is a poor way to add facts that change (it can't easily be updated, it hallucinates confidently,
and it can't cite). Combine: a fine-tuned small model + RAG is common.

## Methods

| Method | What it is | Notes |
|---|---|---|
| Full fine-tuning | Update all weights | Expensive; risk of catastrophic forgetting |
| **LoRA** | Freeze weights; learn low-rank matrices A·B added to selected layers | ~0.1–1% trainable params; adapters can be hot-swapped per tenant/task |
| **QLoRA** | LoRA on a 4-bit quantized base model | Fine-tune large models on a single GPU |
| Prefix / prompt tuning | Learn soft prompt vectors | Cheap; usually weaker than LoRA |
| **SFT** (supervised fine-tuning) | Train on (prompt, ideal response) pairs | First step of instruction tuning |
| **RLHF** | Train a reward model on human preference pairs, then optimize the policy (PPO) with a KL penalty to the SFT model | Powerful, complex, unstable |
| **DPO** | Optimize directly on preference pairs; no separate reward model or RL loop | Simpler and more stable; widely used |
| RLAIF / Constitutional AI | AI-generated feedback guided by principles | Scales preference data |
| RL with verifiable rewards | Reward from checkable outcomes (unit tests pass, math answer correct), e.g. GRPO | How "reasoning" models are commonly trained |
| **Distillation** | Train a small student on a large teacher's outputs | Cut cost/latency for a narrow task; check the provider's terms |

## Data for fine-tuning

- Quality beats quantity: dedupe, filter, and have experts review a sample.
- Match the production input distribution; include hard and negative examples.
- Hold out a test set; compare against the prompted base model and a RAG baseline. **If it doesn't beat them, don't ship it.**
- Watch for overfitting and capability regression on general tasks (run a broad eval too).

## Hyperparameters to mention

Learning rate (most sensitive), epochs (1–3 typical for SFT), LoRA rank r (8–64) and alpha, target modules
(attention projections, sometimes MLP), batch size, sequence length/packing.

## Operating fine-tuned models

Version datasets + base model + adapter; re-run evals when the base model is deprecated; serve multiple LoRA
adapters on one base model (e.g. multi-LoRA serving in vLLM) for per-customer customization.
