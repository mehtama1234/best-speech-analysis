#!/usr/bin/env python3
"""Smoke-test the installable practice surface over HTTP."""

from __future__ import annotations

import functools
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
WRITEUPS = ROOT / "writeups"


def main() -> int:
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(WRITEUPS))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            except PlaywrightError as error:
                print(f"practice PWA browser smoke unavailable: {error}")
                return 2
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"http://127.0.0.1:{server.server_port}/communication-job-practice.html", wait_until="networkidle")
            assert page.locator('link[rel="manifest"]').get_attribute("href") == "communication-patterns-lab.webmanifest"
            registration = page.evaluate("navigator.serviceWorker.ready.then(r => ({scope:r.scope, active:!!r.active}))")
            assert registration["active"] is True
            assert registration["scope"].endswith("/")
            assert page.locator("#lesson option").count() == 18
            context.set_offline(True)
            page.reload(wait_until="domcontentloaded")
            assert page.locator("#lesson option").count() == 18
            assert page.locator("#content h2").inner_text() == "opening"
            context.set_offline(False)
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print("practice PWA browser smoke: manifest and service worker registered over HTTP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
