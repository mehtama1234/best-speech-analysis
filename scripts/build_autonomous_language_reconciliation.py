"""Reconcile exact phrase forms and recurrence candidates without promotion."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHRASES = ROOT / "research/corpus-phrase-form-inventory.json"
RECURRENCE = ROOT / "research/corpus-recurrence-independent-review-workbook.json"
OUT = ROOT / "research/autonomous-language-reconciliation.json"
MD = ROOT / "writeups/autonomous-language-reconciliation.md"


def context_check(item: dict) -> str:
    text = (item.get("transcript_text") or "").lower()
    forms = item.get("matched_forms") or []
    if not text or not forms:
        return "insufficient_retained_context"
    matched = any(re.search(pattern, text) for pattern in forms)
    return "candidate_form_visible_in_retained_text" if matched else "pattern_not_reproduced_check_registry"


def build() -> dict:
    phrase_payload = json.loads(PHRASES.read_text(encoding="utf-8"))
    recurrence_payload = json.loads(RECURRENCE.read_text(encoding="utf-8"))
    forms = []
    for item in phrase_payload["forms"]:
        forms.append({
            "phrase_form": item["phrase_form"],
            "family": item["family"],
            "occurrence_count": item["occurrence_count"],
            "video_count": item["video_count"],
            "train_video_count": item["train_video_count"],
            "holdout_video_count": item["holdout_video_count"],
            "example_count": len(item.get("examples", [])),
            "mechanism_hypothesis": item["mechanism_hypothesis"],
            "internal_status": "exact_retrieval_form_reconciled_not_validated_best_practice",
            "claim_boundary": "Exact retained-caption recurrence is a retrieval fact in this registry; it does not establish intent, function, delivery, effectiveness or generality.",
        })
    recurrence = []
    for item in recurrence_payload["items"]:
        recurrence.append({
            "review_item_id": item["review_item_id"],
            "phrase_family": item["phrase_family"],
            "event_split": item["event_split"],
            "video_id": item["video_id"],
            "title": item["title"],
            "evidence_id": item["evidence_id"],
            "start_seconds": item["start_seconds"],
            "end_seconds": item["end_seconds"],
            "transcript_text": item["transcript_text"],
            "matched_forms": item["matched_forms"],
            "source_url": item["source_url"],
            "internal_context_check": context_check(item),
            "original_independent_review_status": "not_received",
            "internal_status": "context_candidate_reconciled_not_independent",
            "claim_boundary": "This is an internally checked transcript candidate. It does not establish that the phrase performs the proposed function, recurs across independent events, has delivery meaning or improves communication effectiveness.",
        })
    return {
        "schema_version": "1.0",
        "reconciliation_id": "autonomous-language-reconciliation",
        "status": "internal_phrase_and_recurrence_reconciliation_complete_not_validation",
        "claim_boundary": "This report reconciles the exact phrase inventory and recurrence-review queue against retained transcript text. It does not establish independent agreement, speaker intent, function, delivery meaning, effectiveness or listener outcomes.",
        "phrase_form_count": len(forms),
        "recurrence_candidate_count": len(recurrence),
        "phrase_forms": forms,
        "recurrence_candidates": recurrence,
    }


def render(report: dict) -> str:
    family_counts = Counter(item["family"] for item in report["phrase_forms"])
    context_counts = Counter(item["internal_context_check"] for item in report["recurrence_candidates"])
    lines = [
        "# Autonomous language reconciliation",
        "",
        "Status: **internal phrase and recurrence reconciliation complete; not independent validation**.",
        "",
        report["claim_boundary"],
        "",
        f"The report covers **{report['phrase_form_count']} exact phrase forms** and **{report['recurrence_candidate_count']} recurrence candidates**.",
        "",
        "## Phrase-form inventory",
        "",
        "| Form | Family | Occurrences | Videos | Train | Holdout | Mechanism status |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for item in report["phrase_forms"]:
        lines.append(f"| `{item['phrase_form']}` | `{item['family']}` | {item['occurrence_count']} | {item['video_count']} | {item['train_video_count']} | {item['holdout_video_count']} | `{item['internal_status']}` |")
    lines += ["", "Families: " + "; ".join(f"`{k}`={v}" for k, v in sorted(family_counts.items())), "", "## Recurrence candidates", "", f"Internal context checks: " + "; ".join(f"`{k}`={v}" for k, v in sorted(context_counts.items())) + ".", "", "| Candidate | Family | Split | Evidence | Matched form(s) | Internal check |", "|---|---|---|---|---|---|"]
    for item in report["recurrence_candidates"]:
        forms = ", ".join(f"`{x}`" for x in item["matched_forms"])
        lines.append(f"| `{item['review_item_id']}` | `{item['phrase_family']}` | `{item['event_split']}` | [{item['evidence_id']}]({item['source_url']}) | {forms} | `{item['internal_context_check']}` |")
    lines += ["", "## Transfer rule", "", "Use a phrase as a retrieval handle. Read the surrounding transcript, rewrite the job in your own context, add conditions and limits, and test whether a listener can restate the intended function. Do not treat recurrence as proof of a best practice or use a connector as a complete technique.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    report = build()
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MD.write_text(render(report), encoding="utf-8")
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "markdown": str(MD.relative_to(ROOT)), "phrase_forms": report["phrase_form_count"], "recurrence_candidates": report["recurrence_candidate_count"]}, indent=2))
