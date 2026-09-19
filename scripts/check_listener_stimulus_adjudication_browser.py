#!/usr/bin/env python3
"""Browser smoke test for the listener-stimulus adjudication form."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright

from validate_listener_stimulus_adjudication import validate


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "writeups/communication-job-listener-stimulus-adjudication.html"


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as error:
            print(f"stimulus adjudication browser smoke unavailable: {error}")
            return 2
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(PAGE.as_uri(), wait_until="load")
        assert page.locator("fieldset").count() == 19
        page.evaluate(
            """() => {
              for (const field of document.querySelectorAll('input, textarea')) {
                if (field.type === 'date') field.value = '2026-09-18';
                else field.value = 'synthetic adjudication smoke';
              }
              for (const field of document.querySelectorAll('select[required]')) field.selectedIndex = 1;
            }"""
        )
        for field in page.locator("input[type='date']").all():
            field.fill("2026-09-18")
        page.locator("input[name='review_a_code']").fill("synthetic-review-a")
        page.locator("input[name='review_b_code']").fill("synthetic-review-b")
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        with page.expect_download() as download_info:
            page.locator("#download").click()
        exported = json.loads(Path(download_info.value.path()).read_text())
        errors = validate(exported)
        assert errors == [], f"adjudication export failed validator: {errors[:8]}"
        assert len(exported["responses"]) == 54
        browser.close()
    print("listener stimulus adjudication browser smoke test: 18-pair decision form renders, exports and validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
