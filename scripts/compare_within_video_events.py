#!/usr/bin/env python3
"""Compare candidate speech-function segments with same-video baselines."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, median, stdev

from build_segment_registry import candidate_functions


METRICS = [
    "mean_rms_db",
    "speech_activity_fraction",
    "mean_zero_crossing_rate",
    "mean_spectral_centroid_hz",
    "mean_pitch_hz_proxy",
    "mean_pitch_confidence_proxy",
]


def stats(values: list[float]) -> dict:
    return {
        "video_count": len(values),
        "mean_delta": round(mean(values), 5) if values else None,
        "median_delta": round(median(values), 5) if values else None,
        "stddev": round(stdev(values), 5) if len(values) > 1 else 0.0 if values else None,
        "minimum": round(min(values), 5) if values else None,
        "maximum": round(max(values), 5) if values else None,
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    deltas = defaultdict(lambda: defaultdict(list))
    segment_counts = defaultdict(lambda: defaultdict(int))
    for path in sorted((root / "data/features").glob("*.json")):
        report = json.loads(path.read_text())
        rows = [row for row in report.get("aligned_transcript", []) if row.get("audio_window_count", 0) > 0]
        baseline = {}
        for metric in METRICS:
            values = [row[metric] for row in rows if row.get(metric) is not None]
            baseline[metric] = mean(values) if values else None
        by_label = defaultdict(list)
        for row in rows:
            for label in candidate_functions(row.get("text", "")):
                by_label[label].append(row)
        for label, labeled_rows in by_label.items():
            segment_counts[label][report["video_id"]] = len(labeled_rows)
            for metric in METRICS:
                values = [row[metric] for row in labeled_rows if row.get(metric) is not None]
                if values and baseline[metric] is not None:
                    deltas[label][metric].append(mean(values) - baseline[metric])

    report = {"schema_version": "0.1", "comparison": "within_video_labeled_segment_mean_minus_all_segment_mean", "patterns": {}}
    for label in sorted(deltas):
        report["patterns"][label] = {
            "label_status": "heuristic_retrieval_aid_requires_manual_review",
            "video_count_by_segment_presence": len(segment_counts[label]),
            "segment_count": sum(segment_counts[label].values()),
            "metric_deltas": {metric: stats(deltas[label][metric]) for metric in METRICS},
        }
    output = root / "research/within-video-event-comparison.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Within-video event comparison",
        "",
        "For each candidate label, this compares the mean measurement of matching transcript segments with the mean measurement of all usable segments in the same video. The contrast reduces—but does not eliminate—speaker, microphone, editing, and topic confounds. Labels are heuristic retrieval aids.",
        "",
        "| Candidate label | Videos | Segments | RMS delta dB | Activity delta | ZCR delta | Spectral centroid delta Hz | Pitch proxy delta Hz | Pitch confidence delta |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for label, item in report["patterns"].items():
        md = item["metric_deltas"]
        lines.append(f"| `{label}` | {item['video_count_by_segment_presence']} | {item['segment_count']} | {md['mean_rms_db']['mean_delta']} | {md['speech_activity_fraction']['mean_delta']} | {md['mean_zero_crossing_rate']['mean_delta']} | {md['mean_spectral_centroid_hz']['mean_delta']} | {md['mean_pitch_hz_proxy']['mean_delta']} | {md['mean_pitch_confidence_proxy']['mean_delta']} |")
    lines += [
        "",
        "## Reading the table",
        "",
        "A positive RMS delta means the labeled segments were louder than that video's overall usable segments on average. It does not mean the speaker was more confident or that the delivery was more effective. A label should only become a research finding after manual review, counterexamples, and replication on a larger stratified sample.",
        "",
    ]
    (root / "writeups/within-video-event-comparison.md").write_text("\n".join(lines))
    print(f"wrote {output} and within-video report for {len(report['patterns'])} labels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
