#!/usr/bin/env python3
"""Build a cautious delivery report from reviewed transcript functions.

This report never uses heuristic labels as ground truth. Only annotations that
were transcript-reviewed and marked supported contribute to a function summary;
unsupported annotations remain visible as counterexamples.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
try:
    from .review_evidence import load_annotations, label_supported, supported_labels
    from .delivery_quality import screened_value, rate_exclusion_reason
except ImportError:
    from review_evidence import load_annotations, label_supported, supported_labels
    from delivery_quality import screened_value, rate_exclusion_reason


METRICS = {
    "mean_rms_db": "RMS dB",
    "mean_pitch_hz_proxy": "pitch proxy Hz",
    "words_per_second_proxy": "words/second proxy",
    "transcript_gap_before_seconds": "gap before seconds",
    "transcript_gap_after_seconds": "gap after seconds",
}


def number(values: list[float]) -> dict:
    return {
        "count": len(values),
        "mean": round(mean(values), 5) if values else None,
        "stddev": round(stdev(values), 5) if len(values) > 1 else 0.0 if values else None,
        "minimum": round(min(values), 5) if values else None,
        "maximum": round(max(values), 5) if values else None,
    }


def build_patterns(groups: dict[str, list[dict]], registry: dict, measured: dict, segments: dict) -> dict:
    patterns = {}
    for label, rows in sorted(groups.items()):
        examples = []
        for row in rows:
            evidence_id = row["evidence_id"]
            video_id = evidence_id.split(":", 1)[0]
            feature = measured.get(evidence_id, {})
            segment = segments.get(evidence_id, {})
            start = segment.get("start_seconds")
            video = registry.get(video_id, {})
            examples.append({
                "annotation_id": row["annotation_id"],
                "evidence_id": evidence_id,
                "video_id": video_id,
                "title": video.get("title"),
                "channel": video.get("channel"),
                "start_seconds": start,
                "url": f"https://www.youtube.com/watch?v={video_id}&t={int(start)}" if start is not None else video.get("url"),
                "end_seconds": segment.get("end_seconds"),
                "text": segment.get("text"),
                "source_transcript_file": segment.get("source_transcript_file"),
                "transcript_evidence_status": "available" if segment else "missing_registry_segment",
                "measurement_status": "aligned_features_available" if feature else "no_aligned_features",
                "confidence": row.get("confidence"),
                "confidence_source": "legacy_annotation_not_reassessed",
                "contextual_review_id": row.get("contextual_review_id"),
                "contextual_label_decisions": row.get("label_decisions", {}),
                "reviewed_speech_function": row.get("reviewed_speech_function"),
                "measurements": {key: screened_value(feature, key) for key in METRICS},
                "raw_words_per_second_proxy": feature.get("words_per_second_proxy"),
                "rate_exclusion_reason": rate_exclusion_reason(feature),
            })

        metric_summary = {
            key: number([
                example["measurements"][key]
                for example in examples
                if example["measurements"].get(key) is not None
            ])
            for key in METRICS
        }
        patterns[label] = {
            "contextually_reviewed_example_count": sum("contextual_review_id" in row for row in rows),
            "reviewed_supported_example_count": len(rows),
            "distinct_video_count": len({row["evidence_id"].split(":", 1)[0] for row in rows}),
            "distinct_uploader_count": len({registry.get(row["evidence_id"].split(":", 1)[0], {}).get("channel") for row in rows}),
            "measurement_summary": metric_summary,
            "examples": sorted(examples, key=lambda item: item["evidence_id"]),
        }
    return patterns


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    annotations = load_annotations(root)
    registry = {
        row["video_id"]: row
        for line in (root / "data/metadata/video-registry.jsonl").read_text().splitlines()
        if line.strip()
        for row in [json.loads(line)]
    }
    measured = {}
    needed = {row["evidence_id"] for row in annotations}
    with (root / "research/segment-registry.jsonl").open() as source:
        segments = {row["evidence_id"]: row for line in source if line.strip()
                    for row in [json.loads(line)] if row["evidence_id"] in needed}
    for path in (root / "data/features").glob("*.json"):
        report = json.loads(path.read_text())
        measured.update({row["evidence_id"]: row for row in report.get("aligned_transcript", [])})

    supported = [row for row in annotations if supported_labels(row)]
    function_groups: dict[str, list[dict]] = defaultdict(list)
    label_groups: dict[str, list[dict]] = defaultdict(list)
    for row in supported:
        function_groups[row["reviewed_speech_function"]].append(row)
        for label in supported_labels(row):
            label_groups[label].append(row)
    patterns = build_patterns(function_groups, registry, measured, segments)
    label_patterns = build_patterns(label_groups, registry, measured, segments)

    label_audit = defaultdict(lambda: {"supported": 0, "unsupported": 0, "evidence_ids": []})
    for row in annotations:
        for label in row.get("candidate_labels", []):
            label_audit[label]["supported" if label_supported(row, label) else "unsupported"] += 1
            if not label_supported(row, label):
                label_audit[label]["evidence_ids"].append(row["evidence_id"])
    for value in label_audit.values():
        total = value["supported"] + value["unsupported"]
        value["reviewed_count"] = total
        value["support_rate"] = round(value["supported"] / total, 3) if total else None

    report = {
        "schema_version": "0.2",
        "review_provenance": "Legacy reviewer identity unknown; contextual overrides are assistant transcript-only judgments, not independent human review.",
        "policy": "Only transcript-reviewed supported annotations enter function summaries. This is an evidence index, not a causal or effectiveness test.",
        "reviewed_annotation_count": len(annotations),
        "supported_annotation_count": len(supported),
        "feature_record_count": len(list((root / "data/features").glob("*.json"))),
        "candidate_label_audit": dict(sorted(label_audit.items())),
        "patterns_by_reviewed_function": patterns,
        "patterns_by_candidate_label": label_patterns,
    }
    output = root / "research/reviewed-delivery-patterns.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# Reviewed delivery patterns",
        "",
        "Rate-quality screening excludes caption durations below a provisional 0.25-second floor; raw features remain unchanged. This does not validate speech timing. See timing-quality-audit.md.",
        "",
        "Review provenance: legacy reviewer identity is unknown. Contextual per-label overrides are assistant transcript-only judgments, not independent human review. See research/contextual-label-reviews.json for rubric, context IDs and hashes.",
        "",
        "This report groups only transcript-reviewed, supported transcript functions. It is an evidence index, not a test that any delivery pattern causes comprehension, persuasion, or effectiveness. The pitch field is a coarse spectral proxy; transcript gaps and words/second are alignment proxies.",
        "",
        f"Reviewed annotations: **{len(annotations)}**; supported annotations used in summaries: **{len(supported)}**; feature records available: **{report['feature_record_count']}**.",
        "",
        "## Summary",
        "",
        "| Reviewed function | Examples | Videos | Uploaders | RMS dB | Pitch proxy Hz | Words/second | Gap before s |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for function, item in patterns.items():
        summary = item["measurement_summary"]
        def value(key: str) -> str:
            return str(summary[key]["mean"]) if summary[key]["mean"] is not None else "n/a"
        lines.append(
            f"| `{function}` | {item['reviewed_supported_example_count']} | {item['distinct_video_count']} | {item['distinct_uploader_count']} | {value('mean_rms_db')} | {value('mean_pitch_hz_proxy')} | {value('words_per_second_proxy')} | {value('transcript_gap_before_seconds')} |"
        )

    lines += ["", "## Evidence by function", ""]
    for function, item in patterns.items():
        lines += [
            f"### `{function}`",
            "",
            f"Reviewed supported examples: **{item['reviewed_supported_example_count']}** across **{item['distinct_video_count']}** videos and **{item['distinct_uploader_count']}** uploaders. Uploader identity is not treated as speaker identity.",
            "",
        ]
        for example in item["examples"]:
            measurements = ", ".join(
                f"{METRICS[key]}={value}"
                for key, value in example["measurements"].items()
                if value is not None
            ) or "no aligned feature values"
            lines += [
                f"- [{example['evidence_id']}]({example['url']}): {example.get('text') or '(transcript text unavailable)'}; {measurements}.",
            ]
            if example["contextual_review_id"]:
                for label, decision in example["contextual_label_decisions"].items():
                    lines.append(f"  Contextual `{label}`: {decision.get('subtype', 'see review reason')}; attribution: {decision.get('view_attribution', 'not separately adjudicated')}. {decision['reason']}")
        lines.append("")

    lines += [
        "## Aggregate by candidate label",
        "",
        "These aggregates combine supported reviewed examples that share a retrieval label, even when their more specific reviewed functions differ.",
        "",
        "| Candidate label | Examples | Videos | Uploaders | RMS dB | Pitch proxy Hz | Words/second | Gap before s |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for label, item in label_patterns.items():
        summary = item["measurement_summary"]
        def label_value(key: str) -> str:
            return str(summary[key]["mean"]) if summary[key]["mean"] is not None else "n/a"
        lines.append(
            f"| `{label}` | {item['reviewed_supported_example_count']} | {item['distinct_video_count']} | {item['distinct_uploader_count']} | {label_value('mean_rms_db')} | {label_value('mean_pitch_hz_proxy')} | {label_value('words_per_second_proxy')} | {label_value('transcript_gap_before_seconds')} |"
        )

    lines += [
        "## Counterexample audit",
        "",
        "The candidate labels remain imperfect retrieval aids. Unsupported reviewed examples are retained rather than discarded:",
        "",
        "| Candidate label | Reviewed | Supported | Unsupported | Support rate |",
        "|---|---:|---:|---:|---:|",
    ]
    for label, item in sorted(label_audit.items()):
        lines.append(f"| `{label}` | {item['reviewed_count']} | {item['supported']} | {item['unsupported']} | {item['support_rate']} |")
    lines += [
        "",
        "A repeated measurement in this report is evidence that the reviewed examples share an observable property. It is not evidence that the property is universal, speaker-independent, intentional, or effective. General claims require more reviewed examples, explicit counterexamples, and comparisons against same-video baselines and speech-function controls.",
        "",
    ]
    (root / "writeups/reviewed-delivery-patterns.md").write_text("\n".join(lines))
    print(json.dumps({"supported_annotations": len(supported), "function_count": len(patterns), "output": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
