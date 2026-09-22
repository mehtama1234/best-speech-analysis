#!/usr/bin/env python3
"""Check the fieldbook's chapter, index, links, print view and small-screen layout."""

from __future__ import annotations

import http.server
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

from fieldbook_core_chapters import JOB_CHAPTERS
from fieldbook_public_source_readings import PUBLIC_SOURCE_READINGS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/professional-pattern-fieldbook-browser-smoke.json"


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("professional fieldbook browser smoke unavailable: playwright is not installed")
        return 1
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(0.4)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(f"http://127.0.0.1:{port}/writeups/speaking-patterns-fieldbook.html")
            assert page.locator(".job-chapter").count() == len(JOB_CHAPTERS)
            assert page.locator(".card").count() == 55
            assert page.locator("#job-contents a").count() == len(JOB_CHAPTERS)
            for chapter in JOB_CHAPTERS:
                section = page.locator(f'#job-{chapter["id"]}')
                assert section.count() == 1
                assert chapter["title"] in section.inner_text()
            for href in page.locator('a[href^="#"]').evaluate_all('(links)=>links.map(a=>a.getAttribute("href"))'):
                assert page.locator(href).count() == 1, href

            page.emulate_media(media="print")
            assert page.locator(".print-index").is_visible()
            assert not page.locator(".catalog").is_visible()
            page.emulate_media(media="screen")
            page.screenshot(path="/tmp/speaking-fieldbook-desktop.png")
            page.locator("#job-explain").scroll_into_view_if_needed()
            page.screenshot(path="/tmp/speaking-fieldbook-chapter.png")

            for index in range(55):
                card = page.locator(".card").nth(index)
                pattern_id = card.get_attribute("id").removeprefix("pattern-")
                expected_video_links = page.evaluate(
                    """(id) => {
                        const model = JSON.parse(document.getElementById('fieldbook-data').textContent);
                        return model.items.find(item => item.pattern_id === id).source_video_links.map(link => link.url);
                    }""",
                    pattern_id,
                )
                card.locator("button").click()
                assert page.locator("#move-dialog").is_visible()
                source_example = page.locator('#move-dialog .source-example')
                assert source_example.count() == 1
                for paragraph in PUBLIC_SOURCE_READINGS[pattern_id]:
                    assert paragraph in source_example.inner_text(), pattern_id
                assert page.locator("#move-dialog h4").all_text_contents() == ["Before", "After"]
                assert page.locator("#move-dialog blockquote").count() == 2
                assert page.locator("#move-dialog #move-content ul").count() == 2
                assert page.locator("#move-dialog #move-content ul").nth(0).locator("li").count() == 3
                actual_video_links = page.locator(
                    '#move-dialog a[href^="https://www.youtube.com/watch?v="]'
                ).evaluate_all('(links)=>links.map(link=>link.href)')
                assert actual_video_links == expected_video_links, pattern_id
                detail_link = page.locator('#move-dialog a[href^="../"]')
                assert detail_link.count() == 1
                response = page.request.get(f"http://127.0.0.1:{port}/" + detail_link.get_attribute("href").removeprefix("../"))
                assert response.ok, detail_link.get_attribute("href")
                page.keyboard.press("Escape")
                assert not page.locator("#move-dialog").is_visible()

            page.locator("#category").select_option("structural_subtheme")
            assert page.locator(".card").count() > 0
            page.locator("#search").fill("analogy")
            assert page.locator(".card").count() >= 1
            page.locator("#search").fill("no-matching-pattern-zzzz")
            assert page.locator(".card").count() == 0
            page.locator("#search").fill("")
            page.locator("#category").select_option("")

            page.set_viewport_size({"width": 390, "height": 844})
            page.locator("#job-explain").scroll_into_view_if_needed()
            page.screenshot(path="/tmp/speaking-fieldbook-mobile.png")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors, errors
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    OUT.write_text(json.dumps({
        "schema_version": "1.0",
        "report_id": "professional-pattern-fieldbook-browser-smoke",
        "status": "professional_pattern_fieldbook_browser_smoke_passed",
        "checks": {
            "speaking_job_chapters": len(JOB_CHAPTERS),
            "research_index_entries": 55,
            "all_index_details_opened": True,
            "all_55_invented_before_after_examples_opened": True,
            "source_links_resolve": True,
            "search_and_category_filter_worked": True,
            "print_index_visible_and_interactive_index_hidden": True,
            "mobile_overflow": False,
            "page_errors": 0,
        },
        "claim_boundary": "This checks local page behavior only; it does not show that the advice works.",
    }, indent=2) + "\n")
    print("professional fieldbook browser smoke: seven chapters, 55 index entries, links and responsive layout passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
