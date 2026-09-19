#!/usr/bin/env python3
"""Build a practical transfer guide for the exact phrase-form inventory."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/corpus-phrase-form-inventory.json"
OUT = ROOT / "writeups/phrase-transfer-guide.md"


FAMILY_GUIDANCE = {
    "call_to_action": (
        "Name the actor, feasible action, resources or authority, consent path and limit.",
        "Does this phrase make a real role available, or only create moral pressure?",
    ),
    "conclusion_or_summary": (
        "State the takeaway, connect it to the preceding reason and name what remains open.",
        "Does the summary add orientation, or merely announce confidence and closure?",
    ),
    "contrast_or_disagreement": (
        "Name the earlier frame fairly, say what changed and preserve any genuine overlap.",
        "Is this a real distinction, or a false binary hidden inside a small connector?",
    ),
    "definition": (
        "Give the plain meaning, one example and one boundary; do not let the phrase stand in for a definition.",
        "Could the listener use the term and say what it does not mean?",
    ),
    "example": (
        "State the claim, give a bounded case and return to the claim without implying prevalence or causation.",
        "Is the case illustrative, representative, or being asked to do unsupported evidentiary work?",
    ),
    "question": (
        "Ask one answerable question, provide context and make it safe to answer, decline or clarify.",
        "Does the listener receive a genuine answer path rather than a disguised demand?",
    ),
    "story_or_personal_experience": (
        "Give a bounded scene, separate what happened from what it means and state what it cannot prove.",
        "Are privacy, consent and the difference between illustration and proof preserved?",
    ),
    "uncertainty_or_qualification": (
        "Attach the qualifier to a specific claim, name the condition and say what would change it.",
        "Does the wording calibrate certainty, or merely make an unclear claim harder to challenge?",
    ),
}


def main() -> int:
    inventory = json.loads(SOURCE.read_text())
    lines = [
        "# Phrase transfer guide",
        "",
        "Status: **50 exact transcript forms with provisional transfer instructions; not validated scripts**.",
        "",
        "Use a phrase as a retrieval handle, not as a magic word. The same form can perform different jobs, and recurrence does not prove effectiveness. Read the linked source context, rewrite the meaning for your relationship and stakes, then test whether a listener can restate the intended job.",
        "",
        f"Inventory scope: **{inventory['form_count']} forms** across **{inventory['eligible_caption_segment_count']} retained caption segments**. Counts are transcript retrieval counts, not independent recurrence, delivery or listener evidence.",
        "",
    ]
    current_family = None
    for item in inventory["forms"]:
        family = item["family"]
        if family != current_family:
            guidance, question = FAMILY_GUIDANCE[family]
            lines += [
                f"## `{family}`",
                "",
                f"**Transfer recipe:** {guidance}",
                "",
                f"**Context check:** {question}",
                "",
                "| Exact form | Videos | Occurrences | Retained example |",
                "|---|---:|---:|---|",
            ]
            current_family = family
        example = (item.get("examples") or [{}])[0]
        text = " ".join(str(example.get("text", "")).split())
        if len(text) > 220:
            text = text[:219].rstrip() + "…"
        evidence = example.get("evidence_id", "source context")
        url = example.get("source_url", "")
        source = f"[{evidence}]({url})" if url else f"`{evidence}`"
        lines.append(f"| `{item['phrase_form']}` | {item['video_count']} | {item['occurrence_count']} | {text} ({source}) |")
    lines += [
        "",
        "## Transfer drill",
        "",
        "1. Copy the source phrase only as a retrieval cue; do not copy its claim.",
        "2. Write the job in plain language without the phrase.",
        "3. Rewrite it for your listener, relationship, authority and access mode.",
        "4. Add the evidence status, condition, consent path or limit that the source may omit.",
        "5. Ask for a restatement and record the non-fit case.",
        "",
        "The [learner field guide](learner-field-guide.md) supplies the 18 job cards; the [phrase inventory](corpus-phrase-form-inventory.md) supplies the full retrieval counts and the [corpus findings catalog](corpus-findings-catalog.md) supplies video-level context.",
        "",
    ]
    OUT.write_text("\n".join(lines))
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "forms": inventory["form_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
