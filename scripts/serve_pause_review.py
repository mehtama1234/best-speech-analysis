#!/usr/bin/env python3
"""Loopback-only, allowlisted review server with byte-range media support."""
import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def byte_range(header, size):
    if header is None:
        return 0, size - 1
    match = re.fullmatch(r'bytes=(\d*)-(\d*)', header)
    if not match or not any(match.groups()) or size <= 0:
        raise ValueError('Unsupported byte range')
    left, right = match.groups()
    if not left:
        length = int(right)
        if length <= 0:
            raise ValueError('Empty suffix')
        return max(0, size - length), size - 1
    start, end = int(left), min(int(right), size - 1) if right else size - 1
    if start >= size or end < start:
        raise ValueError('Unsatisfiable range')
    return start, end


def handler(root=ROOT):
    packet = json.loads((root / 'research/pause-review-packet.json').read_text())
    page = root / 'writeups/pause-review-browser.html'
    allowed = {'/': page, '/writeups/pause-review-browser.html': page}
    for row in packet['examples']:
        if 'clip' in row:
            path = row['clip']['path']
            if not re.fullmatch(r'data/cache/pause-review-clips/[a-f0-9]{20}\.webm', path):
                raise ValueError('Unexpected clip path')
            allowed['/' + path] = root / path

    class ReviewHandler(BaseHTTPRequestHandler):
        def do_HEAD(self):
            self.send_file(False)

        def do_GET(self):
            self.send_file(True)

        def log_message(self, *_args):
            pass

        def send_file(self, body):
            path = allowed.get(urlsplit(self.path).path)
            if path is None or not path.is_file() or path.is_symlink():
                self.send_error(404)
                return
            size = path.stat().st_size
            requested = self.headers.get('Range')
            try:
                start, end = byte_range(requested, size)
            except ValueError:
                self.send_response(416)
                self.send_header('Content-Range', f'bytes */{size}')
                self.send_header('Content-Length', '0')
                self.end_headers()
                return
            self.send_response(206 if requested else 200)
            self.send_header('Content-Type', 'video/webm' if path.suffix == '.webm' else 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(end - start + 1))
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            if requested:
                self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
            self.end_headers()
            if body:
                try:
                    with path.open('rb') as stream:
                        stream.seek(start)
                        remaining = end - start + 1
                        while remaining:
                            block = stream.read(min(65536, remaining))
                            if not block:
                                break
                            self.wfile.write(block)
                            remaining -= len(block)
                except (BrokenPipeError, ConnectionResetError):
                    pass
    return ReviewHandler


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8891)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler())
    print(f'Review browser: http://127.0.0.1:{args.port}/', flush=True)
    server.serve_forever()
