# Local Expert Pack (working title)

Turn a small local LLM (1–8B) into a set of **swappable domain experts** on modest hardware.
One base model + a swappable **knowledge base**, **persona**, and **tools** per niche — pick the expert for the task,
switch when the task changes. Built to run on a cheap laptop GPU, offline, with per-call tool approval.

> Status: **v0.1, early.** It runs today on the author's setup (Windows 11 + Docker Desktop + an NVIDIA GTX 1050 Ti,
> 4 GB). Paths currently assume a `dockerData` layout (see below) — making it path-portable is on the roadmap.
> This is a work in progress shared in the open; expect rough edges.

## Idea
Small models reason weakly but imitate and retrieve well. So instead of making a tiny model *know* everything,
you give it **the right notes and tools at answer time** and a focused persona. A 4B with a good knowledge base and
a verifier can beat a much larger general model *on its niche* — the specialist-on-a-drag-strip effect. This pack is
the machinery to do that, plus a benchmark to prove whether a given tweak actually helped.

## What's inside
- `mcp/` — dependency-free (standard-library Python) MCP tool servers:
  - `kb_server.py` — swappable knowledge bases (list / use / search / read), keyword retrieval, no vector DB.
  - `memory_server.py` — durable per-user memory (remember / recall / list / forget).
  - `web_server.py` — web search (keyless multi-engine: Mojeek → DuckDuckGo → Bing; optional Brave/SearXNG) + page fetch, with SSRF guards.
  - `youtube_server.py` — video transcripts via yt-dlp.
  - `gmail_server.py` — **read-only** Gmail (IMAP), opt-in.
  - `mcp_stdio.py` — shared MCP/JSON-RPC loop + HTML-to-text helper.
- `kb/` — mentor-curated, source-cited knowledge bases for 13 niches (foundations + an academic layer each).
- `profiles.json` + `assistant.ps1` — the expert profiles and the launcher that swaps them.
- `compose.assistant.yaml` — the runtime (llama.cpp CUDA server, hardened: read-only FS, localhost-only, caps dropped).
- `persona.md` — the shared base persona (tool rules, safety, research pipeline).
- `eval/` — the domain-accuracy benchmark (`eval.json`) and harness (`run_eval.py`).
- `BENCHMARKS.md` — the running results log. Every tweak is measured here.

## Requirements
- Docker Desktop (WSL 2 backend on Windows) with GPU passthrough, or any host that can run the llama.cpp CUDA image.
- An NVIDIA GPU (tested on a 4 GB Pascal card) or adjust for CPU-only.
- A GGUF model (any 1–8B instruct model) placed where the compose file mounts models.

## Runtime data (created locally, **not** in this repo)
`memory/`, `workspace/`, `logs/`, `cache/`, `models/`, `bin/`, and `secrets/*.env` are machine-specific and/or private,
and are git-ignored. Copy `secrets/*.env.example` to `secrets/*.env` and fill in to enable web/Gmail options.

## Safety
Content from the web, email, transcripts and files is treated as data, never instructions. Tool calls require
per-call approval in the web UI. Code execution is **off** by default. Legal/health/finance knowledge carries
non-advice framing. Only test systems you own or are authorised to test.

## Licence
MIT (see LICENSE).

## Roadmap
Path-portable config · chunked retrieval for small context windows · a non-MCP fallback · a `models.json`
(recommended GPU-layers/context per model & VRAM) · optional calculator/verifier tool · per-domain LoRA adapters.
