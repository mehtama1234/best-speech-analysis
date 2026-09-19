#!/usr/bin/env python3
"""Record bounded internal midpoint-frame observations for raw delivery samples."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "research/communication-job-delivery-sampling.json"
PREFLIGHT = ROOT / "research/communication-job-delivery-measurement-preflight.json"
OUT = ROOT / "research/communication-job-delivery-internal-observations.json"
MD = ROOT / "writeups/communication-job-delivery-internal-observations.md"

# These are deliberately narrow visual/setting descriptions of the inspected
# midpoint frame. They do not label emotion, intent, confidence or audience
# response. A frame with a subtitle overlay does not prove exact audio timing.
NOTES = {
    "delivery:opening:01": ("partially_aligned", "A male speaker is visible at a microphone in front of a The Secret Life of Walter Mitty/TCL theatre backdrop; large edited subtitles cover the lower frame.", "Promotional stage/interview composition with branding and burned-in subtitle styling."),
    "delivery:opening:02": ("partially_aligned", "A bald male speaker is visible standing against a BMW Melbourne backdrop; large edited subtitles are present.", "Branded event/interview composition; the frame cannot establish the opening's full edit or audience response."),
    "delivery:closing:01": ("indeterminate", "A blurred black-and-white crowd image and large colored text are visible; no live speaker is visible.", "Edited graphic/cutaway rather than observable speaker delivery; the caption alignment and source edit require review."),
    "delivery:closing:02": ("partially_aligned", "A male speaker with glasses is visible at a microphone against the Mitty backdrop; subtitle text covers the lower frame.", "Promotional stage composition with event branding and burned-in subtitles."),
    "delivery:question:01": ("partially_aligned", "A woman is visible at a lectern with one hand raised near her face; edited subtitle text overlays the frame.", "Formal lecture/stage setting with English Speeches branding; the frame cannot establish who asked or answered."),
    "delivery:question:02": ("partially_aligned", "An older male speaker and a seated interviewer are visible in a BMW-branded interview setting; subtitles are overlaid.", "Two-person interview composition; the midpoint frame cannot establish turn timing or question ownership."),
    "delivery:answer_or_response:01": ("partially_aligned", "A young male speaker is visible seated in the BMW-branded interview setting; edited subtitles are overlaid.", "Interview/event composition; the question-answer boundary is not observable from one frame."),
    "delivery:answer_or_response:02": ("partially_aligned", "An older male speaker is visible seated in an indoor room with a bookshelf/background; caption text is overlaid.", "Interview-like interior; edit history and the literal question are not established by the frame."),
    "delivery:story_or_personal_experience:01": ("partially_aligned", "A male speaker is visible at the Mitty event microphone with the story wording overlaid.", "Promotional stage composition with large burned-in subtitles; continuous delivery is not established."),
    "delivery:story_or_personal_experience:02": ("partially_aligned", "A Black woman is visible speaking at a microphone with people standing behind her; edited subtitles are overlaid.", "Formal event composition; the frame supports visible setting and speaker presence, not the truth or effect of the story."),
    "delivery:example_or_case:01": ("partially_aligned", "A Black woman is visible at a microphone with an audience or event group behind her; large subtitles are overlaid.", "Formal event setting with edited caption styling; the example's delivery sequence is not established."),
    "delivery:example_or_case:02": ("partially_aligned", "A male speaker is visible at an event microphone with audience members behind him; the caption names a KFC/China example.", "Public event composition with edited subtitles; one frame cannot establish representativeness or listener understanding."),
    "delivery:contrast_or_disagreement:01": ("partially_aligned", "A seated male actor/speaker is visible at a desk or table with wall clocks and a wood-paneled interior; no clear subtitle is visible in the sampled frame.", "Scripted/interior composition; it may be a scene rather than direct speech footage, so identity and edit context remain open."),
    "delivery:contrast_or_disagreement:02": ("partially_aligned", "A Black woman is visible at a microphone with people behind her and large edited subtitles.", "Formal event composition; no interpersonal target or audience reaction is inferred."),
    "delivery:correction_or_reframe:01": ("partially_aligned", "A male speaker with glasses is visible at a microphone against the Mitty backdrop; subtitle text is overlaid.", "Promotional stage/event setting with visible branding and edited captions."),
    "delivery:correction_or_reframe:02": ("partially_aligned", "A woman is visible behind a lectern with English Speeches branding and subtitle text.", "Formal lecture/stage composition; exact correction timing and vocal delivery remain unverified."),
    "delivery:repair_or_self_correction:01": ("partially_aligned", "A Black male performer/speaker is visible outdoors speaking into a microphone amid a street crowd; edited subtitles are present.", "Outdoor public event with crowd and caption edit; repair timing and identity independence remain open."),
    "delivery:repair_or_self_correction:02": ("partially_aligned", "A male speaker is visible on a blue-lit stage with a microphone and large edited subtitles.", "Formal stage composition with speaker label/branding; one frame cannot establish repair timing or audience response."),
    "delivery:qualification_or_boundary:01": ("indeterminate", "A blurred black-and-white crowd image with large colored text is visible; no speaker is visible.", "Edited graphic/cutaway; it cannot support a vocal or nonverbal qualification observation."),
    "delivery:qualification_or_boundary:02": ("partially_aligned", "A blonde woman is visible speaking on a purple-lit stage; subtitle text is overlaid.", "Stage performance/event composition; certainty, intent and listener calibration are not inferred."),
    "delivery:definition_or_explanation:01": ("partially_aligned", "A woman is visible behind a lectern with English Speeches branding and large subtitles.", "Formal lecture/stage setting; one frame cannot establish explanatory success."),
    "delivery:definition_or_explanation:02": ("partially_aligned", "A young male speaker is visible seated against the BMW-branded backdrop with subtitle text.", "Interview/event composition; source identity and explanatory effect require separate review."),
    "delivery:transition_or_structure:01": ("indeterminate", "A stylized quote graphic with blurred black-and-white people and large text is visible; no speaker is visible.", "Edited graphic/cutaway rather than observable transition delivery."),
    "delivery:transition_or_structure:02": ("indeterminate", "A woman in a scripted interior scene is visible entering through a doorway; the retained transition wording is not visibly isolated.", "Edited fictional scene; visual evidence is limited to scene context."),
    "delivery:callback_or_repetition:01": ("partially_aligned", "A woman is visible behind a lectern with subtitles and English Speeches branding.", "Formal stage/lecture composition; repetition timing and audience response are not observable from one frame."),
    "delivery:callback_or_repetition:02": ("indeterminate", "A television screen showing a close-up face is visible rather than a clearly visible live speaker.", "Edited media insert; it cannot support a live-speaker nonverbal or repetition-delivery observation."),
    "delivery:humor_or_rapport:01": ("indeterminate", "A blurred black-and-white crowd image with large colored text is visible; no speaker is visible.", "Edited graphic/cutaway; humor effect and speaker delivery cannot be inferred."),
    "delivery:humor_or_rapport:02": ("partially_aligned", "Two men are visible outdoors amid a street crowd; one holds a microphone and edited subtitles are present.", "Outdoor public event with crowd and caption edit; humor effect is not inferred from the frame."),
    "delivery:credit_or_acknowledgment:01": ("partially_aligned", "A woman is visible behind a lectern with English Speeches branding and subtitles.", "Formal stage/lecture setting; the credited people and audience response are not established."),
    "delivery:credit_or_acknowledgment:02": ("partially_aligned", "A Black male speaker is visible outdoors with a microphone and crowd; edited subtitles are overlaid.", "Outdoor public event; the frame does not establish who is being credited or the response."),
    "delivery:call_to_action_or_audience_role:01": ("partially_aligned", "A woman is visible behind a lectern with edited subtitles and English Speeches branding.", "Formal lecture/stage composition; action ownership and audience uptake are not observable."),
    "delivery:call_to_action_or_audience_role:02": ("partially_aligned", "A seated male actor/speaker is visible at a table with wall clocks, arms raised; large subtitles are overlaid.", "Scripted/interior composition; gesture meaning and action effect are not inferred."),
    "delivery:persuasion_or_advocacy:01": ("partially_aligned", "A Black woman is visible on a Harvard-branded stage with a large seated audience and edited subtitles.", "Large formal event composition; production scale is visible but persuasion or audience effect is not inferred."),
    "delivery:persuasion_or_advocacy:02": ("indeterminate", "A stylized graphic reading 'I have a dream' is visible over a blurred crowd; no live speaker is visible.", "Edited quotation graphic/cutaway; it cannot support a speaker-delivery observation."),
    "delivery:reflection_or_value_frame:01": ("partially_aligned", "A seated male actor/speaker is visible at a table with wall clocks and one hand extended; edited subtitles are overlaid.", "Scripted/interior composition; gesture function and reflection effect are not inferred."),
    "delivery:reflection_or_value_frame:02": ("indeterminate", "A purple-lit audience is visible from behind; the speaker is not clearly visible and subtitles are overlaid.", "Audience/cutaway composition; it cannot support speaker nonverbal or listener-response evidence."),
}


def main() -> int:
    queue = json.loads(QUEUE.read_text())
    preflight = {item["sample_id"]: item for item in json.loads(PREFLIGHT.read_text())["items"]}
    rows = []
    for item in queue["items"]:
        if not item["raw_media_state"].startswith("raw_audio_video_present"):
            continue
        alignment, visual, setting = NOTES[item["sample_id"]]
        midpoint = round((item["start_seconds"] + item["end_seconds"]) / 2, 3)
        measurement = preflight.get(item["sample_id"])
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
            "vocal_timing_observation": "Manual listening was not performed in this pass; retained transcript timing and feature values remain separate from a vocal interpretation.",
            "audio_measurements": measurement["audio_measurements"] if measurement else None,
            "audio_measurement_status": measurement["measurement_status"] if measurement else "unmatched_preflight",
            "audio_measurement_and_limit": f"Feature proxy file {measurement['feature_file'] if measurement and measurement.get('feature_file') else 'not available'}; words-per-second, RMS, speech activity, zero-crossing, spectral centroid and pitch-confidence fields are reproducible proxies, not validated vocal meaning or effectiveness.",
            "nearest_sampled_frame_measurement": measurement["nearest_sampled_frame"] if measurement else None,
            "measurement_evidence_ids_matched": measurement["evidence_ids_matched"] if measurement else [],
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
