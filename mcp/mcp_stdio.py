"""Shared stdio MCP loop (newline-delimited JSON-RPC 2.0) for the assistant's tool servers. Standard library only."""
import json
import re
import sys
from html.parser import HTMLParser


def run(server_name, tools, call_tool):
    """tools: list of MCP tool dicts. call_tool(name, args) -> (text, is_error)."""

    def reply(msg_id, result=None, error=None):
        out = {"jsonrpc": "2.0", "id": msg_id}
        if error is not None:
            out["error"] = error
        else:
            out["result"] = result
        sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
        sys.stdout.flush()

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
        if msg_id is None:  # notification: no response
            continue
        if method == "initialize":
            reply(msg_id, {
                "protocolVersion": params.get("protocolVersion", "2025-06-18"),
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": server_name, "version": "1.0.0"},
            })
        elif method == "ping":
            reply(msg_id, {})
        elif method == "tools/list":
            reply(msg_id, {"tools": tools})
        elif method == "tools/call":
            try:
                text, is_error = call_tool(params.get("name"), params.get("arguments") or {})
            except Exception as e:  # report failures to the model instead of crashing
                text, is_error = f"Tool error: {type(e).__name__}: {e}", True
            reply(msg_id, {"content": [{"type": "text", "text": text}], "isError": is_error})
        else:
            reply(msg_id, error={"code": -32601, "message": f"Method not found: {method}"})


class _TextParser(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "head", "template", "iframe"}
    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "pre", "blockquote"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip, self.title, self.in_title = [], 0, "", False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        if tag in self.SKIP:
            self.skip += 1
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif not self.skip:
            self.parts.append(data)


def html_to_text(html):
    """Return (title, readable text) for an HTML document."""
    p = _TextParser()
    p.feed(html)
    text = re.sub(r"[ \t\r\f\v]+", " ", "".join(p.parts))
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return p.title.strip(), text.strip()
