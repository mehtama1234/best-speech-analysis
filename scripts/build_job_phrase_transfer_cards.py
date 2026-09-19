#!/usr/bin/env python3
"""Join provisional job cards to exact multi-word phrase candidates for practice."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHRASES = ROOT / "research/job-phrase-candidate-inventory.json"
CARDS = ROOT / "research/communication-job-cards.json"
OUT = ROOT / "research/job-phrase-transfer-cards.json"
MD = ROOT / "writeups/job-phrase-transfer-cards.md"


def main() -> int:
    phrase_report = json.loads(PHRASES.read_text())
    card_by_job = {row["canonical_job"]: row for row in json.loads(CARDS.read_text())["cards"]}
    forms_by_job: dict[str, list[dict]] = {}
    for row in phrase_report["forms"]:
        forms_by_job.setdefault(row["canonical_job"], []).append(row)
    cards = []
    for job in sorted(card_by_job):
        card = card_by_job[job]
        forms = sorted(forms_by_job.get(job, []), key=lambda row: (row["candidate_kind"] == "marker_only_retrieval_form", -row["video_count"], -row["occurrence_count"], row["phrase_form"]))[:3]
        cards.append({
            "canonical_job": job,
            "problem": card["problem"],
            "mechanism_hypothesis": card["mechanism"],
            "repeatable_form": card["form"],
            "practice": card["practice"],
            "self_check": card["self_check"],
            "non_fit": card["non_fit"],
            "phrase_candidates": forms,
            "status": "provisional_transfer_card_requires_context_and_learner_review",
            "transfer_instruction": "Rewrite the candidate in your own words, preserve the job, add the relevant condition/consent/evidence limit, and test listener restatement.",
        })
    report = {
        "schema_version": "1.0",
        "report_id": "job-phrase-transfer-cards",
        "status": "provisional_phrase_transfer_cards_not_validated",
        "source_phrase_inventory": "research/job-phrase-candidate-inventory.json",
        "source_job_cards": "research/communication-job-cards.json",
        "claim_boundary": "These cards join transcript-derived job hypotheses to exact phrase retrieval candidates. They do not prove that a phrase performs the job, that the source speaker intended it, or that adapting it improves delivery or listener outcomes.",
        "card_count": len(cards),
        "cards": cards,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Job phrase transfer cards", "", "Status: **provisional phrase transfer cards; not validated**.", "", report["claim_boundary"], "", "Use the phrase as a retrieval handle, not a script. Rewrite it for your relationship and situation, then add the evidence, condition, consent or limit required by the job.", ""]
    for card in cards:
        lines += [f"## `{card['canonical_job']}`", "", f"**Listener problem:** {card['problem']}", "", f"**Repeatable form:** {card['repeatable_form']}", "", f"**Why it may help:** {card['mechanism_hypothesis']}", "", "**Candidate phrase handles:**"]
        for phrase in card["phrase_candidates"]:
            example = phrase["examples"][0] if phrase["examples"] else {}
            kind = "marker-only; inspect context, do not imitate" if phrase["candidate_kind"] == "marker_only_retrieval_form" else "content-bearing candidate"
            lines.append(f"- `{phrase['phrase_form']}` — **{kind}**; {phrase['video_count']} videos / {phrase['occurrence_count']} occurrences; example [{example.get('evidence_id', '')}]({example.get('source_url', '')})")
        lines += ["", f"**Practice:** {card['practice']}", "", f"**Self-check:** {card['self_check']}", "", f"**Do not use when:** {card['non_fit']}", "", f"**Transfer:** {card['transfer_instruction']}", ""]
    MD.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "cards": len(cards), "phrase_handles": sum(len(card["phrase_candidates"]) for card in cards)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
