#!/usr/bin/env python3
"""Record a bounded internal frame/audio review of the raw-media queue."""

from __future__ import annotations

import json
from pathlib import Path


OBSERVATIONS = {
    "2fWJh-_UG5s": {
        "evidence_id": "2fWJh-_UG5s:00005",
        "pattern_id": "candidate-question",
        "sampled_time_seconds": 14.52,
        "frame_observation": "A single speaker is visible in a formal White House press-room setting with a U.S. flag and White House backdrop. The large on-screen caption displays the short phrase ‘how about that’.",
        "alignment_decision": "visible_caption_overlap",
        "alignment_limit": "The frame supports wording, speaker visibility and setting; it does not establish whether the question invited a response or changed audience behavior.",
    },
    "3AIoHLr8nTI": {
        "evidence_id": "3AIoHLr8nTI:00004",
        "pattern_id": "candidate-uncertainty-or-qualification",
        "sampled_time_seconds": 53.64,
        "frame_observation": "A single speaker in academic regalia is visible against a purple graduation backdrop with an NYU mark. Large subtitles are visible and the frame is a stable speaker shot rather than a cutaway.",
        "alignment_decision": "visible_caption_overlap_partial",
        "alignment_limit": "The displayed subtitle overlaps the retained segment but the retained caption contains a longer sentence than the sampled frame; no claim is made about the delivery of the qualification itself.",
    },
    "9fEurt2OZ0I": {
        "evidence_id": "9fEurt2OZ0I:00008",
        "pattern_id": "candidate-story-or-personal-experience",
        "sampled_time_seconds": 33.92,
        "frame_observation": "The speaker is shown in a close interview-style shot with an audience or room behind him. Large colored subtitles visibly carry the account beginning ‘police, they said…’.",
        "alignment_decision": "visible_caption_overlap",
        "alignment_limit": "The frame supports a first-person story segment and its subtitle treatment; it does not verify the narrated biography or infer sincerity.",
    },
    "AwA0Jnfj3ao": {
        "evidence_id": "AwA0Jnfj3ao:00000",
        "pattern_id": "candidate-call-to-action",
        "sampled_time_seconds": 7.285,
        "frame_observation": "The frame is a promotional ‘coming up’ treatment combining a portrait and an interview image; the target caption is not visibly isolated as spoken text in this frame.",
        "alignment_decision": "setting_visible_caption_not_aligned",
        "alignment_limit": "The source edit prevents treating this frame as exact visual evidence for the candidate call-to-action label; the transcript also assigns the line to interviewer framing.",
    },
    "C8-twwwTETE": {
        "evidence_id": "C8-twwwTETE:00021",
        "pattern_id": "candidate-uncertainty-or-qualification",
        "sampled_time_seconds": 48.36,
        "frame_observation": "Two speakers are visible outdoors at a public ceremony with a crowd, podium and event branding. The subtitle ‘And I think one of the things I noticed’ is visible over the shot.",
        "alignment_decision": "visible_caption_overlap",
        "alignment_limit": "The frame supports multi-speaker public setting and wording; it does not identify which speaker produced every word or establish audience response.",
    },
    "OfwfTN1mEyM": {
        "evidence_id": "OfwfTN1mEyM:00018",
        "pattern_id": "candidate-question",
        "sampled_time_seconds": 42.76,
        "frame_observation": "A single speaker is visible on a blue international-event stage with event branding. The subtitle includes ‘I feel like I’m in a waterfall’, with no audience shown in the sampled frame.",
        "alignment_decision": "visible_caption_overlap_partial",
        "alignment_limit": "The caption and setting are visible, but the phrase is a comparison/description rather than proof that a question function occurred; the heuristic label remains provisional.",
    },
    "aXmM0VZv810": {
        "evidence_id": "aXmM0VZv810:00001",
        "pattern_id": "candidate-question",
        "sampled_time_seconds": 5.079,
        "frame_observation": "The frame shows a digital-globe event graphic and small on-screen speaker labels while subtitles display a request for a bigger round of applause. The sampled image does not isolate a single speaker’s face.",
        "alignment_decision": "visible_caption_overlap_setting_and_edit",
        "alignment_limit": "The words are visible, but the edit, graphic treatment and absent isolated speaker view prevent claims about gaze, gesture, vocal emphasis or question function.",
    },
    "bR4tDSa3O10": {
        "evidence_id": "bR4tDSa3O10:00024",
        "pattern_id": "candidate-question",
        "sampled_time_seconds": 66.18,
        "frame_observation": "A single speaker in graduation regalia is visible against a purple and orange stage backdrop. The subtitle ends with ‘Happy Mother’s Day’, while the preceding question-like wording is partly outside the sampled frame.",
        "alignment_decision": "visible_caption_overlap_boundary_transition",
        "alignment_limit": "The frame supports the public ceremony and nearby wording, but not the exact boundary or function of the full retained caption.",
    },
    "gDadfh0ZdBM": {
        "evidence_id": "gDadfh0ZdBM:00001",
        "pattern_id": "candidate-example",
        "sampled_time_seconds": 30.8,
        "frame_observation": "Two characters are visible in a dark film scene near a doorway. The candidate text ‘let me give you one piece of advice’ is not displayed as an exact subtitle in the sampled frame.",
        "alignment_decision": "setting_visible_caption_not_aligned",
        "alignment_limit": "This is fictional edited footage, not a live speech setting; the frame supports scene context only and should not be generalized to real-world speaker practice without separate review.",
    },
    "jxY2-YgAgm0": {
        "evidence_id": "jxY2-YgAgm0:00005",
        "pattern_id": "candidate-question",
        "sampled_time_seconds": 20.08,
        "frame_observation": "A single speaker is visible at a formal desk with U.S. flags and a windowed government-room setting. The subtitle ‘The individuals lying about me are devoid of ethical standards’ is clearly visible.",
        "alignment_decision": "visible_caption_overlap",
        "alignment_limit": "The frame supports wording and institutional setting; it does not verify the allegation, speaker intent, vocal affect or audience interpretation.",
    },
    "r2kP2Pqdx6w": {
        "evidence_id": "r2kP2Pqdx6w:00001",
        "pattern_id": "candidate-call-to-action",
        "sampled_time_seconds": 5.8,
        "frame_observation": "Two speakers are seated on a blue event stage with a moderator table and conference branding. The subtitle ‘Let’s take responsibility for today’ is visibly aligned with the shot.",
        "alignment_decision": "visible_caption_overlap_multi_speaker",
        "alignment_limit": "The frame supports a shared interview/debate setting and wording; it does not establish who is being addressed, whether the invitation was accepted or any effect on listeners.",
    },
}


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    queue = json.loads((root / "research/multimodal-coverage-audit.json").read_text())["manual_review_queue"]
    queue_by_id = {row["video_id"]: row for row in queue}
    items = []
    for video_id, observation in OBSERVATIONS.items():
        if video_id not in queue_by_id:
            raise SystemExit(f"{video_id} is not in the current raw-media queue")
        feature_path = root / "data/features" / f"{video_id}.json"
        feature = json.loads(feature_path.read_text()) if feature_path.exists() else {}
        aligned = next((row for row in feature.get("aligned_transcript", []) if row.get("evidence_id") == observation["evidence_id"]), {})
        frames = feature.get("sampled_frames", [])
        nearest_frame = min(frames, key=lambda row: abs(row.get("time_seconds", 0) - observation["sampled_time_seconds"])) if frames else {}
        items.append({
            **observation,
            "video_id": video_id,
            "title": queue_by_id[video_id]["title"],
            "video_source": f"data/video/{video_id}.mp4",
            "audio_source": f"data/audio/{video_id}.m4a",
            "feature_source": f"data/features/{video_id}.json",
            "transcript_text": aligned.get("text"),
            "measured_audio_proxy": {
                key: aligned.get(key)
                for key in ("words_per_second_proxy", "mean_rms_db", "speech_activity_fraction", "mean_zero_crossing_rate", "mean_spectral_centroid_hz", "mean_pitch_hz_proxy", "mean_pitch_confidence_proxy", "audio_window_count")
            },
            "nearest_frame_measurement": {
                key: nearest_frame.get(key)
                for key in ("time_seconds", "width", "height", "mean_luminance", "luminance_std", "face_count", "face_measurement_status")
            },
            "feature_limit": "Audio values are coarse proxies; scene-pixel/face fields are measurements, not emotion, intent, confidence, authenticity or audience-effect evidence.",
            "review_status": "internal_bounded_review_not_independent",
        })
    report = {
        "schema_version": "1.0",
        "review_id": "multimodal-expansion-manual-review-01",
        "status": "internal_bounded_review_complete_independent_review_pending",
        "reviewer": "internal project agent",
        "independence": "not_independent",
        "claim_boundary": "These observations describe one representative frame and aligned transcript/audio feature record per raw-media queue item. They do not establish delivery meaning, speaker intent, audience response, communication effectiveness or learner outcome.",
        "method": {
            "selection": "one deterministic raw-media queue item per selected expansion video",
            "frame_rule": "one representative frame near the first available heuristic candidate interval",
            "observed_fields": ["speaker visibility", "setting", "on-screen text", "shot/edit context", "caption alignment"],
            "measured_fields": ["caption-aligned acoustic proxies", "nearest sampled-frame scene measurements"],
            "not_inferred": ["emotion", "intent", "confidence", "authenticity", "audience effect", "persuasion", "comprehension"],
        },
        "items": items,
        "next_actions": [
            "Have an independent reviewer inspect the same 11 intervals and record agreement, disagreement and boundary decisions.",
            "Resample both interval boundaries for the partial and edit-contaminated alignments.",
            "Add counterexample intervals before promoting any candidate into a general lesson.",
            "Keep all observations provisional until source/event independence and learner checks are complete.",
        ],
    }
    out = root / "research/multimodal-expansion-manual-review.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    md = root / "writeups/multimodal-expansion-manual-review.md"
    lines = [
        "# Multimodal expansion: bounded internal review",
        "",
        "Status: **internal bounded review complete; independent review pending**.",
        "",
        "Eleven raw-media queue items were inspected at one representative frame near a timestamped heuristic candidate. The records preserve exact transcript evidence IDs, local media paths, caption alignment decisions, and coarse feature values. They do not infer emotion, intent, confidence, effectiveness or audience response.",
        "",
        "| Video | Candidate | Alignment |",
        "|---|---|---|",
    ]
    for item in items:
        lines.append(f"| `{item['video_id']}` | `{item['pattern_id']}` | `{item['alignment_decision']}` |")
    lines += ["", "The full observations and measured proxies are in the JSON report. This internal pass is not independent validation.", ""]
    md.write_text("\n".join(lines))
    print(json.dumps({"output": str(out), "items": len(items), "status": report["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
