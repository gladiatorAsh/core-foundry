# Back-of-envelope estimation

## Numbers to remember (orders of magnitude)

| Operation | Time |
|---|---|
| L1 cache reference | ~1 ns |
| Main memory reference | ~100 ns |
| Compress 1 KB (fast codec) | ~2–3 µs |
| Read 1 MB sequentially from memory | ~10 µs (tens of GB/s) |
| SSD random read | ~16–100 µs |
| Round trip within a datacenter | ~0.5 ms |
| Read 1 MB sequentially from SSD | ~50 µs–1 ms |
| Disk (HDD) seek | ~2–10 ms |
| Round trip California ↔ Netherlands | ~150 ms |

Conversions: 1 day ≈ **86,400 s ≈ 10^5 s**. 1 month ≈ 2.5 × 10^6 s. 1 year ≈ 3 × 10^7 s.
1 million requests/day ≈ **12 QPS**. Peak ≈ 2–3× average (more for spiky consumer apps).

| Unit | Bytes |
|---|---|
| char (ASCII/UTF-8 Latin) | 1 B |
| int64 / timestamp | 8 B |
| UUID | 16 B |
| Typical tweet-sized row | ~300 B–1 KB |
| Image (compressed) | ~200 KB–2 MB |
| 1 minute of 1080p video | ~50–100 MB |
| Embedding, 1536 dims × float32 | ~6 KB (≈1.5 KB with int8 quantization) |

Rough per-node capacity (sanity checks, not promises): a web/app server handles ~1–10K simple RPS;
a Postgres primary ~5–20K simple writes/s; a Redis node ~100K+ ops/s; a Kafka broker ~100s of MB/s.

## LLM-specific numbers

- 1 token ≈ 4 characters of English ≈ ¾ of a word. 1,000 tokens ≈ 750 words.
- Cost per request ≈ `input_tokens × price_in + output_tokens × price_out`. Output tokens usually cost 3–5× more and
  dominate latency (they're generated one at a time).
- Latency ≈ time-to-first-token (prefill, grows with prompt length) + output_tokens × time-per-output-token.
- KV-cache memory per token ≈ `2 × layers × kv_heads × head_dim × bytes`. For a 70B-class model with GQA in fp16 that's
  roughly a few hundred KB per token, so long contexts × many concurrent users exhaust GPU memory fast.

## Worked example: a URL shortener

- 100M new URLs/month → ~40 writes/s average, ~100 peak.
- Read:write = 100:1 → ~4K reads/s average, ~10K peak. Cache the hot 20% (it serves ~80% of reads).
- Storage: 100M × 12 months × 5 yrs = 6B rows × ~500 B ≈ **3 TB**. Fits a sharded KV store easily.
- Key space: base62, 7 chars → 62^7 ≈ 3.5 × 10^12 ≫ 6 × 10^9, so collisions are rare.

## Worked example: an enterprise RAG assistant

- 50K employees, 20% DAU = 10K users × 10 questions/day = 100K questions/day ≈ **1.2 QPS avg**, ~5–10 peak.
  (LLM apps are usually **cost**-bound and **GPU/token-rate**-bound, not QPS-bound.)
- Each request: ~3K input tokens (system + 5 chunks × 500 + question) + ~400 output tokens.
  Daily tokens ≈ 100K × 3.4K ≈ 340M tokens/day, so the model price per million tokens decides the budget.
- Corpus: 2M documents × 10 chunks = 20M chunks × 6 KB embeddings ≈ **120 GB of vectors** (plus text + metadata).
  Quantize or use a smaller dimension to cut memory; shard the index.
