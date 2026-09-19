#!/usr/bin/env python3
"""Build source-linked counterexample candidates without promoting judgments."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "research/communication-job-curriculum-index.json"
OUT = ROOT / "research/communication-job-counterexample-candidate-queue.json"
MD = ROOT / "writeups/communication-job-counterexample-candidate-queue.md"

TYPES = [
    ("absent_but_speech_works", "No automatic absence or success inference is made; reviewer must compare a same-job case and document the alternative choice."),
    ("present_but_speech_fails", "Candidate is a bounded inspection target only; transcript/setting evidence cannot establish failure or listener outcome."),
    ("alternate_function", "Candidate is a comparison target only; reviewer must verify that a similar form serves another communication job in context."),
    ("confound_or_setting", "Candidate is selected because media, editing, setting or caption boundaries are visible; reviewer must document the confound."),
    ("misuse_or_copying_risk", "No source is required for a reviewer-grounded safety case; reviewer must state the accessibility, consent, privacy or appropriateness concern."),
]


def source_from_example(example: dict) -> dict:
    segments = example.get("exact_segments", [])
    first = segments[0] if segments else {}
    last = segments[-1] if segments else first
    return {
        "evidence_id": first.get("evidence_id"),
        "video_id": example.get("video_id"),
        "title": example.get("title"),
        "start_seconds": first.get("start_seconds"),
        "end_seconds": last.get("end_seconds"),
        "source_url": example.get("source_url"),
        "transcript_excerpt": " ".join(segment.get("text", "") for segment in segments),
    }


def main() -> int:
    curriculum = json.loads(CURRICULUM.read_text())
    rows = []
    for lesson in curriculum["lessons"]:
        examples = lesson.get("exact_examples", [])
        delivery = lesson.get("delivery_samples", [])
        for kind, selection_boundary in TYPES:
            if kind == "confound_or_setting" and delivery:
                sample = delivery[0]
                candidate = {
                    "evidence_id": sample.get("evidence_id"),
                    "video_id": sample.get("video_id"),
                    "title": sample.get("title"),
                    "start_seconds": sample.get("start_seconds"),
                    "end_seconds": sample.get("end_seconds"),
                    "source_url": sample.get("source_url"),
                    "transcript_excerpt": sample.get("transcript_excerpt"),
                }
                selection = "Queued from the first delivery sample because raw-media, subtitle, setting and editing checks are relevant; this is not a confirmed confound."
            elif kind in {"present_but_speech_fails", "alternate_function"} and examples:
                candidate = source_from_example(examples[0])
                selection = "Queued from the first exact example as a comparison target; no failure, alternate function or outcome is asserted."
            else:
                candidate = {"evidence_id": None, "video_id": None, "title": None, "start_seconds": None, "end_seconds": None, "source_url": None, "transcript_excerpt": None}
                selection = "No source candidate preselected; reviewer must supply or explicitly record no_candidate_found."
            rows.append({
                "candidate_id": f"candidate-counterexample:{lesson['canonical_job']}:{kind}",
                "review_item_id": f"counterexample:{lesson['canonical_job']}:{kind}",
                "card_id": lesson["pattern_id"],
                "canonical_job": lesson["canonical_job"],
                "counterexample_type": kind,
                "candidate_status": "candidate_requires_check",
                "candidate": candidate,
                "selection_note": selection,
                "review_required": selection_boundary,
                "independent_review_status": "not_reviewed",
                "claim_boundary": "Candidate routing is not a counterexample judgment and does not establish speech success, failure, listener outcome, causality or effectiveness.",
            })
    report = {
        "schema_version": "1.0",
        "queue_id": "communication-job-counterexample-candidate-queue",
        "status": "candidate_queue_not_independently_reviewed",
        "source_curriculum": "research/communication-job-curriculum-index.json",
        "job_count": len(curriculum["lessons"]),
        "candidate_count": len(rows),
        "source_linked_candidate_count": sum(bool(row["candidate"].get("evidence_id")) for row in rows),
        "confirmed_counterexample_count": 0,
        "claim_boundary": "This queue routes possible counterexample checks. Candidate presence is not evidence; absence of a candidate is not evidence that a counterexample does not exist.",
        "items": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Communication-job counterexample candidate queue", "", "Status: **candidate routing only; independently unreviewed**.", "", report["claim_boundary"], "", f"Jobs: **{report['job_count']}** · candidates: **{report['candidate_count']}** · source-linked: **{report['source_linked_candidate_count']}** · confirmed: **0**.", "", "| Job | Type | Candidate status | Source | Review boundary |", "|---|---|---|---|---|"]
    for row in rows:
        source = row["candidate"].get("evidence_id") or "reviewer must select or record none"
        lines.append(f"| `{row['canonical_job']}` | `{row['counterexample_type']}` | `{row['candidate_status']}` | `{source}` | {row['review_required']} |")
    lines += ["", "Use the [independent workbook](communication-job-counterexample-workbook.html) to accept, reject, replace or mark each candidate `no_candidate_found`. Do not copy candidate status into a confirmed result.", ""]
    MD.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "candidate_count": len(rows), "source_linked": report["source_linked_candidate_count"], "confirmed": 0}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
