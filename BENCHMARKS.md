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

### Run 001 — sampling sweep — INVALID (harness bug; kept for the record)
- Date: 2026-10-18. Raw: `eval/results-20261018-193745.json`.
- Bug: the harness capped `max_tokens` at 450 and read only `message.content`. Qwen's hidden "thinking"
  consumed the budget, so many answers returned empty → false low scores (17% / 17% / 31%). This was a
  measurement fault, not a model result. Logged, not deleted — every number is saved, including the broken ones.
- Fix applied for Run 002: disable the model's thinking for the eval (facts are already in-context, so no chain
  of thought is needed), raise `max_tokens` to 1024, and record `finish_reason`.

### Run 002 — sampling sweep (domain accuracy) — VALID
- Date: 2026-10-18. Raw: `eval/results-20261018-194350.json`.
- Setup: Qwen3.5-4B (Q4_K_M), 24 GPU layers, 16384 ctx, flash-attn, q8_0 KV; thinking off; 6-item set; open-book
  (relevant KB docs injected as context, chunked retrieval in the live tool).

| Config | Avg coverage (auto) | Avg words | Filler phrases | Avg tok/s |
|---|---|---|---|---|
| greedy_t0.0 | 90% | 59 | 0 | 9.0 |
| low_t0.2 | 90% | 57 | 0 | 8.7 |
| default_t0.7 | 100% | 65 | 0 | 8.8 |

Verification (manual): the only sub-100% items (`code-bigo`, `sec-owasp` at greedy/low) were checked by hand and are
**correct answers** the auto-scorer missed — `code-bigo` wrote `O(n²)` (superscript) vs the scorer's literal
`o(n^2)`; `sec-owasp` named three valid OWASP risks with correct defences, just not the exact trio the key list
required. **True domain accuracy ≈ 100% across all three configs.** Zero filler in all 18 answers (concision rules
holding). Speed ~9 tok/s.

Takeaways:
- RAG + chunked retrieval + direct answers (thinking off) gives near-perfect grounded accuracy on this set at ~9 tok/s.
- Sampling: `default_t0.7` edged highest here, but greedy/low are effectively tied and deterministic. For
  factual/grounded work, low temperature (0.0–0.2) is the safer default; keep it per-task.
- Scorer lesson: substring key-lists under-count correct answers (formatting, valid alternatives). Treat auto-coverage
  as a screen; confirm sub-100% items by hand. Next: expand the set with more and harder items, plus some closed-book
  items to separate "knowledge in weights" from "retrieval".
