#!/usr/bin/env python3
"""
workbench — a tiny zero-dependency web server for on-the-fly diagrams & tools.

What it does:
  * Serves the ./tools/ folder of self-contained HTML/JS/CSS bundles.
  * Renders the home page (/) from home.html, a template that lives alongside
    this file. Placeholders (__GRID__, __COUNT__, etc.) are replaced at request
    time with live tool discovery output.
  * Live-reloads the browser whenever any file under ./tools/ changes, via
    Server-Sent Events. A tiny <script> is injected into every served .html
    page; a background thread watches file mtimes and bumps a version counter.

Stdlib only (works on system Python 3.9+). No pip installs, no node_modules.

A "tool" is either:
  * tools/<name>.html              (a single self-contained file), or
  * tools/<name>/index.html        (a folder that ships its own assets)

Run:        python3 server.py
Config:     WORKBENCH_HOST (default 127.0.0.1), WORKBENCH_PORT (default 8765)
Access:     http://localhost:8765
"""

import html
import os
import sys
import threading
import time
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# --- config ---------------------------------------------------------------

BASE_DIR  = Path(__file__).resolve().parent
TOOLS_DIR = BASE_DIR / "tools"
HOST = os.environ.get("WORKBENCH_HOST", "127.0.0.1")
PORT = int(os.environ.get("WORKBENCH_PORT", "8765"))
POLL_INTERVAL = 0.5  # seconds between mtime scans

# Injected into every served HTML page. EventSource auto-reconnects so a
# server restart will simply reload the page once it comes back up.
LIVERELOAD_SNIPPET = (
    "<script>(function(){var s=new EventSource('/__livereload');"
    "s.onmessage=function(){location.reload();};})();</script>"
)

# --- live-reload version counter ------------------------------------------

_version = 0
_version_lock = threading.Lock()


def _scan_max_mtime():
    """Return (latest_mtime, file_count) across all files in tools/.
    Count changes register even when mtimes don't move (adds/deletes)."""
    latest, count = 0.0, 0
    if TOOLS_DIR.is_dir():
        for root, _dirs, files in os.walk(TOOLS_DIR):
            for name in files:
                count += 1
                try:
                    m = os.path.getmtime(os.path.join(root, name))
                except OSError:
                    continue
                if m > latest:
                    latest = m
    return latest, count


def _watch_loop():
    global _version
    last = _scan_max_mtime()
    while True:
        time.sleep(POLL_INTERVAL)
        current = _scan_max_mtime()
        if current != last:
            last = current
            with _version_lock:
                _version += 1


def current_version():
    with _version_lock:
        return _version


# --- tool discovery & home page -------------------------------------------

def _title_from_html(path: Path, fallback: str) -> str:
    """Pull <title> text for a friendly label; fall back to the file/folder name."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return fallback
    lower = text.lower()
    i = lower.find("<title>")
    if i != -1:
        j = lower.find("</title>", i)
        if j != -1:
            title = text[i + len("<title>"):j].strip()
            if title:
                return title
    return fallback


def discover_tools():
    """Return a sorted list of {name, url, title} dicts for every tool in tools/."""
    tools = []
    if not TOOLS_DIR.is_dir():
        return tools
    for entry in sorted(TOOLS_DIR.iterdir(), key=lambda p: p.name.lower()):
        if entry.name.startswith("."):
            continue
        if entry.is_file() and entry.suffix.lower() in (".html", ".htm"):
            tools.append({
                "name":  entry.name,
                "url":   "/" + entry.name,
                "title": _title_from_html(entry, entry.stem),
            })
        elif entry.is_dir() and (entry / "index.html").is_file():
            tools.append({
                "name":  entry.name + "/",
                "url":   "/" + entry.name + "/",
                "title": _title_from_html(entry / "index.html", entry.name),
            })
    return tools


def render_home() -> bytes:
    tools = discover_tools()

    if tools:
        cards = "\n".join(
            '<a class="card" href="{url}">'
            '<span class="title">{title}</span>'
            '<span class="path">{name}</span></a>'.format(
                url=html.escape(t["url"], quote=True),
                title=html.escape(t["title"]),
                name=html.escape(t["name"]),
            )
            for t in tools
        )
        grid = '<div class="grid">{}</div>'.format(cards)
    else:
        grid = (
            '<div class="empty">'
            '<span class="empty-glyph">📂</span>'
            '<h3>No tools yet</h3>'
            '<p>Drop an <code>.html</code> file (or a folder with '
            '<code>index.html</code>) into <code>tools/</code> and '
            'it appears here automatically.</p>'
            '</div>'
        )

    template_path = BASE_DIR / "home.html"
    try:
        page = template_path.read_text(encoding="utf-8")
    except OSError:
        return (
            "<html><body style='font-family:monospace;padding:2rem'>"
            "<h2>workbench</h2><p>⚠️ home.html template not found alongside server.py.</p>"
            "<p>Re-run setup or copy home.html next to server.py.</p>"
            "</body></html>"
        ).encode()

    page = (page
        .replace("__GRID__",     grid)
        .replace("__COUNT__",    str(len(tools)))
        .replace("__PLURAL__",   "" if len(tools) == 1 else "s")
        .replace("__HOST__",     html.escape(HOST))
        .replace("__PORT__",     str(PORT))
        .replace("__LIVERELOAD__", LIVERELOAD_SNIPPET)
    )
    return page.encode("utf-8")


# --- request handler -------------------------------------------------------

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(TOOLS_DIR), **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def do_GET(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path == "/":
            return self._send_home()
        if path == "/__livereload":
            return self._send_livereload()
        fs_path = Path(self.translate_path(self.path))
        if fs_path.is_dir():
            index = fs_path / "index.html"
            if index.is_file():
                return self._send_html_with_reload(index)
        if fs_path.is_file() and fs_path.suffix.lower() in (".html", ".htm"):
            return self._send_html_with_reload(fs_path)
        return super().do_GET()

    def _send_home(self):
        body = render_home()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_html_with_reload(self, fs_path: Path):
        try:
            text = fs_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return
        idx = text.lower().rfind("</body>")
        if idx != -1:
            text = text[:idx] + LIVERELOAD_SNIPPET + text[idx:]
        else:
            text += LIVERELOAD_SNIPPET
        body = text.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_livereload(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        last_seen = current_version()
        try:
            self.wfile.write(b": connected\n\n")
            self.wfile.flush()
            while True:
                time.sleep(POLL_INTERVAL)
                v = current_version()
                if v != last_seen:
                    last_seen = v
                    self.wfile.write(b"data: reload\n\n")
                else:
                    self.wfile.write(b": keep-alive\n\n")
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            return


def main():
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    threading.Thread(target=_watch_loop, daemon=True).start()
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    httpd.daemon_threads = True
    print(
        "workbench serving %s on http://%s:%d  (Ctrl-C to stop)" % (TOOLS_DIR, HOST, PORT),
        flush=True,
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down", flush=True)
        httpd.shutdown()


if __name__ == "__main__":
    main()
