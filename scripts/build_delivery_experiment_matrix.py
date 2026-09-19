#!/usr/bin/env python3
"""Build concrete, bounded delivery experiments for all shared speech jobs."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/communication-job-cards.json"
OUT = ROOT / "research/delivery-experiment-matrix.json"
MD = ROOT / "writeups/delivery-experiment-matrix.md"

SPECS = {
    "opening": ("pause after the purpose sentence", "face or orient toward the available listener/channel", "typed heading or captioned purpose line"),
    "closing": ("slow slightly before the takeaway and release", "make the end boundary visible through stillness or a clear sign-off", "written takeaway plus open question"),
    "question": ("leave a full beat after the specific question", "offer an opt-out or turn-taking cue", "typed question with an explicit pass option"),
    "answer_or_response": ("state the direct answer before changing pace for context", "keep the response frame visually distinct from the question", "two labeled text blocks: answer / context"),
    "story_or_personal_experience": ("pause between scene, meaning and limit", "use only comfortable, consent-respecting orientation; do not perform emotion", "captioned or written scene with a stated boundary"),
    "example_or_case": ("mark the return from example to claim with a short pause", "show the claim/example distinction in a shared visual outline", "claim → example → boundary in text"),
    "contrast_or_disagreement": ("stress only the change-word or clause, not every contrast", "keep body orientation open where safe; do not use stare or proximity as pressure", "side-by-side earlier/current view with overlap"),
    "correction_or_reframe": ("slow on the correction and resume normal rate", "use a neutral reset rather than a dramatic apology gesture", "struck-through starting frame and corrected frame"),
    "repair_or_self_correction": ("stop cleanly, repair in one sentence, then continue", "make the turn boundary visible without theatrical self-punishment", "written correction with old/new wording"),
    "qualification_or_boundary": ("pause before the condition or uncertainty", "make the boundary available in the visual channel or text", "claim / condition / what would change my view"),
    "definition_or_explanation": ("reduce rate on the new term, then return to conversational pace", "point to or display the term only if that supports access", "plain definition, example and non-example"),
    "transition_or_structure": ("pause at the bridge and name the relationship", "use a visible agenda or section change when helpful", "written bridge sentence between sections"),
    "callback_or_repetition": ("change pause or emphasis only when the returning anchor has a new use", "reuse an accessible visual anchor without requiring imitation", "anchor → development → changed return"),
    "humor_or_rapport": ("leave room for a response; do not rush to explain the joke", "use self-directed or situational lightness, never another person's vulnerability", "optional light opening followed by plain transition"),
    "credit_or_acknowledgment": ("slow on the named contribution and consequence", "orient attention to the credited person or source only with consent and access", "name / contribution / consequence in text"),
    "call_to_action_or_audience_role": ("separate the problem, action, owner and limit with pauses", "make the requested action and opt-out path visible", "action checklist with owner, support, consent and limit"),
    "persuasion_or_advocacy": ("place evidence status before the strongest appeal", "keep stance readable without using posture or volume to overpower dissent", "claim / mechanism / tradeoff / accountable actor"),
    "reflection_or_value_frame": ("pause between event, interpretation and verified fact", "allow a non-performative reflective posture; do not copy a speaker's affect", "event / value / uncertainty / next question"),
}


def build() -> dict:
    cards = {card["canonical_job"]: card for card in json.loads(CARDS.read_text())["cards"]}
    rows = []
    for job, card in cards.items():
        vocal, visible, accessible = SPECS[job]
        rows.append({
            "job": job,
            "status": "constructed_delivery_experiment_not_validation_evidence",
            "communication_problem": card["problem"],
            "repeatable_form": card["form"],
            "vocal_variable": vocal,
            "observable_body_or_setting_variable": visible,
            "accessible_alternate": accessible,
            "experiment": f"Deliver the same {job.replace('_', ' ')} twice. Keep wording and content constant; change only {vocal}. If using video, inspect the observable body/setting variable without assigning meaning to it.",
            "listener_self_check": "Ask a consenting listener for the takeaway, the unresolved point and whether the format created pressure or access burden. Treat one response as local feedback, not general proof.",
            "measurement_boundary": "Audio timing and pose/face values are navigation proxies. They do not establish intentional delivery, emotion, gesture meaning, comprehension, persuasion or effectiveness.",
            "anti_imitation": "Borrow the communication choice, not the speaker's accent, identity, status, body language, emotional performance or biography.",
        })
    report = {
        "schema_version": "1.0",
        "matrix_id": "shared-18-job-delivery-experiment-matrix",
        "status": "constructed_practice_matrix_not_validation_evidence",
        "claim_boundary": "These are controlled rehearsal ideas for inspecting delivery choices. They are not findings that any vocal, visual or setting variable is effective.",
        "source": "research/communication-job-cards.json",
        "job_count": len(rows),
        "rows": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Delivery experiment matrix", "", "Status: **constructed practice matrix; not validation evidence**.", "", report["claim_boundary"], "", "For every communication job, hold wording and content constant and change one delivery variable. Use typed, captioned, audio-only or video modes according to access and consent. Do not interpret a detector output as emotion, intent or effectiveness.", "", "| Job | Vocal variable | Observable body/setting variable | Accessible alternate |", "|---|---|---|---|"]
    for row in rows:
        lines.append(f"| `{row['job']}` | {row['vocal_variable']} | {row['observable_body_or_setting_variable']} | {row['accessible_alternate']} |")
    lines += ["", "## Practice loop", "", "1. Choose one job and write the listener problem.", "2. Deliver the same wording twice, changing one vocal variable.", "3. If using video, inspect the listed body/setting feature without imitating or assigning psychological meaning.", "4. Repeat in an accessible alternate modality.", "5. Ask a consenting listener for takeaway, unresolved point and access/pressure burden.", "6. Keep local feedback separate from corpus recurrence or effectiveness claims.", "", "The [JSON matrix](../research/delivery-experiment-matrix.json) contains the full experiment prompts and boundaries.", ""]
    MD.write_text("\n".join(lines))
    return report


if __name__ == "__main__":
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "job_count": build()["job_count"]}, indent=2))
