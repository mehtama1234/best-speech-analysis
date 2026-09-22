#!/usr/bin/env python3
"""Build practical presentation sequences from expanded candidate cards."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/expanded-pattern-candidate-cards.json"
OUT = ROOT / "research/presentation-sequence-library.json"
MD = ROOT / "writeups/presentation-sequence-library.md"

SEQUENCES = [
    ("explain_an_unfamiliar_idea", "Explain an unfamiliar idea", ["expanded-relation-premise_correction", "expanded-relation-analogy_transfer", "expanded-relation-scope_repair"], "Help the listener understand the idea without letting an analogy become proof."),
    ("make_a_proposal", "Make a proposal", ["expanded-cluster-purpose_attention_example", "expanded-relation-question_redefinition", "expanded-relation-evidence_gap", "expanded-relation-hands_off"], "Move from purpose to a bounded choice while showing what is still unverified."),
    ("report_an_incident", "Report an incident or failure", ["expanded-cluster-failure_to_reframe", "expanded-relation-expectation_reversal", "expanded-relation-scope_repair", "expanded-cluster-unfinished_work_to_commitment"], "Describe what happened, correct the frame, and name the next accountable step."),
    ("lead_a_room", "Lead a room through change", ["expanded-relation-credit_redirection", "expanded-cluster-authority_to_service", "expanded-cluster-unity_across_scale", "expanded-cluster-invitation_to_low_barrier_entry"], "Connect authority to service and give people a voluntary next role."),
    ("answer_a_hard_question", "Answer a hard question", ["expanded-relation-question_redefinition", "expanded-relation-premise_correction", "expanded-relation-evidence_gap", "expanded-relation-scope_repair"], "Answer the decision-relevant question while preserving uncertainty and scope."),
    ("tell_a_story_with_a_point", "Tell a story with a point", ["expanded-relation-story_to_thesis", "expanded-relation-metric_revaluation", "expanded-relation-sorrow_and_continuation", "expanded-relation-scope_repair"], "Use a bounded scene, make the lesson explicit, and avoid turning one story into universal proof."),
]

# Sentence-level drafting scaffolds make each mined architecture usable in a
# real talk. They preserve the candidate status of the underlying pattern.
DRAFT_TEMPLATES = {
    "explain_an_unfamiliar_idea": [
        ("orient", "You may be wondering ____. The distinction that matters is ____.", "Can the listener state the question and distinction?", "Do not replace the listener's question with a more convenient one."),
        ("make_visible", "Think of ____ as ____. The part that carries over is ____.", "Can the listener say what the analogy does and does not cover?", "An analogy is an aid to understanding, not evidence by itself."),
        ("bound_claim", "So, in this situation ____. That holds when ____, and I would revise it if ____.", "Can the listener repeat the conclusion and its condition?", "Keep uncertainty visible instead of using fluency to imply certainty."),
    ],
    "make_a_proposal": [
        ("name_purpose", "The problem we are trying to solve is ____. The smallest useful outcome is ____.", "Can the listener name the problem and outcome?", "Do not inflate a local proposal into a universal solution."),
        ("ask_decision", "The decision we need today is ____. The question behind it is ____.", "Can the listener tell what decision is requested?", "Do not use a reframed question to evade a legitimate objection."),
        ("show_gap", "We know ____. We do not yet know ____. The next test is ____.", "Can the listener distinguish evidence from assumption?", "Do not present an unrun test as a result."),
        ("assign_next_turn", "____ owns the next decision. I can provide ____. The next step is ____.", "Can the listener see who acts and what support exists?", "Preserve consent, authority, and an opt-out where the burden is real."),
    ],
    "report_an_incident": [
        ("state_event", "At ____, ____ happened. The immediate impact was ____. We have contained ____.", "Can the listener separate observation from interpretation?", "Do not assign motive or blame without evidence."),
        ("correct_frame", "We expected ____. What we observed was ____. That means ____; it does not yet mean ____.", "Can the listener say what changed in the frame?", "A failure is an event to analyze, not an identity verdict."),
        ("narrow_claim", "The supported conclusion is ____. It applies to ____. We still need ____.", "Can the listener identify the boundary?", "Do not turn one incident into a broad causal or prevalence claim."),
        ("commit_action", "____ will do ____ by ____. We will check ____ and report back at ____.", "Can the listener identify the owner and check?", "Commit only to an action the owner has authority and support to carry out."),
    ],
    "lead_a_room": [
        ("locate_room", "We are here because ____. The work already contributed by ____ makes ____ possible.", "Can people see themselves and their work accurately represented?", "Do not use praise as proof that the plan is correct."),
        ("role_to_service", "My role gives me responsibility for ____. It does not replace your knowledge of ____.", "Can people name their agency and your responsibility?", "Do not turn hierarchy into consent."),
        ("bridge_scales", "This small action matters because ____. We can disagree about ____ and still share ____.", "Can the listener state the value without erasing disagreement?", "Unity language must not erase unequal risk or dissent."),
        ("invite_entry", "If you want to help, one useful entry is ____. You will have ____. This role does not require ____.", "Can a person choose a realistic next role?", "Do not assign unsafe or unpaid care work without consent and support."),
    ],
    "answer_a_hard_question": [
        ("answer_first", "The direct answer is ____. The reason it is difficult is ____.", "Did the listener get an answer before the reframing?", "Do not bury a refusal or uncertainty inside a long setup."),
        ("repair_premise", "That question assumes ____. The distinction we need is ____.", "Can the listener state the corrected question fairly?", "Do not caricature the question to make it easier to defeat."),
        ("show_gap", "The evidence supports ____. It does not establish ____. We would need ____ to know more.", "Can the listener identify the missing evidence?", "Do not imply status closes an evidence gap."),
        ("close_scope", "For this decision, my answer is ____. It changes if ____. The next question is ____.", "Can the listener repeat the answer and condition?", "Keep remaining uncertainty available for the next turn."),
    ],
    "tell_a_story_with_a_point": [
        ("set_scene", "At ____, I was ____. The detail that matters is ____.", "Can the listener locate the scene and stakes?", "Protect privacy and avoid using another person's story without permission."),
        ("turn_to_point", "What this showed me was ____. The decision it changed was ____.", "Can the listener distinguish the scene from the lesson?", "A vivid scene illustrates a possibility; it does not prove a general rule."),
        ("revalue_measure", "We usually measure ____. In this case that missed ____. The measure I now care about is ____.", "Can the listener name both measures?", "Do not dismiss useful measures without showing the tradeoff."),
        ("continue_without_resolution", "The unresolved part is ____. I cannot promise ____. I can do ____ next.", "Can the listener hear both the limit and the next action?", "Do not force closure or universal meaning onto a difficult story."),
    ],
}


def build() -> dict:
    cards = {card["card_id"]: card for card in json.loads(CARDS.read_text())["cards"]}
    sequences = []
    for sequence_id, title, card_ids, purpose in SEQUENCES:
        selected = [cards[card_id] for card_id in card_ids if card_id in cards]
        draft_template = [
            {"section_id": section_id, "title": card["title"], "sentence_stem": stem, "listener_check": listener_check, "boundary_check": boundary}
            for card, (section_id, stem, listener_check, boundary) in zip(selected, DRAFT_TEMPLATES[sequence_id])
        ]
        sequences.append({
            "sequence_id": sequence_id,
            "title": title,
            "purpose": purpose,
            "pattern_ids": [card["card_id"] for card in selected],
            "steps": [{"title": card["title"], "form": card["candidate_form"], "practice": card["practice_prompt"], "check": card["self_check"], "evidence_ids": card["evidence_ids"], "examples": card["examples"][:2]} for card in selected],
            "draft_template": draft_template,
            "status": "candidate_presentation_architecture_not_validated",
        })
    return {
        "schema_version": "1.0",
        "library_id": "presentation-sequence-library",
        "status": "source_linked_candidate_sequences_not_validated",
        "sequence_count": len(sequences),
        "claim_boundary": "These sequences combine corpus-mined candidate patterns into drafting architectures. They are practice hypotheses, not validated recipes, delivery findings, learner outcomes, listener outcomes or effectiveness evidence.",
        "sequences": sequences,
    }


def render(report: dict) -> str:
    lines = ["# Presentation sequence library", "", f"Status: **{report['status']}**. Sequences: **{report['sequence_count']}**.", "", report["claim_boundary"], ""]
    for sequence in report["sequences"]:
        lines += [f"## {sequence['title']}", "", sequence["purpose"], "", "Use this order:"]
        for number, step in enumerate(sequence["steps"], 1):
            lines += [f"{number}. **{step['title']}** — {step['form']}", f"   Practice: {step['practice']}", f"   Check: {step['check']}"]
            for example in step["examples"]:
                label = example.get("label") or example.get("relation_type") or "source example"
                lines.append(f"   Source: `{example['review_id']}` / `{example['video_id']}` / {label}; evidence `{', '.join(example['evidence_ids'][:3])}` ([{example['writeup']}]({example['writeup']}))")
        lines += ["", "Draft with these sentence stems:"]
        for number, section in enumerate(sequence["draft_template"], 1):
            label = section["section_id"].replace("_", " ").title()
            lines += [f"{number}. **{section['title']}** ({label}) — `{section['sentence_stem']}`", f"   Listener check: {section['listener_check']}", f"   Boundary check: {section['boundary_check']}"]
        lines += ["", "Keep the evidence, condition, consent and non-fit visible while drafting.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    report = build()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"presentation sequence library: {report['sequence_count']} sequences")
