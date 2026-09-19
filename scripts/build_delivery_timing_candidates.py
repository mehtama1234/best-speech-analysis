#!/usr/bin/env python3
"""Build bounded vocal-timing candidates from aligned proxy measurements."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "research/communication-job-delivery-measurement-preflight.json"
FRAMES = ROOT / "research/communication-job-delivery-interval-frame-audit.json"
OUT = ROOT / "research/communication-job-delivery-timing-candidates.json"
MD = ROOT / "writeups/communication-job-delivery-timing-candidates.md"


def main() -> int:
    preflight = json.loads(PREFLIGHT.read_text())
    frame_rows = {row["sample_id"]: row for row in json.loads(FRAMES.read_text())["items"]}
    rows = []
    for item in preflight["items"]:
        frame = frame_rows[item["sample_id"]]
        # Only intervals with a stable visible-speaker or stable-scene frame
        # sequence are routed. Multi-shot and graphic rows remain edit risks.
        if frame["delivery_navigation_status"] != "limited":
            continue
        audio = item["audio_measurements"]
        tags = []
        if audio["transcript_gap_before_seconds"] >= 1.0:
            tags.append("gap_before_captioned_unit")
        if audio["transcript_gap_after_seconds"] >= 1.0:
            tags.append("gap_after_captioned_unit")
        if audio["words_per_second_proxy"] <= 1.5:
            tags.append("lower_caption_density_proxy")
        if audio["words_per_second_proxy"] >= 4.0:
            tags.append("higher_caption_density_proxy")
        rows.append({
            "sample_id": item["sample_id"],
            "canonical_job": item["canonical_job"],
            "video_id": item["video_id"],
            "evidence_ids": item["evidence_ids_matched"],
            "source_url": frame["source_url"],
            "frame_sequence_type": frame["frame_sequence_type"],
            "candidate_tags": tags,
            "audio_measurements": audio,
            "candidate_interpretation": "No timing candidate promoted" if not tags else "Inspect whether the measured boundary or density change is audible and aligned; do not infer intentional pause or delivery effect from the proxy.",
            "practice_test": "Read the same wording twice: once with the measured boundary/density preserved and once with the timing changed. Ask a consenting listener for the takeaway and unresolved point.",
            "status": "proxy_candidate_requires_manual_listening",
            "independence": "not_independent",
        })
    report = {
        "schema_version": "1.0",
        "report_id": "communication-job-delivery-timing-candidates",
        "status": "proxy_timing_candidates_manual_listening_pending",
        "source_preflight": "research/communication-job-delivery-measurement-preflight.json",
        "source_frame_audit": "research/communication-job-delivery-interval-frame-audit.json",
        "eligibility_rule": "Only rows with delivery_navigation_status=limited are routed; multi-shot, graphic, insert and speaker-visibility-change rows are excluded.",
        "thresholds": {"gap_candidate_seconds": 1.0, "lower_density_words_per_second": 1.5, "higher_density_words_per_second": 4.0},
        "claim_boundary": "These are transcript/audio feature candidates for manual listening. They do not prove an intentional pause, emphasis, pace choice, emotion, confidence, intent, identity, alignment, effectiveness or listener outcome.",
        "item_count": len(rows),
        "candidate_count": sum(bool(row["candidate_tags"]) for row in rows),
        "items": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Delivery timing candidates", "", "Status: **proxy candidates; manual listening and independent review pending**.", "", report["claim_boundary"], "", f"Stable/limited intervals routed: **{len(rows)}** · tagged candidates: **{report['candidate_count']}**.", "", "| Sample | Job | Candidate tags | W/s proxy | Gap before | Gap after |", "|---|---|---|---:|---:|---:|"]
    for row in rows:
        a = row["audio_measurements"]
        tags = ", ".join(row["candidate_tags"]) or "none"
        lines.append(f"| `{row['sample_id']}` | `{row['canonical_job']}` | {tags} | {a['words_per_second_proxy']} | {a['transcript_gap_before_seconds']} | {a['transcript_gap_after_seconds']} |")
    lines += ["", "## How to use a candidate", "", "1. Open the source interval and listen across the entire captioned unit.", "2. Decide whether the gap is speech, silence, editing, music or missing audio.", "3. Record `indeterminate` when the source does not establish the cause.", "4. Rehearse the wording with and without the timing feature and ask a consenting listener for restatement.", "5. Keep the observation local to the wording, speaker and access mode; do not promote it to a general best practice.", ""]
    MD.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "interval_count": len(rows), "candidate_count": report["candidate_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
