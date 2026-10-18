"""MCP YouTube tool: fetch a video's subtitles/auto-captions with yt-dlp and return them as plain text."""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_stdio import run  # noqa: E402

YTDLP = os.environ.get("YTDLP", "/opt/assistant/bin/yt-dlp")
ALLOWED = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "music.youtube.com"}

TOOLS = [
    {
        "name": "transcript",
        "description": "Get the transcript (subtitles or auto-captions) of a YouTube video as plain text, with its title and length.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "YouTube video URL."},
                "lang": {"type": "string", "description": "Subtitle language code (default en)."},
                "max_chars": {"type": "integer", "description": "Maximum characters (default 24000, max 40000)."},
            },
            "required": ["url"],
        },
    }
]


def vtt_to_text(vtt):
    out, last = [], None
    for line in vtt.splitlines():
        line = line.strip()
        if not line or line == "WEBVTT" or "-->" in line or line.startswith(("Kind:", "Language:", "NOTE")) or line.isdigit():
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        if line and line != last:  # auto-captions repeat each line
            out.append(line)
            last = line
    return " ".join(out)


def transcript(url, lang, max_chars):
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    if host not in ALLOWED:
        return "Only YouTube URLs are supported.", True
    work = tempfile.mkdtemp(dir="/tmp")
    try:
        cmd = [sys.executable, YTDLP, "--skip-download", "--no-simulate", "--write-subs", "--write-auto-subs",
               # exact codes only: a pattern like "en.*" also matches dozens of machine-translated tracks (HTTP 429)
               "--sub-langs", f"{lang},{lang}-orig,{lang}-US,{lang}-GB", "--sub-format", "vtt", "--no-playlist", "--no-cache-dir",
               "--no-warnings", "--quiet", "--print", "%(title)s\t%(duration_string)s",
               "-o", os.path.join(work, "%(id)s.%(ext)s"), url]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=150, env={**os.environ, "HOME": work})
        if p.returncode != 0:
            return f"yt-dlp failed: {(p.stderr or p.stdout).strip()[-600:]}", True
        title, _, duration = (p.stdout.strip().splitlines() or [""])[0].partition("\t")
        files = sorted(glob.glob(os.path.join(work, "*.vtt")), key=lambda f: ("-orig" in f, ".auto" in f))
        if not files:
            return f"No '{lang}' subtitles or captions available for: {title or url}", True
        with open(files[0], encoding="utf-8", errors="replace") as f:
            text = vtt_to_text(f.read())
        note = f"\n\n[truncated to {max_chars} characters]" if len(text) > max_chars else ""
        return f"Title: {title}\nLength: {duration}\nSubtitles: {os.path.basename(files[0])}\n\n{text[:max_chars]}{note}", False
    except subprocess.TimeoutExpired:
        return "yt-dlp timed out.", True
    finally:
        shutil.rmtree(work, ignore_errors=True)


def call_tool(name, args):
    if name == "transcript":
        return transcript(str(args.get("url", "")).strip(), str(args.get("lang") or "en").strip(),
                          max(1000, min(int(args.get("max_chars") or 24000), 40000)))
    return f"Unknown tool: {name}", True


if __name__ == "__main__":
    run("youtube", TOOLS, call_tool)
