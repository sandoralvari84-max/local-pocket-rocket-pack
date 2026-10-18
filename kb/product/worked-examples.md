# Product management — worked examples (mentor-curated, round 3: reasoning by example)

Method: restate → retrieve facts → reason in steps → check → concise answer.

## Example 1 — "Sales wants a custom feature for one big prospect. Do we build it?"
- Restate: decide on a one-client feature request.
- Facts (foundations › prioritisation, build trap; advanced.md › prioritisation, strategy): outcomes over outputs; RICE; avoid the feature factory; strategic fit.
- Steps:
  1. Separate the underlying need from the asked-for solution (jobs-to-be-done). Is the need common to many customers, or unique to this one?
  2. Score it: Reach (how many benefit), Impact, Confidence, Effort (RICE); check fit with strategy.
  3. If it's broadly useful and on-strategy, prioritise it. If it's one-off, consider a paid services/custom path, not core roadmap.
  4. Guard against the build trap: one big logo is not automatically worth the opportunity cost.
- Check: decision follows from reach/fit/opportunity-cost, not just deal size; matches the KB.
- Answer: Only if the need is shared by many customers and fits strategy (score it with RICE). If it's unique to this client, handle it as custom/paid work, not core roadmap — don't let one deal drive the product.

## Example 2 — "How do we know if we have product-market fit?"
- Restate: determine whether PMF exists, with evidence.
- Facts (advanced.md › Metrics & experimentation): retention curve flattening; Sean Ellis 40% test; cohorts, not signups.
- Steps:
  1. Signups and downloads are vanity — look at retention cohorts over time.
  2. If the retention curve flattens (a stable core keeps using it), that's the clearest PMF signal; if it decays to zero, no fit.
  3. Cross-check with the Sean Ellis test: ≥ 40% of users would be "very disappointed" without the product.
- Check: uses retention + survey signal rather than top-of-funnel vanity; matches the KB.
- Answer: Measure cohort retention — a flattening curve plus ≥ 40% "very disappointed" on the Sean Ellis test indicates PMF. Growing signups with decaying retention means you don't have it yet.
