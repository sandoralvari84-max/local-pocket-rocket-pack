"""Domain-accuracy benchmark for the local assistant. Standard library only; run with python -I.

Runs every item in two modes:
  open   = the relevant niche KB docs are injected as context (the kit in use)
  closed = no KB; the model answers from its own weights (the baseline)
The open-minus-closed gap is the kit's value. For each item it records a key-point coverage score, word count,
filler count, and generation speed. Writes a results JSON and prints a summary. Usage: python -I run_eval.py
"""
import json
import os
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
KB_ROOT = r"D:\dockerData\assistant\kb"
ENDPOINT = "http://127.0.0.1:8082/v1/chat/completions"
MODEL = "assistant"
CONFIG = {"temperature": 0.2, "top_p": 0.9}  # low temp is the recommended default for grounded/factual work

SYSTEM_OPEN = ("You are a precise assistant. Answer the question using ONLY the reference material provided. "
               "Be concise and factual. If the answer is not in the material, say so.")
SYSTEM_CLOSED = ("You are a precise assistant. Answer the question from your own knowledge. "
                 "Be concise and factual. If you are not sure, say you don't know.")

FILLER = ["it's important to note", "in today's", "delve", "leverage", "seamless", "robust", "game-changing",
          "navigate the landscape", "as an ai", "it's not just", "i'd be happy to", "great question",
          "certainly", "dive into"]


def normalise(s):
    # fold unicode superscripts so e.g. O(n²) matches the key "o(n^2)"
    return (s.replace("\u00b2", "^2").replace("\u00b3", "^3")).lower()


def fluff(answer):
    low = answer.lower()
    return len(answer.split()), sum(low.count(p) for p in FILLER)


def kb_context(kb):
    folder = os.path.join(KB_ROOT, kb)
    parts = []
    for fn in sorted(os.listdir(folder)):
        if fn.endswith(".md"):
            with open(os.path.join(folder, fn), encoding="utf-8") as f:
                parts.append(f"=== {fn} ===\n{f.read()}")
    return "\n\n".join(parts)


def ask(question, context, params):
    system = (SYSTEM_OPEN + "\n\nREFERENCE MATERIAL:\n" + context) if context is not None else SYSTEM_CLOSED
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": question}],
        "chat_template_kwargs": {"enable_thinking": False},
        "max_tokens": 1024, "seed": 1, "stream": False,
    }
    payload.update(params)
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    wall = time.time() - t0
    choice = data["choices"][0]
    text = choice["message"].get("content") or choice["message"].get("reasoning_content") or ""
    tps = (data.get("timings") or {}).get("predicted_per_second")
    return text, tps, wall, choice.get("finish_reason")


def coverage(answer, keys):
    low = normalise(answer)
    hit = [k for k in keys if k in low]
    return len(hit) / len(keys), hit


def main():
    eval_set = json.load(open(os.path.join(HERE, "eval.json"), encoding="utf-8"))["items"]
    contexts = {it["kb"]: kb_context(it["kb"]) for it in eval_set}
    results = {}
    print(f"{len(eval_set)} items x 2 modes = {len(eval_set) * 2} generations\n")
    for mode in ("open", "closed"):
        results[mode] = []
        covs, tpss = [], []
        for it in eval_set:
            ctx = contexts[it["kb"]] if mode == "open" else None
            try:
                text, tps, wall, finish = ask(it["question"], ctx, CONFIG)
                cov, hit = coverage(text, it["must_include"])
            except Exception as e:
                text, tps, finish, cov, hit = f"ERROR: {e}", None, "error", 0.0, []
            nwords, nfiller = fluff(text)
            covs.append(cov)
            if tps:
                tpss.append(tps)
            results[mode].append({"id": it["id"], "kb": it["kb"], "coverage": round(cov, 2), "hit": hit,
                                  "missing": [k for k in it["must_include"] if k not in hit],
                                  "tok_s": round(tps, 1) if tps else None, "finish": finish,
                                  "words": nwords, "filler": nfiller, "answer": text})
            print(f"[{mode:6}] {it['id']:<14} {cov*100:3.0f}%  {nwords:4d}w  {round(tps,1) if tps else '?'} t/s")
        avg = sum(covs) / len(covs) * 100
        results[mode + "_summary"] = {"avg_coverage_pct": round(avg, 1),
                                      "avg_tok_s": round(sum(tpss) / len(tpss), 1) if tpss else 0,
                                      "total_filler": sum(r["filler"] for r in results[mode])}
        print(f"  -> {mode}: avg coverage {avg:.1f}%\n")
    gap = results["open_summary"]["avg_coverage_pct"] - results["closed_summary"]["avg_coverage_pct"]
    results["kit_gain_points"] = round(gap, 1)
    print(f"KIT GAIN (open - closed): {gap:+.1f} points")
    out = os.path.join(HERE, f"results-{time.strftime('%Y%m%d-%H%M%S')}.json")
    json.dump(results, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Saved:", out)


if __name__ == "__main__":
    main()
