# Autonomous browser smoke receipt

Status: **core_browser_smoke_passed**.

This receipt verifies local rendering, navigation, export and bounded browser interactions. It does not establish learner outcomes, listener outcomes, evidence validity or communication effectiveness.

Checks passed: **17/17**.

| Script | Result | Output |
|---|---|---|
| `scripts/check_shared_curriculum_browser.py` | `0` | shared curriculum browser smoke test: 18 cards, filters and mobile layout render |
| `scripts/check_communication_job_practice_browser.py` | `0` | communication-job practice browser smoke test: 18-job selector, evidence/delivery view and local export render |
| `scripts/check_communication_job_learner_browser.py` | `0` | communication-job learner browser smoke test: 18-card, 72-task form renders, exports and validates |
| `scripts/check_communication_job_listener_browser.py` | `0` | communication-job listener browser smoke test: 6-task form renders, exports, blocks unlocked outcomes and validates synthetic override |
| `scripts/check_vertical_slice_lesson_browser.py` | `0` | vertical slice lesson browser smoke test: lesson index and 5-section learner check render |
| `scripts/check_vertical_slice_02_learner_browser.py` | `0` | vertical slice 02 learner browser smoke test: 12-task form renders and exports |
| `scripts/check_independent_review_forms_browser.py` | `0` | checking blinded transcript review form
checking identity review form
checking function review form
checking phrase form review form
checking recurrence review form
checking counterexample review form
checking listener stimulus review form
checking multimodal review form
independent-review browser smoke test: 8 review forms render, export and validate |
| `scripts/check_communication_job_delivery_browser.py` | `0` | communication-job delivery browser smoke test: 36-item form renders, exports and validates |
| `scripts/check_multimodal_independent_review_browser.py` | `0` | multimodal independent-review browser smoke test: 21-item form renders and exports |
| `scripts/check_listener_stimulus_adjudication_browser.py` | `0` | listener stimulus adjudication browser smoke test: 18-pair decision form renders, exports and validates |
| `scripts/check_listener_stimulus_review_browser.py` | `0` | listener stimulus review browser smoke test: 18-pair form, export and validator |
| `scripts/check_vertical_slice_02_review_browser.py` | `0` | vertical slice 02 review browser smoke test: 15-item form renders and exports |
| `scripts/check_practice_pwa_browser.py` | `0` | practice PWA browser smoke: manifest and service worker registered over HTTP |
| `scripts/check_recovered_pattern_priority_review_browser.py` | `0` | {"status": "priority_review_browser_passed", "item_count": 162, "checks": 8, "export_validator": "passed_on_synthetic_partial_and_complete_exports"} |
| `scripts/check_unified_pattern_library_browser.py` | `0` | unified pattern library browser smoke: 74 cards, layer filters and search passed |
| `scripts/check_presentation_builder_browser.py` | `0` | presentation builder browser smoke: architecture, pattern selection, preview and Markdown export passed |
| `scripts/check_professional_pattern_fieldbook_browser.py` | `0` | professional fieldbook browser smoke: featured cases, 55-card catalog, filtering and search passed |

Uses Playwright Chromium; when present, /tmp/best-speech-libs supplies user-space shared libraries and is not a repository artifact.
