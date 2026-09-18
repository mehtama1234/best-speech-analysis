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
        cards = page.locator("article.card")
        assert cards.count() == 8, f"expected 8 cards, got {cards.count()}"
        assert page.locator("#search").count() == 1
        assert page.locator("#slice").count() == 1
        page.locator("#slice").select_option("vertical-slice-02")
        assert cards.count() == 3, "slice filter did not isolate three candidate lessons"
        page.locator("#search").fill("definition")
        assert cards.count() == 1, "search did not isolate definition candidate"
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        browser.close()
    print("shared curriculum browser smoke test: 8 cards, filters and mobile layout render")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
