#!/usr/bin/env python3
"""Route fixed-corpus videos that still lack local raw audiovisual media."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COVERAGE = ROOT / "research/full-corpus-media-coverage.json"
DELIVERY = ROOT / "research/communication-job-delivery-sampling.json"
LEDGER = ROOT / "data/media-status.jsonl"
RECOVERY_LEDGER = ROOT / "data/full-corpus-media-recovery.jsonl"
OUT = ROOT / "research/full-corpus-media-recovery-queue.json"
MD = ROOT / "writeups/full-corpus-media-recovery-queue.md"


def main() -> int:
    coverage = json.loads(COVERAGE.read_text())
    delivery = json.loads(DELIVERY.read_text())
    ledger = {}
    for ledger_path in (LEDGER, RECOVERY_LEDGER):
        if ledger_path.exists():
            for line in ledger_path.read_text().splitlines():
                if line.strip():
                    row = json.loads(line)
                    ledger[row["video_id"]] = row
    delivery_ids = {item["video_id"] for item in delivery["items"]}
    rows = []
    for video in coverage["videos"]:
        if video["media_state"] == "raw_audio_video_present":
            continue
        existing = ledger.get(video["video_id"], {})
        video_status = existing.get("video_status", "not_attempted")
        audio_status = existing.get("audio_status", "not_attempted")
        if video["video_id"] in delivery_ids:
            priority = "lesson_delivery_sample"
        elif video["media_state"] == "derived_features_only":
            priority = "feature_backed_next_candidate"
        else:
            priority = "fixed_corpus_transcript_only"
        rows.append({
            "video_id": video["video_id"],
            "title": video["title"],
            "source_url": video["source_url"],
            "media_state": video["media_state"],
            "priority": priority,
            "video_download_status": video_status,
            "audio_download_status": audio_status,
            "transcript_review_status": video["transcript_review_status"],
            "recovery_decision": "not_attempted" if video_status == "not_attempted" and audio_status == "not_attempted" else "review_existing_attempt_or_retry_safely",
            "claim_boundary": "Recovery routing only; a downloaded file requires identity, alignment, delivery and safety review before use as evidence.",
        })
    rows.sort(key=lambda row: ({"lesson_delivery_sample": 0, "feature_backed_next_candidate": 1, "fixed_corpus_transcript_only": 2}[row["priority"]], row["video_id"]))
    report = {
        "schema_version": "1.0",
        "queue_id": "full-corpus-media-recovery-queue",
        "status": "recovery_routing_not_media_validation",
        "source_coverage": str(COVERAGE.relative_to(ROOT)),
        "source_delivery_queue": str(DELIVERY.relative_to(ROOT)),
        "source_download_ledger": [str(LEDGER.relative_to(ROOT)), str(RECOVERY_LEDGER.relative_to(ROOT))],
        "item_count": len(rows),
        "counts": {"by_priority": dict(sorted(Counter(row["priority"] for row in rows).items())), "by_media_state": dict(sorted(Counter(row["media_state"] for row in rows).items())), "by_video_status": dict(sorted(Counter(row["video_download_status"] for row in rows).items()))},
        "claim_boundary": "This queue identifies fixed-corpus videos without local raw A/V and preserves prior download outcomes. It does not prove availability, identity, alignment, delivery meaning or effectiveness, and it does not authorize bypassing access, licensing or platform restrictions.",
        "items": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Full-corpus media recovery queue", "", "Status: **recovery routing; not media validation**.", "", report["claim_boundary"], "", f"Queued missing/derived items: **{len(rows)}**.", "", "| Priority | Media state | Existing video status | Items |", "|---|---|---|---:|"]
    grouped = Counter((row["priority"], row["media_state"], row["video_download_status"]) for row in rows)
    for (priority, state, status), count in sorted(grouped.items()):
        lines.append(f"| `{priority}` | `{state}` | `{status}` | {count} |")
    lines += ["", "## Operating rule", "", "1. Review access, licensing and source restrictions before any retry.", "2. Recover only what is permitted and record the result in `data/media-status.jsonl`.", "3. Rebuild the full-corpus availability audit after recovery.", "4. Treat every recovered file as unverified until speaker/event identity, transcript alignment and delivery review are completed.", "5. Keep transcript-derived lessons usable when media cannot be recovered; never infer nonverbal or vocal findings from absence.", ""]
    MD.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "item_count": len(rows), "counts": report["counts"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
