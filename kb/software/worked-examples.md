# Software engineering — worked examples (mentor-curated, round 3: reasoning by example)

Method: restate → retrieve facts → reason in steps → check → concise answer.

## Example 1 — "Our deploys keep breaking production. How do we make releases safer?"
- Restate: reduce production incidents caused by releases.
- Facts (advanced.md › Delivery & operations): trunk-based dev, feature flags, blue-green/canary, automated rollback; DORA metrics (change failure rate, time to restore).
- Steps:
  1. Gate every merge on a green automated build + tests (CI) so broken code can't reach main.
  2. Ship behind feature flags so release ≠ deploy; turn features on gradually.
  3. Roll out with canary or blue-green and automatic rollback on error-rate/latency breach.
  4. Track change failure rate and time-to-restore to see if it's improving.
- Check: each step attacks a cause (bad code merged, big-bang release, no safe undo, no measurement); consistent with the KB.
- Answer: Enforce CI gates, release behind feature flags, roll out canary/blue-green with automated rollback, and measure change-failure-rate and time-to-restore to confirm it's working.

## Example 2 — "A service is intermittently slow. Where do we start?"
- Restate: diagnose intermittent latency without guessing.
- Facts (advanced.md › Observability): logs, metrics, traces; SLIs/SLOs; alert on symptoms; find the bottleneck before optimising.
- Steps:
  1. Look at metrics for the latency percentiles (p95/p99), not the average — intermittent spikes hide in the tail.
  2. Use distributed traces to find which span/downstream call is slow (DB query, external API, lock contention).
  3. Correlate with logs and resource metrics at the spike times.
  4. Fix the proven bottleneck; re-measure.
- Check: method is measure → localise → fix → re-measure, not speculate; matches "measure before optimising".
- Answer: Start from tail-latency metrics (p95/p99), use traces to localise the slow span, confirm with logs at those timestamps, fix that bottleneck, then re-measure. Don't optimise on a guess.
