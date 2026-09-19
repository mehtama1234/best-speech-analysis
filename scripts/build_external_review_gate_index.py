#!/usr/bin/env python3
"""Build one reviewer-facing index for every pending human/data gate."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "research/external-review-gate-index.json"
OUT_MD = ROOT / "writeups/external-review-gate-index.md"
OUT_HTML = ROOT / "writeups/external-review-gate-index.html"


def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def build() -> dict:
    specs = [
        ("identity", "Corpus speaker/event identity and duplication", "research/corpus-identity-review-workbook.json", "writeups/corpus-identity-review-workbook.html", "scripts/validate_corpus_identity_review.py", "scripts/compare_corpus_identity_reviews.py", "Review all 395 queue items; do not treat title matches as proof of distinct events."),
        ("function", "Transcript function labels", "research/corpus-function-independent-review-workbook.json", "writeups/corpus-function-independent-review-workbook.html", "scripts/validate_corpus_function_review.py", "scripts/compare_corpus_function_reviews.py", "Review 187 candidate function items in full context."),
        ("recurrence", "Phrase recurrence and event-level eligibility", "research/corpus-recurrence-independent-review-workbook.json", "writeups/corpus-recurrence-independent-review-workbook.html", "scripts/validate_corpus_recurrence_review.py", "scripts/compare_corpus_recurrence_reviews.py", "Review 192 train/holdout phrase candidates; preserve indeterminate decisions."),
        ("phrase_forms", "Exact phrase-form exactness and recurrence", "research/corpus-phrase-form-independent-review-workbook.json", "writeups/corpus-phrase-form-independent-review-workbook.html", "scripts/validate_corpus_phrase_form_review.py", "scripts/compare_corpus_phrase_form_reviews.py", "Review all 50 retrieved forms before changing the inventory."),
        ("multimodal", "Independent audio/visual evidence boundaries", "research/multimodal-independent-review-workbook.json", "writeups/multimodal-independent-review-workbook.html", "scripts/validate_multimodal_independent_review.py", "scripts/compare_multimodal_independent_reviews.py", "Review 21 bounded internal media observations; proxies are not meaning or outcomes."),
        ("delivery", "Communication-job delivery observations", "research/communication-job-delivery-sampling.json", "writeups/communication-job-delivery-sampling.html", "scripts/validate_communication_job_delivery_review.py", "scripts/compare_communication_job_delivery_reviews.py", "Review 36 queued samples; record missingness and identity limits."),
        ("counterexamples", "Counterexamples, confounds and misuse limits", "research/communication-job-counterexample-workbook.json", "writeups/communication-job-counterexample-workbook.html", "scripts/validate_communication_job_counterexample_review.py", "scripts/summarize_communication_job_counterexamples.py", "Review 90 slots; no candidate is preferable to a forced example."),
        ("learner", "Learner teachability observations", "research/communication-job-learner-check.json", "writeups/communication-job-learner-check.html", "scripts/validate_communication_job_learner_record.py", "scripts/summarize_communication_job_learner_records.py", "Run the consented 18-job learner protocol; do not call it effectiveness evidence."),
        ("listener_stimuli", "Matched listener stimulus suitability", "research/communication-job-listener-stimulus-review-workbook.json", "writeups/communication-job-listener-stimulus-review-workbook.html", "scripts/validate_listener_stimulus_review.py", "scripts/compare_listener_stimulus_reviews.py", "Review 18 matched pairs for equivalence, accessibility, safety and blinding before locking."),
        ("listener_outcomes", "Blinded listener comprehension/recall", "research/communication-job-listener-outcome-protocol.json", "writeups/communication-job-listener-record.html", "scripts/validate_communication_job_listener_record.py", "scripts/summarize_communication_job_listener_records.py", "Run only after stimuli are independently reviewed and locked."),
    ]
    gates = []
    for gate_id, title, source, form, validator, comparator, action in specs:
        data = read(source)
        count = data.get("item_count", data.get("pattern_count", data.get("card_count", data.get("stimulus_pair_count", data.get("job_count", data.get("item_count", 0))))))
        if gate_id == "learner":
            count = data["task_count"]
        if gate_id == "listener_outcomes":
            count = len(data["patterns"])
        gates.append({"gate_id": gate_id, "title": title, "status": data.get("status", "unknown"), "item_count": count, "source": source, "form": form, "validator": validator, "comparator_or_summarizer": comparator, "action": action, "claim_boundary": data.get("claim_boundary", "")})
    return {"schema_version": "1.0", "index_id": "external-review-gate-index", "status": "review_operations_ready_research_evidence_incomplete", "claim_boundary": "This index routes independent review and participant-data collection. The presence of a form, validator or comparator is not evidence that a gate has been completed.", "gates": gates}


def write_outputs() -> dict:
    index = build()
    OUT_JSON.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    lines = ["# External review and data-collection gate index", "", "Status: **operations ready; research evidence incomplete**.", "", index["claim_boundary"], "", "| Gate | Status | Items/tasks | Form | Validator | Comparison/summary |", "|---|---|---:|---|---|---|"]
    for gate in index["gates"]:
        lines.append(f"| `{gate['gate_id']}` | `{gate['status']}` | {gate['item_count']} | `{gate['form']}` | `{gate['validator']}` | `{gate['comparator_or_summarizer']}` |")
    lines += ["", "## Operating rule", "", "Use the form only after reading its claim boundary. Validate every export, compare independent exports where a comparator is supplied, preserve disagreements, and adjudicate before changing any research denominator or lesson status.", ""]
    OUT_MD.write_text("\n".join(lines))
    rows = "".join(f"<tr><td><code>{html.escape(g['gate_id'])}</code></td><td>{html.escape(g['title'])}</td><td>{html.escape(g['status'])}</td><td>{g['item_count']}</td><td><a href='../{html.escape(g['form'], quote=True)}'>form</a></td><td><code>{html.escape(g['validator'])}</code></td><td><code>{html.escape(g['comparator_or_summarizer'])}</code></td></tr>" for g in index["gates"])
    OUT_HTML.write_text(f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>External review gate index</title><style>body{{font:15px/1.45 system-ui,sans-serif;max-width:1200px;margin:2rem auto;padding:0 1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ccd3da;padding:.45rem;text-align:left;vertical-align:top}}.notice{{background:#fff6d6;border-left:4px solid #b8860b;padding:1rem}}</style><h1>External review and data-collection gate index</h1><div class='notice'>{html.escape(index['claim_boundary'])}</div><table><thead><tr><th>Gate</th><th>Purpose</th><th>Status</th><th>Items/tasks</th><th>Form</th><th>Validator</th><th>Comparator/summary</th></tr></thead><tbody>{rows}</tbody></table><p>Validate every export; preserve disagreement; adjudicate before promotion.</p>")
    print(json.dumps({"output": str(OUT_JSON.relative_to(ROOT)), "gate_count": len(index["gates"])}, indent=2))
    return index


if __name__ == "__main__":
    write_outputs()
