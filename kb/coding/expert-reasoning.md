# Coding — expert reasoning layer (how an expert thinks, not what they know)

This layer teaches the *method* of expert problem-solving, not facts. Imitate the approach: form a hypothesis from
evidence, test the cheapest one first, and verify before concluding. "I don't know yet, here's how I'd find out" beats
a confident guess.

## Debugging methodology (the core skill)
- Reproduce reliably first. A bug you can't trigger on demand, you can't fix with confidence.
- Read the actual error and stack trace top to bottom; the first line is often a symptom, the cause is lower.
- Bisect: halve the search space each step (git bisect, comment out halves, binary-search inputs). Don't read all the code.
- Change ONE thing at a time; revert what didn't help. Keep a hypothesis log so you don't loop.
- "It works on my machine" = an environment difference: versions, config, data, timezone, locale, permissions. Diff them.
- The bug is usually in your code, not the compiler/library/OS — assume that until proven otherwise.

### Worked case — intermittent 500s under load, fine in staging
- Evidence: fails only in prod, only at peak, ~1% of requests, no stack trace in app logs.
- Hypotheses, cheapest first: (1) a downstream timeout under load; (2) connection-pool exhaustion; (3) a race on shared state.
- Test (1)/(2) first — free from metrics: check DB connection-pool saturation and downstream p99 latency at peak. Pool
  at 100% with requests queuing → exhaustion. Fix: raise pool size *and* find the leak (unclosed connections / slow
  queries holding them). Verify by watching pool utilization after the change, not by "it feels better."
- Only if pool is healthy do you chase the harder race hypothesis. Order matters: eliminate cheap explanations first.

## Performance methodology
- Measure before optimizing; the bottleneck is rarely where you'd guess. Profile, read the flame graph, find the top cost.
- Optimize the proven hot path only; a 10x speedup on 2% of runtime is noise.
- Know the order of magnitude: memory ns, SSD µs, network ms. An N+1 query (100 × 1ms round-trips) dwarfs any CPU micro-opt.
- Fix the algorithm/data-structure before micro-optimizing; O(n²)→O(n) beats hand-tuned O(n²).

### Worked case — a report endpoint got slow as data grew
- Measure: the endpoint spends 90% of time in the DB, issuing one query per row (N+1). CPU and serialization are fine.
- Decide: a single JOIN/batched query replaces the loop; add an index on the filter/join column. Caching is premature
  until the query itself is sane.
- Verify: EXPLAIN shows an index scan not a seq scan; p95 latency drops; re-check at 10x data to confirm it scales.

## Design-decision reasoning (trade-offs, not dogma)
- State the forces: read/write ratio, scale, consistency needs, team size, deadline, reversibility.
- Prefer the simplest thing that could work; you can extract complexity later, but you can't easily un-distribute a system.
- Name what you're trading. "Microservices for independent deploys, paid for in distributed-systems complexity" — if you
  can't name the cost, you haven't understood the choice.
- Optimize for the reader and for change; code is read and modified far more than written.

### Worked case — "should we add a cache here?"
- Forces: the data is read 1000x more than written, slightly stale is acceptable, the source query is expensive.
- Reasoning: high read:write + staleness-tolerant + expensive source = a strong cache candidate. The hard part is
  invalidation — decide the strategy (TTL vs write-through) up front, and a wrong answer is cheap to detect (stale reads).
- Decision: TTL cache with a short expiry, measured hit rate; revisit if staleness complaints appear. Don't cache first —
  confirm the query is already as fast as it reasonably can be (indexes) so you're not caching a fixable problem.

## Reviewing code like an expert
- Correctness and edge cases first (empty, null, boundary, concurrent, failure), then design, then style — in that order.
- Ask "what happens when this fails?" at every I/O boundary. Untrusted input, missing error handling, and resource leaks
  are the high-value findings; nitpicks are not.
- A good review leaves the author knowing *why*, not just *what* to change.

## The meta-rule
An expert is calibrated: confident where the evidence supports it, explicit about uncertainty elsewhere, and able to
say how they'd resolve the uncertainty. That calibration — not a bigger pile of facts — is the expertise.
