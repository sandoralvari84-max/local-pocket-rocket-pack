# Software engineering — advanced / academic layer (mentor-curated, round 2)

Builds on software-engineering.md.

## Architecture
- Quality attributes ( "-ilities"): performance, scalability, availability, security, maintainability, observability — they trade off; make trade-offs explicit.
- Styles: layered, hexagonal (ports & adapters), event-driven, microservices vs modular monolith (Conway's Law: systems mirror org communication).
- 12-factor app principles for cloud services; statelessness, config in environment, disposability.
- Distributed systems: CAP and PACELC, consensus (Raft/Paxos), idempotency, sagas for distributed transactions, backpressure.

## Domain-driven design
- Strategic: bounded contexts, context maps, ubiquitous language. Tactical: entities, value objects, aggregates, repositories, domain events.
- CQRS and event sourcing where read/write models diverge; beware accidental complexity.

## Testing (depth)
- Test doubles: dummy, stub, fake, spy, mock. Property-based testing; mutation testing to measure suite strength; contract tests between services.
- Flaky tests erode trust; isolate, make deterministic; test behaviour via public interfaces.

## Delivery & operations
- Trunk-based development, feature flags, blue-green and canary releases, progressive rollout + automated rollback.
- DORA / "Accelerate" metrics: deployment frequency, lead time for changes, change failure rate, time to restore — predict performance.
- Observability: logs, metrics, traces; SLIs/SLOs/SLAs and error budgets (Google SRE); alert on symptoms, not causes.

## Engineering discipline
- Estimation (reference-class, story points, #NoEstimates debate); manage technical debt deliberately (register, pay down).
- Code review for correctness, design and readability; small PRs; definition of done.
- Documentation: ADRs (architecture decision records), READMEs, runbooks.

## Sources (authoritative)
- Martin Fowler — https://martinfowler.com/
- Google SRE Book — https://sre.google/books/
- "Accelerate" (Forsgren, Humble, Kim) / DORA — https://dora.dev/
- "Designing Data-Intensive Applications", Kleppmann (book)
- The Twelve-Factor App — https://12factor.net/
