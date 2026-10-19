"""Eval-CI gate: fail (exit 1) when a change regresses the kit. Standard library only; run with python -I.

Compares a CANDIDATE results file against a BASELINE and enforces:
  - coverage eval (run_eval.py output): held-out coverage must not fall more than --tol points below baseline, AND
    the kit must still beat the closed-book baseline (open > closed).
  - task eval (run_tasks.py output): efficiency must not regress — avg words and avg wall-time per task must not rise
    more than --cost-tol percent above baseline (quality on the task eval is judged separately and noted, not auto-gated).
Usage: python -I eval_gate.py --baseline <file> --candidate <file> [--tol 3.0] [--cost-tol 20]
Exit 0 = pass, 1 = regression. Intended to run in CI before shipping a KB/model/stack change."""
import argparse
import json
import sys


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def kind(d):
    if "open_summary" in d:
        return "coverage"
    if d.get("items") and "arms" in d["items"][0]:
        return "task"
    raise SystemExit("unrecognised results file: " + str(list(d.keys())[:5]))


def avg(d, arm, field):
    vals = [it["arms"][arm][field] for it in d["items"] if arm in it["arms"]]
    return sum(vals) / len(vals) if vals else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--tol", type=float, default=3.0, help="allowed held-out coverage drop, points")
    ap.add_argument("--cost-tol", type=float, default=20.0, help="allowed words/time rise, percent")
    ap.add_argument("--arm", default="kit_fast", help="task-eval arm to gate on")
    a = ap.parse_args()
    base, cand = load(a.baseline), load(a.candidate)
    k = kind(cand)
    fails = []
    if k == "coverage":
        bo = base["open_summary"]["heldout_coverage_pct"]
        co = cand["open_summary"]["heldout_coverage_pct"]
        print(f"held-out coverage: baseline {bo:.1f}  ->  candidate {co:.1f}  (tol -{a.tol})")
        if co < bo - a.tol:
            fails.append(f"held-out coverage regressed {bo:.1f} -> {co:.1f}")
        oc = cand["open_summary"]["avg_coverage_pct"]
        cc = cand["closed_summary"]["avg_coverage_pct"]
        print(f"kit vs baseline (full): open {oc:.1f} vs closed {cc:.1f}")
        if oc <= cc:
            fails.append(f"kit no longer beats closed-book ({oc:.1f} <= {cc:.1f})")
    else:
        for field in ("words", "wall_s"):
            b, c = avg(base, a.arm, field), avg(cand, a.arm, field)
            rise = (c - b) / b * 100 if b else 0.0
            print(f"{a.arm} avg {field}: baseline {b:.1f} -> candidate {c:.1f}  ({rise:+.1f}%, tol +{a.cost_tol}%)")
            if rise > a.cost_tol:
                fails.append(f"{field} rose {rise:+.1f}% (> {a.cost_tol}%)")
        print("note: task-eval QUALITY is rubric-judged separately and is not auto-gated here.")
    if fails:
        print("\nGATE: FAIL")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("\nGATE: PASS")


if __name__ == "__main__":
    main()
