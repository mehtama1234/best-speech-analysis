#!/usr/bin/env python3
"""Browser smoke test for the 36-item delivery-observation form."""

import json
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright

from validate_communication_job_delivery_review import validate


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "writeups/communication-job-delivery-sampling.html"
QUEUE = json.loads((ROOT / "research/communication-job-delivery-sampling.json").read_text())


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as error:
            print(f"communication-job delivery browser smoke unavailable: {error}")
            return 2
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(PAGE.as_uri(), wait_until="load")
        assert page.locator("fieldset").count() == QUEUE["item_count"] + 1
        assert page.locator("video").count() == QUEUE["item_count"]
        assert page.locator("audio").count() == QUEUE["item_count"]
        assert page.locator("a[href^='../data/features/']").count() == QUEUE["item_count"]
        page.locator("input[name='reviewer_name']").fill("delivery-browser-smoke")
        page.locator("input[name='reviewer_role']").fill("synthetic browser test")
        page.locator("input[name='review_date']").fill("2026-09-18")
        page.locator("textarea[name='review_modality']").fill("browser smoke")
        page.locator("textarea[name='conflict_statement']").fill("Synthetic browser test; not a research review.")
        for select in page.locator("select[required]").all():
            select.select_option(index=1)
        for textarea in page.locator("textarea[required]").all():
            if not textarea.input_value():
                textarea.fill("Synthetic smoke-test observation; not retained as evidence.")
        for field in page.locator("input[required]").all():
            if field.get_attribute("name") not in {"reviewer_name", "reviewer_role", "review_date"} and not field.input_value():
                field.fill("synthetic")
        with page.expect_download() as download_info:
            page.locator("#download").click()
        exported = json.loads(Path(download_info.value.path()).read_text())
        assert validate(exported, QUEUE) == []
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        browser.close()
    print("communication-job delivery browser smoke test: 36-item form renders, exports and validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
