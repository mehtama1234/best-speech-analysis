#!/usr/bin/env python3
"""Build an evidence-linked index for videos that have no safe practice route."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/corpus-findings-catalog.json"
OUT = ROOT / "writeups/unclassified-lesson-leads.md"


def clip(value: object, limit: int = 260) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def lead_for(row: dict) -> str:
    claims = []
    for relation in row.get("observed_relations", []):
        claim = clip(relation.get("claim"), 220)
        if claim and claim not in claims:
            claims.append(claim)
    if claims:
        return " / ".join(claims[:2])
    for function in row.get("observed_functions", []):
        reason = clip(function.get("reason"), 220)
        if reason and reason not in claims:
            claims.append(reason)
    return " / ".join(claims[:2]) or "No concise structural claim was recorded; inspect the linked full-context writeup."


def main() -> int:
    catalog = json.loads(SOURCE.read_text())
    rows = [
        row for row in catalog["video_findings"]
        if not row.get("candidate_job_forms") and not row.get("structural_candidate_job_forms")
    ]
    lines = [
        "# Unclassified lesson leads",
        "",
        "Status: **160 transcript-derived inspection leads; no canonical practice labels assigned**.",
        "",
        "These videos are not being discarded. Their full-context reviews contain recorded claims, boundaries or next tests, but the current evidence is not strong enough for a safe automatic route into the 18 practice jobs. Use this index to choose what to inspect next; do not treat a lead as a lesson, recurrence finding or best practice.",
        "",
        "For each row, read the linked writeup and evidence IDs, then ask: what communication problem is present, what words perform it, what alternative function is plausible, what delivery evidence is missing, and what would falsify the proposed lesson?",
        "",
        f"Coverage: **{len(rows)} videos**. The primary function route and conservative named-relation route are summarized in the [corpus learning map](corpus-learning-map.md).",
        "",
        "| # | Video / review | Recorded lesson lead | Limits / next test |",
        "|---:|---|---|---|",
    ]
    for index, row in enumerate(rows, 1):
        title = clip(row.get("title"), 90)
        writeup = row.get("writeup")
        lead = lead_for(row)
        limits = clip(" ".join(row.get("limits", [])[:2]), 240)
        if not limits:
            limits = clip(row.get("next_test") or "See the full-context writeup and evidence IDs.", 240)
        lines.append(f"| {index} | [{title}](../{writeup}) `{row['video_id']}` | {lead} | {limits} |")
    lines += [
        "",
        "## Review discipline",
        "",
        "A lead becomes a candidate only after the surrounding transcript supports a bounded function, an alternate-function check and a clear evidence boundary. Promotion still requires independent review, delivery inspection, counterexamples, learner teachability and listener testing.",
        "",
    ]
    OUT.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "lead_count": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
