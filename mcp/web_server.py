"""MCP web tools: web search (multi-engine / Brave / SearXNG) and page fetch. Standard library only.

search backend is chosen in /opt/assistant/secrets/search.env (SEARCH_BACKEND = auto|ddg|brave|searxng):
  auto    - keyless, tries Mojeek, then DuckDuckGo lite, then Bing, and returns the first that answers
  brave   - Brave Search API (BRAVE_API_KEY); reliable, free tier
  searxng - a self-hosted SearXNG instance (SEARXNG_URL), json output
fetch refuses non-http(s) URLs and any host that resolves to a loopback, private, link-local or otherwise
non-public address (re-checked on every redirect), so the model cannot reach the laptop, the LAN or Docker's host.
"""
import html as html_mod
import ipaddress
import json
import os
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_stdio import html_to_text, run  # noqa: E402

UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
]
MAX_BYTES = 3 * 1024 * 1024
BLOCKED_HOSTS = {"localhost", "host.docker.internal", "gateway.docker.internal", "kubernetes.docker.internal"}
CONFIG_FILE = os.environ.get("SEARCH_ENV_FILE", "/opt/assistant/secrets/search.env")

TOOLS = [
    {
        "name": "search",
        "description": "Search the web. Returns titles, URLs and snippets. Use fetch to read a result.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query."},
                "max_results": {"type": "integer", "description": "Number of results (default 6, max 10)."},
            },
            "required": ["query"],
        },
    },
    {
        "name": "fetch",
        "description": "Download a public web page and return its readable text (truncated).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "http(s) URL to read."},
                "max_chars": {"type": "integer", "description": "Maximum characters of text (default 12000, max 30000)."},
            },
            "required": ["url"],
        },
    },
]


def config():
    vals = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    vals[k.strip()] = v.strip().strip('"').strip("'")
    return vals


# ---- low-level HTTP ---------------------------------------------------------

def check_public(url):
    u = urllib.parse.urlsplit(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise ValueError("only http(s) URLs with a hostname are allowed")
    host = u.hostname.lower().rstrip(".")
    if host in BLOCKED_HOSTS or host.endswith(".local") or host.endswith(".internal"):
        raise ValueError(f"host not allowed: {host}")
    for info in socket.getaddrinfo(host, u.port or (443 if u.scheme == "https" else 80)):
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            raise ValueError(f"host resolves to a non-public address ({ip})")


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_public(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = urllib.request.build_opener(SafeRedirect)


def raw_get(url, headers=None, data=None, guard=True, timeout=25):
    """Low-level GET/POST. guard=False for trusted, explicitly-configured search endpoints only."""
    if guard:
        check_public(url)
    h = {"User-Agent": UAS[0], "Accept-Language": "en,es;q=0.8"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h)
    opener = OPENER if guard else urllib.request.build_opener()
    with opener.open(req, timeout=timeout) as r:
        body = r.read(MAX_BYTES + 1)
        return r.headers.get_content_type(), r.headers.get_content_charset() or "utf-8", body[:MAX_BYTES], r.geturl()


def clean(s):
    return html_mod.unescape(re.sub(r"<[^>]+>", "", s)).strip()


# ---- search engines ---------------------------------------------------------

def _engine_mojeek(query, n, ua):
    url = "https://www.mojeek.com/search?" + urllib.parse.urlencode({"q": query})
    _, cs, body, _ = raw_get(url, headers={"User-Agent": ua}, guard=False)
    html = body.decode(cs, "replace")
    out = []
    for m in re.finditer(r'<a[^>]+class="[^"]*\bult\b[^"]*"[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', html, re.S):
        out.append((clean(m.group(2)), html_mod.unescape(m.group(1)), ""))
        if len(out) >= n:
            break
    if not out:  # fallback pattern for Mojeek result titles
        for m in re.finditer(r'<a class="title"[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', html, re.S):
            out.append((clean(m.group(2)), html_mod.unescape(m.group(1)), ""))
            if len(out) >= n:
                break
    return out


def _engine_ddg_lite(query, n, ua):
    data = urllib.parse.urlencode({"q": query}).encode()
    _, cs, body, _ = raw_get("https://lite.duckduckgo.com/lite/", headers={"User-Agent": ua}, data=data, guard=False)
    html = body.decode(cs, "replace")
    out = []
    for m in re.finditer(r'<a[^>]+class="result-link"[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', html, re.S):
        href = m.group(1)
        if "uddg=" in href:
            href = urllib.parse.unquote(urllib.parse.parse_qs(urllib.parse.urlsplit(href).query).get("uddg", [href])[0])
        out.append((clean(m.group(2)), href, ""))
        if len(out) >= n:
            break
    return out


def _engine_bing(query, n, ua):
    url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": query, "setlang": "en"})
    _, cs, body, _ = raw_get(url, headers={"User-Agent": ua}, guard=False)
    html = body.decode(cs, "replace")
    out = []
    for block in re.split(r'<li class="b_algo"', html)[1:]:
        m = re.search(r'<h2>\s*<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', block, re.S)
        if not m:
            continue
        s = re.search(r'<p[^>]*>(.*?)</p>', block, re.S)
        out.append((clean(m.group(2)), html_mod.unescape(m.group(1)), clean(s.group(1)) if s else ""))
        if len(out) >= n:
            break
    return out


def search_auto(query, n):
    errors = []
    for name, fn in (("mojeek", _engine_mojeek), ("ddg-lite", _engine_ddg_lite), ("bing", _engine_bing)):
        for ua in UAS[:2]:
            try:
                res = fn(query, n, ua)
                if res:
                    return res, name
            except Exception as e:  # try the next engine/UA
                errors.append(f"{name}: {type(e).__name__}")
                break
    raise RuntimeError("all keyless engines failed (" + ", ".join(dict.fromkeys(errors)) + ")")


def search_brave(query, n, key):
    url = "https://api.search.brave.com/res/v1/web/search?" + urllib.parse.urlencode({"q": query, "count": n})
    _, cs, body, _ = raw_get(url, headers={"X-Subscription-Token": key, "Accept": "application/json"}, guard=False)
    data = json.loads(body.decode(cs, "replace"))
    return [(r.get("title", ""), r.get("url", ""), clean(r.get("description", "")))
            for r in data.get("web", {}).get("results", [])[:n]], "brave"


def search_searxng(query, n, base):
    url = base.rstrip("/") + "/search?" + urllib.parse.urlencode({"q": query, "format": "json", "safesearch": 0})
    _, cs, body, _ = raw_get(url, guard=False)
    data = json.loads(body.decode(cs, "replace"))
    return [(r.get("title", ""), r.get("url", ""), clean(r.get("content", "")))
            for r in data.get("results", [])[:n]], "searxng"


def search(query, n):
    cfg = config()
    backend = (cfg.get("SEARCH_BACKEND") or "auto").lower()
    if backend == "brave" and cfg.get("BRAVE_API_KEY"):
        results, used = search_brave(query, n, cfg["BRAVE_API_KEY"])
    elif backend == "searxng" and cfg.get("SEARXNG_URL"):
        results, used = search_searxng(query, n, cfg["SEARXNG_URL"])
    else:
        results, used = search_auto(query, n)
    results = [(t, u, s) for t, u, s in results if u.startswith("http")]
    if not results:
        return "No results (the search engine returned nothing; try rephrasing).", True
    body = "\n\n".join(f"{i}. {t}\n{u}" + (f"\n{s}" if s else "") for i, (t, u, s) in enumerate(results, 1))
    return f"[via {used}]\n\n{body}", False


# ---- fetch ------------------------------------------------------------------

def fetch(url, max_chars):
    ctype, charset, body, final = raw_get(url, guard=True)
    if ctype in ("text/html", "application/xhtml+xml"):
        title, text = html_to_text(body.decode(charset, "replace"))
    elif ctype.startswith("text/") or ctype in ("application/json", "application/xml"):
        title, text = "", body.decode(charset, "replace")
    else:
        return f"Unsupported content type: {ctype}", True
    note = f"\n\n[truncated to {max_chars} characters]" if len(text) > max_chars else ""
    return f"URL: {final}\nTitle: {title}\n\n{text[:max_chars]}{note}", False


def call_tool(name, args):
    if name == "search":
        q = str(args.get("query", "")).strip()
        if not q:
            return "Empty query.", True
        try:
            return search(q, max(1, min(int(args.get("max_results") or 6), 10)))
        except (RuntimeError, urllib.error.URLError, socket.gaierror, TimeoutError, ValueError) as e:
            return f"Search failed: {e}", True
    if name == "fetch":
        try:
            return fetch(str(args.get("url", "")).strip(), max(500, min(int(args.get("max_chars") or 12000), 30000)))
        except (ValueError, urllib.error.URLError, socket.gaierror, TimeoutError) as e:
            return f"Could not fetch: {e}", True
    return f"Unknown tool: {name}", True


if __name__ == "__main__":
    run("web", TOOLS, call_tool)
