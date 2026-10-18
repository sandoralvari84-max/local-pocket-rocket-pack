# Prompt packs — the mobile / no-install edition

Each file here is a self-contained **expert prompt**: a persona plus that niche's vetted, source-cited knowledge,
condensed to ~1,000 tokens so it fits on a phone. No Docker, no server, no install — it works in any local-LLM app.

## Use it on a phone (or anywhere)
1. Install a local-LLM app and load a small model (Gemma, Qwen or Llama, ~2–3 GB at Q4):
   - Android: **PocketPal**, **ChatterUI**, or **Google AI Edge Gallery** (built for Gemma).
   - Desktop: LM Studio, Jan, or the full kit in this repo.
2. Open the pack for your task (e.g. `coding.md`), copy everything **below the dashed line**, and paste it into the
   app's **system prompt** (or send it as your first message).
3. Ask your question. The model answers from the embedded reference knowledge — offline, private.

## What you get vs the full kit
- Prompt packs = the knowledge, by hand, on any device. Most of the value, zero setup.
- The full kit (this repo) adds automatic retrieval across the complete knowledge bases, tools (web, files,
  memory), and the profile launcher — on a desktop with Docker.

## Packs
13 experts: webdesign, design, marketing, coding, cybersecurity, software, datascience, product, business, legal,
health, finance, philosophy. Legal/health/finance are general education, not professional advice.

Regenerate from the knowledge bases anytime; these are built directly from `kb/`.
