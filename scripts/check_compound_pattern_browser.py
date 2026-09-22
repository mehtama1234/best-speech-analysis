#!/usr/bin/env python3
"""Smoke-test the compound pattern practice browser."""

from __future__ import annotations

import http.server
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/compound-pattern-browser-smoke.json"
sys.path.insert(0, str(ROOT))
from scripts.validate_compound_pattern_practice_record import validate


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("compound pattern browser smoke unavailable: playwright is not installed")
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
            page.goto(f"http://127.0.0.1:{port}/writeups/compound-pattern-bundles.html")
            assert page.locator(".card").count() == 24
            assert page.locator(".card blockquote").count() >= 24
            page.locator("#topic").fill("A safer launch process")
            page.locator("#audience").fill("The product team")
            page.locator("#bundle-select").select_option("bundle-audience_invitation_and_next_turn-then-objection_and_response")
            page.locator("#generate").click()
            assert "A safer launch process" in page.locator("#draft").input_value()
            assert "objection_and_response" in page.locator("#draft").input_value()
            page.locator("#listener-restatement").fill("The room heard the two moves and the open condition.")
            page.locator("#next-revision").fill("Make the bridge shorter.")
            page.locator("#save").click()
            assert "Saved on this device." in page.locator("#status").inner_text()
            page.reload()
            page.locator("#load").click()
            assert page.locator("#topic").input_value() == "A safer launch process"
            assert "two moves" in page.locator("#listener-restatement").input_value()
            with page.expect_download() as download_info:
                page.locator("#download").click()
            record = json.loads(download_info.value.path().read_text())
            assert record["record_type"] == "local_compound_pattern_practice_record"
            assert record["source_evidence_ids"]
            assert "two moves" in record["reflections"]["listener-restatement"]
            assert validate(record) == []
            with page.expect_download() as markdown_download:
                page.locator("#download-md").click()
            assert "compound-pattern-practice.md" in markdown_download.value.suggested_filename
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    OUT.write_text(json.dumps({"schema_version": "1.0", "report_id": "compound-pattern-browser-smoke", "status": "compound_pattern_browser_smoke_passed", "bundle_count": 24, "checks": {"rendered": True, "scaffold_generated": True, "local_save_reload": True, "reflection_saved": True, "json_export": True, "markdown_export": True}, "claim_boundary": "Local runtime smoke test only; it is not recurrence proof, learner evidence, listener outcomes or effectiveness evidence."}, indent=2) + "\n")
    print("compound pattern browser smoke: 24 bundles, scaffold, save, reload and JSON export passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
