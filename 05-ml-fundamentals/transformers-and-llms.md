# Transformers and LLMs

## Self-attention

`Attention(Q, K, V) = softmax(QKᵀ / √d_k) V`

- Q, K, V are linear projections of the input tokens. Each output is a weighted average of value vectors, weighted by query–key similarity.
- **√d_k scaling** keeps dot products from growing with dimension, which would saturate softmax and shrink gradients.
- **Multi-head:** h heads with smaller dims attend to different relationships; outputs are concatenated and projected.
- **Causal mask:** decoder tokens can't attend to future positions (set those scores to −∞ before softmax).
- Cost: **O(n²·d)** time and O(n²) memory in sequence length n, the core long-context bottleneck. FlashAttention cuts memory traffic
  (exact attention, IO-aware); sparse/linear/sliding-window attention trade exactness for scale.
- **MQA / GQA:** share K/V projections across heads (all heads / groups of heads) → much smaller KV cache, faster decoding.

```python
import numpy as np
def attention(Q, K, V, causal=False):
    d = Q.shape[-1]
    scores = Q @ K.swapaxes(-1, -2) / np.sqrt(d)
    if causal:
        n = scores.shape[-1]
        scores = scores + np.triu(np.full((n, n), -np.inf), k=1)
    scores = scores - scores.max(axis=-1, keepdims=True)       # numerical stability
    w = np.exp(scores); w /= w.sum(axis=-1, keepdims=True)
    return w @ V
```

## The transformer block (decoder-only, modern)

`x = x + Attention(RMSNorm(x))` → `x = x + MLP(RMSNorm(x))` with a SwiGLU MLP (hidden ≈ 4× or ~2.7× with gating).
Residual stream + pre-norm. Final norm → linear "unembedding" → softmax over the vocabulary.

## Positional information

- Sinusoidal (original), learned absolute embeddings (GPT-2), **RoPE** (rotary: rotate Q/K by position-dependent angles, so the dot
  product depends on relative position; standard in Llama/Qwen/Mistral), ALiBi (linear distance bias).
- Context extension: RoPE scaling (position interpolation, NTK-aware, YaRN) + continued training on long sequences.

## Architecture families

| Type | Examples | Good for |
|---|---|---|
| Encoder-only | BERT, RoBERTa | Classification, embeddings, extraction (bidirectional context) |
| Decoder-only | GPT, Llama, Claude, Gemini, Mistral, Qwen | Generation; dominant for LLMs |
| Encoder–decoder | T5, BART, original Transformer | Translation, summarization (seq2seq) |

## Tokenization

BPE / byte-level BPE, WordPiece, SentencePiece (Unigram). Subwords balance vocabulary size against sequence length.
Effects: token counts drive cost; non-English text and code often take more tokens; tokenization quirks explain
weak character-level tasks (counting letters, spelling) and arithmetic glitches.

## Training stages

1. **Pre-training:** next-token prediction on trillions of tokens (web, code, books); learns knowledge and skills.
2. **Mid-training / continued pre-training** (optional): domain or long-context data.
3. **Supervised fine-tuning (SFT):** instruction–response pairs → follows instructions.
4. **Preference tuning:** RLHF (reward model + PPO) or DPO; RLAIF / Constitutional AI → helpful, harmless, honest behavior.
5. **RL for reasoning:** reinforcement learning with verifiable rewards (math, code tests) produces long chain-of-thought "reasoning models".

## Scaling laws

Loss falls as a power law in parameters N, data D, and compute C. **Chinchilla (2022):** compute-optimal training uses
≈ **20 tokens per parameter**. In practice models are "over-trained" well past that (e.g. Llama 3 used ~15T tokens) because
**inference cost** favors smaller models trained longer. Training compute ≈ **6·N·D FLOPs**; inference ≈ 2·N FLOPs per token.

## Decoding

Greedy · beam search (good for translation, bland for chat) · temperature · top-k · top-p (nucleus) · min-p ·
repetition penalties · **constrained decoding** (grammar/JSON schema) for structured outputs · speculative decoding (speed, same distribution).

## Prompting techniques

Clear instructions + role, few-shot examples, delimiters for untrusted content, **chain-of-thought** ("think step by step"),
self-consistency (sample several reasoning paths, majority vote), decomposition, ask for structured output,
put stable content first (prefix caching). Reasoning models need less "think step by step" and more clear goals and constraints.

## Hallucination

Causes: training on next-token likelihood (fluent ≠ true), knowledge gaps, exposure bias, ambiguous prompts, decoding randomness.
Mitigations: RAG + citations, abstention instructions, lower temperature, self-consistency checks, verification with tools,
fine-tuning on "I don't know" examples, grounding checks post-generation.

## Multimodal and embeddings

- **CLIP:** contrastive training of image and text encoders into one space → zero-shot classification, image search.
- Vision–language models: a vision encoder → projector → LLM tokens.
- **Text embedding models** (for RAG) are usually encoder models trained contrastively; dimensions 384–3072; Matryoshka embeddings can be truncated to fewer dims with modest loss.

## Interview questions to rehearse (answer in < 2 min each)

1. Why divide by √d_k? 2. What does the KV cache store and why does GQA shrink it? 3. Why do transformers need positional
encodings? How does RoPE work? 4. RLHF vs DPO? 5. Why are LLMs bad at counting letters? 6. What's the complexity of attention
and how do long-context models cope? 7. LoRA: why does a low-rank update work? 8. What is temperature mathematically?
(Divide logits by T before softmax.) 9. Pre-norm vs post-norm? 10. How would you reduce hallucinations in a production assistant?
