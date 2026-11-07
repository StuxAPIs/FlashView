"""FlashView's local dev server: serves the repo like GitHub Pages does (clean URLs: /about -> about.html,
404.html for anything missing, application/wasm for Ruffle), and with DEV_MODE=1 (the default from
dev-server.sh/.bat) injects a small "local dev" banner into every page.
Usage: python -I scripts/dev-server.py <root> <port>"""
import functools
import http.server
import os
import sys

ROOT = os.path.abspath(sys.argv[1])
PORT = int(sys.argv[2])
DEV_MODE = os.environ.get("DEV_MODE", "1") == "1"
BANNER = (b'<div style="position:fixed;left:0;right:0;bottom:0;z-index:2147483647;background:#c8102e;color:#fff;'
          b'font:600 12px/1.6 system-ui,sans-serif;text-align:center;padding:3px">LOCAL DEV &middot; dev-server '
          b'(run with --no-dev-mode to hide)</div>')


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".wasm": "application/wasm",
                      ".md": "text/markdown; charset=utf-8", ".webmanifest": "application/manifest+json"}

    def resolve(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        local = os.path.normpath(os.path.join(ROOT, path.lstrip("/")))
        if not local.startswith(ROOT):
            return None
        if os.path.isdir(local):
            index = os.path.join(local, "index.html")
            if os.path.isfile(index):
                return index
        if os.path.isfile(local):
            return local
        if os.path.isfile(local + ".html"):
            return local + ".html"
        return None

    def do_GET(self):
        target = self.resolve()
        status = 200
        if target is None:
            target, status = os.path.join(ROOT, "404.html"), 404
        with open(target, "rb") as f:
            body = f.read()
        ctype = self.guess_type(target)
        if target.endswith(".html"):
            ctype = "text/html; charset=utf-8"
            if DEV_MODE:
                body = body.replace(b"</body>", BANNER + b"</body>", 1)
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self):
        self.do_GET()


http.server.ThreadingHTTPServer(("127.0.0.1", PORT), functools.partial(Handler, directory=ROOT)).serve_forever()
