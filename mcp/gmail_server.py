"""MCP Gmail tools, READ-ONLY: search and read messages over IMAP. No send, delete, move or flag changes.

Mailboxes are opened read-only (EXAMINE) and bodies fetched with BODY.PEEK, so messages are not marked as read.
Credentials come from a local env file you fill in yourself (GMAIL_USER, GMAIL_APP_PASSWORD = Google App Password).
"""
import email
import email.policy
import imaplib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_stdio import html_to_text, run  # noqa: E402

ENV_FILE = os.environ.get("GMAIL_ENV_FILE", "/opt/assistant/secrets/gmail.env")

TOOLS = [
    {
        "name": "search",
        "description": "Search Gmail (read-only). Uses Gmail search syntax, e.g. 'from:bank newer_than:7d'. Returns uid, date, sender and subject.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Gmail search query; empty = latest messages."},
                "limit": {"type": "integer", "description": "Maximum messages (default 10, max 30)."},
                "unread_only": {"type": "boolean", "description": "Only unread messages."},
                "folder": {"type": "string", "description": "Mailbox (default INBOX; '[Gmail]/All Mail' for everything)."},
            },
        },
    },
    {
        "name": "read",
        "description": "Read one email (read-only) by uid from search. Returns headers, text body and attachment names.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "uid": {"type": "string", "description": "Message uid from search."},
                "folder": {"type": "string", "description": "Same mailbox used in search (default INBOX)."},
                "max_chars": {"type": "integer", "description": "Maximum body characters (default 8000, max 20000)."},
            },
            "required": ["uid"],
        },
    },
]


def creds():
    vals = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.lstrip().startswith("#"):
                    k, v = line.split("=", 1)
                    vals[k.strip()] = v.strip().strip('"').strip("'")
    user, pw = vals.get("GMAIL_USER", ""), vals.get("GMAIL_APP_PASSWORD", "").replace(" ", "")
    if not user or not pw:
        raise RuntimeError("Gmail is not configured: fill GMAIL_USER and GMAIL_APP_PASSWORD in "
                           r"D:\dockerData\assistant\secrets\gmail.env")
    return user, pw


def connect(folder):
    user, pw = creds()
    m = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=30)
    m.login(user, pw)
    typ, _ = m.select(f'"{folder}"', readonly=True)
    if typ != "OK":
        m.logout()
        raise RuntimeError(f"Cannot open mailbox {folder}")
    return m


def search(query, limit, unread_only, folder):
    m = connect(folder)
    try:
        crit = []
        if query:
            crit += ["X-GM-RAW", '"' + query.replace("\\", "\\\\").replace('"', '\\"') + '"']
        if unread_only:
            crit.append("UNSEEN")
        typ, data = m.uid("SEARCH", None, *(crit or ["ALL"]))
        uids = data[0].split()[-limit:][::-1] if typ == "OK" and data and data[0] else []
        if not uids:
            return "No messages found.", False
        rows = []
        for uid in uids:
            typ, d = m.uid("FETCH", uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
            if typ != "OK" or not d or not isinstance(d[0], tuple):
                continue
            h = email.message_from_bytes(d[0][1], policy=email.policy.default)
            rows.append(f"uid {uid.decode()} | {h.get('Date', '')} | {h.get('From', '')} | {h.get('Subject', '(no subject)')}")
        return "\n".join(rows), False
    finally:
        m.logout()


def read(uid, folder, max_chars):
    m = connect(folder)
    try:
        typ, d = m.uid("FETCH", uid.encode(), "(BODY.PEEK[])")
        if typ != "OK" or not d or not isinstance(d[0], tuple):
            return f"No message with uid {uid} in {folder}.", True
        msg = email.message_from_bytes(d[0][1], policy=email.policy.default)
        part = msg.get_body(preferencelist=("plain", "html"))
        body = part.get_content() if part else ""
        if part is not None and part.get_content_type() == "text/html":
            body = html_to_text(body)[1]
        attachments = [a.get_filename() or "(unnamed)" for a in msg.iter_attachments()]
        note = f"\n\n[truncated to {max_chars} characters]" if len(body) > max_chars else ""
        head = "\n".join(f"{k}: {msg.get(k, '')}" for k in ("From", "To", "Date", "Subject"))
        att = f"\nAttachments: {', '.join(attachments)}" if attachments else ""
        return f"{head}{att}\n\n{body[:max_chars]}{note}", False
    finally:
        m.logout()


def call_tool(name, args):
    folder = str(args.get("folder") or "INBOX")
    try:
        if name == "search":
            return search(str(args.get("query") or "").strip(), max(1, min(int(args.get("limit") or 10), 30)),
                          bool(args.get("unread_only")), folder)
        if name == "read":
            return read(str(args.get("uid", "")).strip(), folder, max(500, min(int(args.get("max_chars") or 8000), 20000)))
    except (RuntimeError, imaplib.IMAP4.error, OSError) as e:
        return f"Gmail error: {e}", True
    return f"Unknown tool: {name}", True


if __name__ == "__main__":
    run("gmail", TOOLS, call_tool)
