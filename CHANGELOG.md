# Changelog

## v1.0.1 — 2026-10-19 (corrected release)
The clean release to adopt. Corrects a data-handling mistake in v1.0.0:
- Removed the 5 hard-47 result JSONs from the tree — they had exposed the 10 held-out items' answer keys and outputs.
- Benchmarks now publish only **aggregate** numbers for the held-out set; its per-item questions, keys and outputs are
  kept **private** so the set stays blind. Scores are framed as results on their specific test sets, not a general
  guarantee; held-out aggregates are reproducible only in a controlled/local run, not from public data.
- The 10 exposed held-out items are **retired**; a fresh blind set will be authored in v2.
- No credentials or personal data were ever involved (the exposed artifacts were evaluation Q&A on generic facts).

## v1.0.0 — 2026-10-19 (initial release — superseded by v1.0.1)
First public release of the measured mini-expert framework: 13 knowledge bases + 13 reasoning layers + the layered
quality stack (sharp retrieval, brevity, abstention, deep mode), router, tools, guardrails, and two benchmark
harnesses. **Note:** this tag's tree still contains the earlier benchmark artifacts (the hard-47 result JSONs with
the now-retired held-out items). Preserved intact as the historical record; use v1.0.1 for the corrected state.
