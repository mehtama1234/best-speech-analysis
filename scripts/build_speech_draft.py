#!/usr/bin/env python3
"""Create a local Markdown speech worksheet from a corpus-derived sequence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "research/presentation-sequence-library.json"


def build(sequence_id: str, topic: str, audience: str, outcome: str) -> str:
    report = json.loads(LIBRARY.read_text())
    sequence = next((item for item in report["sequences"] if item["sequence_id"] == sequence_id), None)
    if sequence is None:
        available = ", ".join(item["sequence_id"] for item in report["sequences"])
        raise ValueError(f"unknown sequence {sequence_id!r}; choose one of: {available}")
    lines = [
        f"# Speech worksheet: {topic}",
        "",
        f"- Audience: {audience}",
        f"- Smallest useful outcome: {outcome}",
        f"- Sequence: `{sequence_id}`",
        "",
        sequence["purpose"],
        "",
        "## Orient",
        "",
        "Name the situation, why it matters, and the route.",
        "",
        "Write the sequence moves below in your own words. Keep the condition, evidence and non-fit visible.",
        "",
    ]
    for number, section in enumerate(sequence["draft_template"], 1):
        lines += [
            f"## {number}. {section['title']}",
            "",
            f"Sentence stem: `{section['sentence_stem']}`",
            "",
            "Source examples:",
        ]
        for example in next(step["examples"] for step in sequence["steps"] if step["title"] == section["title"]):
            lines.append(f"- `{example['review_id']}` / `{example['video_id']}` — evidence `{', '.join(example['evidence_ids'][:3])}` ({example['writeup']})")
            if example.get("excerpt"):
                lines.append(f"  > {example['excerpt']}")
        lines += [
            "",
            "Your version:",
            "",
            "_Write here._",
            "",
            f"Listener check: {section['listener_check']}",
            f"Boundary check: {section['boundary_check']}",
            "",
        ]
    lines += [
        "## Close",
        "",
        "Return to the takeaway, name the remaining limit or next step, and invite one answerable next turn.",
        "",
        "## Listener reflection",
        "",
        "- Restatement:",
        "- Still unclear:",
        "- Non-fit or pressure point:",
        "- Next revision:",
        "",
        "## Claim boundary",
        "",
        report["claim_boundary"],
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sequence_id")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = build(args.sequence_id, args.topic, args.audience, args.outcome)
    if args.output:
        args.output.write_text(text + "\n")
        print(f"speech worksheet written: {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
