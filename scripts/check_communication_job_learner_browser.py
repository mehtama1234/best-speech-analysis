#!/usr/bin/env python3
"""Browser smoke test for the complete 18-job learner-check form.

The exported record is synthetic and temporary. Passing proves only that the
full lesson protocol can export a record accepted by its schema validator.
"""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright

from validate_communication_job_learner_record import validate


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "writeups/communication-job-learner-check.html"


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as error:
            print(f"communication-job learner browser smoke unavailable: {error}")
            return 2
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(PAGE.as_uri(), wait_until="load")
        assert page.locator("#check").count() == 1
        assert page.locator("fieldset").count() == 20  # session + 18 cards + facilitator record
        page.evaluate(
            """() => {
              for (const field of document.querySelectorAll('input, textarea')) {
                if (field.type === 'checkbox') field.checked = true;
                else if (field.type !== 'hidden' && !field.value) {
                  if (field.type === 'date') field.value = '2026-09-18';
                  else if (field.type === 'number') field.value = '2';
                  else field.value = 'synthetic learner smoke response';
                }
              }
              for (const field of document.querySelectorAll('select[required]')) {
                if (field.options.length > 1) field.selectedIndex = 1;
              }
            }"""
        )
        for field in page.locator("input[type='date']").all():
            field.fill("2026-09-18")
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        with page.expect_download() as download_info:
            page.locator("#download").click()
        exported_path = Path(download_info.value.path())
        exported = json.loads(exported_path.read_text())
        errors = validate(exported)
        assert errors == [], f"learner export failed validator: {errors[:8]}"
        assert len(exported["task_bank_ids"]) == 72
        browser.close()
    print("communication-job learner browser smoke test: 18-card, 72-task form renders, exports and validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
