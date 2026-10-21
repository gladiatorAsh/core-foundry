# Retrieval-augmented generation (RAG)

## Why RAG

Grounds answers in your data (fresher than training data, private data), enables **citations**, reduces
hallucination, and is far cheaper to update than fine-tuning. RAG gives the model **knowledge**; fine-tuning
mostly changes **behavior/format/style**.

## Ingestion pipeline (offline / incremental)

1. **Connectors** (SharePoint, Confluence, Drive, tickets, DBs) with change feeds or crawls; capture **ACLs** and metadata.
2. **Parsing:** layout-aware extraction for PDFs (tables, headers), OCR for scans, HTML cleanup. Quality here caps everything downstream.
3. **Chunking:**
   - Fixed-size with overlap (e.g. 300–800 tokens, 10–20% overlap): simple, robust baseline.
   - Structure-aware: split by headings/sections/paragraphs; keep tables intact.
   - Semantic chunking: split where embedding similarity between sentences drops.
   - **Parent–child / small-to-big:** embed small chunks for precise matching, return the larger parent section for context.
   - Add **contextual headers** (doc title, section path) to each chunk before embedding; this measurably improves retrieval.
4. **Enrichment:** metadata (source, date, author, product, language), optional LLM-generated summaries or hypothetical questions per chunk.
5. **Embedding:** choose the model by retrieval benchmarks *on your data* (MTEB is a starting point). Record the
   model version; **changing the embedding model means re-embedding everything** (blue/green index).
6. **Indexing:** vector index (HNSW is the common default) + keyword index (BM25) + filterable metadata fields + ACL fields.
7. **Deletes and updates:** tombstones, re-index on change, honor deletion SLAs.

## Retrieval (online)

1. **Query understanding:** rewrite conversational follow-ups into standalone queries ("what about for contractors?" → full question);
   optional decomposition of multi-part questions; HyDE (embed a hypothetical answer) for sparse queries.
2. **Hybrid search:** BM25 (exact terms, IDs, acronyms) + dense vectors (semantics), fused with **Reciprocal Rank Fusion**
   `score = Σ 1/(k + rank_i)`, k ≈ 60.
3. **Security trimming:** filter by the user's groups/ACLs **inside the search query** (pre-filter), never after generation.
4. **Re-ranking:** a cross-encoder (or an LLM re-ranker) scores the top ~50 and keeps the top 5–10. Biggest quality gain per ms.
5. **Context assembly:** dedupe, order by relevance (models attend more to the start and end of long contexts, the
   "lost in the middle" effect), respect a token budget, include citation IDs.

## Generation

- System prompt: answer only from the provided sources, cite them as [n], say "I don't know" when the context is insufficient.
- Structured output (JSON schema) when downstream code consumes it.
- **Grounding check** (optional): verify each claim is supported by a cited chunk (NLI model or LLM judge); drop or flag unsupported claims.

## Vector search internals

| Index | Idea | Trade-off |
|---|---|---|
| Flat (brute force) | Exact | O(n), fine for < ~1M vectors |
| **HNSW** | Multi-layer proximity graph | High recall/low latency, memory hungry, slower builds |
| IVF (+PQ) | Cluster into lists; search nearest lists; product-quantize vectors | Less memory, recall depends on `nprobe` |
| DiskANN / ScaNN | Disk-resident graph / anisotropic quantization | Billion-scale, cost-efficient |

Similarity: cosine (normalize vectors, then dot product = cosine). Quantization (int8/binary) cuts memory 4–32× with a small recall loss; re-score the top results with full precision.

**Filtered ANN** is hard: post-filtering can return too few results; pre-filtering can break graph connectivity.
Most engines do filtered traversal. Mention it when ACLs or tenant filters are very selective.

## Advanced patterns

- **GraphRAG:** build an entity/relationship graph + community summaries; good for "global" questions across a corpus; expensive to build.
- **Agentic RAG:** the model decides when/what to retrieve, iterates, and calls multiple sources/tools.
- **Corrective / self-reflective RAG:** grade retrieved docs; if they're weak, rewrite the query or fall back to web/another source.
- **Long-context vs RAG:** long context windows don't remove RAG. Cost and latency scale with tokens, attention degrades
  in the middle, and permissions still need enforcement. Use long context for a few long documents and RAG for large corpora.
- **Caching:** cache embeddings of frequent queries, retrieval results, and full answers (semantic cache with a high
  similarity threshold, scoped per permission set).

## Failure modes → fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Right doc exists but isn't retrieved | Chunking split the answer; vocabulary mismatch; embedding weak on jargon | Better chunking/headers, hybrid search, query rewrite, domain-tuned embeddings |
| Retrieved but answer is wrong | Too much noisy context; lost in the middle | Re-ranker, fewer/better chunks, reorder |
| Confident answers with no support | Prompt doesn't permit "I don't know"; weak grounding | Abstention instructions, grounding check, citations required |
| Stale answers | Index lag, no deletes | Change feeds, freshness metadata + recency boost |
| Data leak across users | ACLs not enforced at retrieval; shared cache | Security filters in queries, per-permission cache keys |
| Slow | Too many chunks/tokens, serial calls | Parallel retrieval, smaller re-ranker, streaming, prompt caching |

## Interview soundbites

- "I evaluate retrieval and generation separately: recall@k and MRR on a labeled query set, then faithfulness and answer quality."
- "Hybrid plus a re-ranker is my default; pure vector search misses exact identifiers like error codes and SKUs."
- "ACLs are captured at ingestion and enforced as filters at query time; the LLM never sees a chunk the user can't."
