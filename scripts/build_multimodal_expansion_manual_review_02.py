#!/usr/bin/env python3
"""Record the second bounded internal multimodal review pass."""

from __future__ import annotations

import json
from pathlib import Path


OBSERVATIONS = {
    "JdUq2opPY-Q": ("JdUq2opPY-Q:00000", "candidate-unclassified", 6.30, "A close cinematic shot shows a single character in a dark, rain-lit setting. The candidate transcript is not displayed as an aligned subtitle in the sampled frame.", "setting_visible_caption_not_aligned", "The film edit supports scene context only; it does not support a delivery claim about a real speaker."),
    "W-mgdUdOjhs": ("W-mgdUdOjhs:00007", "candidate-question", 31.52, "A close cinematic shot shows one character against a nearly black background. No exact candidate caption is visible in the sampled frame.", "setting_visible_caption_not_aligned", "The source is fictional edited footage and the visible frame cannot establish the question function or delivery."),
    "ZwMVMbmQBug": ("ZwMVMbmQBug:00000", "candidate-unclassified", 1.61, "The frame shows a television or monitor presentation of a speaker and another screen in a dark room; no exact retained caption is visible.", "edit_and_screen_context_not_aligned", "The screen-within-screen edit and absent subtitle prevent exact visual alignment and generalization to live speaking."),
    "aHXxveJTJoE": ("aHXxveJTJoE:00001", "candidate-question", 4.44, "Two puppet characters are visible at a table in a brightly lit fictional scene. The candidate wording is not visibly subtitled in this frame.", "fictional_setting_caption_not_aligned", "The scene supports fictional dialogue context only; no claim is made about real-speaker gaze, gesture or listener effect."),
    "dPi40lQetew": ("dPi40lQetew:00005", "candidate-question", 14.77, "Several characters are visible in a film scene with a Movieclips watermark. The candidate question-like caption is not visibly aligned in the sampled frame.", "fictional_setting_caption_not_aligned", "The film scene and publisher watermark are source-quality boundaries; the heuristic question label requires context review."),
    "hZ0YhrgYejI": ("hZ0YhrgYejI:00000", "candidate-question-or-qualification", 8.87, "The frame is a promotional title-card collage with multiple public figures and ‘English Speeches’ branding rather than an isolated speaker shot.", "title_card_not_aligned", "The edit does not isolate the speaker or exact wording; no delivery or speaker attribution claim is made from this frame."),
    "m92yvNscIAo": ("m92yvNscIAo:00000", "candidate-unclassified", 2.56, "A character is shown beside a lit computer display in a dark fictional scene. The candidate wording is not visibly subtitled in the sampled frame.", "fictional_setting_caption_not_aligned", "The frame supports scene and edit context only, not a live communication pattern or real-world practice recommendation."),
    "pmAL79dnvu0": ("pmAL79dnvu0:00042", "candidate-story-or-personal-experience", 139.68, "Two people are visible on a public event stage with a crowd behind them. The large subtitle ‘When I was a little girl’ is visibly aligned with the sampled shot.", "visible_caption_overlap_multi_speaker", "The frame supports wording, public setting and multiple visible people; it does not establish speaker turn ownership, sincerity or audience effect."),
    "u1gg_L-syCw": ("u1gg_L-syCw:00009", "candidate-uncertainty-or-qualification", 39.54, "A blurred person is shown walking through an indoor corridor or lobby; the sampled frame does not visibly display the retained caption.", "cutaway_caption_not_aligned", "The cutaway prevents claims about the speaker’s visible delivery or exact caption alignment."),
    "xRiwgtdyjQk": ("xRiwgtdyjQk:00016", "candidate-question", 42.30, "A single speaker is visible at a podium in front of repeated U.S. flags. The subtitle ‘We have thousands of friends in this incredible moment’ is clearly visible.", "visible_caption_overlap", "The frame supports wording and formal setting; it does not verify the political claim, intent or audience response."),
}


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    coverage = json.loads((root / "research/multimodal-coverage-audit.json").read_text())
    queue = {row["video_id"]: row for row in coverage["manual_review_queue"]}
    existing = json.loads((root / "research/multimodal-expansion-manual-review.json").read_text())
    existing_ids = {item["video_id"] for item in existing["items"]}
    items = []
    for video_id, (evidence_id, pattern_id, sampled_time, observation, decision, limit) in OBSERVATIONS.items():
        if video_id not in queue or video_id in existing_ids:
            raise SystemExit(f"invalid second-pass item: {video_id}")
        feature = json.loads((root / "data/features" / f"{video_id}.json").read_text())
        aligned = next((row for row in feature.get("aligned_transcript", []) if row.get("evidence_id") == evidence_id), {})
        frames = feature.get("sampled_frames", [])
        frame = min(frames, key=lambda row: abs(row.get("time_seconds", 0) - sampled_time)) if frames else {}
        items.append({
            "video_id": video_id,
            "title": queue[video_id]["title"],
            "evidence_id": evidence_id,
            "pattern_id": pattern_id,
            "sampled_time_seconds": sampled_time,
            "transcript_text": aligned.get("text"),
            "frame_observation": observation,
            "alignment_decision": decision,
            "alignment_limit": limit,
            "video_source": f"data/video/{video_id}.mp4",
            "audio_source": f"data/audio/{video_id}.m4a",
            "feature_source": f"data/features/{video_id}.json",
            "measured_audio_proxy": {key: aligned.get(key) for key in ("words_per_second_proxy", "mean_rms_db", "speech_activity_fraction", "mean_zero_crossing_rate", "mean_spectral_centroid_hz", "mean_pitch_hz_proxy", "mean_pitch_confidence_proxy", "audio_window_count")},
            "nearest_frame_measurement": {key: frame.get(key) for key in ("time_seconds", "width", "height", "mean_luminance", "luminance_std", "face_count", "face_measurement_status")},
            "feature_limit": "Audio values are coarse proxies; scene-pixel/face fields are measurements, not emotion, intent, confidence, authenticity or audience-effect evidence.",
            "review_status": "internal_bounded_review_not_independent",
        })
    report = {
        "schema_version": "1.0",
        "review_id": "multimodal-expansion-manual-review-02",
        "status": "internal_bounded_review_complete_independent_review_pending",
        "reviewer": "internal project agent",
        "independence": "not_independent",
        "claim_boundary": "These observations describe one representative frame and aligned transcript/audio feature record per newly available raw-media queue item. They do not establish delivery meaning, speaker intent, audience response, communication effectiveness or learner outcome.",
        "method": {"selection": "new raw-complete transcribed items not covered by pass 01", "frame_rule": "one representative frame near the first available heuristic candidate interval", "observed_fields": ["speaker visibility", "setting", "on-screen text", "shot/edit context", "caption alignment"], "measured_fields": ["caption-aligned acoustic proxies", "nearest sampled-frame scene measurements"], "not_inferred": ["emotion", "intent", "confidence", "authenticity", "audience effect", "persuasion", "comprehension"]},
        "items": items,
        "next_actions": ["Have an independent reviewer inspect both passes together.", "Resample interval boundaries for cutaways, title cards and fictional edits.", "Add counterexamples before promoting any candidate into a general lesson.", "Keep all observations provisional until source/event independence and learner checks are complete."],
    }
    out = root / "research/multimodal-expansion-manual-review-02.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    md = root / "writeups/multimodal-expansion-manual-review-02.md"
    lines = ["# Multimodal expansion: bounded internal review pass 02", "", "Status: **internal bounded review complete; independent review pending**.", "", "Ten newly raw-complete queue items were inspected at one representative frame. Non-aligned film, title-card and cutaway cases are retained rather than discarded.", "", "| Video | Candidate | Alignment |", "|---|---|---|"]
    lines += [f"| `{item['video_id']}` | `{item['pattern_id']}` | `{item['alignment_decision']}` |" for item in items]
    md.write_text("\n".join(lines) + "\n")
    print(json.dumps({"output": str(out), "items": len(items), "status": report["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
