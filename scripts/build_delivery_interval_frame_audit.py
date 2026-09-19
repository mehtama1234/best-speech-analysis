#!/usr/bin/env python3
"""Record a bounded three-frame audit for the 36 job-level delivery clips.

The labels describe only what is visible in three extracted frames. They do
not establish continuous delivery, speaker identity, intent, vocal meaning or
listener response.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "research/communication-job-delivery-sampling.json"
OUT = ROOT / "research/communication-job-delivery-interval-frame-audit.json"
MD = ROOT / "writeups/communication-job-delivery-interval-frame-audit.md"

# These observations were made from start, midpoint and end frames extracted
# at the queue's recorded interval. They are navigation and missingness notes,
# not semantic interpretations of gesture, emotion or performance.
OBSERVATIONS = {
    "delivery:opening:01": ("stable_speaker_frame", "speaker_visible_all_three", "Same male speaker remains at a microphone against the Mitty/TCL backdrop; the crop changes slightly and subtitles persist.", "limited"),
    "delivery:opening:02": ("multi_shot", "speaker_visible_but_changes", "The interval moves from a close speaker view to a bald speaker and then a two-person interview composition.", "limited"),
    "delivery:closing:01": ("graphic_or_cutaway", "speaker_not_visible", "All three frames show a blurred black-and-white graphic with large colored text rather than a live speaker.", "not_usable_for_speaker_delivery"),
    "delivery:closing:02": ("stable_speaker_frame", "speaker_visible_all_three", "The same male speaker remains at the Mitty microphone across the three frames, with changing subtitle text.", "limited"),
    "delivery:question:01": ("stable_speaker_frame", "speaker_visible_all_three", "The same woman remains behind the lectern; hand position and gaze direction vary slightly.", "limited"),
    "delivery:question:02": ("interview_multi_shot", "speaker_and_listener_visible", "Two-person interview framing persists, ending on the older male speaker in a tighter crop.", "limited"),
    "delivery:answer_or_response:01": ("multi_shot", "speakers_change", "The interval cuts between an older speaker, a standing younger speaker and another two-person composition.", "not_usable_for_continuous_speaker_delivery"),
    "delivery:answer_or_response:02": ("stable_speaker_frame", "speaker_visible_all_three", "The same seated male speaker remains centered in the indoor interview composition.", "limited"),
    "delivery:story_or_personal_experience:01": ("stable_speaker_frame", "speaker_visible_all_three", "The same male speaker remains at the Mitty microphone while the subtitle line changes.", "limited"),
    "delivery:story_or_personal_experience:02": ("stable_speaker_frame", "speaker_visible_all_three", "The same woman remains at the microphone with the event group behind her.", "limited"),
    "delivery:example_or_case:01": ("stable_speaker_frame", "speaker_visible_all_three", "The same woman remains at the event microphone; only caption text and facial orientation change.", "limited"),
    "delivery:example_or_case:02": ("stable_speaker_frame", "speaker_visible_all_three", "The same male speaker remains in the public event composition with a crowd behind him.", "limited"),
    "delivery:contrast_or_disagreement:01": ("stable_scene_frame", "speaker_visible_all_three", "The same seated male actor/speaker remains at the desk with wall clocks; the scene may be scripted.", "limited"),
    "delivery:contrast_or_disagreement:02": ("stable_speaker_frame", "speaker_visible_all_three", "The same woman remains at the microphone with event attendees behind her.", "limited"),
    "delivery:correction_or_reframe:01": ("stable_speaker_frame", "speaker_visible_all_three", "The same male speaker remains at the Mitty microphone; subtitle text changes across the interval.", "limited"),
    "delivery:correction_or_reframe:02": ("stable_speaker_frame", "speaker_visible_all_three", "The same woman remains behind the lectern in the English Speeches composition.", "limited"),
    "delivery:repair_or_self_correction:01": ("stable_speaker_frame", "speaker_visible_all_three", "The same male speaker remains in the outdoor crowd composition with a microphone.", "limited"),
    "delivery:repair_or_self_correction:02": ("stable_speaker_frame", "speaker_visible_all_three", "The same male speaker remains on the blue-lit stage; mouth and head position change.", "limited"),
    "delivery:qualification_or_boundary:01": ("graphic_or_cutaway", "speaker_not_visible", "All three frames show the same blurred crowd graphic and large typography.", "not_usable_for_speaker_delivery"),
    "delivery:qualification_or_boundary:02": ("stable_speaker_frame", "speaker_visible_all_three", "The same woman remains on the purple-lit stage with changing subtitle text.", "limited"),
    "delivery:definition_or_explanation:01": ("stable_speaker_frame", "speaker_visible_all_three", "The same woman remains behind the lectern; the camera stays on the stage composition.", "limited"),
    "delivery:definition_or_explanation:02": ("stable_speaker_frame", "speaker_visible_all_three", "The same young male speaker remains against the BMW backdrop.", "limited"),
    "delivery:transition_or_structure:01": ("graphic_or_cutaway", "speaker_not_visible", "All three frames show the same stylized quotation graphic with no visible speaker.", "not_usable_for_speaker_delivery"),
    "delivery:transition_or_structure:02": ("scripted_scene_change", "speaker_not_visible", "The frames show a woman in a dark interior scene and then a different action/setting; no live speech delivery is isolated.", "not_usable_for_speaker_delivery"),
    "delivery:callback_or_repetition:01": ("stable_speaker_frame", "speaker_visible_all_three", "The same woman remains behind the lectern across the three frames.", "limited"),
    "delivery:callback_or_repetition:02": ("insert_to_room_cut", "speaker_not_visible", "The interval shows a television insert and then a wider room scene rather than a clearly visible live speaker.", "not_usable_for_speaker_delivery"),
    "delivery:humor_or_rapport:01": ("graphic_or_cutaway", "speaker_not_visible", "All three frames show a blurred crowd graphic with colored text.", "not_usable_for_speaker_delivery"),
    "delivery:humor_or_rapport:02": ("stable_speaker_frame", "speakers_visible_all_three", "Two men remain in the outdoor crowd composition; one holds the microphone while the other stands nearby.", "limited"),
    "delivery:credit_or_acknowledgment:01": ("stable_speaker_frame", "speaker_visible_all_three", "The same woman remains behind the lectern with the event branding visible.", "limited"),
    "delivery:credit_or_acknowledgment:02": ("stable_speaker_frame", "speaker_visible_all_three", "The same male speaker remains outdoors with the crowd and microphone.", "limited"),
    "delivery:call_to_action_or_audience_role:01": ("stable_speaker_frame", "speaker_visible_all_three", "The same woman remains behind the lectern; the visible gesture and subtitle line change.", "limited"),
    "delivery:call_to_action_or_audience_role:02": ("stable_scene_frame", "speaker_visible_all_three", "The same male actor remains at the table with wall clocks and raises both arms across the interval.", "limited"),
    "delivery:persuasion_or_advocacy:01": ("audience_to_stage_cut", "speaker_visibility_changes", "The interval cuts from a crowd/audience view to the Harvard-branded stage and then holds on the stage group.", "not_usable_for_continuous_speaker_delivery"),
    "delivery:persuasion_or_advocacy:02": ("graphic_or_cutaway", "speaker_not_visible", "All three frames show a quotation graphic over a blurred crowd; no live speaker is visible.", "not_usable_for_speaker_delivery"),
    "delivery:reflection_or_value_frame:01": ("stable_scene_frame", "speaker_visible_all_three", "The same seated male actor/speaker remains at the table; hand position changes across frames.", "limited"),
    "delivery:reflection_or_value_frame:02": ("multi_shot", "speaker_visibility_changes", "The interval cuts among a BMW interview, a purple-lit audience and a two-person interview composition.", "not_usable_for_continuous_speaker_delivery"),
}


def main() -> int:
    queue = json.loads(QUEUE.read_text())
    by_id = {item["sample_id"]: item for item in queue["items"]}
    rows = []
    for sample_id, (sequence, visibility, observation, usability) in OBSERVATIONS.items():
        item = by_id[sample_id]
        start, end = item["start_seconds"], item["end_seconds"]
        rows.append({
            "sample_id": sample_id,
            "canonical_job": item["canonical_job"],
            "video_id": item["video_id"],
            "evidence_id": item["evidence_id"],
            "source_video": f"data/video/{item['video_file']}",
            "source_url": item["source_url"],
            "sampled_frame_times_seconds": [round(start, 3), round((start + end) / 2, 3), round(end, 3)],
            "frame_count": 3,
            "frame_sequence_type": sequence,
            "speaker_visibility": visibility,
            "visual_sequence_observation": observation,
            "delivery_navigation_status": usability,
            "reviewer_code": "internal-project-agent",
            "independence": "not_independent",
        })
    report = {
        "schema_version": "1.0",
        "report_id": "communication-job-delivery-interval-frame-audit",
        "status": "internal_three_frame_visual_audit_independent_review_pending",
        "source_queue": "research/communication-job-delivery-sampling.json",
        "item_count": len(rows),
        "method": {"frame_rule": "start, midpoint and end of each raw A/V queue interval", "inspection": "manual visual inspection of extracted frames", "not_performed": ["continuous video review", "manual vocal listening", "speaker/event identity verification", "gesture or emotion interpretation", "audience outcome measurement"]},
        "claim_boundary": "Three-frame visual sequences distinguish speaker visibility and production/cutaway risk for navigation. They do not establish continuous delivery, gesture meaning, emotion, intent, identity, alignment, effectiveness or listener response.",
        "items": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    counts = {}
    for row in rows:
        counts[row["frame_sequence_type"]] = counts.get(row["frame_sequence_type"], 0) + 1
    lines = ["# Communication-job delivery — three-frame interval audit", "", "Status: **internal visual navigation audit; independent review pending**.", "", report["claim_boundary"], "", f"Intervals: **{len(rows)}** · frames per interval: **3**.", "", "| Sample | Job | Sequence | Speaker visibility | Navigation status |", "|---|---|---|---|---|"]
    for row in rows:
        lines.append(f"| `{row['sample_id']}` | `{row['canonical_job']}` | `{row['frame_sequence_type']}` | `{row['speaker_visibility']}` | `{row['delivery_navigation_status']}` |")
    lines += ["", "## What this changes", "", "Stable-speaker rows can be opened for bounded delivery inspection. Graphic, insert, scripted-scene and multi-shot rows must not be used as evidence for a continuous speaker gesture, gaze, pause or vocal pattern. The three-frame audit is internal and non-independent.", ""]
    MD.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "item_count": len(rows), "sequence_counts": counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
