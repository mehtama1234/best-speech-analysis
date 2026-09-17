#!/usr/bin/env python3
"""Build a deterministic review queue from pilot evidence candidates."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from build_segment_registry import candidate_functions
from analyze_pauses_and_rhythm import pause_after, pause_before


def sort_key(row: dict) -> str:
    return hashlib.sha256(row["evidence_id"].encode()).hexdigest()


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    reviewed = {
        json.loads(line)["evidence_id"]
        for line in (root / "research/annotation-ledger.jsonl").read_text().splitlines()
        if line.strip()
    }
    reviewed_pause = {
        json.loads(line)["evidence_id"]
        for line in (root / "research/pause-review-ledger.jsonl").read_text().splitlines()
        if line.strip()
    }
    reviewed |= reviewed_pause
    transcript_cache = {}
    by_label = defaultdict(list)
    by_pause = []
    for path in sorted((root / "data/features").glob("*.json")):
        report = json.loads(path.read_text())
        video_id = report["video_id"]
        transcript_cache[video_id] = json.loads((root / "data/transcripts" / f"{video_id}.json").read_text()).get("transcript", [])
        for row in report.get("aligned_transcript", []):
            if row["evidence_id"] in reviewed or not row.get("audio_window_count"):
                continue
            candidate = {
                "evidence_id": row["evidence_id"],
                "video_id": video_id,
                "start_seconds": row["start_seconds"],
                "end_seconds": row["end_seconds"],
                "text": row["text"],
                "mean_rms_db": row.get("mean_rms_db"),
                "speech_activity_fraction": row.get("speech_activity_fraction"),
                "mean_zero_crossing_rate": row.get("mean_zero_crossing_rate"),
                "mean_spectral_centroid_hz": row.get("mean_spectral_centroid_hz"),
                "pause_before_seconds": pause_before(report.get("audio_windows", []), row["start_seconds"]),
                "pause_after_seconds": pause_after(report.get("audio_windows", []), row["end_seconds"]),
            }
            labels = candidate_functions(row.get("text", ""))
            for label in labels:
                by_label[label].append(candidate)
            by_pause.append(candidate)

    selected = {}
    for label, candidates in sorted(by_label.items()):
        candidates = sorted(candidates, key=sort_key)
        # Preserve cross-video coverage before filling the remaining slots.
        chosen = []
        seen_videos = set()
        for row in candidates:
            if row["video_id"] not in seen_videos:
                chosen.append(row)
                seen_videos.add(row["video_id"])
            if len(chosen) >= 8:
                break
        for row in candidates:
            if len(chosen) >= 12:
                break
            if row not in chosen:
                chosen.append(row)
        for row in chosen:
            selected[row["evidence_id"]] = {**row, "review_targets": [label]}

    pause_candidates = sorted(by_pause, key=lambda row: (-(row["pause_before_seconds"] + row["pause_after_seconds"]), sort_key(row)))
    # Add examples from long measured low-energy neighborhoods when available.
    for row in sorted(pause_candidates, key=sort_key):
        if len([x for x in selected.values() if "pause_event" in x.get("review_targets", [])]) >= 12:
            break
        if row["evidence_id"] not in selected:
            selected[row["evidence_id"]] = {**row, "review_targets": ["pause_event"]}

    queue = []
    for evidence_id, row in sorted(selected.items()):
        ordinal = int(evidence_id.rsplit(":", 1)[1])
        transcript = transcript_cache[row["video_id"]]
        context = []
        for index in range(max(0, ordinal - 2), min(len(transcript), ordinal + 3)):
            context.append({
                "ordinal": index,
                "text": " ".join(str(transcript[index].get("text", "")).split()),
                "start_time": transcript[index].get("startTimeText"),
            })
        queue.append({**row, "context": context, "review_status": "unreviewed"})

    output = root / "research/annotation-queue.jsonl"
    with output.open("w") as handle:
        for row in queue:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    summary = {
        "schema_version": "0.1",
        "queue_count": len(queue),
        "candidate_target_counts": {label: sum(label in row["review_targets"] for row in queue) for label in sorted({label for row in queue for label in row["review_targets"]})},
        "excluded_reviewed_evidence_count": len(reviewed),
        "policy": "Deterministic review queue with cross-video coverage; labels are heuristic retrieval aids.",
    }
    (root / "research/annotation-queue-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
