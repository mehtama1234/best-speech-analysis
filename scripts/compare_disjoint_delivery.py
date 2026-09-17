"""Exploratory same-video comparisons excluding reviewed spans and guard bands.

These are disjoint reference segments, NOT randomized or function-matched controls.
"""
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean

try:
    from .review_evidence import load_annotations, supported_labels
    from .delivery_quality import screened_value
except ImportError:
    from review_evidence import load_annotations, supported_labels
    from delivery_quality import screened_value

METRICS = ("mean_rms_db", "mean_pitch_hz_proxy", "words_per_second_proxy")


def numeric(value):
    return type(value) in (int, float) and math.isfinite(value)


def compare_video(rows, target_ids, excluded_ids, guard_seconds=5, minimum_controls=5):
    by_id = {row["evidence_id"]: row for row in rows}
    if len(by_id) != len(rows):
        raise ValueError("Duplicate feature evidence identity")
    if guard_seconds < 0 or minimum_controls < 1:
        raise ValueError("Invalid comparison settings")
    # Exclude entire inspected context, all other legacy targets, and a guard band.
    spans = [(row["start_seconds"] - guard_seconds, row["end_seconds"] + guard_seconds)
             for row in rows if row["evidence_id"] in excluded_ids | target_ids]
    usable = [row for row in rows if row.get("audio_window_count", 0) > 0]
    targets = [row for row in usable if row["evidence_id"] in target_ids]
    controls = [row for row in usable
                if row["evidence_id"] not in excluded_ids | target_ids
                and not any(row["start_seconds"] < end and row["end_seconds"] > start
                            for start, end in spans)]
    metrics = {}
    for metric in METRICS:
        values = [screened_value(row, metric) for row in targets if screened_value(row, metric) is not None]
        reference = [screened_value(row, metric) for row in controls if screened_value(row, metric) is not None]
        all_reference = [screened_value(row, metric) for row in usable if screened_value(row, metric) is not None]
        eligible = bool(values) and len(reference) >= minimum_controls
        metrics[metric] = {
            "target_count": len(values), "control_count": len(reference),
            "target_mean": mean(values) if values else None,
            "control_mean": mean(reference) if reference else None,
            "delta": mean(values) - mean(reference) if eligible else None,
            "all_usable_reference_count": len(all_reference),
            "all_usable_delta_same_targets": mean(values) - mean(all_reference) if eligible else None,
            "status": "computed" if eligible else "insufficient_measurements",
        }
    return {"requested_target_ids": sorted(target_ids),
            "measured_target_ids": sorted(row["evidence_id"] for row in targets),
            "control_ids": sorted(row["evidence_id"] for row in controls),
            "excluded_context_or_target_ids": sorted(set(by_id) & excluded_ids),
            "metrics": metrics}


def main():
    root = Path(__file__).resolve().parents[1]
    annotations = load_annotations(root)
    review_path = root / "research/contextual-label-reviews.json"
    reviews = json.loads(review_path.read_text())["reviews"]
    excluded = {row["evidence_id"] for row in annotations}
    excluded.update(eid for review in reviews for eid in review["context_evidence_ids"])
    targets = defaultdict(lambda: defaultdict(set))
    for row in annotations:
        for label in supported_labels(row):
            targets[label][row["evidence_id"].split(":")[0]].add(row["evidence_id"])
    features = {}
    sources = [root / "research/annotation-ledger.jsonl", review_path, Path(__file__),
               root / "scripts/review_evidence.py", root / "scripts/delivery_quality.py"]
    for path in sorted((root / "data/features").glob("*.json")):
        report = json.loads(path.read_text())
        features[report["video_id"]] = report.get("aligned_transcript", [])
        sources.append(path)
    patterns = {}
    for label, videos in sorted(targets.items()):
        comparisons = {video: compare_video(features.get(video, []), ids, excluded)
                       for video, ids in sorted(videos.items())}
        metrics = {}
        for metric in METRICS:
            deltas = [item["metrics"][metric]["delta"] for item in comparisons.values()
                      if item["metrics"][metric]["delta"] is not None]
            all_deltas = [item["metrics"][metric]["all_usable_delta_same_targets"]
                          for item in comparisons.values() if item["metrics"][metric]["delta"] is not None]
            metrics[metric] = {
                "video_count": len(deltas),
                "mean_video_delta": mean(deltas) if deltas else None,
                "mean_all_usable_delta_same_targets_and_videos": mean(all_deltas) if all_deltas else None,
                "positive_videos": sum(value > 0 for value in deltas),
                "negative_videos": sum(value < 0 for value in deltas),
                "zero_videos": sum(value == 0 for value in deltas),
            }
        patterns[label] = {"requested_video_count": len(videos),
                           "per_video": comparisons, "metrics": metrics}
    output = {"schema_version": "1.0",
              "method": "equal-video mean of target mean minus disjoint same-video reference mean",
              "guard_seconds": 5, "minimum_controls_per_metric": 5,
              "rate_screen": "Exclude invalid/nonfinite rates and caption durations below provisional 0.25 seconds; raw features unchanged.",
              "limits": ["Reference segments may contain unreviewed instances of the same function.",
                         "Not matched for function, duration, scene, music or camera conditions.",
                         "Targets may contain overlapping captions; counts are not independent observations.",
                         "Both targets and controls require overlapping audio windows; this differs from older reports that retained some transcript-only target metrics.",
                         "No causal, speaker-independent or audience-outcome inference.",
                         "Audio pitch and transcript timing remain unvalidated screening proxies."],
              "source_sha256": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in sources},
              "patterns": patterns}
    (root / "research/disjoint-delivery-comparison.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Delivery compared with disjoint same-video segments", "",
             "Exploratory sensitivity analysis, not matched controls or evidence of effectiveness.",
             "Rate screening excludes caption durations below a provisional 0.25-second floor; it is not validated alignment. See timing-quality-audit.md.",
             "Every legacy annotation target and every context caption inspected in contextual review",
             "is excluded from the reference pool, with a five-second guard band. At least five",
             "finite-valued reference segments are required per metric. Each video contributes",
             "one delta; missing comparisons remain missing, not zero.", "",
             "| Label | RMS delta / videos | Pitch proxy delta / videos | WPS proxy delta / videos |",
             "| --- | --- | --- | --- |"]
    for label, item in patterns.items():
        cells = []
        for metric in METRICS:
            result = item["metrics"][metric]
            value = result["mean_video_delta"]
            cells.append(f"{value:.3f} / {result['video_count']}" if value is not None else "unavailable / 0")
        lines.append("| " + label + " | " + " | ".join(cells) + " |")
    lines += ["", "RMS deltas are in dB; pitch-proxy deltas in Hz; WPS in words/second.",
              "Full target/reference IDs, per-metric denominators, per-video signs and source hashes",
              "are in [the comparison record](../research/disjoint-delivery-comparison.json).", "",
              "## Like-for-like WPS sensitivity", "",
              "Both columns use identical eligible target segments and videos. Only the reference pool changes.",
              "These are transcript timing proxies, not validated articulation rates.", "",
              "| Label | All usable reference | Disjoint reference |", "| --- | --- | --- |"]
    for label, item in patterns.items():
        metric = item["metrics"]["words_per_second_proxy"]
        before = metric["mean_all_usable_delta_same_targets_and_videos"]
        after = metric["mean_video_delta"]
        if before is not None:
            lines.append(f"| {label} | {before:.3f} | {after:.3f} |")
    lines += ["", "## Limits", ""]
    lines += ["- " + limit for limit in output["limits"]]
    lines += ["", "The older all-usable-segment baseline is retained separately. This comparison",
              "removes direct target/context contamination; it does not remove selection bias",
              "or validate the underlying measurements. Review coverage changes the exclusion",
              "pool, so rebuild this report after contextual reviews change.", ""]
    (root / "writeups/disjoint-delivery-comparison.md").write_text("\n".join(lines))
    print(json.dumps({"patterns": len(patterns), "output": "research/disjoint-delivery-comparison.json"}))


if __name__ == "__main__":
    main()
