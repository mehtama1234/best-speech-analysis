"""Audit stored caption timing/features without downloading or altering media."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean

from delivery_quality import rate_exclusion_reason, screened_value


def main():
    root = Path(__file__).resolve().parents[1]
    totals = Counter()
    videos = []
    exclusions = []
    extremes = []
    hashes = {}
    for path in sorted((root / "data/features").glob("*.json")):
        payload = json.loads(path.read_text())
        rows = payload["aligned_transcript"]
        counts = Counter()
        raw_rates, screened_rates = [], []
        for index, row in enumerate(rows):
            counts["segments"] += 1
            counts["overlap_previous_caption"] += index > 0 and row["start_seconds"] < rows[index-1]["end_seconds"]
            counts["no_audio_windows"] += row.get("audio_window_count", 0) == 0
            duration = row["end_seconds"] - row["start_seconds"]
            reason = rate_exclusion_reason(row)
            if reason:
                counts["rate_excluded"] += 1
                exclusions.append({"evidence_id": row["evidence_id"], "duration_seconds": duration,
                                   "word_count": row["word_count"], "raw_rate": row["words_per_second_proxy"],
                                   "reason": reason, "start_seconds": row["start_seconds"],
                                   "end_seconds": row["end_seconds"], "feature_file": str(path.relative_to(root))})
            value = screened_value(row, "words_per_second_proxy")
            if value is not None:
                screened_rates.append(value)
            raw_rates.append(row["words_per_second_proxy"])
            if row["words_per_second_proxy"] > 8:
                counts["rate_above_8_review_flag"] += 1
                extremes.append({"evidence_id": row["evidence_id"], "raw_rate": row["words_per_second_proxy"],
                                 "duration_seconds": duration, "excluded": bool(reason)})
        totals.update(counts)
        videos.append({"video_id": payload["video_id"], "counts": dict(counts),
                       "raw_mean_caption_rate": mean(raw_rates) if raw_rates else None,
                       "screened_mean_caption_rate": mean(screened_rates) if screened_rates else None})
        hashes[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    for name in ("scripts/audit_timing_quality.py", "scripts/delivery_quality.py"):
        hashes[name] = hashlib.sha256((root/name).read_bytes()).hexdigest()
    result = {"schema_version": "1.0", "scope": "stored multimodal features, not full transcript corpus or listening review",
              "feature_video_count": len(videos), "counts": dict(totals), "videos": videos,
              "rate_exclusions": exclusions, "high_rate_review_flags": extremes,
              "policy": "0.25-second minimum is a provisional quality guard, not a biological speech-rate rule. Rates above 8 are review flags, not automatic exclusions. Overlap is flagged, not repaired.",
              "source_sha256": hashes}
    (root / "research/timing-quality-audit.json").write_text(json.dumps(result, indent=2) + "\n")
    lines = ["# Caption timing quality audit", "", result["scope"] + ".", "",
             f"Videos: {len(videos)}; segments: {totals['segments']}; captions overlapping their predecessor: {totals['overlap_previous_caption']}; no audio windows: {totals['no_audio_windows']}; excluded caption rates: {totals['rate_excluded']}.", "",
             "## Excluded rates", "", "Raw records are preserved; no timestamps are silently repaired.", ""]
    for row in exclusions:
        lines.append(f"- {row['evidence_id']}: {row['word_count']} words / {row['duration_seconds']:.6f}s = {row['raw_rate']} words/s; {row['reason']}.")
    lines += ["", "## Method and limits", "", result["policy"], "",
              "Caption display intervals are not exact spoken-word boundaries. An audio-window overlap only proves that a window intersects the caption interval, not that the words were spoken throughout it. Overlapping captions reuse acoustic windows; segment counts are not independent audio observations. Mean caption rates weight captions equally, not speech duration.", "",
              "The shared screening helper is applied to current delivery summaries, baselines, individual cards and the disjoint comparison. Raw feature files remain unchanged. Screening an obvious artifact does not validate the remaining timing or pitch proxies.", "",
              "[Machine-readable counts, per-video means, flags and source hashes](../research/timing-quality-audit.json).", ""]
    (root / "writeups/timing-quality-audit.md").write_text("\n".join(lines))
    print(json.dumps({"videos": len(videos), **dict(totals)}))


if __name__ == "__main__":
    main()
