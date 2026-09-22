#!/usr/bin/env python3
"""Runtime smoke test for the recovered-pattern priority review browser."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.validate_recovered_pattern_priority_review_export import validate


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "writeups/recovered-pattern-priority-review.html"


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as exc:
            print(json.dumps({"status": "browser_unavailable", "error": str(exc)}))
            return 0
        page = browser.new_page(accept_downloads=True)
        page.goto(HTML.as_uri())
        assert page.locator("#progress").inner_text().startswith("Item 1 of 162")
        assert page.locator("#items").inner_text().find("pattern_id") < 0
        assert page.locator("#item").inner_text().find("Proposed move to check:") >= 0
        assert page.locator("#item").inner_text().find("Transcript made from the linked video’s audio") >= 0
        assert page.locator("#decision option").nth(1).inner_text().startswith("Yes — the excerpt shows this move")
        page.fill("#reviewer_code", "smoke-reviewer")
        page.fill("#reviewer_role", "independent reviewer")
        page.fill("#review_date", "2026-09-22")
        page.fill("#conflict_statement", "No conflict.")
        page.check("#independent_attestation")
        page.select_option("#decision", "indeterminate")
        for field in ["primary_function", "alternate_explanation", "context_note", "identity_note", "uncertainty_note"]:
            page.fill("#" + field, "Smoke-test note")
        page.click("#save")
        assert "saved locally" in page.locator("#status").inner_text()
        page.click("#next")
        assert page.locator("#progress").inner_text().startswith("Item 2 of 162")
        page.click("#restore")
        assert page.locator("#reviewer_code").input_value() == "smoke-reviewer"
        with page.expect_download() as partial_download_info:
            page.click("#download")
        partial = json.loads(partial_download_info.value.path().read_text())
        assert validate(partial) == []
        assert sum(response.get("decision") in {"supports_candidate", "alternate_function", "not_enough_context", "indeterminate", "identity_mismatch", "duplicate_or_compilation"} for response in partial["responses"].values()) == 1
        assert len(partial["responses"]) == 2
        assert sum(not response.get("decision") for response in partial["responses"].values()) == 1
        # Then complete the packet and confirm the validator reports a full export.
        for item_number in range(2, 163):
            if item_number > 2:
                assert page.locator("#progress").inner_text().startswith(f"Item {item_number} of 162")
            page.select_option("#decision", "indeterminate")
            for field in ["primary_function", "alternate_explanation", "context_note", "identity_note", "uncertainty_note"]:
                page.fill("#" + field, "Synthetic browser smoke record; not human evidence.")
            if item_number < 162:
                page.click("#next")
        with page.expect_download() as download_info:
            page.click("#download")
        download = download_info.value
        assert download.suggested_filename == "recovered-pattern-priority-review.json"
        exported = json.loads(download.path().read_text())
        assert validate(exported) == []
        browser.close()
    print(json.dumps({"status": "priority_review_browser_passed", "item_count": 162, "checks": 8, "export_validator": "passed_on_synthetic_partial_and_complete_exports"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
