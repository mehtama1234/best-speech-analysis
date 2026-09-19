#!/usr/bin/env python3
"""Record bounded internal midpoint-frame observations for raw delivery samples."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "research/communication-job-delivery-sampling.json"
OUT = ROOT / "research/communication-job-delivery-internal-observations.json"
MD = ROOT / "writeups/communication-job-delivery-internal-observations.md"

# These are deliberately narrow visual/setting descriptions of the inspected
# midpoint frame. They do not label emotion, intent, confidence or audience
# response. A frame with a subtitle overlay does not prove exact audio timing.
NOTES = {
    "delivery:opening:01": ("partially_aligned", "Older man is visible seated at a branded formal event; the frame carries a large edited subtitle overlay and event watermark.", "Interview/event set with BMW branding; edited subtitle treatment is visible."),
    "delivery:opening:02": ("partially_aligned", "Single woman is visible at a lectern or press-room setting with flags; a large subtitle overlay is visible.", "Formal press-room composition; flags and broadcast-style subtitle editing are visible."),
    "delivery:closing:01": ("partially_aligned", "A male speaker is visible in a formal event/interview composition with subtitle text; other people are partly visible behind him.", "Branded event setting with edited subtitle overlay; exact shot boundaries are not established by one frame."),
    "delivery:closing:02": ("partially_aligned", "A male speaker/interviewer is visible seated at a branded event while the closing wording is overlaid.", "Formal interview/event setting with subtitle overlay and background branding."),
    "delivery:question:01": ("partially_aligned", "Two people are visible in a seated interview setting and the retained question wording is overlaid.", "Branded interview/event setup; the frame cannot establish turn timing or who is speaking."),
    "delivery:question:02": ("partially_aligned", "A woman is visible in a formal press setting with flags and subtitle text.", "Press-room composition and edited caption overlay; no listener response is inferred."),
    "delivery:answer_or_response:01": ("partially_aligned", "A male speaker is visible seated at the branded event with a subtitle overlay.", "Interview/event set; the frame does not identify the question-answer boundary."),
    "delivery:answer_or_response:02": ("partially_aligned", "A single man is visible in an indoor formal setting with the answer wording overlaid.", "Interior interview/podium-like setting; camera/edit history is unavailable from the frame."),
    "delivery:story_or_personal_experience:01": ("partially_aligned", "A male speaker is visible seated at the branded event and the personal-story wording is overlaid.", "Formal interview/event setting with edited subtitles."),
    "delivery:story_or_personal_experience:02": ("partially_aligned", "A woman is visible at a graduation podium with stage seating behind her and subtitle text.", "Graduation-stage setting; the frame supports setting only, not biographical truth or effect."),
    "delivery:example_or_case:01": ("partially_aligned", "A male speaker is visible in a branded event setting with a large subtitle overlay.", "Formal event/interview setting with edited caption styling."),
    "delivery:example_or_case:02": ("partially_aligned", "A woman is visible at a graduation podium with audience/stage seating and subtitle text.", "Graduation ceremony setting; one frame cannot establish whether the example function was understood."),
    "delivery:contrast_or_disagreement:01": ("partially_aligned", "A seated older man is visible in an interior interview setting with subtitle text; wall clocks are visible.", "Interview/lecture-like interior; subtitle overlay is edited into the image."),
    "delivery:contrast_or_disagreement:02": ("partially_aligned", "A woman is visible on a graduation stage with a subtitle overlay.", "Graduation-stage setting; no interpersonal disagreement or audience reaction is inferred."),
    "delivery:correction_or_reframe:01": ("partially_aligned", "A woman is visible at a podium/stage with the correction wording overlaid.", "Formal stage setting with edited subtitles; exact delivery timing remains unverified."),
    "delivery:correction_or_reframe:02": ("indeterminate", "Multiple people are visible in a scripted interior film scene; the retained wording is not visibly isolated in this midpoint frame.", "Edited fictional scene, not a live speech setting; do not generalize its visual composition to public speaking."),
    "delivery:repair_or_self_correction:01": ("partially_aligned", "A male performer/speaker is visible outdoors addressing a crowd with a microphone and subtitle overlay.", "Outdoor public event with crowd and edited captions; speaker identity/event independence remains unverified."),
    "delivery:qualification_or_boundary:01": ("partially_aligned", "A woman is visible on a graduation stage with subtitle text.", "Graduation-stage setting; the frame cannot establish vocal certainty or listener calibration."),
    "delivery:qualification_or_boundary:02": ("indeterminate", "Multiple people are visible in a scripted interior film scene; the retained qualification is not isolated by the midpoint frame.", "Edited fictional scene; visual evidence is limited to scene context."),
    "delivery:definition_or_explanation:01": ("partially_aligned", "A male speaker is visible seated at a branded formal event with subtitle text.", "Interview/event set with edited captions; no inference about explanatory success."),
    "delivery:definition_or_explanation:02": ("partially_aligned", "A male speaker is visible at a podium with flags and subtitle text.", "Formal political/podium setting; source identity and event context require independent review."),
    "delivery:transition_or_structure:01": ("indeterminate", "A person is visible moving through a dim scripted interior scene; the retained transition wording is not visibly isolated.", "Edited fictional scene with limited visual speech evidence."),
    "delivery:transition_or_structure:02": ("partially_aligned", "A male speaker is visible at a podium with flags and subtitle text.", "Formal political/podium setting with edited caption overlay."),
    "delivery:callback_or_repetition:01": ("indeterminate", "A television/inserted screen image is visible rather than a clearly visible live speaker; the retained wording is not isolated in the frame.", "Edited media insert; cannot support a live-speaker delivery observation."),
    "delivery:callback_or_repetition:02": ("partially_aligned", "Two people are visible outdoors among a crowd with subtitle text.", "Outdoor public event and cutaway-like composition; no audience comprehension is inferred."),
    "delivery:humor_or_rapport:01": ("partially_aligned", "A male performer/speaker is visible outdoors with a crowd and subtitle overlay.", "Outdoor public event with edited captions; humor effect is not inferred from the frame."),
    "delivery:credit_or_acknowledgment:01": ("partially_aligned", "A male performer/speaker is visible outdoors addressing a crowd with subtitle text.", "Outdoor public event; the frame does not establish who is being credited or audience response."),
    "delivery:credit_or_acknowledgment:02": ("partially_aligned", "A male speaker is visible at a podium with flags and edited subtitle text.", "Formal political/podium setting; identity and event independence remain open."),
    "delivery:call_to_action_or_audience_role:01": ("indeterminate", "An older man is visible in a scripted interior scene; the retained action wording is not visibly isolated.", "Edited fictional scene; not transcript-linked live delivery evidence."),
    "delivery:call_to_action_or_audience_role:02": ("partially_aligned", "An older man is visible seated indoors and gesturing with subtitle text; wall clocks are visible.", "Interior interview/film-like setting with edited captions; gesture function is not inferred."),
    "delivery:persuasion_or_advocacy:01": ("partially_aligned", "A male speaker is visible at a podium with flags and subtitle text.", "Formal political/podium setting with edited caption overlay."),
    "delivery:persuasion_or_advocacy:02": ("partially_aligned", "A woman is visible on a graduation stage with subtitle text.", "Graduation-stage setting; persuasion or audience effect is not inferred."),
    "delivery:reflection_or_value_frame:01": ("partially_aligned", "An older man is visible seated indoors and gesturing while subtitle text is overlaid.", "Interior interview/film-like setting with wall clocks and edited captions."),
    "delivery:reflection_or_value_frame:02": ("indeterminate", "Audience and stage lighting are visible, but the speaker is not clearly visible in the midpoint frame; subtitle text is overlaid.", "Audience/cutaway composition; cannot support speaker nonverbal observation."),
}


def main() -> int:
    queue = json.loads(QUEUE.read_text())
    rows = []
    for item in queue["items"]:
        if item["raw_media_state"] != "raw_audio_video_present":
            continue
        alignment, visual, setting = NOTES[item["sample_id"]]
        midpoint = round((item["start_seconds"] + item["end_seconds"]) / 2, 3)
        rows.append({
            "sample_id": item["sample_id"],
            "canonical_job": item["canonical_job"],
            "video_id": item["video_id"],
            "evidence_id": item["evidence_id"],
            "source_video": f"data/video/{item['video_file']}",
            "source_url": item["source_url"],
            "sampled_midpoint_seconds": midpoint,
            "frame_method": "single midpoint frame extracted with bundled imageio-ffmpeg and inspected internally",
            "transcript_alignment": alignment,
            "visual_observation": visual,
            "setting_editing_music_observation": setting,
            "vocal_timing_observation": "Manual listening was not performed in this pass; retained transcript timing and any feature proxy remain separate from a vocal interpretation.",
            "audio_measurement_and_limit": f"Feature proxy file data/features/{item['feature_file']}; proxy values do not establish loudness meaning, pitch meaning, emotion, intent or effectiveness.",
            "speaker_event_identity": "Not independently verified; source-frame observation only.",
            "missingness_or_accessibility_note": "Single-frame sampling cannot establish continuous gaze, gesture, posture, editing sequence, room acoustics, accessibility or audience response.",
            "reviewer_code": "internal-project-agent",
            "independence": "not_independent",
        })
    report = {
        "schema_version": "1.0",
        "report_id": "communication-job-delivery-internal-observations",
        "status": "internal_midpoint_frame_observations_complete_independent_review_pending",
        "source_queue": "research/communication-job-delivery-sampling.json",
        "item_count": len(rows),
        "claim_boundary": "These are bounded internal midpoint-frame observations. They do not establish continuous delivery meaning, vocal effectiveness, speaker intent, audience response, speaker/event identity, teachability or listener outcomes.",
        "method": {"frame_rule": "midpoint of each raw audio/video queue interval", "tool": "imageio-ffmpeg bundled FFmpeg", "not_performed": ["manual vocal listening", "independent review", "continuous video review", "audience outcome measurement"]},
        "items": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Communication-job delivery — internal midpoint-frame observations", "", "Status: **internal observations complete; independent review pending**.", "", report["claim_boundary"], "", f"Raw audio/video samples inspected: **{len(rows)}**.", "", "| Sample | Job | Alignment | Visual/setting boundary |", "|---|---|---|---|"]
    for row in rows:
        lines.append(f"| `{row['sample_id']}` | `{row['canonical_job']}` | `{row['transcript_alignment']}` | {row['visual_observation']} {row['setting_editing_music_observation']} |")
    lines += ["", "No row is independent evidence. Manual vocal listening, full-sequence editing review, identity verification and listener outcomes remain separate gates.", ""]
    MD.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "item_count": len(rows), "independence": "not_independent"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
