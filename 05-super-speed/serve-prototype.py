"""Serve only this module's self-contained prototype on localhost."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import sys

HTML = Path(__file__).resolve().with_name("prototype.html")

class PrototypeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlsplit(self.path).path
        if route == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        if route not in ("/", "/prototype.html"):
            self.send_error(404)
            return
        body = HTML.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    with ThreadingHTTPServer(("127.0.0.1", port), PrototypeHandler) as server:
        print(f"Local prototype: http://127.0.0.1:{server.server_port}", flush=True)
        server.serve_forever()

