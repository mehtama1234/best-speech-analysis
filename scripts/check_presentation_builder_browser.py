#!/usr/bin/env python3
"""Smoke-test the presenter-facing architecture and pattern builder."""

from __future__ import annotations

import json
import http.server
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/presentation-builder-browser-smoke.json"


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("presentation builder browser smoke unavailable: playwright is not installed")
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
            page.goto(f"http://127.0.0.1:{port}/writeups/presentation-builder.html")
            page.locator("#topic").fill("A safer launch process")
            page.locator("#audience").fill("The product team")
            page.locator("#outcome").fill("Choose one next experiment")
            page.locator("#sequence").select_option("make_a_proposal")
            assert page.locator(".pattern").nth(0).input_value() == "purpose_attention_example"
            assert page.locator(".pattern").nth(1).input_value() == "question_redefinition"
            assert page.locator(".pattern").nth(2).input_value() == "evidence_gap"
            page.locator(".pattern").nth(0).select_option("scope_repair")
            page.locator(".pattern").nth(1).select_option("premise_correction")
            assert "A safer launch process" in page.locator("#preview").inner_text()
            assert "Make a proposal" in page.locator("#preview").inner_text()
            assert "scope_repair" in page.locator("#preview").inner_text()
            assert "premise_correction" in page.locator("#preview").inner_text()
            with page.expect_download() as download_info:
                page.locator("#download").click()
            text = download_info.value.path().read_text()
            assert "A safer launch process" in text
            assert "Selected pattern moves" in text
            assert "scope_repair" in text
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    OUT.write_text(json.dumps({
        "schema_version": "1.0",
        "report_id": "presentation-builder-browser-smoke",
        "status": "presentation_builder_browser_smoke_passed",
        "checks": {"architecture_selected": True, "pattern_moves_selected": 2, "outline_rendered": True, "markdown_downloaded": True},
        "claim_boundary": "This verifies local rendering and export only; it is not learner, listener or effectiveness evidence.",
    }, indent=2) + "\n")
    print("presentation builder browser smoke: architecture, pattern selection, preview and Markdown export passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
