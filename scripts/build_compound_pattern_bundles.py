#!/usr/bin/env python3
"""Mine recurring co-occurrences among the exhaustive candidate pattern leads."""

from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "research/exhaustive-pattern-inventory.json"
EVIDENCE = ROOT / "research/corpus-evidence-bank.json"
OUT = ROOT / "research/compound-pattern-bundles.json"
MD = ROOT / "writeups/compound-pattern-bundles.md"


def build() -> dict:
    inventory = json.loads(IN.read_text())
    evidence_map = {}
    for record in json.loads(EVIDENCE.read_text())["records"]:
        for segment in record.get("segments", []):
            if segment.get("text"):
                evidence_map[segment["evidence_id"]] = segment["text"]
    items = []
    for collection, kind, id_key in (("themes", "theme", "theme_id"), ("relation_patterns", "relation", "relation_type"), ("unmatched_clusters", "cluster", "cluster_id")):
        for item in inventory[collection]:
            item_id = item[id_key]
            items.append({
                "name": f"{kind}:{item_id}",
                "kind": kind,
                "item_id": item_id,
                "candidate_form": item["candidate_form"],
                "examples": item["examples"],
            })
    by_review: dict[str, set[str]] = defaultdict(set)
    by_name = {item["name"]: item for item in items}
    for item in items:
        for example in item["examples"]:
            by_review[example["review_id"]].add(item["name"])
    pair_reviews: dict[tuple[str, str], set[str]] = defaultdict(set)
    for review_id, names in by_review.items():
        for pair in itertools.combinations(sorted(names), 2):
            pair_reviews[pair].add(review_id)
    ranked = sorted(pair_reviews.items(), key=lambda pair: (-len(pair[1]), pair[0]))
    bundles = []
    for (left_name, right_name), review_ids in ranked:
        if len(review_ids) < 3:
            continue
        left = by_name[left_name]
        right = by_name[right_name]
        examples = []
        videos = set()
        for review_id in sorted(review_ids):
            left_example = next(example for example in left["examples"] if example["review_id"] == review_id)
            right_example = next(example for example in right["examples"] if example["review_id"] == review_id)
            videos.update((left_example["video_id"], right_example["video_id"]))
            examples.append({
                "review_id": review_id,
                "video_id": left_example["video_id"],
                "left_evidence_ids": left_example["evidence_ids"],
                "right_evidence_ids": right_example["evidence_ids"],
                "left_label": left_example.get("label", left_example.get("relation_type", left_name)),
                "right_label": right_example.get("label", right_example.get("relation_type", right_name)),
                "left_excerpt": evidence_map.get(left_example["evidence_ids"][0], ""),
                "right_excerpt": evidence_map.get(right_example["evidence_ids"][0], ""),
                "writeup": left_example["writeup"],
            })
            if len(examples) == 3:
                break
        bundle_id = "bundle-" + left["item_id"] + "-then-" + right["item_id"]
        bundles.append({
            "bundle_id": bundle_id,
            "left_pattern": left_name,
            "right_pattern": right_name,
            "candidate_form": f"{left['candidate_form']} → then {right['candidate_form']}",
            "cooccurrence_review_count": len(review_ids),
            "cooccurrence_video_count": len(videos),
            "practice_prompt": f"Draft a short talk that first uses the {left['item_id']} move, then the {right['item_id']} move. Keep the condition and non-fit visible.",
            "self_check": "Can a listener name both moves, why the second follows the first, and what remains unproven?",
            "non_fit_warning": "Co-occurrence is a discovery signal, not evidence that the two moves work better together or belong in this order.",
            "examples": examples,
            "status": "candidate_compound_architecture_requires_contextual_review",
        })
    practice_bundles = bundles[:24]
    return {
        "schema_version": "1.0",
        "bundle_inventory_id": "compound-pattern-bundles",
        "status": "source_linked_compound_candidates_not_validated",
        "source": "research/exhaustive-pattern-inventory.json",
        "candidate_item_count": len(items),
        "bundle_count": len(practice_bundles),
        "candidate_bundle_count": len(bundles),
        "practice_bundle_selection": "top_24_by_distinct_review_cooccurrence_then_stable_id",
        "minimum_cooccurrence_reviews": 3,
        "claim_boundary": "Bundles are recurring co-occurrences among corpus-mined candidate themes, relation architectures and unmatched clusters. They are not ordered causal sequences, effectiveness findings, recurrence proof, learner evidence, listener outcomes or validated recipes.",
        "bundles": practice_bundles,
        "all_candidate_bundles": bundles,
    }


def render(report: dict) -> str:
    lines = ["# Compound pattern bundles", "", f"Status: **{report['status']}**. Practice bundles: **{report['bundle_count']}**; all recurring candidates: **{report['candidate_bundle_count']}**; source leads: **{report['candidate_item_count']}**.", "", report["claim_boundary"], "", "The JSON retains every pair appearing in at least three distinct full-context reviews. The browser and this report show the top 24 practice candidates; the remaining candidates remain available in `all_candidate_bundles` for review.", ""]
    for bundle in report["bundles"]:
        lines += [f"## {bundle['bundle_id']}", "", f"**Co-occurrence:** {bundle['cooccurrence_review_count']} reviews / {bundle['cooccurrence_video_count']} videos", "", f"**Candidate form:** {bundle['candidate_form']}", "", f"**Practice:** {bundle['practice_prompt']}", "", f"**Self-check:** {bundle['self_check']}", "", f"**Non-fit:** {bundle['non_fit_warning']}", "", "**Source examples:**"]
        for example in bundle["examples"]:
            lines.append(f"- `{example['review_id']}` / `{example['video_id']}` — {example['left_label']} + {example['right_label']} ([source]({example['writeup']})); evidence: `{example['left_evidence_ids'][0]}`, `{example['right_evidence_ids'][0]}`")
            if example.get("left_excerpt") or example.get("right_excerpt"):
                lines.append(f"  > First move: {example.get('left_excerpt', '')}  ")
                lines.append(f"  > Second move: {example.get('right_excerpt', '')}")
        lines += ["", "---", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    report = build()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"compound pattern bundles: {report['bundle_count']}")
