#!/usr/bin/env python3
"""Join reviewed speech-function annotations to measured pilot features."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    feature_rows = {}
    for path in (root / "data/features").glob("*.json"):
        report = json.loads(path.read_text())
        for row in report.get("aligned_transcript", []):
            feature_rows[row["evidence_id"]] = row
    annotations = [json.loads(line) for line in (root / "research/annotation-ledger.jsonl").read_text().splitlines() if line.strip()]
    cards = []
    for annotation in annotations:
        measured = feature_rows.get(annotation["evidence_id"], {})
        cards.append({**annotation, "measured_delivery": {
            "mean_rms_db": measured.get("mean_rms_db"),
            "speech_activity_fraction": measured.get("speech_activity_fraction"),
            "mean_zero_crossing_rate": measured.get("mean_zero_crossing_rate"),
            "mean_spectral_centroid_hz": measured.get("mean_spectral_centroid_hz"),
            "audio_window_count": measured.get("audio_window_count"),
        }, "measurement_status": "direct_audio_summary_when_available" if measured else "no_pilot_media_for_video"})
    output = root / "research/reviewed-pattern-cards.json"
    output.write_text(json.dumps({"schema_version": "0.1", "cards": cards}, ensure_ascii=False, indent=2) + "\n")

    markdown = [
        "# Reviewed speech-pattern cards",
        "",
        "These cards are reviewed examples, not universal findings. The text function was reviewed from the transcript; delivery fields are directly measured audio summaries when pilot media exists.",
        "",
    ]
    for card in cards:
        measured = card["measured_delivery"]
        markdown.extend([
            f"## {card['annotation_id']}: `{card['reviewed_speech_function']}`",
            "",
            f"Evidence: `{card['evidence_id']}`",
            f"Candidate labels: {', '.join(card['candidate_labels'])}",
            f"Supported by review: **{card['candidate_label_supported']}**",
            f"Confidence: **{card['confidence']}**",
            "",
            f"Direct observation: {card['direct_observation']}",
            "",
            f"Interpretation: {card['interpretation']}",
            "",
            f"Limitation: {card['limitations']}",
            "",
            f"Delivery measurements: RMS {measured['mean_rms_db']}; speech-activity proxy {measured['speech_activity_fraction']}; zero-crossing rate {measured['mean_zero_crossing_rate']}; spectral centroid {measured['mean_spectral_centroid_hz']} Hz; overlapping audio windows {measured['audio_window_count']}.",
            "",
        ])
    (root / "writeups/reviewed-pattern-cards.md").write_text("\n".join(markdown))
    print(f"wrote {len(cards)} reviewed cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
