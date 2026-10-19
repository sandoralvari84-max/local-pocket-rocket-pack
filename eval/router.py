"""Niche router: classify a query to the best-matching KB niche, so the assistant auto-selects the right profile
instead of the user choosing. Standard library only; no embeddings. Builds a per-niche vocabulary from that niche's
KB files (document frequency), down-weights terms common to many niches (so generic words do not dominate), and scores
the query by weighted overlap. Returns (niche, confidence, ranked). Low confidence -> caller can fall back to 'general'
or ask. Usage: python -I router.py "your query"  (self-tests if no query given)."""
import math
import os
import re
import sys

KB_ROOT = r"D:\dockerData\assistant\kb"
STOP = set("the a an of to in on for and or is are be as it its this that with how you your we our do does what when "
           "where which who why not no yes can could should would will from by at if then so a i".split())


def _terms(s):
    return [w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 2]


def _load():
    niches = {}
    for n in sorted(os.listdir(KB_ROOT)):
        d = os.path.join(KB_ROOT, n)
        if not os.path.isdir(d) or n.startswith("_"):
            continue
        tf = {}
        for fn in os.listdir(d):
            if fn.endswith(".md"):
                with open(os.path.join(d, fn), encoding="utf-8") as f:
                    for w in _terms(f.read()):
                        tf[w] = tf.get(w, 0) + 1
        if tf:
            niches[n] = tf
    # idf across niches: a term in few niches is discriminative
    dfreq = {}
    for tf in niches.values():
        for w in tf:
            dfreq[w] = dfreq.get(w, 0) + 1
    N = len(niches)
    idf = {w: math.log(1 + N / df) for w, df in dfreq.items()}
    return niches, idf


_NICHES, _IDF = _load()


def route(query):
    qt = _terms(query)
    scores = {}
    for n, tf in _NICHES.items():
        s = 0.0
        for w in qt:
            if w in tf:
                s += math.log(1 + tf[w]) * _IDF.get(w, 1.0)
        scores[n] = s
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top = ranked[0][1] if ranked else 0.0
    total = sum(v for _, v in ranked) or 1.0
    conf = round(top / total, 2)  # share of mass on the winner
    return ranked[0][0], conf, ranked[:3]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        n, c, r = route(" ".join(sys.argv[1:]))
        print(f"-> {n} (conf {c})  top3={[(x, round(y,1)) for x,y in r]}")
    else:
        cases = {
            "A thread race loses increments on a shared counter, how to fix?": "coding",
            "Is this login endpoint vulnerable to credential stuffing?": "cybersecurity",
            "Our model is 99% accurate but fails on new data": "datascience",
            "Should we rewrite the monolith as microservices?": ("software", "coding"),
            "A big customer demands a feature or they churn": "product",
            "Is this supplement worth taking?": "health",
            "Can I use this copyrighted image on my site?": ("legal", "webdesign"),
            "How do I price against a competitor to protect margin?": ("business", "marketing"),
            "The signup form has a high abandonment rate": ("design", "product"),
        }
        ok = 0
        for q, want in cases.items():
            n, c, r = route(q)
            good = n in (want if isinstance(want, tuple) else (want,))
            ok += good
            print(f"  {'ok ' if good else 'HM '} {n:13s} conf {c}  <- {q[:48]}")
        print(f"{ok}/{len(cases)} routed to an acceptable niche")
