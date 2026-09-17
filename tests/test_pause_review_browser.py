import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from scripts.serve_pause_review import byte_range, handler
from scripts.build_pause_review_browser import digest

ROOT = Path(__file__).resolve().parents[1]


class PauseBrowserTests(unittest.TestCase):
    def test_ranges(self):
        self.assertEqual(byte_range(None, 100), (0, 99))
        self.assertEqual(byte_range('bytes=10-20', 100), (10, 20))
        self.assertEqual(byte_range('bytes=90-', 100), (90, 99))
        self.assertEqual(byte_range('bytes=-10', 100), (90, 99))
        self.assertEqual(byte_range('bytes=0-1000', 100), (0, 99))
        for value in ['bytes=100-', 'bytes=20-10', 'bytes=-0', 'bytes=-', 'bytes=1-2,5-6']:
            with self.assertRaises(ValueError):
                byte_range(value, 100)

    def test_packet_and_source_hashes(self):
        packet = json.loads((ROOT / 'research/pause-review-packet.json').read_text())
        audit = json.loads((ROOT / 'research/local-pause-audio-audit.json').read_text())
        self.assertEqual({r['evidence_id'] for r in packet['examples']}, {r['evidence_id'] for r in audit['examples']})
        for path, expected in packet['source_sha256'].items():
            if path.startswith(('data/audio/', 'data/video/')) and not (ROOT / path).exists():
                continue
            self.assertEqual(digest(ROOT / path), expected, path)
        for row in packet['examples']:
            self.assertTrue(any(c['evidence_id'] == row['evidence_id'] for c in row['context']))
            if 'clip' in row and (ROOT / row['clip']['path']).exists():
                self.assertEqual(digest(ROOT / row['clip']['path']), row['clip']['sha256'])
        page = (ROOT / 'writeups/pause-review-browser.html').read_text()
        self.assertNotIn('__PACKET_JSON__', page)
        self.assertIn('Synchronization is unverified.', page)

    def test_server_allowlist_and_range(self):
        server = ThreadingHTTPServer(('127.0.0.1', 0), handler())
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f'http://127.0.0.1:{server.server_port}'
        try:
            with urlopen(base + '/') as response:
                self.assertEqual(response.status, 200)
            for path in ['/.env', '/research/pause-review-packet.json', '/data/video/test.mp4', '/../README.md']:
                with self.assertRaises(HTTPError) as error:
                    urlopen(base + path)
                self.assertEqual(error.exception.code, 404)
            with urlopen(Request(base + '/', headers={'Range': 'bytes=0-14'})) as response:
                self.assertEqual(response.status, 206)
                self.assertEqual(len(response.read()), 15)
            with self.assertRaises(HTTPError) as error:
                urlopen(Request(base + '/', headers={'Range': 'bytes=999999999-'}))
            self.assertEqual(error.exception.code, 416)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
