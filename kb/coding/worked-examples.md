# Programming — worked examples (mentor-curated, round 3: reasoning by example)

Each example shows the method: restate → retrieve facts → reason in steps → check → concise answer. Imitate this shape.

## Example 1 — "I need to find whether a list of a million IDs contains any duplicates. How?"
- Restate: detect duplicates in a large list; choose an approach and justify its cost.
- Facts (advanced.md › Data structures, Algorithms & complexity): hash tables give average O(1) lookup/insert; nested comparison is O(n²); pick the data structure before micro-optimising.
- Steps:
  1. Naïve: compare every pair → O(n²). For n = 1,000,000 that's ~10¹² operations — far too slow.
  2. Better: insert into a hash set; if an element is already present, it's a duplicate. Each insert/lookup is average O(1), so the whole pass is O(n) time, O(n) extra space.
  3. If memory is tight and you can mutate/sort: sort first (O(n log n)) then scan adjacent equal pairs (O(n)), using O(1) extra space — trades time for space.
- Check: O(n) with a set beats O(n²); the sort option is correct when memory matters. Both actually answer "any duplicates".
- Answer: Use a hash set in one pass — O(n) time, O(n) space; return true on the first already-present ID. If memory is constrained, sort then scan neighbours (O(n log n), O(1) extra).

## Example 2 — "Two threads sometimes corrupt a shared counter. Why, and how do I fix it?"
- Restate: diagnose and fix intermittent wrong results on a shared counter under threads.
- Facts (advanced.md › Concurrency): race conditions occur when threads interleave on shared state; fixes use mutual exclusion (mutex/atomic); beware deadlock's four conditions.
- Steps:
  1. `counter += 1` is not atomic: read, add, write. Two threads can read the same old value and both write old+1, losing an increment — a race condition.
  2. Fix A: make the operation atomic (an atomic integer / fetch-and-add).
  3. Fix B: guard it with a mutex/lock around the read-modify-write.
  4. If adding locks, avoid deadlock: acquire multiple locks in a consistent global order (breaks the circular-wait condition).
- Check: cause (non-atomic RMW) matches the symptom (lost updates, intermittent); both fixes serialise the update; deadlock note prevents a new bug.
- Answer: It's a race on a non-atomic read-modify-write. Use an atomic increment, or a mutex around the update; if you add multiple locks, always take them in the same order to avoid deadlock.
