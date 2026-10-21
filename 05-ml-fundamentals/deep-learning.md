# Deep learning

## Backpropagation

Chain rule applied backward through the computation graph; each node computes the local gradient × the upstream gradient.
Cost ≈ 2× the forward pass. Autodiff frameworks build the graph and handle this.

**Vanishing/exploding gradients:** repeated multiplication through many layers/time steps. Fixes: ReLU-family activations,
careful init (He for ReLU, Xavier/Glorot for tanh), **residual connections**, normalization, gradient clipping (for exploding), LSTM/GRU gates (for RNNs).

## Activations

ReLU (cheap, sparse; dead neurons) · Leaky ReLU · GELU / SiLU (Swish) (smooth; standard in transformers) ·
SwiGLU (gated; used in most modern LLM MLPs) · sigmoid/tanh (gates, outputs) · softmax (multiclass outputs, attention weights).

## Optimizers

- **SGD + momentum:** accumulates velocity; generalizes well; needs LR tuning.
- **Adam:** per-parameter adaptive LR from first/second moment estimates, with bias correction. **AdamW** decouples weight decay (the standard for transformers).
- LR schedules: **warmup** (stabilizes early training, especially for Adam + transformers) then cosine or linear decay.
- Batch size vs LR: larger batches typically need a larger LR (roughly linear scaling, up to a point).
- Mixed precision (bf16/fp16 + fp32 master weights) for speed/memory; bf16 has fp32's range, so no loss scaling is needed.

## Normalization

- **BatchNorm:** normalize over the batch per feature; behaves differently in train vs eval; poor for small batches and sequences.
- **LayerNorm:** normalize over features per example; the standard in transformers. **RMSNorm:** skips mean-centering; cheaper; used by Llama-family models.
- **Pre-norm** (normalize before attention/MLP, inside the residual) trains more stably for deep transformers than post-norm.

## Regularization

Dropout (randomly zero activations; scale at train time), weight decay, data augmentation, early stopping,
label smoothing, stochastic depth, mixup.

## Architectures (one line each)

- **CNN:** local receptive fields + weight sharing → translation equivariance; pooling → some invariance. ResNet (skip connections), EfficientNet (scaling).
- **RNN / LSTM / GRU:** sequential state; gates control memory; hard to parallelize, so transformers replaced them for most NLP.
- **Transformer:** self-attention over all positions in parallel; see [transformers-and-llms.md](transformers-and-llms.md).
- **Vision Transformer (ViT):** image patches as tokens. **Diffusion models:** learn to denoise; generate by iterative denoising.
- **Mixture of Experts (MoE):** a router sends each token to the top-k of many expert MLPs, so there are more total parameters at a similar
  compute per token; challenges are load balancing and memory.

## Embeddings and representation learning

- Embedding = a learned dense vector where geometry encodes similarity.
- **Two-tower models:** separate encoders for query/user and item; dot product similarity; items pre-computed into an ANN index.
- **Contrastive learning** (SimCLR, CLIP, sentence embeddings): pull positives together, push negatives apart (InfoNCE loss);
  **in-batch negatives** are cheap; **hard negatives** improve quality.
- Cross-encoder vs bi-encoder: a cross-encoder jointly encodes (query, doc) for accurate scores but can't precompute, so it's used for re-ranking.

## Training at scale (know the vocabulary)

- **Data parallel** (replicate the model, split the batch; all-reduce gradients). **FSDP / ZeRO** shard optimizer states, gradients, and parameters across GPUs.
- **Tensor parallel** (split matrices within layers), **pipeline parallel** (split layers across GPUs; micro-batches to fill the bubble).
- Gradient accumulation (simulate larger batches), activation checkpointing (recompute activations to save memory).
- Memory for training with Adam ≈ 16–20 bytes/param in mixed precision (weights, gradients, two moments, fp32 master copy) + activations.

## Debugging a model that won't train

1. Overfit a single small batch first (it should reach ~0 loss).
2. Check data and labels (shuffling, preprocessing mismatch, label leakage).
3. LR range test; check for NaNs (LR too high, log(0), fp16 overflow).
4. Monitor gradient norms per layer; check initialization.
5. Compare against a simple baseline to make sure the model beats it.
