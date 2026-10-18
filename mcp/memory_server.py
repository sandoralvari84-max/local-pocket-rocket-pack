"""Minimal MCP memory server (stdio, newline-delimited JSON-RPC 2.0). Standard library only.

Spawned by llama-server via --mcp-servers-config. Notes live in a JSONL file (MEMORY_FILE, default
/memory/memory.jsonl), one JSON object per line: {"id", "created", "text", "tags"}.
"""
import datetime
import json
import os
import re
import sys
import tempfile
import uuid

MEMORY_FILE = os.environ.get("MEMORY_FILE", "/memory/memory.jsonl")
MAX_TEXT = 1000

TOOLS = [
    {
        "name": "remember",
        "description": "Save one short, self-contained fact about the user, their preferences, projects or decisions for future conversations. Never store secrets.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The fact to remember, as one sentence."},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Optional short topic tags."},
            },
            "required": ["text"],
        },
    },
    {
        "name": "recall",
        "description": "Search saved memories by keywords and return the best matches.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Keywords to search for."},
                "limit": {"type": "integer", "description": "Maximum results (default 5)."},
            },
            "required": ["query"],
        },
    },
    {
        "name": "list",
        "description": "List the most recent saved memories.",
        "inputSchema": {
            "type": "object",
            "properties": {"limit": {"type": "integer", "description": "Maximum results (default 20)."}},
        },
    },
    {
        "name": "forget",
        "description": "Delete one saved memory by its id (get ids from recall or list).",
        "inputSchema": {
            "type": "object",
            "properties": {"id": {"type": "string", "description": "The memory id to delete."}},
            "required": ["id"],
        },
    },
]


def load():
    if not os.path.exists(MEMORY_FILE):
        return []
    items = []
    with open(MEMORY_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return items


def save_all(items):
    # Atomic rewrite in the same directory (the only writable mount).
    d = os.path.dirname(MEMORY_FILE) or "."
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".memory-", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    os.replace(tmp, MEMORY_FILE)


def words(s):
    return set(re.findall(r"[\w']{2,}", s.lower()))


def fmt(items):
    if not items:
        return "No memories found."
    return "\n".join(
        f"[{it['id']}] {it['text']}" + (f"  (tags: {', '.join(it['tags'])})" if it.get("tags") else "")
        for it in items
    )


def call_tool(name, args):
    if name == "remember":
        text = str(args.get("text", "")).strip()[:MAX_TEXT]
        if not text:
            return "Nothing to remember: text is empty.", True
        tags = [str(t).strip()[:40] for t in (args.get("tags") or []) if str(t).strip()][:8]
        item = {
            "id": uuid.uuid4().hex[:8],
            "created": datetime.datetime.now().isoformat(timespec="seconds"),
            "text": text,
            "tags": tags,
        }
        os.makedirs(os.path.dirname(MEMORY_FILE) or ".", exist_ok=True)
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
        return f"Saved memory {item['id']}.", False
    if name == "recall":
        q = words(str(args.get("query", "")))
        limit = max(1, min(int(args.get("limit") or 5), 50))
        scored = []
        for it in load():
            score = len(q & words(it["text"] + " " + " ".join(it.get("tags", []))))
            if score:
                scored.append((score, it["created"], it))
        scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
        return fmt([it for _, _, it in scored[:limit]]), False
    if name == "list":
        limit = max(1, min(int(args.get("limit") or 20), 200))
        return fmt(load()[-limit:][::-1]), False
    if name == "forget":
        mid = str(args.get("id", "")).strip()
        items = load()
        kept = [it for it in items if it["id"] != mid]
        if len(kept) == len(items):
            return f"No memory with id {mid}.", True
        save_all(kept)
        return f"Forgot memory {mid}.", False
    return f"Unknown tool: {name}", True


def reply(msg_id, result=None, error=None):
    out = {"jsonrpc": "2.0", "id": msg_id}
    if error is not None:
        out["error"] = error
    else:
        out["result"] = result
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            reply(None, error={"code": -32700, "message": "Parse error"})
            continue
        method, msg_id, params = msg.get("method"), msg.get("id"), msg.get("params") or {}
        if msg_id is None:  # notification (e.g. notifications/initialized): no response
            continue
        if method == "initialize":
            reply(msg_id, {
                "protocolVersion": params.get("protocolVersion", "2025-06-18"),
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "memory", "version": "1.0.0"},
            })
        elif method == "ping":
            reply(msg_id, {})
        elif method == "tools/list":
            reply(msg_id, {"tools": TOOLS})
        elif method == "tools/call":
            try:
                text, is_error = call_tool(params.get("name"), params.get("arguments") or {})
            except Exception as e:  # report tool failures to the model instead of crashing
                text, is_error = f"Tool error: {e}", True
            reply(msg_id, {"content": [{"type": "text", "text": text}], "isError": is_error})
        else:
            reply(msg_id, error={"code": -32601, "message": f"Method not found: {method}"})


if __name__ == "__main__":
    main()
