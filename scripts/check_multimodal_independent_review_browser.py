#!/usr/bin/env python3
"""Browser smoke test for the blank multimodal reviewer workbook."""

import json
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "writeups/multimodal-independent-review-workbook.html"


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as error:
            print(f"multimodal independent-review browser smoke unavailable: {error}")
            return 2
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(PAGE.as_uri(), wait_until="load")
        assert page.locator("fieldset").count() == 22
        page.locator("input[name='reviewer_name']").fill("independent-smoke")
        page.locator("input[name='reviewer_role']").fill("reviewer")
        page.locator("input[name='review_date']").fill("2026-09-18")
        page.locator("input[name='review_modality']").fill("browser smoke")
        page.locator("textarea[name='conflict_statement']").fill("No conflict")
        page.locator("input[name='independent_attestation']").check()
        for select in page.locator("select[required]").all(): select.select_option(index=1)
        for textarea in page.locator("textarea[required]").all():
            if not textarea.input_value(): textarea.fill("smoke review")
        with page.expect_download() as download_info:
            page.locator("#download").click()
        exported = json.loads(Path(download_info.value.path()).read_text())
        assert exported["workbook_id"] == "multimodal-independent-review-workbook"
        assert exported["responses"]["independent_attestation"] is True
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        browser.close()
    print("multimodal independent-review browser smoke test: 21-item form renders and exports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
