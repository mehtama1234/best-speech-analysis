#!/usr/bin/env python3
"""Build a bounded full-local-media atlas of transcript/audio timing candidates."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "research/full-reading-queue.json"
FEATURE_DIR = ROOT / "data/features"
OUT = ROOT / "research/full-corpus-timing-candidate-atlas.json"
MD = ROOT / "writeups/full-corpus-timing-candidate-atlas.md"


def main() -> int:
    queue = json.loads(QUEUE.read_text())
    source_by_video = {row.get("video_id") or row.get("id"): row for row in queue.get("videos", queue.get("items", []))}
    candidates = []
    raw_counts = Counter()
    aligned_video_count = 0
    aligned_segment_count = 0
    density_selected = Counter()
    for path in sorted(FEATURE_DIR.glob("*.json")):
        report = json.loads(path.read_text())
        video_id = report.get("video_id")
        rows = [row for row in report.get("aligned_transcript", []) if row.get("evidence_id")]
        if not rows:
            continue
        aligned_video_count += 1
        aligned_segment_count += len(rows)
        source = source_by_video.get(video_id, {})
        url = source.get("url") or source.get("source_url") or f"https://www.youtube.com/watch?v={video_id}"
        title = source.get("title") or video_id

        def add(row: dict, reason: str, selected: bool = True) -> None:
            if not selected:
                return
            candidates.append({
                "candidate_id": f"{video_id}:{row['evidence_id'].split(':')[-1]}:{reason}",
                "video_id": video_id,
                "title": title,
                "source_url": url,
                "evidence_id": row["evidence_id"],
                "start_seconds": row.get("start_seconds"),
                "end_seconds": row.get("end_seconds"),
                "text": row.get("text", ""),
                "candidate_reason": reason,
                "words_per_second_proxy": row.get("words_per_second_proxy"),
                "transcript_gap_before_seconds": row.get("transcript_gap_before_seconds"),
                "transcript_gap_after_seconds": row.get("transcript_gap_after_seconds"),
                "mean_rms_db": row.get("mean_rms_db"),
                "speech_activity_fraction": row.get("speech_activity_fraction"),
                "feature_file": str(path.relative_to(ROOT)),
                "status": "proxy_candidate_requires_full_media_and_manual_listening",
            })

        for row in rows:
            before = row.get("transcript_gap_before_seconds")
            after = row.get("transcript_gap_after_seconds")
            if before is not None and before >= 1.0:
                raw_counts["gap_before"] += 1
                add(row, "gap_before_captioned_unit")
            if after is not None and after >= 1.0:
                raw_counts["gap_after"] += 1
                add(row, "gap_after_captioned_unit")

        # Density is highly confounded by caption segmentation. Retain only
        # the three lowest and three highest eligible rows per video, while
        # reporting the unbounded raw counts separately.
        density_rows = [row for row in rows if row.get("words_per_second_proxy") is not None and (row.get("word_count") or 0) >= 5]
        low = [row for row in density_rows if row["words_per_second_proxy"] <= 1.5]
        high = [row for row in density_rows if row["words_per_second_proxy"] >= 4.0]
        raw_counts["low_density"] += len(low)
        raw_counts["high_density"] += len(high)
        for row in sorted(low, key=lambda x: (x["words_per_second_proxy"], x["evidence_id"]))[:3]:
            density_selected["low_density"] += 1
            add(row, "lower_caption_density_proxy")
        for row in sorted(high, key=lambda x: (-x["words_per_second_proxy"], x["evidence_id"]))[:3]:
            density_selected["high_density"] += 1
            add(row, "higher_caption_density_proxy")

    # A segment can satisfy multiple candidate reasons; preserve each reason
    # because the review question differs for a boundary and density flag.
    report = {
        "schema_version": "1.0",
        "report_id": "full-corpus-timing-candidate-atlas",
        "status": "full_local_feature_proxy_atlas_manual_listening_pending",
        "source_queue": "research/full-reading-queue.json",
        "source_feature_directory": "data/features",
        "claim_boundary": "This atlas routes transcript/audio feature candidates for navigation. Caption gaps may reflect editing, missing captions, music, turn changes or silence; density reflects retained caption segmentation. No row establishes an intentional pause, pace choice, vocal meaning, identity, alignment, effectiveness or listener outcome.",
        "eligibility": "Feature reports with at least one aligned retained transcript row; density rows require at least five retained words and retain at most three low and three high rows per video.",
        "thresholds": {"gap_candidate_seconds": 1.0, "lower_density_words_per_second": 1.5, "higher_density_words_per_second": 4.0, "density_word_count_minimum": 5, "density_rows_per_video_per_side": 3},
        "coverage": {"aligned_video_count": aligned_video_count, "aligned_segment_count": aligned_segment_count, "candidate_record_count": len(candidates), "candidate_video_count": len({row["video_id"] for row in candidates}), "raw_tag_counts": dict(raw_counts), "selected_density_counts": dict(density_selected)},
        "items": candidates,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    reasons = Counter(row["candidate_reason"] for row in candidates)
    lines = ["# Full-corpus timing candidate atlas", "", "Status: **full local feature proxy atlas; manual listening and independent review pending**.", "", report["claim_boundary"], "", f"Aligned feature coverage: **{aligned_video_count} videos / {aligned_segment_count} caption rows** · routed candidate records: **{len(candidates)}** across **{report['coverage']['candidate_video_count']} videos**.", "", "| Candidate reason | Routed records | Raw matches before density cap |", "|---|---:|---:|"]
    for reason in ("gap_before_captioned_unit", "gap_after_captioned_unit", "lower_caption_density_proxy", "higher_caption_density_proxy"):
        raw_key = {"gap_before_captioned_unit": "gap_before", "gap_after_captioned_unit": "gap_after", "lower_caption_density_proxy": "low_density", "higher_caption_density_proxy": "high_density"}[reason]
        lines.append(f"| `{reason}` | {reasons[reason]} | {raw_counts[raw_key]} |")
    lines += ["", "## Review rule", "", "Open the linked source interval and inspect the complete captioned unit. Decide whether the boundary or density comes from speech, silence, an edit, music, a turn change, caption segmentation or missing data. Preserve `indeterminate` when the source cannot establish the cause. The atlas is a navigation surface, not a best-practice ranking.", ""]
    MD.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "aligned_videos": aligned_video_count, "aligned_segments": aligned_segment_count, "candidate_records": len(candidates), "candidate_videos": report["coverage"]["candidate_video_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
