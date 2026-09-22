#!/usr/bin/env python3
"""Browser smoke test for the 18-job local practice surface."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "writeups/communication-job-practice.html"


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as error:
            print(f"practice-surface browser smoke unavailable: {error}")
            return 2
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(PAGE.as_uri(), wait_until="load")
        lesson = page.locator("#lesson")
        assert lesson.count() == 1
        assert lesson.locator("option").count() == 18
        assert page.locator("#content h2").inner_text() == "opening"

        # Exercise every generated lesson. A selector count alone can pass
        # while later payloads contain broken evidence or step joins, so this
        # checks the complete 18-job surface before testing local persistence.
        options = lesson.locator("option")
        for index in range(options.count()):
            option = options.nth(index)
            canonical_job = option.get_attribute("value")
            label = option.inner_text()
            lesson.select_option(canonical_job)
            assert page.locator("#content h2").inner_text() == label
            assert page.locator("#content .example").count() >= 1
            assert page.locator("#content .delivery").count() == 2
            assert page.locator("#content .step").count() == 6

        lesson.select_option("17")
        assert page.locator("#content h2").inner_text() == "reflection_or_value_frame"
        assert page.locator("#content .step").count() == 6
        assert page.locator("#content .delivery").count() == 2
        page.locator("#participant").fill("smoke-practice")
        page.locator("#accessibility").fill("typed, captioned smoke path")
        page.locator("#consent").check()
        page.locator("textarea[data-step='rehearse']").fill("synthetic rehearsal response")
        page.locator("textarea[data-step='self_check']").fill("synthetic self-check response")
        page.locator("textarea[data-step='boundary']").fill("synthetic boundary response")
        page.locator("#save-local").click()
        assert "Saved locally" in page.locator("#local-status").inner_text()
        page.locator("textarea[data-step='self_check']").fill("synthetic revised self-check response")
        page.locator("#save-local").click()
        page.locator("#compare-local").click()
        assert "latest two local versions" in page.locator("#local-status").inner_text()
        assert "synthetic revised self-check response" in page.locator("#local-diff").inner_text()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        with page.expect_download() as download_info:
            page.locator("#download").click()
        exported = json.loads(Path(download_info.value.path()).read_text())
        assert exported["record_type"] == "local_communication_practice_record"
        assert exported["canonical_job"] == "reflection_or_value_frame"
        assert exported["consent"] is True
        assert exported["source_evidence_ids"]
        assert exported["delivery_sample_ids"]
        assert "effectiveness evidence" in exported["claim_boundary"]
        page.locator("#import-file").set_input_files({
            "name": "practice.json",
            "mimeType": "application/json",
            "buffer": json.dumps(exported).encode(),
        })
        page.locator("#import-local").click()
        page.locator("#local-status").wait_for(state="visible")
        page.wait_for_function("document.querySelector('#local-status').innerText.includes('Imported')")
        assert "Imported and saved locally" in page.locator("#local-status").inner_text()
        invalid = dict(exported)
        invalid["claim_boundary"] = "practice result"
        page.locator("#import-file").set_input_files({
            "name": "invalid-practice.json",
            "mimeType": "application/json",
            "buffer": json.dumps(invalid).encode(),
        })
        page.locator("#import-local").click()
        page.wait_for_function("document.querySelector('#local-status').innerText.includes('Import rejected')")
        assert "claim boundary is invalid" in page.locator("#local-status").inner_text()
        page.once("dialog", lambda dialog: dialog.accept())
        page.locator("#clear-local").click()
        assert "history cleared" in page.locator("#local-status").inner_text()
        assert "No browser-local versions saved" in page.locator("#local-list").inner_text()
        browser.close()
    print("communication-job practice browser smoke test: 18-job selector, evidence/delivery view and local export render")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
