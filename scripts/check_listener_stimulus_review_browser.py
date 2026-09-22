#!/usr/bin/env python3
"""Smoke-test the 18-pair listener stimulus review workbook."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright

from validate_listener_stimulus_review import validate

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "writeups/communication-job-listener-stimulus-review-workbook.html"


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as error:
            print(f"stimulus review browser smoke unavailable: {error}")
            return 2
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(PAGE.as_uri(), wait_until="load")
        assert page.locator("html[lang='en']").count() == 1
        assert page.locator("fieldset").count() == 19
        assert page.locator("#export-status[aria-live='polite']").count() == 1
        for control in page.locator("input, select, textarea").all():
            if control.get_attribute("type") == "checkbox":
                control.check()
            elif control.get_attribute("type") == "date":
                control.fill("2026-09-19")
            elif control.evaluate("el => el.tagName.toLowerCase()") == "select":
                control.select_option(index=1)
            else:
                control.fill("synthetic review response")
        with page.expect_download() as download_info:
            page.locator("#download").click()
        exported = json.loads(Path(download_info.value.path()).read_text())
        assert validate(exported) == []
        assert "downloaded locally" in page.locator("#export-status").inner_text()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        browser.close()
    print("listener stimulus review browser smoke test: 18-pair form, export and validator")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
