#!/usr/bin/env python3
"""Materialize the local LLM's conservative shortlist with source cards."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JUDGE = ROOT / "research/local-llm-expanded-pattern-judge.json"
CARDS = ROOT / "research/expanded-pattern-candidate-cards.json"
OUT = ROOT / "research/expanded-pattern-llm-shortlist.json"
MD = ROOT / "writeups/expanded-pattern-llm-shortlist.md"


def build() -> dict:
    judge = json.loads(JUDGE.read_text())
    cards = {card["card_id"]: card for card in json.loads(CARDS.read_text())["cards"]}
    selected = []
    for item in (judge.get("judgment") or {}).get("strongest_candidates", []):
        card = cards.get(item.get("card_id"))
        if not card:
            continue
        selected.append({
            "card_id": card["card_id"],
            "title": card["title"],
            "candidate_form": card["candidate_form"],
            "practice_prompt": card["practice_prompt"],
            "self_check": card["self_check"],
            "non_fit_warning": card["non_fit_warning"],
            "source_record_count": card["source_record_count"],
            "source_video_count": card["source_video_count"],
            "evidence_ids": card["evidence_ids"],
            "examples": card["examples"],
            "model_reason": item,
        })
    return {
        "schema_version": "1.0",
        "shortlist_id": "expanded-pattern-llm-shortlist",
        "status": "local_model_shortlist_for_practice_review_not_promotion",
        "source_judge": "research/local-llm-expanded-pattern-judge.json",
        "candidate_count": len(selected),
        "promotion_eligible": False,
        "claim_boundary": "This shortlist reflects a local model's aggregate screen over 33 candidate cards. It is a prioritization aid, not semantic validation, independent review, learner evidence, listener outcome evidence, causal evidence or proof of effectiveness.",
        "cards": selected,
    }


def render(report: dict) -> str:
    lines = [
        "# Expanded-pattern LLM shortlist",
        "",
        f"Status: **{report['status']}**. Shortlisted cards: **{report['candidate_count']}**. Promotion eligible: **{report['promotion_eligible']}**.",
        "",
        report["claim_boundary"],
        "",
    ]
    for card in report["cards"]:
        lines += [
            f"## {card['title']}",
            "",
            f"**Candidate form:** {card['candidate_form']}",
            "",
            f"**Practice:** {card['practice_prompt']}",
            "",
            f"**Self-check:** {card['self_check']}",
            "",
            f"**Non-fit:** {card['non_fit_warning']}",
            "",
            f"**Source coverage:** {card['source_record_count']} records across {card['source_video_count']} videos.",
            "",
            "**Model selection record:**",
            "```json",
            json.dumps(card["model_reason"], ensure_ascii=False, indent=2),
            "```",
            "",
            "**Examples:**",
        ]
        for example in card["examples"][:3]:
            lines.append(f"- `{example['review_id']}` / `{example['video_id']}` — {example.get('excerpt', '')} ([{example['writeup']}]({example['writeup']}))")
        lines += ["", "---", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    report = build()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"expanded pattern LLM shortlist: {report['candidate_count']} cards")
