#!/usr/bin/env python3
"""Local preview server: python3 scripts/serve.py  →  http://localhost:8000

Same as `python3 -m http.server`, but tells the browser never to cache, so a plain
reload always shows the latest CSS and images (the stock server sends no cache
headers and Chrome happily keeps stale stylesheets for a while)."""
import http.server, os, sys

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def log_message(self, *a):  # keep the terminal quiet
        pass

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
print(f'serving on http://localhost:{port} (no-cache)')
http.server.ThreadingHTTPServer(('127.0.0.1', port), NoCache).serve_forever()
