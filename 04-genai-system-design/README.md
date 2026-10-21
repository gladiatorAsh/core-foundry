# GenAI / LLM system design

This is the round where your experience counts most. Most candidates can sketch "embed → vector DB →
LLM". Staff candidates win on **evaluation, permissions, cost/latency engineering, failure handling, and rollout**.

| File | What's in it |
|---|---|
| [framework.md](framework.md) | How to run a 45–60 min LLM design interview |
| [rag.md](rag.md) | Retrieval-augmented generation end to end: ingestion, chunking, hybrid search, re-ranking, grounding |
| [llm-serving.md](llm-serving.md) | Inference internals: prefill/decode, KV cache, batching, quantization, speculative decoding, routing |
| [agents.md](agents.md) | Tool use, planning patterns, multi-agent orchestration, memory, MCP, reliability |
| [evaluation.md](evaluation.md) | Offline evals, LLM-as-judge, RAG metrics, online metrics, regression gates |
| [fine-tuning-and-alignment.md](fine-tuning-and-alignment.md) | When to fine-tune; LoRA/QLoRA; SFT, RLHF, DPO; distillation |
| [safety-and-guardrails.md](safety-and-guardrails.md) | Prompt injection, data leakage, jailbreaks, content safety, governance |
| [case-studies.md](case-studies.md) | 8 worked designs: enterprise copilot, support agent, doc intelligence, coding assistant, LLM gateway, … |
| [vendor-neutral-mapping.md](vendor-neutral-mapping.md) | Translate your Azure stack into generic or GCP/AWS terms for FAANG interviews |

## Best external resources

- Chip Huyen, *AI Engineering* (O'Reilly, 2025), plus its [companion repo](https://github.com/chiphuyen/aie-book). The best single book for this round.
- [RAG_Techniques (GitHub)](https://github.com/NirDiamant/RAG_Techniques) and [GenAI_Agents (GitHub)](https://github.com/NirDiamant/GenAI_Agents): runnable notebooks per technique
- [llm-course (GitHub, mlabonne)](https://github.com/mlabonne/llm-course): LLM fundamentals → fine-tuning → deployment
- [ml-engineering (GitHub, stas00)](https://github.com/stas00/ml-engineering): training/inference infrastructure in depth
- [LLMs interview questions (GitHub, Devinterview-io)](https://github.com/Devinterview-io/llms-interview-questions) · [LLMInterviewQuestions (GitHub)](https://github.com/llmgenai/LLMInterviewQuestions)
- [Azure-Samples/azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo): a reference RAG app on your home stack
- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents): workflow vs agent patterns
- [vLLM docs](https://docs.vllm.ai/) (PagedAttention, continuous batching) · [Lilian Weng's blog](https://lilianweng.github.io/) (agents, hallucination, prompt engineering)
- Eugene Yan, ["Patterns for building LLM-based systems"](https://eugeneyan.com/writing/llm-patterns/)

Quiz yourself: `python tools/quiz.py --topic genai`
