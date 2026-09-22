#!/usr/bin/env python3
"""Smoke-test the local three-move triad practice browser."""

from __future__ import annotations

import http.server
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/compound-triad-browser-smoke.json"
sys.path.insert(0, str(ROOT))
from scripts.validate_compound_triad_practice_record import validate

os.environ.setdefault("LD_LIBRARY_PATH", "/tmp/best-speech-libs/usr/lib/x86_64-linux-gnu")


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("compound triad browser smoke unavailable: playwright is not installed")
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
            page.goto(f"http://127.0.0.1:{port}/writeups/compound-pattern-triads.html")
            assert page.locator(".card").count() == 24
            page.locator("#topic").fill("A clearer product update")
            page.locator("#audience").fill("The leadership team")
            page.locator("#triad").select_option("triad-audience_invitation_and_next_turn-then-contrast_and_reversal-then-objection_and_response")
            page.locator("#generate").click()
            assert "A clearer product update" in page.locator("#draft").input_value()
            page.locator("#listener").fill("The listener can restate the three moves.")
            page.locator("#save").click()
            assert "Saved on this device." in page.locator("#status").inner_text()
            page.reload()
            page.locator("#load").click()
            assert page.locator("#topic").input_value() == "A clearer product update"
            with page.expect_download() as download_info:
                page.locator("#download").click()
            record = json.loads(download_info.value.path().read_text())
            assert record["record_type"] == "local_compound_triad_practice_record"
            assert record["source_evidence_ids"]
            assert validate(record) == []
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    OUT.write_text(json.dumps({"schema_version": "1.0", "report_id": "compound-triad-browser-smoke", "status": "compound_triad_browser_smoke_passed", "triad_count": 24, "checks": {"rendered": True, "scaffold_generated": True, "local_save_reload": True, "reflection_saved": True, "json_export": True}, "claim_boundary": "Local runtime smoke test only; it is not recurrence proof, learner evidence, listener outcomes or effectiveness evidence."}, indent=2) + "\n")
    print("compound triad browser smoke: 24 triads, scaffold, save, reload and JSON export passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
