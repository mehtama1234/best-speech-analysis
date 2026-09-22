#!/usr/bin/env python3
"""Mine recurring three-way co-occurrences among candidate pattern leads."""

from __future__ import annotations

import itertools
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "research/exhaustive-pattern-inventory.json"
EVIDENCE = ROOT / "research/corpus-evidence-bank.json"
OUT = ROOT / "research/compound-pattern-triads.json"
MD = ROOT / "writeups/compound-pattern-triads.md"


def build() -> dict:
    inventory = json.loads(IN.read_text())
    evidence = {}
    for record in json.loads(EVIDENCE.read_text())["records"]:
        for segment in record.get("segments", []):
            if segment.get("text"):
                evidence[segment["evidence_id"]] = segment["text"]
    items = []
    for collection, kind, key in (("themes", "theme", "theme_id"), ("relation_patterns", "relation", "relation_type"), ("unmatched_clusters", "cluster", "cluster_id")):
        for item in inventory[collection]:
            items.append({"name": f"{kind}:{item[key]}", "item_id": item[key], "candidate_form": item["candidate_form"], "examples": item["examples"]})
    by_name = {item["name"]: item for item in items}
    by_review = defaultdict(set)
    for item in items:
        for example in item["examples"]:
            by_review[example["review_id"]].add(item["name"])
    triad_reviews = defaultdict(set)
    for review_id, names in by_review.items():
        for triad in itertools.combinations(sorted(names), 3):
            triad_reviews[triad].add(review_id)
    ranked = sorted(((triad, reviews) for triad, reviews in triad_reviews.items() if len(reviews) >= 3), key=lambda item: (-len(item[1]), item[0]))
    triads = []
    for names, review_ids in ranked:
        examples = []
        for review_id in sorted(review_ids):
            source_examples = [next(example for example in by_name[name]["examples"] if example["review_id"] == review_id) for name in names]
            examples.append({
                "review_id": review_id,
                "video_id": source_examples[0]["video_id"],
                "pattern_labels": [example.get("label") or example.get("relation_type") or name for example, name in zip(source_examples, names)],
                "evidence_ids": [example["evidence_ids"][:3] for example in source_examples],
                "excerpts": [evidence.get(example["evidence_ids"][0], "") for example in source_examples],
                "writeup": source_examples[0]["writeup"],
            })
            if len(examples) == 3:
                break
        triad_id = "triad-" + "-then-".join(by_name[name]["item_id"] for name in names)
        triads.append({
            "triad_id": triad_id,
            "pattern_names": list(names),
            "candidate_form": " → then ".join(by_name[name]["candidate_form"] for name in names),
            "cooccurrence_review_count": len(review_ids),
            "practice_prompt": "Draft a talk that tests these three candidate moves in sequence, explaining the bridge between each move.",
            "self_check": "Can a listener name all three moves, why each follows, and what remains unproven?",
            "non_fit_warning": "Three-way co-occurrence is a discovery signal, not evidence of order, compatibility, causality or effectiveness.",
            "examples": examples,
            "status": "candidate_three_move_architecture_requires_contextual_review",
        })
    practice = triads[:24]
    return {
        "schema_version": "1.0",
        "triad_inventory_id": "compound-pattern-triads",
        "status": "source_linked_three_move_candidates_not_validated",
        "candidate_item_count": len(items),
        "candidate_triad_count": len(triads),
        "practice_triad_count": len(practice),
        "minimum_cooccurrence_reviews": 3,
        "claim_boundary": "Triads are recurring co-occurrences among corpus-mined candidate leads. They are not ordered causal sequences, effectiveness findings, learner evidence, listener outcomes or validated recipes.",
        "triads": practice,
        "all_candidate_triads": triads,
    }


def render(report: dict) -> str:
    lines = ["# Compound pattern triads", "", f"Status: **{report['status']}**. Practice triads: **{report['practice_triad_count']}**; all recurring triads: **{report['candidate_triad_count']}**.", "", report["claim_boundary"], "", "The JSON retains every three-way pairing appearing in at least three distinct full-context reviews. This report foregrounds the strongest 24 candidates.", ""]
    for triad in report["triads"]:
        lines += [f"## {triad['triad_id']}", "", f"**Co-occurrence:** {triad['cooccurrence_review_count']} reviews", "", f"**Candidate form:** {triad['candidate_form']}", "", f"**Practice:** {triad['practice_prompt']}", "", f"**Self-check:** {triad['self_check']}", "", f"**Non-fit:** {triad['non_fit_warning']}", "", "**Source examples:**"]
        for example in triad["examples"]:
            lines.append(f"- `{example['review_id']}` / `{example['video_id']}` — {' + '.join(example['pattern_labels'])}; evidence `{example['evidence_ids'][0][0]}`, `{example['evidence_ids'][1][0]}`, `{example['evidence_ids'][2][0]}` ([source]({example['writeup']}))")
            for index, excerpt in enumerate(example["excerpts"], 1):
                if excerpt:
                    lines.append(f"  > Move {index}: {excerpt}")
        lines += ["", "---", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    report = build()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"compound pattern triads: {report['candidate_triad_count']} candidates; {report['practice_triad_count']} practice")
