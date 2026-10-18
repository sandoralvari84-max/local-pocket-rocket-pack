# Programming / CS — advanced / academic layer (mentor-curated, round 2)

Builds on coding-foundations.md. Core computer-science depth.

## Data structures
- Arrays, linked lists, stacks, queues, deques; hash tables (average O(1) lookup, collision handling).
- Trees: binary search trees, balanced trees (AVL, red-black), heaps (priority queues), tries; B-trees for disk/databases.
- Graphs: adjacency list vs matrix; traversals BFS/DFS; shortest path (Dijkstra, Bellman-Ford), MST (Kruskal, Prim).

## Algorithms & complexity
- Asymptotics: Big-O (upper), Ω (lower), Θ (tight); time and space; worst/average/amortised (e.g. dynamic array push is amortised O(1)).
- Sorting: mergesort/heapsort O(n log n) worst case; quicksort O(n log n) average, O(n²) worst; comparison-sort lower bound Ω(n log n).
- Paradigms: divide and conquer, greedy, dynamic programming (optimal substructure + overlapping subproblems), backtracking.
- Tractability: P vs NP; NP-complete problems (SAT, TSP decision) have no known polynomial solution — use heuristics/approximation.

## Concurrency & parallelism
- Concurrency (structure) vs parallelism (simultaneous execution); processes vs threads vs async I/O.
- Hazards: race conditions, deadlock (mutual exclusion, hold-and-wait, no preemption, circular wait), starvation, livelock.
- Primitives: mutexes, semaphores, condition variables, atomics; higher-level: message passing, actors, async/await event loops.

## Memory & runtime
- Stack (frames, automatic) vs heap (dynamic); pointers/references; fragmentation.
- Management models: manual (C/C++), garbage collection (tracing, reference counting), ownership/borrowing (Rust).

## Systems, data & distributed
- Databases: ACID, transaction isolation levels (read committed → serializable), indexing (B-tree/hash), normalization vs denormalization.
- Distributed: CAP theorem (consistency, availability, partition tolerance — pick trade-offs under partition), eventual consistency, idempotency, retries/backoff.
- Caching layers and invalidation; the two hard problems: naming, cache invalidation, and off-by-one errors.

## Design & architecture
- Layered, hexagonal/ports-and-adapters, event-driven, microservices vs monolith trade-offs.
- Domain-Driven Design: bounded contexts, ubiquitous language; API design: REST semantics, idempotency, versioning, pagination.
- Type systems: static vs dynamic, strong vs weak, parametric polymorphism/generics, sum/union types.

## Sources (authoritative / canonical)
- Cormen et al., "Introduction to Algorithms" (CLRS) (textbook)
- Python docs — https://docs.python.org/3/ ; MDN JS — https://developer.mozilla.org/en-US/docs/Web/JavaScript
- Martin Fowler — https://martinfowler.com/
- "Designing Data-Intensive Applications", Martin Kleppmann (book)
