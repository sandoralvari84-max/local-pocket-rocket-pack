# Software engineering — specialist layer (precise facts and hard truths)

The exact definitions and the distributed-systems realities models gloss over.

## Distributed systems truths
- **CAP**: under a network partition you choose consistency OR availability — not "pick 2 of 3" in normal operation.
  PACELC extends it: Else (no partition) you trade Latency vs Consistency. Most systems are AP or CP by design.
- **Exactly-once delivery is impossible** over an unreliable network. Build at-least-once + idempotent consumers, or
  effectively-once via dedup keys.
- Consistency models: strong (linearizable) → sequential → causal → eventual. "Eventually consistent" means stale
  reads are possible; design the UX for it.
- The fallacies of distributed computing still bite: the network is NOT reliable, latency is NOT zero, bandwidth is
  NOT infinite, topology changes.

## Definitions models blur
- **SOLID**: Single-responsibility (one reason to change), Open/closed (extend without modifying), Liskov (subtypes
  substitutable), Interface-segregation (small interfaces), Dependency-inversion (depend on abstractions).
- **Idempotent** ≠ **safe**: GET is both; PUT/DELETE are idempotent but not safe; POST is neither.
- **Coupling vs cohesion**: aim for low coupling (modules independent) and high cohesion (a module does one thing).
- **DORA's four**: deployment frequency, lead time for changes, change failure rate, time to restore. Elite teams
  deploy often with low failure rate — speed and stability correlate, they don't trade off.

## Patterns and their costs
- Design patterns are a vocabulary, not a goal; forcing them adds accidental complexity. Microservices buy
  independent deploys at the cost of distributed-systems pain — a modular monolith is the right default for most teams.
- Premature abstraction (DRY applied too early) couples unrelated things; "a little duplication is cheaper than the
  wrong abstraction."

## Testing & ops realities
- 100% coverage proves code *ran*, not that it's *correct*; weak assertions give false confidence.
- SLOs need error budgets; alert on user-facing symptoms (latency/errors), not on causes (CPU) — cause-alerts page you
  for non-problems.
- Observability = logs + metrics + traces; you can't debug what you can't see.

## Sources
- "Designing Data-Intensive Applications" (Kleppmann); Google SRE Book — https://sre.google/books/
- "Accelerate"/DORA — https://dora.dev/ ; Martin Fowler — https://martinfowler.com/
