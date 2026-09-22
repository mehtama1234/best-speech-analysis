#!/usr/bin/env python3
"""Smoke-test the unified fixed-plus-expansion pattern browser."""

from __future__ import annotations

import http.server
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/unified-pattern-library-browser-smoke.json"


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("unified pattern library browser smoke unavailable: playwright is not installed")
        return 0
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(0.4)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{port}/writeups/unified-pattern-library.html")
            assert page.locator(".card").count() == 74
            assert "Showing 74 of 74" in page.locator("#count").inner_text()
            page.locator("#layer").select_option("fixed corpus")
            assert "Showing 55 of 74" in page.locator("#count").inner_text()
            page.locator("#layer").select_option("expansion source")
            assert "Showing 19 of 74" in page.locator("#count").inner_text()
            expansion_link = page.locator('.card:not([hidden]) a[href="../research/wave-2-unified-candidate-crosswalk.json"]').first
            assert expansion_link.count() == 1
            response = page.request.get(f"http://127.0.0.1:{port}/research/wave-2-unified-candidate-crosswalk.json")
            assert response.ok
            assert "dry-bar-comedy-wave-2-starter" in response.text()
            page.locator("#layer").select_option("")
            page.locator("#search").fill("contrast_and_reversal")
            assert page.locator(".card:not([hidden])").count() == 1
            assert "fixed corpus" in page.locator(".card:not([hidden]) .eyebrow").inner_text().lower()
            assert page.locator('.card:not([hidden]) a[href="communication-job-practice.html"]').count() == 1
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    OUT.write_text(json.dumps({"schema_version": "1.0", "report_id": "unified-pattern-library-browser-smoke", "status": "unified_pattern_library_browser_smoke_passed", "card_count": 74, "fixed_count": 55, "expansion_count": 19, "checks": {"rendered": True, "layer_filter": True, "search_filter": True}, "claim_boundary": "Local runtime smoke test only; it is not semantic validation, learner evidence, listener outcomes or effectiveness evidence."}, indent=2) + "\n")
    print("unified pattern library browser smoke: 74 cards, layer filters and search passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
