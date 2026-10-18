#!/usr/bin/env python3
"""Serve an existing local web export for internal development checks."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8060)
    args = parser.parse_args()
    folder = ROOT / "build/web"
    if not (folder / "index.html").exists():
        parser.error("Export is missing. Run bash tools/export_web.sh first.")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(Handler, directory=str(folder)))
    print(f"Serving the exported build internally on port {args.port}; Ctrl+C stops this process.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
