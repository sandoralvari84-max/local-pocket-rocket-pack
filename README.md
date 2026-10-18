# local-pocket-rocket-pack

**A tuning kit for small local LLMs (1–8B).** Bring your own model; this kit bolts on swappable expert
**knowledge bases**, **tools**, and **personas** to make a small model accurate and useful on cheap hardware,
offline. Pick the expert for the task, switch when the task changes.

> Honest framing: a tuning kit upgrades the car you own — it doesn't turn a hatchback into a supercar. The model's
> size still caps its raw reasoning; everything *around* it is tuned. On a 4 GB laptop GPU, that trade is worth it.

## Why it works
Small models reason weakly but retrieve and imitate well. So instead of hoping a tiny model *knows* a field, you
hand it the right notes and tools at answer time, plus a focused persona. Result: a 4B that answers a niche question
from vetted material — and cites it — instead of guessing.

## Measured result (see [BENCHMARKS.md](BENCHMARKS.md))
30-item benchmark across all 13 niches, Qwen 4B (Q4_K_M) on a GTX 1050 Ti (4 GB), **open-book (with the kit's
knowledge bases) vs closed-book (the same model, no KB)**:

| | Grounded accuracy |
|---|---|
| Open-book (the kit) | **98.3%** |
| Closed-book (baseline) | 85.8% |
| **What the kit adds** | **+12.5 points** |

Zero filler phrases in all answers, ~9 tokens/sec. The gain concentrates where a small model misremembers —
specific thresholds, enumerations, attributions and domain specifics (e.g. WCAG touch-target size, the CIA triad,
GDPR rights went from partial/zero closed-book to 100% with the KB). Every run is logged, raw outputs kept,
reproducible with `eval/run_eval.py`. Numbers, not vibes — and sub-100% items are checked by hand (auto-scoring
under-counts valid answers). This is a 30-item set; a larger, harder set is in progress.

## The 13 experts
`webdesign` · `design` · `marketing` · `coding` · `cybersecurity` · `software` · `datascience` · `product` ·
`business` · `legal` · `health` · `finance` · `philosophy` — each with a foundations layer, an academic layer, and
worked examples (step-by-step reasoning the model imitates). Plus a `general` profile.

## What's inside
- `kb/` — the knowledge bases (one folder per niche), plain Markdown, source-cited.
- `mcp/` — dependency-free (standard-library Python) MCP tool servers: knowledge-base search (chunked retrieval),
  memory, web search + fetch, YouTube transcripts, read-only Gmail.
- `profiles.json` + `assistant.ps1` — expert profiles and the launcher that swaps them.
- `persona.md` — shared persona: a reasoning scaffold, anti-fluff concision, ~70/30 Simplified Technical English.
- `compose.assistant.yaml` — hardened llama.cpp CUDA runtime (read-only FS, localhost-only, caps dropped).
- `eval/` — the accuracy benchmark and harness.

## Requirements
- Docker Desktop (WSL 2 backend on Windows) with GPU passthrough, or any host that runs the llama.cpp CUDA image.
- A 1–8B **instruct** GGUF model.

## Choosing a model
Any 1–8B instruct GGUF works — set its filename in `profiles.json`. Good current options for a ~4 GB GPU:
- **Qwen 4B** (Q4) — strong at "answer only from the context", ~3 GB. Good default.
- **Llama 3.2 3B** — solid instruction-following, very light.
- **Gemma 3 4B** — capable, ~3 GB at Q4.
- **Phi-4-mini** — reasoning / function-calling focus.

Don't take anyone's word for it — run `eval/run_eval.py` against candidates on your own docs and pick by the numbers.

## Quickstart (Windows / PowerShell)
```powershell
# 1. Put a GGUF model where the compose file mounts models, and set its filename in profiles.json.
# 2. Load an expert:
.\assistant.ps1 webdesign      # or marketing, coding, legal, ...
# 3. Open the chat UI (localhost only):
#    http://127.0.0.1:8082
.\assistant.ps1                # list experts + what's running
.\assistant.ps1 -Stop          # stop
```
Add your own docs: drop `.md`/`.txt` files into `kb/<niche>/` — chunked retrieval picks them up, no restart.

## Safety
Content from the web, email, transcripts and files is treated as data, never instructions. Tool calls require
per-call approval in the UI. Code execution is **off** by default. Legal/health/finance knowledge carries non-advice
framing. Only test systems you own or are authorised to test.

## Status
v0.1, early. Runs today on Windows 11 + Docker Desktop + an NVIDIA 4 GB GPU. Paths assume a `dockerData`-style layout;
making it path-portable, adding chunked-retrieval tuning and a non-MCP fallback are on the roadmap.

## Licence
MIT.
