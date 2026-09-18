#!/usr/bin/env python3
"""Reconcile legacy provisional-pattern admission with the shared curriculum."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    legacy = json.loads((ROOT / "research/provisional-practice-patterns.json").read_text())
    shared = json.loads((ROOT / "research/shared-lesson-cards.json").read_text())
    atlas = json.loads((ROOT / "research/corpus-pattern-atlas.json").read_text())
    legacy_labels = {pattern["candidate_label"] for pattern in legacy["patterns"]}
    shared_labels = {card["recurrence"]["phrase_family"] for card in shared["cards"]}
    rows = []
    for label in sorted(shared_labels | legacy_labels):
        card = next((card for card in shared["cards"] if card["recurrence"]["phrase_family"] == label), None)
        old = next((pattern for pattern in legacy["patterns"] if pattern["candidate_label"] == label), None)
        rows.append({
            "label": label,
            "legacy_contextual_admission": bool(old),
            "legacy_status": "legacy_contextual_threshold_pass" if old else "not_admitted_by_legacy_threshold_or_not_in_legacy_guidance",
            "shared_card_present": bool(card),
            "shared_card_status": card["status"] if card else None,
            "shared_validation_status": card["validation"] if card else None,
            "atlas_phrase_status": atlas["phrase_forms"].get(label, {}).get("status"),
        })
    report = {
        "schema_version": "1.0",
        "report_id": "pattern-admission-reconciliation",
        "status": "terminology_reconciled_no_pattern_promoted",
        "legacy_source": "research/provisional-practice-patterns.json",
        "shared_source": "research/shared-lesson-cards.json",
        "atlas_source": "research/corpus-pattern-atlas.json",
        "legacy_contextual_pattern_count": legacy["eligible_pattern_count"],
        "shared_draft_card_count": shared["card_count"],
        "atlas_phrase_family_count": len(atlas["phrase_forms"]),
        "claim_boundary": "Legacy contextual threshold admission, shared draft-card presence and atlas phrase retrieval are different statuses. None establishes independent semantic validation, delivery effectiveness, learner success, listener outcomes or universal best practice.",
        "admission_rules": {
            "legacy_contextual": legacy["policy"],
            "shared_curriculum": "card may be drafted to make a candidate pattern teachable, but remains provisional until independent review, delivery checks and learner checks",
            "atlas": "phrase hit or candidate function is a retrieval aid requiring manual review",
        },
        "patterns": rows,
    }
    (ROOT / "research/pattern-admission-reconciliation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Pattern-admission reconciliation", "",
        "Status: **terminology reconciled; no pattern promoted**.", "",
        report["claim_boundary"], "",
        f"- Legacy contextual threshold passes: **{report['legacy_contextual_pattern_count']}**",
        f"- Shared draft lesson cards: **{report['shared_draft_card_count']}**",
        f"- Atlas phrase families: **{report['atlas_phrase_family_count']}**",
        "", "| Label | Legacy contextual pass | Shared draft card | Current validation |", "|---|---|---|---|",
    ]
    for row in rows:
        validation = row["shared_validation_status"] or {}
        lines.append(f"| `{row['label']}` | {'yes' if row['legacy_contextual_admission'] else 'no'} | {'yes' if row['shared_card_present'] else 'no'} | `{validation.get('independent_review', 'n/a')}` / `{validation.get('learner_status', 'n/a')}` |")
    lines += ["", "The older five-pattern count is not a claim that the newer three candidate cards failed as communication forms; it reflects a different legacy annotation threshold and candidate inventory. Conversely, legacy admission is not independent human validation.", ""]
    (ROOT / "writeups/pattern-admission-reconciliation.md").write_text("\n".join(lines))
    print(json.dumps({"output": "research/pattern-admission-reconciliation.json", "legacy": report["legacy_contextual_pattern_count"], "shared": report["shared_draft_card_count"], "patterns": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
