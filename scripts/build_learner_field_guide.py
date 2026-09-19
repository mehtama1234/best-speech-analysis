#!/usr/bin/env python3
"""Build a concise learner-facing index from the provisional job cards."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "research/communication-job-cards.json"
PHRASES = ROOT / "research/corpus-phrase-form-inventory.json"
OUT = ROOT / "writeups/learner-field-guide.md"


def main() -> int:
    cards = json.loads(CARDS.read_text())["cards"]
    phrase_inventory = json.loads(PHRASES.read_text())
    lines = [
        "# Learner field guide: communication jobs",
        "",
        "Status: **provisional practice guide; not a validated best-practice library**.",
        "",
        "Use this guide to choose a communication job, inspect examples, adapt a form and rehearse it. The cards are transcript-derived hypotheses. Exact phrase families show where wording was retrieved; they do not prove that the wording works, that a speaker intended a particular effect, or that repetition equals effectiveness.",
        "",
        "## The repeatable learning loop",
        "",
        "1. **Name the job.** Are you opening, explaining, asking, disagreeing, repairing, qualifying, closing or doing something else?",
        "2. **State the listener problem.** Say what the listener would otherwise have to infer.",
        "3. **Inspect, then adapt.** Read an exact transcript example and watch/listen to a delivery sample. Borrow the communicative move, not the speaker’s identity, accent, personality or mannerism.",
        "4. **Use the form.** Change the words, stakes, culture and relationship to fit your situation.",
        "5. **Bound the claim.** Mark evidence status, uncertainty, consent, responsibility and what the move cannot solve.",
        "6. **Check the listener.** Ask for a restatement and what remains unclear; treat one response as feedback, not proof of general effectiveness.",
        "7. **Revise.** Keep the useful function, remove imitation and record the non-fit case.",
        "",
        "## The 18 jobs",
        "",
        "| Job | Repeatable form | Indexed phrase families | When not to use |",
        "|---|---|---|---|",
    ]
    for card in cards:
        forms = ", ".join(form["phrase_form"] for form in card["phrase_forms"]) or "No direct family indexed"
        lines.append(f"| **{card['canonical_job']}** | {card['form']} | {forms} | {card['non_fit']} |")

    lines += ["", "## Exact phrase-form index", "", "These are the exact retrieval forms found in retained captions. Read the surrounding source context before adapting one; a frequent form may serve many functions. The train/holdout split is a corpus-retrieval split, not proof of recurrence or effectiveness.", "", "| Phrase form | Retrieval family | Train videos | Holdout videos | Representative retained wording | Source |", "|---|---|---:|---:|---|---|"]
    for item in phrase_inventory["forms"]:
        example = (item.get("examples") or [{}])[0]
        lines.append(f"| `{item['phrase_form']}` | `{item['family']}` | {item['train_video_count']} | {item['holdout_video_count']} | {example.get('text', '')} | [{example.get('evidence_id', 'source')}]({example.get('source_url', '')}) |")

    lines += ["", "## Detailed practice cards", ""]
    for card in cards:
        forms = ", ".join(form["phrase_form"] for form in card["phrase_forms"]) or "No direct family indexed"
        lines += [
            f"### {card['canonical_job']}",
            "",
            f"**Listener problem:** {card['problem']}",
            "",
            f"**Why it might help:** {card['mechanism']}",
            "",
            f"**Use this form:** {card['form']}",
            "",
            f"**Retrieved phrase families:** {forms}. These are search evidence, not scripts.",
            "",
            f"**Practice:** {card['practice']}",
            "",
            f"**Self-check:** {card['self_check']}",
            "",
            f"**Boundary:** {card['non_fit']}",
            "",
            f"**Evidence status:** {len(card['exact_examples'])} transcript examples and {len(card['delivery_observations'])} bounded delivery samples; independent review and outcome evidence remain pending.",
            "",
        ]

    lines += [
        "## Delivery inspection questions",
        "",
        "When watching or listening to a sample, record observations rather than explanations:",
        "",
        "- **Voice and timing:** Where does the speaker slow, speed up, pause, restart or overlap? Is the observation based on listening or only on a transcript/proxy?",
        "- **Visible action:** Is the speaker visible continuously? What posture, gaze, gesture or facial movement is actually observable, and what is missing?",
        "- **Setting and edit:** Is this a podium, interview, staged scene, cutaway, music bed or subtitle edit? Could the edit explain the apparent effect?",
        "- **Alignment:** Does the retained wording clearly belong to the visible speaker at that moment? Use `indeterminate` when it does not.",
        "- **Accessibility:** Could the cue be replaced with a textual, captioned, audio-only or asynchronous practice route? Do not require eye contact, facial expression, recording or disclosure.",
        "",
        "## Safety and evidence boundary",
        "",
        "Do not copy a speaker’s identity, accent, personality, status performance or mannerism. Do not treat an emotional image, vocal intensity, proxy measurement, applause, popularity or repeated phrase as proof of truth, comprehension, persuasion or effectiveness. Keep source identity, recurrence, delivery interpretation, learner teachability and listener outcomes as separate gates.",
        "",
        "For the cross-job synthesis of repeatable verbal moves and delivery-inspection questions, see [Repeatable communication patterns across the corpus](repeatable-communication-patterns.md).",
        "",
        "For the complete evidence chain and promotion criteria, see [the end-to-end goal](end-to-end-goal.md) and [the validation handoff](validation-handoff.md).",
        "",
    ]
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT.relative_to(ROOT)} ({len(cards)} jobs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
