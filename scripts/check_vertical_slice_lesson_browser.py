#!/usr/bin/env python3
"""Browser smoke test for the learner-facing vertical-slice lesson index.

This checks rendering and navigation labels only; it does not validate evidence
or infer anything about learner outcomes.
"""

from pathlib import Path
import json
from playwright.sync_api import Error as PlaywrightError, sync_playwright

from score_vertical_slice_learner_records import load_record


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "writeups/vertical-slice-01-lesson-index.html"


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as error:
            print(
                "browser smoke test unavailable: install a runnable Chromium "
                f"and its shared libraries ({error})"
            )
            return 2
        page = browser.new_page()
        page.goto(PAGE.as_uri(), wait_until="load")
        page.wait_for_selector("article.card")
        cards = page.locator("article.card")
        count = cards.count()
        assert count == 5, f"expected five lesson cards, got {count}"
        for index in range(count):
            card = cards.nth(index)
            text = card.inner_text()
            for label in ("Open draft lesson", "Inspect evidence packet", "Practice flow", "Learner check"):
                assert label in text, f"card {index + 1} missing {label}"
        assert page.locator("h1").count() == 1
        assert page.locator("label").filter(has_text="Filter lessons").locator("input#search").count() == 1
        page.locator("#search").fill("uncertainty")
        assert cards.count() == 1, "lesson filter did not narrow to one card"
        page.set_viewport_size({"width": 390, "height": 844})
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "mobile horizontal overflow"
        page.goto((ROOT / "writeups/vertical-slice-01-learner-check.html").as_uri(), wait_until="load")
        assert page.locator("fieldset.pattern").count() == 5
        assert page.locator("input[name='consent']").count() == 1
        assert page.locator("input[type='hidden'][name$='_task_bank_ids']").count() == 5
        assert page.locator("#download").count() == 1
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "learner mobile horizontal overflow"
        for index in range(page.locator("input[required]").count()):
            field = page.locator("input[required]").nth(index)
            if field.get_attribute("type") == "checkbox":
                field.check()
            elif field.get_attribute("type") != "hidden":
                field.fill("smoke-test" if field.get_attribute("type") != "date" else "2026-09-18")
        for index in range(page.locator("select[required]").count()):
            field = page.locator("select[required]").nth(index)
            field.select_option(index=1)
        for index in range(page.locator("textarea[required]").count()):
            page.locator("textarea[required]").nth(index).fill("smoke-test response")
        for field in page.locator("textarea[name^='p']").all():
            if not field.input_value():
                field.fill("smoke-test response")
        for field in page.locator("input[type='number'][name^='p']").all():
            field.fill("2")
        with page.expect_download() as download_info:
            page.locator("#download").click()
        exported = json.loads(Path(download_info.value.path()).read_text())
        assert exported["record_type"] == "learner_observation"
        assert exported["responses"]["consent"] is True
        assert "p1_task_bank_ids" in exported["responses"]
        _, errors, _ = load_record(Path(download_info.value.path()))
        assert errors == [], f"learner export failed validator: {errors}"
        browser.close()
    print("vertical slice lesson browser smoke test: lesson index and 5-section learner check render")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
