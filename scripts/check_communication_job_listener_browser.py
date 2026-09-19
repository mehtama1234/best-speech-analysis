#!/usr/bin/env python3
"""Browser smoke test for the current listener observation form.

This proves only that the form renders, exports and satisfies the local record
schema. It creates no retained listener evidence and makes no outcome claim.
"""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright

from validate_communication_job_listener_record import validate


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "writeups/communication-job-listener-record.html"


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as error:
            print(f"listener browser smoke unavailable: {error}")
            return 2
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(PAGE.as_uri(), wait_until="load")
        assert page.locator("#record").count() == 1
        assert page.locator("textarea[name^='task_']").count() == 6
        assert page.locator("select[name^='score_']").count() == 6
        page.locator("input[name='participant_code']").fill("smoke-listener")
        page.locator("input[name='date']").fill("2026-09-18")
        page.locator("input[name='modality']").fill("captioned text")
        page.locator("input[name='stimulus_id']").fill("smoke-stimulus")
        page.locator("input[name='scorer_id_or_blind_code']").fill("smoke-blind")
        page.locator("input[name='consent']").check()
        page.locator("select[name='condition']").select_option("pattern_informed")
        page.locator("select[name='accessibility_issue']").select_option("no")
        for field in page.locator("textarea[name^='task_']").all():
            field.fill("smoke listener response")
        for field in page.locator("select[name^='score_']").all():
            field.select_option("2")
        with page.expect_download() as download_info:
            page.locator("#download").click()
        exported_path = Path(download_info.value.path())
        exported = json.loads(exported_path.read_text())
        assert exported["record_type"] == "communication_job_listener_outcome_observation"
        errors = validate(exported)
        assert errors == [], f"listener export failed validator: {errors}"
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        browser.close()
    print("communication-job listener browser smoke test: 6-task form renders, exports and validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
