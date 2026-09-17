#!/usr/bin/env python3
"""Compare reviewed supported examples with same-video delivery baselines."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, median, stdev
from review_evidence import load_annotations, supported_labels
from delivery_quality import screened_value


METRICS = [
    "mean_rms_db",
    "speech_activity_fraction",
    "mean_zero_crossing_rate",
    "mean_spectral_centroid_hz",
    "mean_pitch_hz_proxy",
    "mean_pitch_confidence_proxy",
    "words_per_second_proxy",
]


def summary(values: list[float]) -> dict:
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
    annotations = load_annotations(root)
    supported = [row for row in annotations if supported_labels(row)]
    feature_by_evidence = {}
    video_baselines = {}
    for path in (root / "data/features").glob("*.json"):
        report = json.loads(path.read_text())
        usable = [row for row in report.get("aligned_transcript", []) if row.get("audio_window_count", 0) > 0]
        video_baselines[report["video_id"]] = {
            metric: mean([screened_value(row, metric) for row in usable if screened_value(row, metric) is not None]) if any(screened_value(row, metric) is not None for row in usable) else None
            for metric in METRICS
        }
        feature_by_evidence.update({row["evidence_id"]: row for row in report.get("aligned_transcript", [])})

    # First calculate one delta per reviewed evidence item, then average within
    # each video so one long transcript cannot dominate the comparison.
    deltas_by_label_video: dict[str, dict[str, dict[str, list[float]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    examples_by_label = defaultdict(list)
    for annotation in supported:
        evidence_id = annotation["evidence_id"]
        video_id = evidence_id.split(":", 1)[0]
        feature = feature_by_evidence.get(evidence_id)
        baseline = video_baselines.get(video_id)
        if not feature or not baseline:
            continue
        labels = supported_labels(annotation)
        for label in labels:
            for metric in METRICS:
                value = screened_value(feature, metric)
                reference = baseline.get(metric)
                if value is not None and reference is not None:
                    deltas_by_label_video[label][video_id][metric].append(value - reference)
            examples_by_label[label].append({
                "evidence_id": evidence_id,
                "video_id": video_id,
                "reviewed_speech_function": annotation.get("reviewed_speech_function"),
                "text": feature.get("text"),
            })

    patterns = {}
    for label, by_video in sorted(deltas_by_label_video.items()):
        video_means = {
            video_id: {
                metric: mean(values) if values else None
                for metric, values in metrics.items()
            }
            for video_id, metrics in by_video.items()
        }
        patterns[label] = {
            "comparison": "supported_reviewed_segments_minus_same_video_all_usable_segments",
            "label_status": "resolved_label_supported_examples; exploratory_only",
            "video_count": len(video_means),
            "example_count": len(examples_by_label[label]),
            "metric_deltas": {
                metric: summary([
                    row[metric]
                    for row in video_means.values()
                    if row.get(metric) is not None
                ])
                for metric in METRICS
            },
            "per_video_deltas": video_means,
            "examples": examples_by_label[label],
        }

    report = {
        "schema_version": "0.2",
        "review_provenance": "Legacy reviewer identity unknown; contextual overrides are assistant transcript-only judgments, not independent human review.",
        "policy": "Only transcript-reviewed supported examples are included. Deltas are video-balanced and exploratory; they do not establish causation, effectiveness, or speaker-independent rules.",
        "supported_annotation_count": len(supported),
        "feature_record_count": len(video_baselines),
        "patterns": patterns,
    }
    output = root / "research/reviewed-delivery-baselines.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# Reviewed delivery versus same-video baselines",
        "",
        "Caption-rate screening excludes durations below a provisional 0.25-second floor; original features are preserved. See timing-quality-audit.md before interpreting deltas.",
        "",
        "Review provenance: legacy reviewer identity is unknown; contextual per-label overrides are assistant transcript-only judgments. Baselines include target segments and are not disjoint matched controls.",
        "",
        "This report compares transcript-reviewed supported examples with all usable transcript segments (including target examples) from the same video. Each video contributes one mean delta per label, which reduces—but does not remove—speaker, microphone, editing, topic, and segmentation confounds. Results are exploratory and do not establish effectiveness or causation.",
        "",
        f"Supported reviewed annotations: **{len(supported)}**; feature records: **{len(video_baselines)}**.",
        "",
        "| Candidate label | Videos | Examples | RMS Δ dB | Pitch Δ Hz | WPS Δ | Spectral centroid Δ Hz |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for label, item in patterns.items():
        md = item["metric_deltas"]
        lines.append(
            f"| `{label}` | {item['video_count']} | {item['example_count']} | {md['mean_rms_db']['mean_delta']} | {md['mean_pitch_hz_proxy']['mean_delta']} | {md['words_per_second_proxy']['mean_delta']} | {md['mean_spectral_centroid_hz']['mean_delta']} |"
        )
    lines += [
        "",
        "## Reading the deltas",
        "",
        "A positive delta means the reviewed segments were higher on that measured quantity than the same video's usable-segment baseline. It does not mean the speaker intentionally changed that feature or that the change improved communication. The small number of reviewed examples and the coarse measurement methods require expansion before generalization.",
        "",
    ]
    (root / "writeups/reviewed-delivery-baselines.md").write_text("\n".join(lines))
    print(json.dumps({"patterns": len(patterns), "output": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
