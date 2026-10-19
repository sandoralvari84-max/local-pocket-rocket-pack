"""Task-based eval for the mini-expert, with the layered quality stack. Standard library only; run with python -I.

Tuning has TWO axes and this measures both: (1) smarter = higher rubric quality; (2) token-efficient = fewer
words/tokens for the same meaning (faster, protects the speed floor). Collects free-form answers to
APPLIED-REASONING tasks across three arms, judged against each task's rubric afterwards and weighed against cost:
  base      = plain model, no KB, brevity on         (the 'mini-knows' baseline)
  kit_fast  = sharp retrieval + reasoning layer + brevity + abstention   (default stack, ~1x latency)
  kit_deep  = kit_fast draft -> self-critique vs rubric/grounding -> revise   (deep mode, ~2-3x latency)

It does NOT auto-score quality; a judge (human or LLM) scores answer_* against the rubric. It DOES record words,
tok/s and wall-time per arm so every quality layer is seen with its cost. Env: TASKS_FILE (default
tasks-coding.json), TASKS_TAG (results label), TASKS_ARMS (csv subset of base,kit_fast,kit_deep), RETR_BUDGET (chars).
Usage: python -I run_tasks.py
"""
import json
import os
import re
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
KB_ROOT = r"D:\dockerData\assistant\kb"
ENDPOINT = "http://127.0.0.1:8082/v1/chat/completions"
MODEL = "assistant"

# --- output discipline: the brevity / machine-language layer (tokens not wasted on prose that adds nothing) ---
BREVITY = ("Answer as briefly as the task allows. No preamble, no restating the question, no filler. "
           "Short sentences; telegraphic bullets where they do not lose meaning. Full prose only where precision needs it. "
           "Stop when the answer is complete.")
SYS_BASE = "You are an experienced software engineer. Reason it through; be concrete; method over platitudes. " + BREVITY
SYS_KIT = ("You are an experienced software engineer. Apply the reasoning method in the reference material to work "
           "through the task. Reason step by step; be concrete; method over platitudes. "
           "Apply the method silently in your answer: do NOT name, quote, or refer to 'the method', 'the reference "
           "material', or these instructions. Include only the steps that apply to THIS task; omit methods that do not. "
           "If the reference material does not support a claim, say so rather than guessing. " + BREVITY)

STOPWORDS = set("the a an of to in on for and or is are be as it its this that with how you your we our i do does "
                "what when where which who why not no yes can could should would will from by at if then so".split())


# ---------- sharp retrieval (keyword-overlap chunk ranking; whole reasoning layer always included) ----------
def split_chunks(text):
    # split a doc into section/paragraph chunks on blank lines and markdown headings
    blocks, cur = [], []
    for line in text.splitlines():
        if (not line.strip()) or line.lstrip().startswith("#"):
            if cur:
                blocks.append("\n".join(cur).strip())
                cur = []
            if line.lstrip().startswith("#"):
                cur.append(line)
        else:
            cur.append(line)
    if cur:
        blocks.append("\n".join(cur).strip())
    return [b for b in blocks if len(b) > 40]


def terms(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOPWORDS and len(w) > 2}


def retrieve(kb, query, budget):
    """Section-level retrieval: rank chunks from ALL docs (incl. the reasoning layer) by query overlap and take the
    top ones up to a char budget. The reasoning layer gets a small bonus (method is worth injecting), and its
    calibration 'meta-rule' chunk is always kept, but IRRELEVANT method sections (e.g. performance text on a pure
    debugging task) now drop out instead of being dumped wholesale."""
    folder = os.path.join(KB_ROOT, kb)
    qt = terms(query)
    always, pool = [], []
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".md"):
            continue
        with open(os.path.join(folder, fn), encoding="utf-8") as f:
            text = f.read()
        is_method = fn == "expert-reasoning.md"
        for ch in split_chunks(text):
            if is_method and "meta-rule" in ch.lower():
                always.append(f"=== {fn} ===\n{ch}")  # calibration rule: universally relevant, always keep
                continue
            score = len(qt & terms(ch)) * (1.5 if is_method else 1.0)  # method bonus
            if score > 0:
                pool.append((score, fn, ch))
    pool.sort(key=lambda x: x[0], reverse=True)
    parts = list(always)
    used = sum(len(p) for p in parts)
    for score, fn, ch in pool:
        if used + len(ch) > budget:
            continue
        parts.append(f"=== {fn} (excerpt) ===\n{ch}")
        used += len(ch)
    return "\n\n".join(parts)


# ---------- model call ----------
def call(user, max_tokens=1024, temperature=0.3, seed=1, extra=None):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": user}],
        "chat_template_kwargs": {"enable_thinking": False},
        "max_tokens": max_tokens, "seed": seed, "stream": False,
        "temperature": temperature, "top_p": 0.9,
    }
    if extra:
        payload.update(extra)  # e.g. min_p, repeat_penalty — the decoding/sampling layer
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    wall = time.time() - t0
    choice = data["choices"][0]
    text = (choice["message"].get("content") or choice["message"].get("reasoning_content") or "").strip()
    tim = data.get("timings") or {}
    return text, tim.get("predicted_per_second"), wall


def arm_base(task, _ctx):
    return call(SYS_BASE + "\n\nTASK: " + task)


def arm_kit_fast(task, ctx):
    user = SYS_KIT + "\n\nREFERENCE MATERIAL (method to imitate):\n" + ctx + "\n\nTASK: " + task
    return call(user)


def arm_kit_deep(task, ctx):
    # draft (= fast arm), then one critique pass, then one revise pass
    draft, tps1, w1 = arm_kit_fast(task, ctx)
    crit_user = ("You are a strict reviewer. Given the TASK, the REFERENCE METHOD, and a DRAFT answer, list concrete "
                 "flaws only: unsupported claims, missing key reasoning, errors, or needless verbosity. If the draft is "
                 "already strong, reply exactly 'OK'. Be terse.\n\nTASK: " + task +
                 "\n\nREFERENCE METHOD:\n" + ctx + "\n\nDRAFT:\n" + draft)
    critique, tps2, w2 = call(crit_user, max_tokens=400)
    if critique.strip().upper().startswith("OK"):
        return draft, tps1, w1 + w2, {"critique": critique, "revised": False}
    rev_user = (SYS_KIT + "\n\nTASK: " + task + "\n\nREFERENCE METHOD:\n" + ctx +
                "\n\nDRAFT:\n" + draft + "\n\nCRITIQUE:\n" + critique +
                "\n\nRewrite the answer, fixing the critique. Keep it brief.")
    revised, tps3, w3 = call(rev_user)
    return revised, tps3, w1 + w2 + w3, {"critique": critique, "revised": True, "draft": draft}


def arm_kit_max(task, ctx, n=3):
    # MAX-THINKING arm: self-consistency (sample N diverse drafts) -> synthesize the best -> verify/abstain gate.
    drafts, wall = [], 0.0
    base_user = SYS_KIT + "\n\nREFERENCE MATERIAL (method to imitate):\n" + ctx + "\n\nTASK: " + task
    for i in range(n):
        d, _tps, w = call(base_user, temperature=0.6, seed=1 + i)  # temp>0 + varied seed = diverse samples
        drafts.append(d)
        wall += w
    labelled = "\n\n".join(f"[CANDIDATE {i+1}]\n{d}" for i, d in enumerate(drafts))
    synth_user = (SYS_KIT + "\n\nTASK: " + task + "\n\nREFERENCE METHOD:\n" + ctx +
                  "\n\nSeveral candidate answers follow. Produce ONE best answer: keep the points the candidates agree "
                  "on, drop what only one asserts without support, fix errors. Output ONLY the final answer itself — "
                  "no candidate numbers, no labels, no commentary about the answer. Be terse.\n\n" + labelled)
    synth, tps_s, w_s = call(synth_user)
    wall += w_s
    # verify / abstain gate: verdict only decides PASS/REVISE/ABSTAIN; the rewrite is a separate clean call (no meta-text)
    ver_user = ("You are a verifier. For the TASK and REFERENCE METHOD, judge the ANSWER. Reply with exactly one word: "
                "PASS (sound and grounded), REVISE (fixable flaws), or ABSTAIN (not supportable from the method). "
                "After the word, optionally one short line naming the flaw.\n\nTASK: " + task +
                "\n\nREFERENCE METHOD:\n" + ctx + "\n\nANSWER:\n" + synth)
    verdict, _tps_v, w_v = call(ver_user, max_tokens=120)
    wall += w_v
    head = verdict.strip().split("\n", 1)
    tag = head[0].strip().upper()
    note = head[1].strip() if len(head) > 1 else ""
    if tag.startswith("REVISE"):
        rev_user = (SYS_KIT + "\n\nTASK: " + task + "\n\nREFERENCE METHOD:\n" + ctx + "\n\nDRAFT:\n" + synth +
                    ("\n\nFLAW TO FIX: " + note if note else "") +
                    "\n\nRewrite the answer fixing the flaw. Output only the answer. Be terse.")
        final, _tps_r, w_r = call(rev_user)
        wall += w_r
        meta = {"gate": "REVISE", "n_samples": n, "note": note}
    elif tag.startswith("ABSTAIN"):
        final, meta = synth + "\n\n[low confidence: " + note + "]", {"gate": "ABSTAIN", "n_samples": n, "note": note}
    else:
        final, meta = synth, {"gate": "PASS", "n_samples": n}
    return final, tps_s, wall, meta


ARMS = {"base": arm_base, "kit_fast": arm_kit_fast, "kit_deep": arm_kit_deep, "kit_max": arm_kit_max}


def main():
    tasks_file = os.environ.get("TASKS_FILE", "tasks-coding.json")
    tag = os.environ.get("TASKS_TAG", "tasks")
    budget = int(os.environ.get("RETR_BUDGET", "6000"))
    arms = [a.strip() for a in os.environ.get("TASKS_ARMS", "base,kit_fast,kit_deep").split(",") if a.strip()]
    with open(os.path.join(HERE, tasks_file), encoding="utf-8") as f:
        spec = json.load(f)
    out = {"tasks_file": tasks_file, "tag": tag, "arms": arms, "retr_budget": budget,
           "judging": spec.get("judging", ""), "items": []}
    for t in spec["tasks"]:
        ctx = retrieve(t["kb"], t["task"], budget)
        rec = {"id": t["id"], "kb": t["kb"], "task": t["task"], "rubric": t["rubric"],
               "ctx_chars": len(ctx), "arms": {}}
        for a in arms:
            print(f"[{t['id']}] {a}...", flush=True)
            res = ARMS[a](t["task"], ctx)
            text, tps, wall = res[0], res[1], res[2]
            extra = res[3] if len(res) > 3 else {}
            rec["arms"][a] = {"answer": text, "words": len(text.split()),
                              "tok_s": round(tps, 1) if tps else None, "wall_s": round(wall, 1), **extra}
            print(f"    {len(text.split())}w  {round(wall,1)}s  {round(tps,1) if tps else '?'} t/s", flush=True)
        out["items"].append(rec)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    path = os.path.join(HERE, f"results-{tag}-{stamp}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    # quick COST summary (the SMART axis is judged separately against the rubric)
    print("\nSaved:", path)
    for a in arms:
        ws = [it["arms"][a]["words"] for it in out["items"]]
        wl = [it["arms"][a]["wall_s"] for it in out["items"]]
        print(f"  {a:9s} avg {sum(ws)//len(ws):3d}w  avg {sum(wl)/len(wl):5.1f}s/task")
    print("Next: judge each item's arms[*].answer against its rubric (0/0.5/1 per point + 1-5 holistic).")


if __name__ == "__main__":
    main()
