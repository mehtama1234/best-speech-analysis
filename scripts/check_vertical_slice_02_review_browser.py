#!/usr/bin/env python3
"""Browser smoke test for the second-slice independent-review form."""

import json
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "writeups/vertical-slice-02-independent-review-workbook.html"


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as error:
            print(f"second-slice review browser unavailable: {error}")
            return 2
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(PAGE.as_uri(), wait_until="load")
        assert page.locator("fieldset").count() == 16, "identity plus 15 item fieldsets expected"
        assert page.locator("fieldset").nth(1).locator("strong").count() == 1
        assert page.locator("input[name='independent_attestation']").count() == 1
        assert page.locator("#download").count() == 1
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "mobile horizontal overflow"
        page.locator("input[name='reviewer_name']").fill("smoke-reviewer")
        page.locator("input[name='reviewer_role']").fill("independent smoke test")
        page.locator("input[name='review_date']").fill("2026-09-18")
        page.locator("input[name='review_modality']").fill("browser smoke")
        page.locator("textarea[name='conflict_statement']").fill("Synthetic browser test; not a research review.")
        page.locator("input[name='independent_attestation']").check()
        for select in page.locator("select[required]").all():
            select.select_option(index=1)
        for textarea in page.locator("textarea[required]").all():
            if textarea.get_attribute("name") != "conflict_statement":
                textarea.fill("Synthetic smoke-test rationale; not retained as evidence.")
        with page.expect_download() as download_info:
            page.locator("#download").click()
        exported = json.loads(Path(download_info.value.path()).read_text())
        assert exported["record_type"] == "independent_review"
        assert exported["workbook_id"] == "vertical-slice-02-independent-review-workbook"
        browser.close()
    print("vertical slice 02 review browser smoke test: 15-item form renders and exports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
