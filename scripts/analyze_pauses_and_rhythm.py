#!/usr/bin/env python3
"""Measure pilot pause and rhythm proxies around transcript events."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, median, stdev

from build_segment_registry import candidate_functions


def pause_before(windows: list[dict], start: float, limit: float = 10.0) -> float:
    eligible = [w for w in windows if w["end_seconds"] <= start + 0.05]
    count = 0
    for window in reversed(eligible):
        if window["speech_activity_proxy"]:
            break
        count += 1
        if count >= int(limit):
            break
    return float(count)


def pause_after(windows: list[dict], end: float, limit: float = 10.0) -> float:
    eligible = [w for w in windows if w["start_seconds"] >= end - 0.05]
    count = 0
    for window in eligible:
        if window["speech_activity_proxy"]:
            break
        count += 1
        if count >= int(limit):
            break
    return float(count)


def summarize(values: list[float]) -> dict:
    return {
        "video_count": len(values),
        "mean": round(mean(values), 4) if values else None,
        "median": round(median(values), 4) if values else None,
        "stddev": round(stdev(values), 4) if len(values) > 1 else 0.0 if values else None,
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    per_label_video = defaultdict(lambda: defaultdict(list))
    examples = defaultdict(list)
    for path in sorted((root / "data/features").glob("*.json")):
        report = json.loads(path.read_text())
        windows = report.get("audio_windows", [])
        rows = report.get("aligned_transcript", [])
        for row in rows:
            if not row.get("audio_window_count"):
                continue
            start = row["start_seconds"]
            end = row["end_seconds"]
            duration = max(end - start, 0.001)
            word_count = len(str(row.get("text", "")).split())
            measurement = {
                "pause_before_seconds": pause_before(windows, start),
                "pause_after_seconds": pause_after(windows, end),
                "caption_word_rate_per_second": word_count / duration,
                "mean_rms_db": row.get("mean_rms_db"),
            }
            for label in candidate_functions(row.get("text", "")):
                per_label_video[label][report["video_id"]].append(measurement)
                if len(examples[label]) < 8:
                    examples[label].append({"evidence_id": row["evidence_id"], "text": row["text"], **measurement})

    report = {"schema_version": "0.1", "measurement_policy": "Pause is a contiguous run of one-second windows below the acoustic activity threshold; transcript gaps are not treated as silence.", "patterns": {}}
    for label, by_video in sorted(per_label_video.items()):
        video_means = {}
        for video_id, rows in by_video.items():
            video_means[video_id] = {
                key: mean([row[key] for row in rows if row[key] is not None])
                for key in ("pause_before_seconds", "pause_after_seconds", "caption_word_rate_per_second", "mean_rms_db")
            }
        report["patterns"][label] = {
            "label_status": "heuristic_retrieval_aid_requires_manual_review",
            "video_count": len(video_means),
            "segment_count": sum(len(rows) for rows in by_video.values()),
            "video_weighted_metrics": {
                key: summarize([row[key] for row in video_means.values() if row[key] is not None])
                for key in ("pause_before_seconds", "pause_after_seconds", "caption_word_rate_per_second", "mean_rms_db")
            },
            "examples": examples[label],
        }
    output = root / "research/pause-rhythm-analysis.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Pilot pause and rhythm analysis",
        "",
        "This report measures acoustic low-energy runs around transcript segments. A pause here means one or more consecutive one-second audio windows below the current activity threshold; a caption gap alone is not treated as silence. Labels are heuristic and require review.",
        "",
        "| Candidate label | Videos | Segments | Mean pause before (s) | Mean pause after (s) | Caption word-rate proxy | Mean RMS dB |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for label, item in report["patterns"].items():
        metrics = item["video_weighted_metrics"]
        lines.append(f"| `{label}` | {item['video_count']} | {item['segment_count']} | {metrics['pause_before_seconds']['mean']} | {metrics['pause_after_seconds']['mean']} | {metrics['caption_word_rate_per_second']['mean']} | {metrics['mean_rms_db']['mean']} |")
    lines += [
        "",
        "## Limits",
        "",
        "The activity threshold is a loudness proxy and can be affected by music, edits, room noise, compression, and microphone gain. Caption word rate is not a validated speaking-rate measure. These outputs are for locating examples for manual review, not for inferring confidence, hesitation, or emotion.",
        "",
    ]
    (root / "writeups/pause-rhythm-analysis.md").write_text("\n".join(lines))
    print(f"wrote {output} and pause-rhythm report for {len(report['patterns'])} labels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

