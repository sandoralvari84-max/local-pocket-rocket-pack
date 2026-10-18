# Benchmarks — running log

**Principle: every test and every number is saved.** This file is append-only — never edit or delete past runs,
only add new ones. Each run also keeps its full raw output as `eval/results-<timestamp>.json` (per-item answers,
key-point coverage, tokens/sec), committed alongside this log. Reproducibility is the whole point: anyone should be
able to re-run `eval/run_eval.py` and get comparable numbers.

## Method
- Harness: `eval/run_eval.py` (standard-library Python). Benchmark set: `eval/eval.json`.
- Mode: open-book / RAG — the relevant niche KB docs are injected as context; we measure how accurately the model
  *uses* known-good knowledge (domain accuracy), plus generation speed.
- Score: `coverage` = fraction of an item's `must_include` key points present in the answer (rough auto-score);
  the mentor also reviews answers qualitatively. Each config uses a fixed `seed`.
- Record for every run: date, hardware, model + quant, GPU layers, context, sampling config, per-item coverage,
  average coverage, average tokens/sec, and the raw results filename.

## Environment (baseline)
- GPU: NVIDIA GTX 1050 Ti, 4 GB (Pascal), driver 582.78 / CUDA 13.0.
- Runtime: llama.cpp CUDA server (image pinned in `compose.assistant.yaml`), Docker Desktop / WSL2, 16 GB RAM.
- Model under test (v0.1): Qwen3.5-4B (Q4_K_M), 24 GPU layers, 16384 context, flash-attn on, q8_0 KV cache.

## Runs

### Run 001 — sampling sweep (domain accuracy) — PENDING
- Date: 2026-10-18
- Purpose: compare sampling configs (greedy t0.0, low t0.2, default t0.7) on the 6-item domain-accuracy set.
- Raw: `eval/results-<timestamp>.json`
- Results: _to be filled when the run completes._

| Config | Avg coverage | Avg tok/s |
|---|---|---|
| greedy_t0.0 | — | — |
| low_t0.2 | — | — |
| default_t0.7 | — | — |

Notes: _pending._
