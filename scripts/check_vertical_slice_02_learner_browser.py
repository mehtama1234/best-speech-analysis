#!/usr/bin/env python3
"""Browser smoke test for the candidate slice-02 learner-check form."""

import json
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright

from validate_vertical_slice_02_learner_record import validate


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "writeups/vertical-slice-02-learner-check.html"


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as error:
            print(f"slice 02 learner browser smoke unavailable: {error}")
            return 2
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(PAGE.as_uri(), wait_until="load")
        assert page.locator("fieldset.pattern").count() == 3
        assert page.locator("textarea[required]").count() == 21
        page.locator("input[name='participant_code']").fill("smoke-learner")
        page.locator("input[name='date']").fill("2026-09-18")
        page.locator("input[name='consent']").check()
        for field in page.locator("input[required]").all():
            if field.get_attribute("type") not in ("checkbox", "hidden", "date") and not field.input_value():
                field.fill("slice-02-smoke")
        for field in page.locator("textarea[required]").all():
            field.fill("smoke response")
        with page.expect_download() as download_info:
            page.locator("#download").click()
        exported = json.loads(Path(download_info.value.path()).read_text())
        assert exported["record_type"] == "learner_observation"
        assert exported["protocol_id"] == "vertical-slice-02-learner-check"
        assert exported["responses"]["consent"] is True
        assert len(exported["task_bank_ids"]) == 12
        errors = validate(Path(download_info.value.path()))
        assert errors == [], f"slice 02 learner export failed validator: {errors}"
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        browser.close()
    print("vertical slice 02 learner browser smoke test: 12-task form renders and exports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
