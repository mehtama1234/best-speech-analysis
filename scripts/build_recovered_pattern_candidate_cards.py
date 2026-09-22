#!/usr/bin/env python3
"""Build source-linked candidate cards for the recovered transcript layers."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

try:
    from scripts.recovered_pattern_rules import recovery_rule
except ImportError:
    from recovered_pattern_rules import recovery_rule


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "research/recovered-pattern-candidate-cards.json"
MARKDOWN = ROOT / "writeups/recovered-pattern-candidate-cards.md"


def read_jsonl(path: Path, layer: str) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            row["evidence_layer"] = layer
            rows.append(row)
    return rows


def registry() -> dict[str, dict]:
    result = {}
    path = ROOT / "data/metadata/video-registry.jsonl"
    for line in path.read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            result[row["video_id"]] = row
    return result


def main() -> int:
    inventory = json.loads((ROOT / "research/exhaustive-pattern-inventory.json").read_text())
    quality_rows = json.loads(
        (ROOT / "research/recovered-transcript-quality-audit.json").read_text()
    )["rows"]
    quality = {
        (row["evidence_layer"], row["video_id"]): row for row in quality_rows
    }
    source_rows = [
        row
        for path, layer in (
            (ROOT / "research/recovered-audio-transcripts.jsonl", "direct_audio"),
            (ROOT / "research/alternate-source-transcripts.jsonl", "alternate_source"),
            (ROOT / "research/external-source-transcripts.jsonl", "external_transcript"),
        )
        for row in read_jsonl(path, layer)
    ]
    groups = [
        ("core_theme", inventory["themes"], "theme_id"),
        ("structural_subtheme", inventory["relation_patterns"], "relation_type"),
        ("additional_subtheme", inventory["unmatched_clusters"], "cluster_id"),
    ]
    metadata = registry()
    cards = []
    by_pattern = Counter()
    by_layer = Counter()
    for row in source_rows:
        video_id = row.get("video_id") or row.get("original_video_id")
        source_quality = quality.get((row["evidence_layer"], video_id), {})
        for category, items, id_key in groups:
            for item in items:
                rule_text = recovery_rule(category, item)
                rule = re.compile(rule_text, re.IGNORECASE)
                evidence = []
                for index, segment in enumerate(row.get("segments", [])):
                    text = str(segment.get("text", ""))
                    if rule.search(text):
                        evidence.append({
                            "segment_index": index,
                            "start": segment.get("start"),
                            "end": segment.get("end"),
                            "text": text,
                        })
                if not evidence:
                    continue
                pattern_id = item[id_key]
                card = {
                    "card_id": f"{row['evidence_layer']}:{video_id}:{pattern_id}",
                    "video_id": video_id,
                    "candidate_video_id": row.get("candidate_video_id"),
                    "title": metadata.get(video_id, {}).get("title"),
                    "evidence_layer": row["evidence_layer"],
                    "pattern_id": pattern_id,
                    "category": category,
                    "candidate_form": item.get("candidate_form", ""),
                    "matching_rule": rule_text,
                    "hit_count": len(evidence),
                    "evidence": evidence[:8],
                    "quality_flags": source_quality.get("flags", []),
                    "quality_disposition": source_quality.get("disposition"),
                    "source_review_status": row.get("review_status"),
                    "claim_status": "recovery_candidate_not_human_validated",
                }
                cards.append(card)
                by_pattern[pattern_id] += 1
                by_layer[row["evidence_layer"]] += 1

    cards.sort(key=lambda card: (card["evidence_layer"], card["video_id"], card["pattern_id"]))
    payload = {
        "schema_version": "1.0",
        "status": "recovered_pattern_candidate_cards",
        "source_transcript_row_count": len(source_rows),
        "candidate_card_count": len(cards),
        "counts_by_evidence_layer": dict(sorted(by_layer.items())),
        "patterns_with_cards": len(by_pattern),
        "cards": cards,
        "claim_boundary": (
            "Cards are regex-assisted retrieval candidates from direct machine, "
            "alternate-source machine, and one external transcript layer. They do "
            "not establish semantic accuracy, source identity, recurrence, speaker "
            "intent, delivery meaning, or effectiveness. Exact excerpts require "
            "human context review before promotion."
        ),
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Recovered pattern candidate cards",
        "",
        "This is the per-video evidence layer for recovered transcripts. Each card",
        "connects one candidate pattern to exact transcript segments while preserving",
        "source, quality and human-review boundaries.",
        "",
        f"- Source transcript rows: **{len(source_rows)}**",
        f"- Candidate cards: **{len(cards)}**",
        f"- Patterns represented: **{len(by_pattern)}/55**",
        f"- Cards by evidence layer: **{dict(sorted(by_layer.items()))}**",
        "",
        "## How to use",
        "",
        "Use a card to open the exact excerpt, read its surrounding context, and",
        "decide whether the words actually perform the candidate function. Treat the",
        "candidate form as a drafting hypothesis, not a rule. Keep the quality flags",
        "and source-review status attached when exporting a card into a lesson.",
        "",
        "## Claim boundary",
        "",
        payload["claim_boundary"],
        "",
        "## Reproducibility",
        "",
        "```bash",
        "python3 scripts/build_recovered_pattern_candidate_cards.py",
        "```",
    ]
    MARKDOWN.write_text("\n".join(lines) + "\n")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "markdown_output": str(MARKDOWN.relative_to(ROOT)),
        "source_transcript_row_count": len(source_rows),
        "candidate_card_count": len(cards),
        "patterns_with_cards": len(by_pattern),
        "counts_by_evidence_layer": dict(sorted(by_layer.items())),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
