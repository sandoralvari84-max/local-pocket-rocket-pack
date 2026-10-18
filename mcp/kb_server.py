"""MCP knowledge-base tool: swappable per-topic document folders with keyword search. Standard library only.

Layout (mounted at /kb): /kb/<name>/*.md|*.txt|*.csv|*.json  -> one knowledge base per subfolder.
The active base is remembered in /kb/.active so it persists across restarts. Search/read act on the active base
unless a 'kb' argument overrides it. Reads are confined to the base folder (no path traversal, no symlink escape).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_stdio import run  # noqa: E402

KB_ROOT = os.environ.get("KB_ROOT", "/kb")
ACTIVE_FILE = os.path.join(KB_ROOT, ".active")
EXTS = (".md", ".txt", ".csv", ".json", ".text", ".log")
MAX_INDEX_BYTES = 2 * 1024 * 1024

TOOLS = [
    {
        "name": "list",
        "description": "List the available knowledge bases (topic folders), their document counts, and which one is active.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "use",
        "description": "Set the active knowledge base by name (e.g. 'marketing', 'design'). Later kb searches use it by default.",
        "inputSchema": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Knowledge base folder name."}},
            "required": ["name"],
        },
    },
    {
        "name": "search",
        "description": "Keyword-search documents in the active knowledge base. Returns the best-matching files with snippets; read one with kb_read.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Keywords to search for."},
                "kb": {"type": "string", "description": "Optional: search this base instead of the active one."},
                "max_results": {"type": "integer", "description": "Number of files (default 6, max 15)."},
            },
            "required": ["query"],
        },
    },
    {
        "name": "read",
        "description": "Read a document from a knowledge base by its relative path (as shown by kb_search).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative path within the base, e.g. 'brand-voice.md'."},
                "kb": {"type": "string", "description": "Optional: base to read from instead of the active one."},
                "max_chars": {"type": "integer", "description": "Maximum characters (default 12000, max 30000)."},
            },
            "required": ["path"],
        },
    },
]


def bases():
    if not os.path.isdir(KB_ROOT):
        return []
    return sorted(d for d in os.listdir(KB_ROOT) if os.path.isdir(os.path.join(KB_ROOT, d)) and not d.startswith("."))


def get_active():
    try:
        with open(ACTIVE_FILE, encoding="utf-8") as f:
            name = f.read().strip()
        return name if name in bases() else None
    except OSError:
        return None


def resolve_base(name):
    name = (name or "").strip()
    if not name:
        raise ValueError("no knowledge base is active; call kb_use first or pass 'kb'")
    if name not in bases():
        raise ValueError(f"unknown knowledge base '{name}'. Available: {', '.join(bases()) or '(none)'}")
    return os.path.realpath(os.path.join(KB_ROOT, name))


def docs_in(base_dir):
    for root, _, files in os.walk(base_dir):
        for fn in files:
            if fn.lower().endswith(EXTS) and not fn.startswith("."):
                yield os.path.join(root, fn)


def words(s):
    return re.findall(r"[\w']{2,}", s.lower())


def call_tool(name, args):
    if name == "list":
        active = get_active()
        avail = bases()
        if not avail:
            return (r"No knowledge bases yet. Create a folder under D:\dockerData\assistant\kb "
                    "(e.g. 'marketing') and drop .md/.txt files in it."), False
        lines = []
        for b in avail:
            n = sum(1 for _ in docs_in(os.path.join(KB_ROOT, b)))
            lines.append(f"{'* ' if b == active else '  '}{b}  ({n} docs)")
        return "Knowledge bases (* = active):\n" + "\n".join(lines), False

    if name == "use":
        nm = str(args.get("name", "")).strip()
        if nm not in bases():
            return f"Unknown knowledge base '{nm}'. Available: {', '.join(bases()) or '(none)'}", True
        with open(ACTIVE_FILE, "w", encoding="utf-8") as f:
            f.write(nm)
        return f"Active knowledge base is now '{nm}'.", False

    if name == "search":
        base_dir = resolve_base(args.get("kb") or get_active())
        terms = set(words(str(args.get("query", ""))))
        if not terms:
            return "Empty query.", True
        limit = max(1, min(int(args.get("max_results") or 6), 15))
        scored = []
        for path in docs_in(base_dir):
            try:
                if os.path.getsize(path) > MAX_INDEX_BYTES:
                    continue
                with open(path, encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except OSError:
                continue
            toks = words(text)
            tf = {t: 0 for t in terms}
            for w in toks:
                if w in tf:
                    tf[w] += 1
            rel = os.path.relpath(path, base_dir).replace("\\", "/")
            name_hits = len(terms & set(words(rel)))
            score = sum(1 for v in tf.values() if v) * 10 + sum(tf.values()) + name_hits * 25
            if score:
                pos = next((text.lower().find(t) for t in terms if text.lower().find(t) >= 0), 0)
                snippet = re.sub(r"\s+", " ", text[max(0, pos - 80):pos + 200]).strip()
                scored.append((score, rel, snippet))
        if not scored:
            return "No matching documents in this knowledge base.", False
        scored.sort(reverse=True)
        return "\n\n".join(f"{rel}\n  {snip}" for _, rel, snip in scored[:limit]), False

    if name == "read":
        base_dir = resolve_base(args.get("kb") or get_active())
        rel = str(args.get("path", "")).strip().lstrip("/\\")
        target = os.path.realpath(os.path.join(base_dir, rel))
        if os.path.commonpath([base_dir, target]) != base_dir:
            return "Path is outside the knowledge base.", True
        if not os.path.isfile(target):
            return f"No such document: {rel}", True
        max_chars = max(500, min(int(args.get("max_chars") or 12000), 30000))
        with open(target, encoding="utf-8", errors="replace") as f:
            text = f.read()
        note = f"\n\n[truncated to {max_chars} characters]" if len(text) > max_chars else ""
        return f"{rel}:\n\n{text[:max_chars]}{note}", False

    return f"Unknown tool: {name}", True


if __name__ == "__main__":
    run("kb", TOOLS, call_tool)
