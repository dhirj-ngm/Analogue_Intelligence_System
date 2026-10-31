"""Loopback-only, read-only case-search app with no new runtime dependencies."""

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from urllib.parse import urlsplit

from ais.pilot import ROOT
from ais.search import CaseSearch

ASSETS = ROOT / "assets/app"
MAX_BODY = 16_384


def create_server(port=8000, search=None):
    search = search or CaseSearch.load()

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(10)

        def send(self, status, body, content_type="application/json; charset=utf-8"):
            if not isinstance(body, bytes):
                body = json.dumps(body, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; script-src 'self'; style-src 'self'; "
                "connect-src 'self'; img-src 'self'; frame-ancestors 'none'; "
                "base-uri 'none'; form-action 'self'",
            )
            self.end_headers()
            self.wfile.write(body)

        def local_request(self):
            hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
            if self.headers.get("Host") not in hosts:
                self.send(403, {"error": "Use the local app address printed at startup."})
                return False
            origin = self.headers.get("Origin")
            if origin and origin not in {f"http://{host}" for host in hosts}:
                self.send(403, {"error": "Cross-origin requests are not allowed."})
                return False
            return True

        def do_GET(self):
            if not self.local_request():
                return
            path = urlsplit(self.path).path
            if path == "/api/catalog":
                self.send(200, search.catalog())
                return
            assets = {
                "/": ("index.html", "text/html; charset=utf-8"),
                "/app.css": ("app.css", "text/css; charset=utf-8"),
                "/app.js": ("app.js", "text/javascript; charset=utf-8"),
                "/icon.svg": ("icon.svg", "image/svg+xml"),
            }
            if path not in assets:
                self.send(404, {"error": "Page not found."})
                return
            name, content_type = assets[path]
            self.send(200, (ASSETS / name).read_bytes(), content_type)

        def do_POST(self):
            if not self.local_request():
                return
            if urlsplit(self.path).path != "/api/search":
                self.send(404, {"error": "Endpoint not found."})
                return
            if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
                self.send(415, {"error": "Send application/json."})
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= MAX_BODY:
                    self.send(413, {"error": "Search body must be between 1 and 16384 bytes."})
                    return
                payload = json.loads(self.rfile.read(size))
                result = search.search(payload)
            except (json.JSONDecodeError, UnicodeDecodeError):
                self.send(
                    400, {"error": "Invalid search. Check the situation, dates and source case."}
                )
                return
            except ValueError as error:
                self.send(400, {"error": str(error)})
                return
            self.send(200, result)

        def log_message(self, fmt, *args):
            # The reader's situation description is not logged or stored.
            pass

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    with create_server(args.port) as server:
        print(f"Case search: http://127.0.0.1:{server.server_port} (Ctrl+C to stop)", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
