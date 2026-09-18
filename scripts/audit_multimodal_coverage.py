#!/usr/bin/env python3
"""Audit the deterministic multimodal expansion against local media and features."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def files_for(directory: Path, video_id: str) -> list[str]:
    return sorted(path.name for path in directory.glob(f"{video_id}.*") if path.is_file())


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "data/metadata/multimodal-expansion.json").read_text())
    status_path = root / "data/media-status.jsonl"
    statuses = {
        row["video_id"]: row
        for line in status_path.read_text().splitlines()
        if line.strip()
        for row in [json.loads(line)]
    }
    atlas = json.loads((root / "research/corpus-pattern-atlas.json").read_text())
    atlas_videos = {row["video_id"]: row for row in atlas["videos"]}
    manual_review_paths = [
        root / "research/multimodal-expansion-manual-review.json",
        root / "research/multimodal-expansion-manual-review-02.json",
    ]
    manual_review_ids = set()
    for manual_review_path in manual_review_paths:
        if manual_review_path.exists():
            manual_review_ids.update(
                row["video_id"]
                for row in json.loads(manual_review_path.read_text()).get("items", [])
            )
    rows = []
    for item in manifest["videos"]:
        video_id = item["video_id"]
        video_files = files_for(root / "data/video", video_id)
        audio_files = files_for(root / "data/audio", video_id)
        feature_files = files_for(root / "data/features", video_id)
        ledger = statuses.get(video_id, {})
        if video_files and audio_files:
            media_state = "raw_audio_video_present"
        elif video_files or audio_files:
            media_state = "partial_raw_media"
        elif feature_files:
            media_state = "derived_features_only"
        else:
            media_state = "raw_media_missing"
        rows.append({
            "video_id": video_id,
            "title": item.get("title"),
            "video_url": item.get("url"),
            "duration_bucket": item.get("duration_bucket"),
            "playlist_memberships": item.get("playlist_memberships", []),
            "transcript_segments": item.get("transcript_segments", 0),
            "selection_reasons": item.get("selection_reasons", []),
            "media_state": media_state,
            "video_files": video_files,
            "audio_files": audio_files,
            "feature_files": feature_files,
            "ledger_video_status": ledger.get("video_status", "missing"),
            "ledger_audio_status": ledger.get("audio_status", "missing"),
            "candidate_function_counts": atlas_videos.get(video_id, {}).get("candidate_function_counts", {}),
            "manual_review_status": (
                "internal_bounded_review_complete_independent_review_pending"
                if video_id in manual_review_ids else "not_manually_reviewed"
            ),
        })

    counts = Counter(row["media_state"] for row in rows)
    feature_count = sum(bool(row["feature_files"]) for row in rows)
    manual_queue = [
        {
            "video_id": row["video_id"],
            "title": row["title"],
            "duration_bucket": row["duration_bucket"],
            "media_state": row["media_state"],
            "transcript_segments": row["transcript_segments"],
            "candidate_function_counts": row["candidate_function_counts"],
            "selection_reasons": row["selection_reasons"],
            "review_status": "not_manually_reviewed",
        }
        for row in rows
        if row["media_state"] == "raw_audio_video_present" and row["transcript_segments"] > 0
    ]
    raw_media_only_queue = [
        {
            "video_id": row["video_id"],
            "title": row["title"],
            "video_url": row["video_url"],
            "video_files": row["video_files"],
            "audio_files": row["audio_files"],
            "feature_files": row["feature_files"],
            "transcript_segments": row["transcript_segments"],
            "review_status": "raw_media_present_but_no_retained_transcript",
        }
        for row in rows
        if row["media_state"] == "raw_audio_video_present" and row["transcript_segments"] == 0
    ]
    report = {
        "schema_version": "0.1",
        "status": "raw_media_reconciled_manual_review_pending",
        "scope": "Deterministic multimodal expansion only; not full-corpus audiovisual validation.",
        "source_manifest": "data/metadata/multimodal-expansion.json",
        "selected_video_count": len(rows),
        "selected_with_transcripts": sum(row["transcript_segments"] > 0 for row in rows),
        "raw_audio_video_present_count": counts["raw_audio_video_present"],
        "partial_raw_media_count": counts["partial_raw_media"],
        "derived_features_only_count": counts["derived_features_only"],
        "raw_media_missing_count": counts["raw_media_missing"],
        "raw_audio_video_with_transcript_count": sum(row["media_state"] == "raw_audio_video_present" and row["transcript_segments"] > 0 for row in rows),
        "raw_audio_video_without_transcript_count": len(raw_media_only_queue),
        "derived_feature_file_count": feature_count,
        "manual_review_queue_count": len(manual_queue),
        "internal_manual_review_count": len(manual_review_ids),
        "internal_manual_review_reports": [
            str(path.relative_to(root)) for path in manual_review_paths if path.exists()
        ],
        "independent_review_status": "pending",
        "independent_review_workbook": "research/multimodal-independent-review-workbook.json",
        "independent_review_form": "writeups/multimodal-independent-review-workbook.html",
        "independent_review_validator": "scripts/validate_multimodal_independent_review.py",
        "media_state_counts": dict(sorted(counts.items())),
        "duration_bucket_counts": dict(sorted(Counter(row["duration_bucket"] for row in rows).items())),
        "videos": rows,
        "manual_review_queue": manual_queue,
        "raw_media_only_queue": raw_media_only_queue,
        "limits": [
            "Raw files prove local availability, not that a human inspected the delivery.",
            "Derived features are measurements/proxies and do not establish speech function or audience effect.",
            "The expansion is stratified but not a complete audiovisual census of the 395 transcript-reviewed videos.",
            "Candidate function counts come from heuristic transcript retrieval and remain unvalidated.",
        ],
    }
    out = root / "research/multimodal-coverage-audit.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    md = root / "writeups/multimodal-coverage-audit.md"
    lines = [
        "# Multimodal expansion coverage audit",
        "",
        "Status: **raw media reconciled; manual review pending**.",
        "",
        f"The deterministic expansion contains **{len(rows)}** selected videos, of which **{counts['raw_audio_video_present']}** have both local raw video and audio, **{counts['partial_raw_media']}** have partial raw media, **{counts['derived_features_only']}** have derived features but no local raw files, and **{counts['raw_media_missing']}** have neither local raw media nor derived features. Derived feature files are present for **{feature_count}** selected videos.",
        "",
        "This is coverage evidence, not a claim that the selected videos have been manually reviewed or that the full corpus has audiovisual coverage. Raw-complete items without retained transcripts are accounted for separately and cannot support transcript-linked speech-function review.",
        "",
        "## Manual-review queue",
        "",
        "The JSON queue is limited to selected videos with both raw streams and nonempty transcripts. Each item keeps its duration stratum, candidate-function counts, and source selection reason so reviewers can sample across settings rather than choosing only famous examples.",
        "",
        "## Limits",
        "",
        *[f"- {limit}" for limit in report["limits"]],
        "",
    ]
    md.write_text("\n".join(lines))
    print(json.dumps({
        "output": str(out),
        "selected": len(rows),
        "raw_audio_video_present": counts["raw_audio_video_present"],
        "partial_raw_media": counts["partial_raw_media"],
        "derived_features_only": counts["derived_features_only"],
        "raw_media_missing": counts["raw_media_missing"],
        "features": feature_count,
        "manual_review_queue": len(manual_queue),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
