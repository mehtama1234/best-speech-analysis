#!/usr/bin/env python3
"""Browser smoke test for the shared provisional curriculum index."""

from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "writeups/shared-provisional-curriculum.html"


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as error:
            print(f"shared curriculum browser smoke unavailable: {error}")
            return 2
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(PAGE.as_uri(), wait_until="load")
        cards = page.locator("article")
        assert cards.count() == 18, f"expected 18 cards, got {cards.count()}"
        assert page.locator("#search").count() == 1
        assert page.locator("#slice").count() == 1
        page.locator("#slice").select_option("communication-job-curriculum")
        assert cards.count() == 18, "curriculum filter changed the complete current lesson set"
        page.locator("#search").fill("opening")
        assert cards.count() == 1, "search did not isolate definition candidate"
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        browser.close()
    print("shared curriculum browser smoke test: 18 cards, filters and mobile layout render")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
