#!/usr/bin/env python3
"""Reconcile fixed-corpus metadata and transcript-review linkage."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/autonomous-identity-reconciliation.json"
MD = ROOT / "writeups/autonomous-identity-reconciliation.md"
VIDEO_ID = re.compile(r"[?&]v=([A-Za-z0-9_-]{6,})")


def build() -> dict:
    queue = json.loads((ROOT / "research/full-reading-queue.json").read_text())
    reviews = json.loads((ROOT / "research/full-context-reviews.json").read_text())["reviews"]
    workbook = json.loads((ROOT / "research/corpus-identity-review-workbook.json").read_text())
    review_by_video = Counter(row.get("video_id") for row in reviews)
    workbook_by_video = {row.get("video_id"): row for row in workbook["items"]}
    rows = []
    errors = []
    for number, video in enumerate(queue["videos"], 1):
        video_id = video.get("video_id")
        problems = []
        if not video_id:
            problems.append("missing_video_id")
        if not video.get("title"):
            problems.append("missing_title")
        workbook_row = workbook_by_video.get(video_id)
        metadata = workbook_row or video
        url_match = VIDEO_ID.search(metadata.get("source_url", ""))
        if not url_match or url_match.group(1) != video_id:
            problems.append("source_url_video_id_mismatch")
        if review_by_video.get(video_id) != 1:
            problems.append("full_context_review_linkage_not_one_to_one")
        if not workbook_row:
            problems.append("identity_workbook_link_missing")
        else:
            for field in ("title",):
                if workbook_row.get(field) != video.get(field):
                    problems.append(f"workbook_{field}_mismatch")
        rows.append({
            "video_id": video_id,
            "queue_order": video.get("queue_order", number),
            "title": video.get("title"),
            "channel": metadata.get("channel"),
            "review_count": review_by_video.get(video_id, 0),
            "metadata_status": "metadata_consistent_not_identity_proof" if not problems else "metadata_reconciliation_issue",
            "issues": problems,
        })
        errors.extend(f"{video_id}: {problem}" for problem in problems)
    duplicate_ids = [video_id for video_id, count in Counter(row.get("video_id") for row in queue["videos"]).items() if count > 1]
    if duplicate_ids:
        errors.append(f"duplicate queue IDs: {', '.join(duplicate_ids)}")
    title_counts = Counter(row.get("title") for row in queue["videos"])
    same_title_groups = sum(count > 1 for count in title_counts.values())
    return {
        "schema_version": "1.0",
        "reconciliation_id": "autonomous-identity-reconciliation",
        "status": "metadata_reconciliation_complete_identity_not_proven" if not errors else "needs_repair",
        "video_count": len(rows),
        "metadata_consistent_count": sum(row["metadata_status"] == "metadata_consistent_not_identity_proof" for row in rows),
        "issue_count": len(errors),
        "same_title_group_count": same_title_groups,
        "errors": errors,
        "rows": rows,
        "claim_boundary": "This checks deterministic metadata consistency, source URL linkage, one-to-one full-context review linkage and identity-workbook coverage. It does not prove who is speaking, event identity, upload/event equivalence, duplication decisions or recurrence eligibility.",
    }


def render(report: dict) -> str:
    return "\n".join([
        "# Autonomous identity reconciliation",
        "",
        f"Status: **{report['status']}**.",
        "",
        report["claim_boundary"],
        "",
        f"Metadata-consistent rows: **{report['metadata_consistent_count']}/{report['video_count']}**; same-title groups retained for review: **{report['same_title_group_count']}**.",
        "",
        "Every fixed-corpus row has a deterministic source-ID/URL check, title and channel fields, exactly one full-context review link, and an identity-workbook row. Blank identity decisions remain blank.",
        "",
        "The result is a provenance preflight, not speaker or event identity evidence.",
        "",
    ])


if __name__ == "__main__":
    report = build()
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"autonomous identity reconciliation: {report['status']} ({report['metadata_consistent_count']}/{report['video_count']})")
    if report["errors"]:
        raise SystemExit(1)
