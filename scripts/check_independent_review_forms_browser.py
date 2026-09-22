#!/usr/bin/env python3
"""Smoke-test every independent-review form through export and validation.

The records created here are synthetic browser fixtures and are never retained
or counted as research evidence. This checks the operational contract between
the generated HTML forms and their named validators.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
FORMS = (
    ("blinded transcript", "writeups/blinded-review-packet.html", "validate_blinded_review_export"),
    ("identity", "writeups/corpus-identity-review-workbook.html", "validate_corpus_identity_review"),
    ("function", "writeups/corpus-function-independent-review-workbook.html", "validate_corpus_function_review"),
    ("phrase form", "writeups/corpus-phrase-form-independent-review-workbook.html", "validate_corpus_phrase_form_review"),
    ("recurrence", "writeups/corpus-recurrence-independent-review-workbook.html", "validate_corpus_recurrence_review"),
    ("counterexample", "writeups/communication-job-counterexample-workbook.html", "validate_communication_job_counterexample_review"),
    ("listener stimulus", "writeups/communication-job-listener-stimulus-review-workbook.html", "validate_listener_stimulus_review"),
    ("multimodal", "writeups/multimodal-independent-review-workbook.html", "validate_multimodal_independent_review"),
)


def populate(page) -> None:
    page.evaluate(
        """() => {
          for (const field of document.querySelectorAll('input, textarea')) {
            if (field.type === 'checkbox') field.checked = true;
            else if (field.type !== 'hidden' && !field.value) {
              if (field.type === 'date') field.value = '2026-09-18';
              else if (field.type === 'url') field.value = 'https://example.invalid/synthetic';
              else field.value = 'Synthetic browser smoke; not a research judgment.';
            }
          }
          for (const field of document.querySelectorAll('select[required]')) {
            if (field.options.length > 1) field.selectedIndex = 1;
          }
        }"""
    )


def main() -> int:
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        except PlaywrightError as error:
            print(f"independent-review browser smoke unavailable: {error}")
            return 2
        for label, relative_page, validator_name in FORMS:
            print(f"checking {label} review form", flush=True)
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.goto((ROOT / relative_page).as_uri(), wait_until="load")
            assert page.locator("#review").count() == 1, f"{label}: review form missing"
            assert page.locator("#download").count() == 1, f"{label}: download control missing"
            if label == "counterexample":
                # The routed candidate is convenience context; the reviewer
                # must still make every judgment from a blank decision state.
                assert page.locator("input[name='item_2_evidence_id']").input_value(), "counterexample: candidate evidence was not prefilled"
                assert page.locator("select[name='item_2_evidence_status']").input_value() == "", "counterexample: evidence decision was prefilled"
                assert page.locator("textarea[name='item_2_context_note']").input_value() == "", "counterexample: context judgment was prefilled"
            populate(page)
            if label == "counterexample":
                draft_field = page.locator("textarea[name='item_2_context_note']")
                draft_field.fill("Synthetic saved reviewer context.")
                page.locator("#save-draft").click()
                draft_field.fill("Mutated after save.")
                page.locator("#restore-draft").click()
                assert draft_field.input_value() == "Synthetic saved reviewer context."
                page.locator("#clear-draft").click()
                assert "cleared" in page.locator("#draft-status").inner_text()
            if label == "blinded transcript":
                draft_field = page.locator("textarea[name='item_2_reason']")
                draft_field.fill("Synthetic saved reviewer context.")
                page.locator("#save-draft").click()
                draft_field.fill("Mutated after save.")
                page.locator("#restore-draft").click()
                assert draft_field.input_value() == "Synthetic saved reviewer context."
                page.locator("#clear-draft").click()
                assert "cleared" in page.locator("#draft-status").inner_text()
            for field in page.locator("input[type='date']").all():
                field.fill("2026-09-18")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"{label}: mobile overflow"
            with page.expect_download(timeout=120_000) as download_info:
                page.locator("#download").click()
            record = json.loads(Path(download_info.value.path()).read_text())
            validator = importlib.import_module(validator_name)
            result = validator.validate(record)
            errors = result.get("errors", []) if isinstance(result, dict) else result
            assert errors == [], f"{label}: exported record failed validator: {errors[:8]}"
            page.close()
        browser.close()
    print("independent-review browser smoke test: 8 review forms render, export and validate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
