#!/usr/bin/env python3
"""Join reviewed speech-function annotations to measured pilot features."""

from __future__ import annotations

import json
from pathlib import Path
from review_evidence import load_annotations, label_supported
from delivery_quality import screened_value, rate_exclusion_reason


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    feature_rows = {}
    for path in (root / "data/features").glob("*.json"):
        report = json.loads(path.read_text())
        for row in report.get("aligned_transcript", []):
            feature_rows[row["evidence_id"]] = row
    annotations = load_annotations(root)
    cards = []
    for annotation in annotations:
        measured = feature_rows.get(annotation["evidence_id"], {})
        cards.append({**annotation, "resolved_label_support": {label: label_supported(annotation, label) for label in annotation["candidate_labels"]}, "measured_delivery": {
            "mean_rms_db": measured.get("mean_rms_db"),
            "speech_activity_fraction": measured.get("speech_activity_fraction"),
            "mean_zero_crossing_rate": measured.get("mean_zero_crossing_rate"),
            "mean_spectral_centroid_hz": measured.get("mean_spectral_centroid_hz"),
            "mean_pitch_hz_proxy": measured.get("mean_pitch_hz_proxy"),
            "mean_pitch_confidence_proxy": measured.get("mean_pitch_confidence_proxy"),
            "words_per_second_proxy": screened_value(measured, "words_per_second_proxy"),
            "raw_words_per_second_proxy": measured.get("words_per_second_proxy"),
            "rate_exclusion_reason": rate_exclusion_reason(measured),
            "transcript_gap_before_seconds": measured.get("transcript_gap_before_seconds"),
            "transcript_gap_after_seconds": measured.get("transcript_gap_after_seconds"),
            "audio_window_count": measured.get("audio_window_count"),
        }, "measurement_status": "direct_audio_summary_when_available" if measured else "no_pilot_media_for_video"})
    output = root / "research/reviewed-pattern-cards.json"
    output.write_text(json.dumps({"schema_version": "0.1", "cards": cards}, ensure_ascii=False, indent=2) + "\n")

    markdown = [
        "# Reviewed speech-pattern cards",
        "",
        "Legacy reviewer identity is unknown. Contextual overrides are explicitly assistant transcript-only review, not independent human review; see research/contextual-label-reviews.json.",
        "",
        "These cards are reviewed examples, not universal findings. The text function was reviewed from the transcript; delivery fields are directly measured audio summaries when pilot media exists.",
        "",
    ]
    for card in cards:
        measured = card["measured_delivery"]
        contextual_lines = []
        for label, decision in card.get("label_decisions", {}).items():
            contextual_lines.append(
                f"Current contextual `{label}`: {decision.get('subtype', 'unspecified')}; "
                f"attribution: {decision.get('view_attribution', 'not separately adjudicated')}. "
                f"{decision['reason']}")
        markdown.extend([
            f"## {card['annotation_id']}: `{card['reviewed_speech_function']}`",
            "",
            f"Evidence: `{card['evidence_id']}`",
            f"Candidate labels: {', '.join(card['candidate_labels'])}",
            f"Legacy shared support decision: **{card['candidate_label_supported']}**; current per-label support: **{card['resolved_label_support']}**",
            f"Contextual review: {card.get('contextual_review_id', 'none; legacy reviewer provenance unknown')}. Original observations below are retained as historical records.",
            *contextual_lines,
            f"Confidence: **{card['confidence']}**",
            "",
            f"Direct observation: {card['direct_observation']}",
            "",
            f"Interpretation: {card['interpretation']}",
            "",
            f"Limitation: {card['limitations']}",
            "",
            f"Delivery measurements: RMS {measured['mean_rms_db']}; speech-activity proxy {measured['speech_activity_fraction']}; zero-crossing rate {measured['mean_zero_crossing_rate']}; spectral centroid {measured['mean_spectral_centroid_hz']} Hz; pitch proxy {measured['mean_pitch_hz_proxy']} Hz; words/second proxy {measured['words_per_second_proxy']}; transcript gap before {measured['transcript_gap_before_seconds']} seconds; transcript gap after {measured['transcript_gap_after_seconds']} seconds; overlapping audio windows {measured['audio_window_count']}.",
            "",
        ])
    (root / "writeups/reviewed-pattern-cards.md").write_text("\n".join(markdown))
    print(f"wrote {len(cards)} reviewed cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
