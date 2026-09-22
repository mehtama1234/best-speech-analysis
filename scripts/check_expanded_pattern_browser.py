#!/usr/bin/env python3
"""Smoke-test the expanded pattern browser and local outline persistence."""

from __future__ import annotations

import http.server
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/expanded-pattern-browser-smoke.json"


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("expanded pattern browser smoke unavailable: playwright is not installed")
        return 0
    port = free_port()
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(0.5)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{port}/writeups/expanded-pattern-candidate-cards.html")
            card_count = page.locator(".card").count()
            assert card_count == 33
            page.locator("#topic").fill("A safer launch process")
            page.locator("#audience").fill("The product team")
            page.locator("#outcome").fill("Choose one next experiment")
            page.locator("#sequence-preset").select_option("explain_an_unfamiliar_idea")
            page.locator("#apply-sequence").click()
            assert page.locator(".pick input:checked").count() == 3
            assert page.locator("#step-prompt-fields textarea").count() == 3
            page.locator("#step-response-orient").fill("The question is what changed, and the distinction is evidence versus assumption.")
            page.locator("#generate").click()
            outline_text = page.locator("#outline").input_value()
            assert "A safer launch process" in outline_text
            assert "Scope Repair" in outline_text
            assert "Sentence stem:" in outline_text
            assert "Boundary check:" in outline_text
            page.locator("#listener-restatement").fill("The team heard the decision and the remaining condition.")
            page.locator("#next-revision").fill("Shorten the second section.")
            page.locator("#save").click()
            assert "Saved on this device." in page.locator("#save-status").inner_text()
            page.reload()
            page.locator("#load").click()
            assert page.locator("#topic").input_value() == "A safer launch process"
            assert "remaining condition" in page.locator("#listener-restatement").input_value()
            assert "evidence versus assumption" in page.locator("#step-response-orient").input_value()
            with page.expect_download() as download_info:
                page.locator("#download-record").click()
            record = json.loads(download_info.value.path().read_text())
            assert record["record_type"] == "local_expanded_pattern_practice_record"
            assert record["schema_version"] == "1.0"
            assert record["source_evidence_ids"]
            assert "evidence versus assumption" in record["step_responses"]["step-response-orient"]
            assert "Loaded from this device." in page.locator("#save-status").inner_text()
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    receipt = {
        "schema_version": "1.0",
        "report_id": "expanded-pattern-browser-smoke",
        "status": "expanded_pattern_browser_smoke_passed",
        "card_count": card_count,
        "sequence_preset": "explain_an_unfamiliar_idea",
        "checks": {
            "outline_generated": True,
            "sentence_template_inserted": True,
            "boundary_check_inserted": True,
            "per_step_responses_saved": True,
            "reflection_saved": True,
            "draft_reloaded": True,
            "practice_json_downloaded": True,
        },
        "claim_boundary": "This is a local runtime smoke test of rendering, drafting, persistence and export. It is not learner-validation evidence, listener outcome evidence or effectiveness evidence.",
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print("expanded pattern browser smoke: 33 cards, generate, save, reload, load and JSON export passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
