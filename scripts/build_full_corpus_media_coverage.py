#!/usr/bin/env python3
"""Audit local audiovisual availability across the full fixed transcript corpus."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "research/full-reading-queue.json"
OUT = ROOT / "research/full-corpus-media-coverage.json"
MD = ROOT / "writeups/full-corpus-media-coverage.md"


def files_for(directory: Path, video_id: str) -> list[str]:
    return sorted(path.name for path in directory.glob(f"{video_id}.*") if path.is_file())


def main() -> int:
    queue = json.loads(QUEUE.read_text())
    video_dir = ROOT / "data/video"
    audio_dir = ROOT / "data/audio"
    feature_dir = ROOT / "data/features"
    rows = []
    for video in queue["videos"]:
        video_id = video["video_id"]
        video_files = files_for(video_dir, video_id)
        audio_files = files_for(audio_dir, video_id)
        feature_files = files_for(feature_dir, video_id)
        if video_files and audio_files:
            state = "raw_audio_video_present"
        elif video_files:
            state = "video_only"
        elif audio_files:
            state = "audio_only"
        elif feature_files:
            state = "derived_features_only"
        else:
            state = "transcript_only_no_local_media"
        rows.append({
            "video_id": video_id,
            "title": video.get("title"),
            "source_url": video.get("url") or f"https://www.youtube.com/watch?v={video_id}",
            "transcript_review_status": "full_context_reviewed",
            "media_state": state,
            "video_files": video_files,
            "audio_files": audio_files,
            "feature_files": feature_files,
        })
    counts = Counter(row["media_state"] for row in rows)
    report = {
        "schema_version": "1.0",
        "coverage_id": "full-corpus-media-coverage",
        "status": "full_transcript_corpus_media_availability_audit_not_audiovisual_validation",
        "source_queue": str(QUEUE.relative_to(ROOT)),
        "video_count": len(rows),
        "counts": dict(sorted(counts.items())),
        "claim_boundary": "This reports local file availability across the 395-video transcript corpus. It does not prove that a file is the correct upload, that a speaker/event is identified, or that any verbal/nonverbal behavior was reviewed or effective.",
        "media_review_boundary": "Only the separately documented selected expansion and 36-sample delivery queue have bounded internal audiovisual observations. Transcript-only rows remain unreviewed for delivery.",
        "videos": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Full-corpus audiovisual availability",
        "",
        "Status: **availability audit; not full-corpus audiovisual validation**.",
        "",
        report["claim_boundary"],
        "",
        report["media_review_boundary"],
        "",
        f"Fixed transcript corpus: **{len(rows)}** videos.",
        "",
        "| Local media state | Videos |",
        "|---|---:|",
    ]
    for state, count in sorted(counts.items()):
        lines.append(f"| `{state}` | {count} |")
    lines += ["", "## Interpretation", "", "- `raw_audio_video_present` means both local file types exist; it does not establish upload identity or correct alignment.", "- `derived_features_only` supports proxy navigation only; it is not a substitute for listening or viewing.", "- `transcript_only_no_local_media` means the corpus lesson can still be transcript-derived, but verbal/nonverbal delivery cannot be inspected locally.", "- Use the [delivery inventory](communication-job-delivery-inventory.md) for the current 36-sample inspection queue and the [end-to-end goal](end-to-end-goal.md) for promotion criteria.", ""]
    MD.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "video_count": len(rows), "counts": dict(sorted(counts.items()))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
