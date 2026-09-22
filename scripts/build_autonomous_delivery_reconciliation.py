"""Reconcile bounded internal delivery observations with local feature proxies."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "research/communication-job-delivery-internal-observations.json"
PREFLIGHT = ROOT / "research/communication-job-delivery-measurement-preflight.json"
OUT = ROOT / "research/autonomous-delivery-reconciliation.json"
MD = ROOT / "writeups/autonomous-delivery-reconciliation.md"

JOB_PROMPTS = {
    "opening": "Can the first sentence orient without rushing?",
    "closing": "Does the final point receive enough space to be retrievable?",
    "question": "Does the timing leave a real answer, decline or clarification path?",
    "answer_or_response": "Is the literal answer distinguishable from the added frame?",
    "story_or_personal_experience": "Are scene, interpretation and limit separated?",
    "example_or_case": "Is the example marked as illustration rather than proof?",
    "contrast_or_disagreement": "Are the positions distinct without turning the transition into an attack?",
    "correction_or_reframe": "Is the valid concern visible before the frame changes?",
    "repair_or_self_correction": "Is the replacement sentence clear and brief?",
    "qualification_or_boundary": "Is uncertainty attached to the exact claim?",
    "definition_or_explanation": "Does the pace leave room for term, example and boundary?",
    "transition_or_structure": "Is the relationship between sections spoken before the shift?",
    "callback_or_repetition": "Does the return add a changed application rather than only volume?",
    "humor_or_rapport": "Is the joke optional, non-targeting and followed by a return to the point?",
    "credit_or_acknowledgment": "Are contribution and responsibility distinguishable?",
    "call_to_action_or_audience_role": "Are actor, action, resources, consent and limit explicit?",
    "persuasion_or_advocacy": "Are stake, mechanism, tradeoff and evidence separated?",
    "reflection_or_value_frame": "Is interpretation marked as interpretation?",
}


def tempo_label(wps: float | None) -> str:
    if wps is None:
        return "not_available"
    if wps > 8:
        return "alignment_outlier_requires_transcript_check"
    if wps < 1.5:
        return "lower_density_proxy"
    if wps < 3:
        return "moderate_density_proxy"
    return "higher_density_proxy"


def build() -> dict:
    observations = json.loads(OBS.read_text(encoding="utf-8"))["items"]
    measurements = {x["sample_id"]: x for x in json.loads(PREFLIGHT.read_text(encoding="utf-8"))["items"]}
    rows = []
    by_job = defaultdict(list)
    for observation in observations:
        measurement = measurements.get(observation["sample_id"], {})
        audio = measurement.get("audio_measurements") or observation.get("audio_measurements") or {}
        before = audio.get("transcript_gap_before_seconds")
        after = audio.get("transcript_gap_after_seconds")
        row = {
            "sample_id": observation["sample_id"],
            "canonical_job": observation["canonical_job"],
            "video_id": observation["video_id"],
            "evidence_id": observation["evidence_id"],
            "source_url": observation["source_url"],
            "transcript_alignment": observation["transcript_alignment"],
            "visual_observation": observation["visual_observation"],
            "setting_observation": observation["setting_editing_music_observation"],
            "audio_proxy": audio,
            "tempo_density_proxy": tempo_label(audio.get("words_per_second_proxy")),
            "entry_gap_candidate": bool(before is not None and before >= 0.75),
            "boundary_gap_candidate": bool(after is not None and after >= 0.75),
            "speech_activity_proxy": audio.get("speech_activity_fraction"),
            "practice_question": JOB_PROMPTS[observation["canonical_job"]],
            "internal_status": "bounded_internal_proxy_reconciliation_not_listening_or_validation",
            "claim_boundary": "Audio and visual values are local proxies and bounded frame observations. They do not establish vocal meaning, emotion, intent, speaker identity, audience response or effectiveness.",
        }
        rows.append(row)
        by_job[row["canonical_job"]].append(row)
    summaries = []
    for job in sorted(by_job):
        group = by_job[job]
        summaries.append({
            "canonical_job": job,
            "sample_count": len(group),
            "alignment_counts": {status: sum(x["transcript_alignment"] == status for x in group) for status in sorted({x["transcript_alignment"] for x in group})},
            "entry_gap_candidates": sum(x["entry_gap_candidate"] for x in group),
            "boundary_gap_candidates": sum(x["boundary_gap_candidate"] for x in group),
            "tempo_proxy_counts": {status: sum(x["tempo_density_proxy"] == status for x in group) for status in sorted({x["tempo_density_proxy"] for x in group})},
            "practice_question": JOB_PROMPTS[job],
        })
    return {
        "schema_version": "1.0",
        "reconciliation_id": "autonomous-delivery-reconciliation",
        "status": "bounded_internal_proxy_reconciliation_complete_manual_listening_pending",
        "item_count": len(rows),
        "job_count": len(summaries),
        "claim_boundary": "This joins the existing 36 bounded internal frame observations to reproducible local audio/transcript proxies. It is not manual listening, independent observation, speaker/event verification, nonverbal interpretation or effectiveness evidence.",
        "method": ["reuse internal midpoint observations", "reuse preflight audio and transcript measurements", "derive descriptive density/gap flags only", "retain alignment and missingness labels"],
        "job_summaries": summaries,
        "items": rows,
    }


def render(report: dict) -> str:
    lines = [
        "# Autonomous delivery reconciliation",
        "",
        "Status: **bounded internal proxy reconciliation complete; manual listening and independent review are not claimed**.",
        "",
        report["claim_boundary"],
        "",
        f"The report covers **{report['item_count']} samples** across **{report['job_count']} communication jobs**. Gap flags and density labels are navigation aids for practice experiments, not instructions to imitate.",
        "",
        "## Job summary",
        "",
        "| Job | Samples | Alignment | Entry-gap candidates | Boundary-gap candidates | Practice question |",
        "|---|---:|---|---:|---:|---|",
    ]
    for summary in report["job_summaries"]:
        alignment = ", ".join(f"{k}={v}" for k, v in summary["alignment_counts"].items())
        lines.append(f"| `{summary['canonical_job']}` | {summary['sample_count']} | {alignment} | {summary['entry_gap_candidates']} | {summary['boundary_gap_candidates']} | {summary['practice_question']} |")
    lines += ["", "## Sample-level records", "", "| Sample | Job | Alignment | Density proxy | Gap flags | Visible/setting boundary |", "|---|---|---|---|---|---|"]
    for row in report["items"]:
        flags = ", ".join(x for x, yes in (("entry", row["entry_gap_candidate"]), ("boundary", row["boundary_gap_candidate"])) if yes) or "none"
        boundary = f"{row['visual_observation']} {row['setting_observation']}"
        lines.append(f"| `{row['sample_id']}` | `{row['canonical_job']}` | `{row['transcript_alignment']}` | `{row['tempo_density_proxy']}` | `{flags}` | {boundary} |")
    lines += ["", "## Safe use", "", "Use one row to choose what to inspect or vary in a learner's own practice: pause, clause length, signposting or access mode. Do not infer a speaker's confidence, sincerity, emotion or persuasion from any row. The full delivery learning guide supplies the practice protocol.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    report = build()
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MD.write_text(render(report), encoding="utf-8")
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "markdown": str(MD.relative_to(ROOT)), "item_count": report["item_count"], "job_count": report["job_count"]}, indent=2))
