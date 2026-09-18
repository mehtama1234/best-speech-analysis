#!/usr/bin/env python3
"""Record a bounded visual source audit for raw media without retained transcripts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = {
    "5i0u4jFmE78": {"time": 80.0, "observation": "Film scene with multiple visible characters in armor and a crowd/background; an on-screen subtitle is visible. This is scripted cinematic footage, not an independently retained speech transcript.", "source_class": "fictional_film_scene"},
    "JDfP3thQYrM": {"time": 300.0, "observation": "Single woman in a close interview/speech-style shot with large English subtitles and branded edit treatment. The visible subtitle is not part of the retained transcript registry for this item.", "source_class": "edited_subtitled_speech_upload"},
    "KieuXXue2Ag": {"time": 180.0, "observation": "Single woman at a formal lectern or chamber setting with large subtitles and broadcast branding. The image supports speaker/setting visibility only; retained transcript coverage is absent.", "source_class": "edited_subtitled_speech_upload"},
    "UtJDpOUIEd8": {"time": 200.0, "observation": "Single woman seated at a branded formal event, looking down toward notes or a device; large subtitles are visible. No retained transcript is available for speech-function alignment.", "source_class": "edited_subtitled_speech_upload"},
    "Y0B32z3WwwA": {"time": 750.0, "observation": "Single man on a dark stage with event branding and visible hand position; the frame is a delivery-setting observation only. No retained transcript is available.", "source_class": "stage_speech_upload"},
    "fBnAMUkNM2k": {"time": 1200.0, "observation": "A large subtitle is visible over a scene showing a woman and a child or child-related visual context; the edit and visible caption require safeguarding and do not establish the underlying claim or delivery effect.", "source_class": "edited_subtitled_speech_upload_sensitive_context"},
    "qOwYULOPuPs": {"time": 600.0, "observation": "Single man in a formal interior setting with large subtitles; the frame supports speaker visibility and institutional setting. No retained transcript is available for exact speech alignment.", "source_class": "edited_subtitled_speech_upload"},
    "zKCjmtxgyNg": {"time": 230.0, "observation": "Single man in a close cinematic shot with large subtitles and a film/tribute edit treatment. This is not retained transcript evidence and should not be generalized as live speaking practice.", "source_class": "edited_film_or_tribute_clip"},
}


def main() -> int:
    coverage = json.loads((ROOT / "research/multimodal-coverage-audit.json").read_text())
    queue = {row["video_id"]: row for row in coverage["raw_media_only_queue"]}
    items = []
    for video_id, observation in OBSERVATIONS.items():
        if video_id not in queue:
            raise SystemExit(f"{video_id} is not in raw_media_only_queue")
        feature = json.loads((ROOT / "data/features" / f"{video_id}.json").read_text())
        frame = min(feature.get("sampled_frames", []), key=lambda row: abs(row.get("time_seconds", 0) - observation["time"]))
        items.append({
            "video_id": video_id,
            "title": queue[video_id]["title"],
            "video_url": queue[video_id]["video_url"],
            "source_class": observation["source_class"],
            "sampled_time_seconds": observation["time"],
            "video_source": f"data/video/{video_id}.mp4",
            "audio_source": f"data/audio/{video_id}.m4a",
            "feature_source": f"data/features/{video_id}.json",
            "transcript_status": "no_retained_transcript_in_segment_registry",
            "visual_observation": observation["observation"],
            "nearest_frame_measurement": {key: frame.get(key) for key in ("time_seconds", "width", "height", "mean_luminance", "luminance_std", "face_count", "face_measurement_status")},
            "review_status": "internal_visual_source_audit_not_independent",
        })
    report = {
        "schema_version": "1.0",
        "report_id": "raw-media-only-visual-audit",
        "status": "internal_visual_source_audit_complete_transcript_missing",
        "reviewer": "internal project agent",
        "independence": "not_independent",
        "claim_boundary": "These are bounded visual/source observations for eight raw-complete items without retained transcript coverage. They do not establish speech function, exact language, delivery effectiveness, speaker intent, audience response or listener outcome.",
        "method": {"selection": "all raw-audio-and-video-complete expansion items with zero retained transcript segments", "frame_rule": "one deterministic midpoint feature frame inspected against the local video", "not_inferred": ["speech function", "emotion", "intent", "effectiveness", "audience response", "listener comprehension"]},
        "item_count": len(items),
        "items": items,
        "next_actions": ["Acquire or reconstruct an admissible transcript before linking any item to exact speech forms.", "Keep sensitive child-related and fictional/edit material under source and safety review.", "Do not merge this report into transcript-linked pattern recurrence counts.", "Obtain independent visual/source review if these items are later used for delivery comparisons."],
    }
    out = ROOT / "research/raw-media-only-visual-audit.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Raw-media-only visual audit", "", "Status: **internal visual/source audit complete; retained transcript missing**.", "", report["claim_boundary"], "", "| Video | Source class | Sampled time | Visual observation |", "|---|---|---:|---|"]
    lines.extend(f"| `{item['video_id']}` | `{item['source_class']}` | {item['sampled_time_seconds']}s | {item['visual_observation']} |" for item in items)
    (ROOT / "writeups/raw-media-only-visual-audit.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"output": str(out), "item_count": len(items), "status": report["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
