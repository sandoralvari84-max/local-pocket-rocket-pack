# Software architecture — expert reasoning layer (how an architect thinks)

Architecture is the set of decisions that are expensive to change. The skill is deciding what to decide now and what to
defer, and naming the trade-off in every choice. Dogma ("always microservices", "never a monolith") is the opposite of the skill.

## Decision method
- State the quality attributes that matter for THIS system and rank them: latency, throughput, availability, consistency, cost, time-to-market, team cognitive load. You cannot maximise all; pick.
- Prefer the simplest architecture that meets the ranked needs; complexity is a loan repaid with interest in operations.
- Defer irreversible decisions (data model, public API, sync vs async boundaries) until the last responsible moment; make reversible ones fast.
- Name the trade-off out loud. "Event-driven for decoupling, paid for in debuggability and eventual consistency." No named cost = decision not understood.

### Worked case — "monolith or microservices?"
- Default to a modular monolith: one deployable, clear internal module boundaries. It gives most of the design benefit with none of the distributed-systems tax.
- Split a service out only when a real force demands it: independent deploy cadence, independent scaling of a hot path, team autonomy at scale, or a hard isolation/compliance boundary. "To scale" alone rarely requires it.
- The costs you take on: network failure modes, distributed transactions you cannot have (so, sagas/eventual consistency), versioned contracts, and an order-of-magnitude more ops. If you cannot staff that, do not split.
- Reversibility: a well-modularised monolith can be carved into services later; a premature mess of services is very hard to re-merge. So the monolith is the cheaper bet under uncertainty.

## Coupling, consistency, failure
- Low coupling + high cohesion is the through-line of every good decision; most "bad architecture" is hidden coupling.
- Choose your consistency explicitly: strong where correctness demands (money, inventory), eventual where availability wins. CAP is a real pick under partition, not a slogan.
- Design for failure: every remote call times out, retries (idempotently), and has a fallback. "It will be up" is not a design.

## The meta-rule
A good architecture decision record states the context, the options, the decision, and the consequences — including the ones
you dislike. An expert is calibrated about which decisions are load-bearing and which are easily changed, and spends their caution accordingly.
