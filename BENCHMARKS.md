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
  answers are also reviewed by hand, not only auto-scored. Each run uses a fixed `seed`.
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

### Run 003 — closed-book baseline vs open-book (the kit's value)
- Date: 2026-10-18. Raw: `eval/results-20261018-205307.json`. 30 items across all 13 niches.
- Model: Qwen3.5-4B Uncensored (Q4_K_M), 24 GPU layers, 16384 ctx, thinking off, temperature 0.2.
- `open` = the relevant niche KB is injected as context (the kit in use); `closed` = no KB, the model answers
  from its own weights (the baseline). The gap is what the kit adds.

| Mode | Avg coverage |
|---|---|
| Open-book (the kit) | 98.3% |
| Closed-book (baseline) | 85.8% |
| **Kit gain (open − closed)** | **+12.5 points** |

Zero filler in all 60 answers; ~9 tok/s. Where the kit matters most (closed-book the model could not recall from
weights, open-book fixed to 100%): WCAG AAA touch-target size (0→100), the CIA triad enumeration (0→100), GDPR
rights and default copyright ownership (50→100), usability-heuristic naming (67→100), funnel stages (50→100),
Big-O ordering (75→100), Core Web Vitals (83→100). The model already knew most *general* concepts cold — that is
why closed-book is a high 85.8% on this fairly standard set — so the kit's value concentrates on specific
thresholds, enumerations, attributions and domain specifics, exactly the facts a small model misremembers.

Caveats: one item (`web-elements`) scored lower open than closed — a scorer artifact ("anchor" vs the key "link"),
not a regression; it shows per-item noise and why sub-100% items are hand-checked. Next: add harder/more obscure
items where closed-book fails more, to widen and better characterise the gap (the current set is deliberately
mainstream, which understates the kit on niche facts).

### Run 004 — 5-model bake-off (which small model to ship)
- Date: 2026-10-18. Raw: `eval/results-<model>-*.json` per model. Same 30-item set as Run 003, identical settings for
  all (20 GPU layers, 8192 ctx, single-message prompt, thinking off, temp 0.2) — directly comparable to each other.

| Model | Open-book (kit) | Closed-book | Kit gain | Speed | Filler |
|---|---|---|---|---|---|
| Qwen3-4B | **92.8%** | 74.4% | +18.4 | 5.8 t/s | 0 |
| Gemma-3-4B | 89.4% | 75.3% | +14.1 | 8.5 t/s | 0 |
| Qwen3.5-4B uncensored | 88.9% | 85.8% | +3.1 | 7.8 t/s | 0 |
| Qwen3.5-4B normal | 88.3% | 88.3% | +0.0 | 6.9 t/s | 0 |
| Llama-3.2-3B | 80.3% | 67.8% | +12.5 | 10.9 t/s | 0 |

Read: **Qwen3-4B** is the most accurate with the kit (and gains most — it knows less natively). **Gemma-3-4B** is the
balanced pick (nearly as accurate, faster, on-device friendly). **Llama-3.2-3B** is the ultra-light option (fastest,
smallest, lower accuracy). The normal Qwen3.5's +0.0 is a coincidence (per-item gains and losses cancelled; 29/30
answers differ) — it is simply a strong native knower, so a mainstream-fact KB adds little to it.

**Blessed bases:** Qwen3-4B (desktop/accuracy), Gemma-3-4B (mobile/balanced default), Llama-3.2-3B (ultra-light).
Caveat: these are mainstream-fact scores; on specialist/obscure/proprietary knowledge the gains run larger (see the
specialist layer and the HARD run below).

### Run 005 — HARD 47-item set, 5-model bake-off (with a held-out honesty line)
- Date: 2026-10-19. Raw: `eval/results-hard47-<model>-*.json`. 47 items (37 derived from the kit's own KB, 10
  blind-authored **held-out** items with primary sources). Same settings across models (20 GPU layers for 4B / 12 for
  the 7B, 8192 ctx, thinking off, temp 0.2). `open` = KB injected (kit); `closed` = model's own weights.

| Model | Closed (base) | Open (kit) | Kit gain | Held-out base | Held-out +kit | **Held-out gain** |
|---|---|---|---|---|---|---|
| Llama-3.2-3B | 56.9 | 87.2 | +30.3 | 70.0 | 70.0 | 0.0 |
| Qwen2.5-7B | 71.3 | 96.8 | +25.5 | 85.0 | 95.0 | **+10.0** |
| Qwen3-4B | 72.3 | 95.7 | +23.4 | 85.0 | 90.0 | +5.0 |
| Gemma-3-4B | 73.4 | 94.7 | +21.3 | 85.0 | 85.0 | 0.0 |
| Qwen3.5-4B | 84.6 | 95.7 | +11.1 | 92.5 | 90.0 | -2.5 |

**Read this honestly.** The big full-set "kit gain" is partly circular: 37/47 items derive from the kit's own KB, so
the kit covering them is partly built in. The **held-out column is the honest measure**, and there the gain is modest
and uneven: it needs *both* room to improve *and* enough model to apply the injected material. The 7B gains most
(+10) because it can actually use the reasoning; the already-strong Qwen3.5-4B has no room (-2.5); the weak 3B cannot
exploit it (0). Takeaway: the kit's knowledge layer helps most where the model *lacks* the knowledge
(private/proprietary data, weaker models, grounding) — not on mainstream facts a capable model already knows.

### Run 006 — task-based mini-expert eval (two axes: reasoning quality AND token efficiency)
- Date: 2026-10-19. Raw: `eval/results-coding-*.json`. Harness: `eval/run_tasks.py`, set: `eval/tasks-coding.json`.
- Unlike the fact-coverage runs above, these are applied-reasoning TASKS scored on a rubric (quality), with words and
  wall-time recorded (efficiency). Model: Qwen3-4B (Q4_K_M), 24 GPU layers. Arms:
  `base` (no KB) → `kit_fast` (sharp retrieval + reasoning layer + brevity + abstention) →
  `kit_deep` (+ critique/revise) → `kit_max` (+ self-consistency + verify). 6 original tasks:

| Arm | Quality (rubric /30) | Avg words | Avg sec/task |
|---|---|---|---|
| base | 37% (11.0) | 167 | 25.3 |
| kit_fast | 78% (23.5) | 103 | 21.5 |
| kit_deep | 82% (24.5) | 95 | 43.8 |
| kit_max | 75% (22.5) | 103 | 117.7 |

**Both axes move with the cheap default (`kit_fast`): quality roughly doubles (37->78%) while using fewer tokens and
less time than `base`.** The expensive arms (`kit_deep`, `kit_max`) add little or (on this model, with v1 prompts)
regress, at 2-5x the time — so they stay as an opt-in "deep mode", kept in the stack and judged *layered* across
models in a later bake-off rather than pruned on one model's result.

After fixing two v1 defects the eval exposed (prompt leakage; whole-file retrieval dumping irrelevant sections ->
section-level retrieval), the default arm improved on the **same 6 tasks from 78% to 85%** at similar length, and
scores **79%** on the full 12-task set. The eval also surfaced concrete v2 work (retrieval bleed on a couple of
tasks; specific rubric gaps) — which is the point: additions are kept only when they move measured quality, not
because the prompts got longer.
