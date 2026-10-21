# LLM inference and serving

## How generation works

- **Prefill:** process the whole prompt in parallel and build the **KV cache**. Compute-bound. Determines **time to first token (TTFT)**.
- **Decode:** generate one token at a time, each attending to the cached keys/values. Memory-bandwidth-bound.
  Determines **time per output token (TPOT)** / inter-token latency.
- Total latency ≈ TTFT + output_tokens × TPOT. **Throughput** = tokens/s across all requests.
- Long prompts hurt TTFT; long outputs hurt total latency. Streaming hides latency but not cost.

## KV cache

- Stores keys and values for every past token at every layer, so decoding doesn't recompute attention inputs.
- Size per token = `2 × layers × kv_heads × head_dim × bytes_per_value`. Grows linearly with context length × batch size.
- It is usually **the** memory bottleneck for serving long contexts and many concurrent users.
- **Multi-query / grouped-query attention (MQA/GQA)** share K/V across heads → much smaller cache.
- **PagedAttention (vLLM):** stores the KV cache in fixed-size blocks like virtual memory pages → little fragmentation, more concurrent sequences.
- **Prefix (prompt) caching:** reuse the KV cache for a shared prefix (system prompt, few-shot examples, a long document).
  Big TTFT and cost savings, so put stable content **first** in prompts. Hosted APIs (OpenAI, Anthropic, Azure OpenAI, Gemini)
  offer discounted cached input tokens.

## Batching

- Static batching wastes GPU time waiting for the longest sequence.
- **Continuous (in-flight) batching:** add and remove sequences each decode step. Standard in vLLM, TGI, TensorRT-LLM, SGLang.
- Chunked prefill: split long prefills so they don't stall the decode of other requests.
- Larger batches raise throughput but also per-request latency, so tune against your SLO.

## Making it faster/cheaper

| Technique | What it does | Trade-off |
|---|---|---|
| **Quantization** (INT8, FP8, INT4: GPTQ, AWQ) | Fewer bytes per weight → less memory, faster decode | Small quality loss; test on your evals |
| **Speculative decoding** | A small draft model proposes k tokens; the big model verifies them in one pass | Same output distribution; speedup depends on acceptance rate |
| **Distillation** | Train a small model to mimic a large one on your task | Training cost; narrower capability |
| **FlashAttention** | IO-aware attention kernel; less memory traffic | Pure win; usually built in |
| **Tensor / pipeline parallelism** | Split a model across GPUs | Communication overhead; needed for big models |
| **Disaggregated prefill/decode** | Separate GPU pools for compute-bound prefill and memory-bound decode | Operational complexity |
| **Model routing / cascades** | Cheap model first; escalate hard queries | Needs a router and quality monitoring |
| **Output limits** | `max_tokens`, concise style instructions | Truncation risk |

## Serving architecture for a multi-tenant LLM platform

```
Clients ─► Gateway (auth, quotas per tenant, rate limit on tokens/min) ─► Router
   Router: model selection, fallbacks across regions/providers, retries with backoff, timeouts
   ├─► Hosted API deployments (provisioned throughput for steady load + pay-as-you-go for bursts)
   └─► Self-hosted pool (vLLM/TensorRT-LLM on GPUs) with autoscaling on queue depth / KV-cache utilization
Shared: semantic + exact response cache, prompt registry, usage metering, tracing, safety filters
```

- **Capacity planning:** measure tokens/s per GPU at your latency SLO for your prompt/output length mix; size for
  peak tokens/min, not requests. GPU cold start is slow (model load), so keep warm capacity.
- **Rate limits** on hosted APIs are in tokens per minute (TPM) and requests per minute (RPM); spread across deployments/regions.
- **Fallbacks:** secondary region or model; graceful degradation (shorter answers, smaller model, cached answers).

## Self-host vs API

| Self-host open weights (Llama, Mistral, Qwen, Gemma) | Hosted API (GPT, Claude, Gemini, Azure OpenAI) |
|---|---|
| Control, data stays in your VPC, fine-tuning freedom, cost-efficient at high steady utilization | Frontier quality, no infra, elastic, fast iteration |
| GPU ops burden, utilization risk, you own upgrades and safety | Per-token cost, rate limits, vendor dependence, data-handling terms to review |

## Sampling parameters

Temperature (randomness; 0 = near-greedy), top-p (nucleus), top-k, repetition/frequency penalties, stop sequences,
`max_tokens`, seed (best-effort reproducibility). For extraction/classification: low temperature + structured outputs.
