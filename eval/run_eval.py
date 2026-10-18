"""Domain-accuracy sampling sweep for the local assistant. Standard library only; run with python -I.

For each sampling config and each eval item: inject that niche's KB docs as context, ask the question,
record the answer, a rough key-point coverage score, and generation speed. Writes a results JSON and
prints a summary so we can compare configs. Usage:  python -I run_eval.py
"""
import json
import os
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
KB_ROOT = r"D:\dockerData\assistant\kb"
ENDPOINT = "http://127.0.0.1:8082/v1/chat/completions"
MODEL = "assistant"

CONFIGS = {
    "greedy_t0.0": {"temperature": 0.0},
    "low_t0.2": {"temperature": 0.2, "top_p": 0.9},
    "default_t0.7": {"temperature": 0.7, "top_p": 0.95},
}

SYSTEM = ("You are a precise assistant. Answer the question using ONLY the reference material provided. "
          "Be concise and factual. If the answer is not in the material, say so.")


def kb_context(kb):
    folder = os.path.join(KB_ROOT, kb)
    parts = []
    for fn in sorted(os.listdir(folder)):
        if fn.endswith(".md"):
            with open(os.path.join(folder, fn), encoding="utf-8") as f:
                parts.append(f"=== {fn} ===\n{f.read()}")
    return "\n\n".join(parts)


def ask(question, context, params):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM + "\n\nREFERENCE MATERIAL:\n" + context},
            {"role": "user", "content": question},
        ],
        "max_tokens": 450, "seed": 1, "stream": False,
    }
    payload.update(params)
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    wall = time.time() - t0
    msg = data["choices"][0]["message"]
    text = msg.get("content", "") or ""
    tps = (data.get("timings") or {}).get("predicted_per_second")
    return text, tps, wall


def coverage(answer, keys):
    low = answer.lower()
    hit = [k for k in keys if k in low]
    return len(hit) / len(keys), hit


def main():
    eval_set = json.load(open(os.path.join(HERE, "eval.json"), encoding="utf-8"))["items"]
    contexts = {it["kb"]: kb_context(it["kb"]) for it in eval_set}
    results = {}
    print(f"Running {len(eval_set)} items x {len(CONFIGS)} configs = {len(eval_set)*len(CONFIGS)} generations\n")
    for cname, params in CONFIGS.items():
        results[cname] = []
        covs, tpss = [], []
        for it in eval_set:
            try:
                text, tps, wall = ask(it["question"], contexts[it["kb"]], params)
                cov, hit = coverage(text, it["must_include"])
            except Exception as e:
                text, tps, wall, cov, hit = f"ERROR: {e}", None, None, 0.0, []
            covs.append(cov)
            if tps:
                tpss.append(tps)
            results[cname].append({"id": it["id"], "kb": it["kb"], "coverage": round(cov, 2),
                                   "hit": hit, "missing": [k for k in it["must_include"] if k not in hit],
                                   "tok_s": round(tps, 1) if tps else None, "answer": text})
            print(f"[{cname}] {it['id']:<14} coverage {cov*100:3.0f}%  {round(tps,1) if tps else '?'} tok/s")
        avg_cov = sum(covs) / len(covs) * 100
        avg_tps = sum(tpss) / len(tpss) if tpss else 0
        print(f"  -> {cname}: avg coverage {avg_cov:.0f}%, avg {avg_tps:.1f} tok/s\n")
        results[cname + "_summary"] = {"avg_coverage_pct": round(avg_cov), "avg_tok_s": round(avg_tps, 1)}
    out = os.path.join(HERE, f"results-{time.strftime('%Y%m%d-%H%M%S')}.json")
    json.dump(results, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Saved:", out)


if __name__ == "__main__":
    main()
