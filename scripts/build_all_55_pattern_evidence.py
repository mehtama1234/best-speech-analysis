#!/usr/bin/env python3
"""Build one evidence matrix for all 55 presenter-facing pattern candidates."""

from __future__ import annotations

import json
import re
from pathlib import Path

try:
    from scripts.recovered_pattern_rules import recovery_rule
except ImportError:
    from recovered_pattern_rules import recovery_rule

ROOT = Path(__file__).resolve().parents[1]


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def mine(rows: list[dict], rule: re.Pattern[str], quality: dict[str, dict]) -> tuple[int, int, int]:
    video_ids = set()
    hits = 0
    flagged_video_ids = set()
    for row in rows:
        found = [segment for segment in row.get("segments", []) if rule.search(segment.get("text", ""))]
        if found:
            video_id = row.get("video_id") or row.get("original_video_id")
            video_ids.add(video_id)
            if quality.get(video_id, {}).get("flags"):
                flagged_video_ids.add(video_id)
            hits += len(found)
    return len(video_ids), hits, len(flagged_video_ids)


def main() -> int:
    inventory = json.loads((ROOT / "research/exhaustive-pattern-inventory.json").read_text())
    direct = jsonl(ROOT / "research/recovered-audio-transcripts.jsonl")
    alternate = jsonl(ROOT / "research/alternate-source-transcripts.jsonl")
    external = jsonl(ROOT / "research/external-source-transcripts.jsonl")
    quality_rows = json.loads((ROOT / "research/recovered-transcript-quality-audit.json").read_text())["rows"]
    quality = {
        (row["evidence_layer"], row["video_id"]): row for row in quality_rows
    }
    groups = [
        ("core_theme", inventory["themes"], "theme_id", "episode_hit_count"),
        ("structural_subtheme", inventory["relation_patterns"], "relation_type", "relation_count"),
        ("additional_subtheme", inventory["unmatched_clusters"], "cluster_id", "label_hit_count"),
    ]
    patterns = []
    for category, items, id_key, canonical_hit_key in groups:
        for item in items:
            rule_text = recovery_rule(category, item)
            rule = re.compile(rule_text, re.IGNORECASE)
            direct_count, direct_hits, direct_flagged = mine(
                direct, rule, {(key[1]): value for key, value in quality.items() if key[0] == "direct_audio"}
            )
            alternate_count, alternate_hits, alternate_flagged = mine(
                alternate, rule, {(key[1]): value for key, value in quality.items() if key[0] == "alternate_source"}
            )
            external_count, external_hits, external_flagged = mine(
                external, rule, {(key[1]): value for key, value in quality.items() if key[0] == "external_transcript"}
            )
            examples = item.get("examples") or [{}]
            example = examples[0]
            patterns.append({
                "pattern_id": item[id_key],
                "category": category,
                "candidate_form": item.get("candidate_form", ""),
                "matching_rule": rule_text,
                "canonical_video_count": item.get("video_count", 0),
                "canonical_source_record_count": item.get(canonical_hit_key, 0),
                "direct_recovered_video_count": direct_count,
                "direct_recovered_segment_hits": direct_hits,
                "direct_recovered_flagged_video_count": direct_flagged,
                "alternate_source_video_count": alternate_count,
                "alternate_source_segment_hits": alternate_hits,
                "alternate_source_flagged_video_count": alternate_flagged,
                "external_transcript_video_count": external_count,
                "external_transcript_segment_hits": external_hits,
                "external_transcript_flagged_video_count": external_flagged,
                "example_video_id": example.get("video_id", ""),
                "example_label": example.get("label") or example.get("claim", "source-linked candidate"),
                "example_writeup": example.get("writeup", ""),
                "example_evidence_ids": example.get("evidence_ids", [])[:5],
                "status": "candidate_pattern_not_effectiveness_validated",
            })
    payload = {
        "schema_version": "1.0",
        "status": "all_55_pattern_evidence_layers_reconciled",
        "pattern_count": len(patterns),
        "canonical_full_context_review_count": 395,
        "direct_recovered_transcript_count": len([r for r in direct if r.get("status") == "machine_transcript_candidate"]),
        "alternate_source_transcript_count": len([r for r in alternate if r.get("status") == "alternate_machine_transcript_candidate"]),
        "external_transcript_count": len([r for r in external if r.get("status") == "external_transcript_candidate"]),
        "patterns": patterns,
        "claim_boundary": "Canonical counts are mined from full-context candidate records. Recovery counts are machine retrieval leads from separate evidence layers. No row proves recurrence, speaker intent, delivery meaning, learner evidence, listener outcomes, or effectiveness.",
    }
    (ROOT / "research/all-55-pattern-evidence.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# All 55 presentation-pattern evidence matrix",
        "",
        "This matrix reconciles every presenter-facing candidate: 22 core themes, 18 structural subthemes, and 15 additional subthemes. Evidence layers remain separate.",
        "",
        f"- Pattern rows: **{len(patterns)}**",
        f"- Canonical project-generated single-pass full-context corpus (not independent validation): **{payload['canonical_full_context_review_count']}**",
        f"- Direct recovered machine transcripts: **{payload['direct_recovered_transcript_count']}**",
        f"- Alternate-source machine transcripts: **{payload['alternate_source_transcript_count']}**",
        f"- External transcript candidates: **{payload['external_transcript_count']}**",
        "",
        "| Category | Pattern | Canonical videos | Direct recovered | Alternate source | External | How to use |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in patterns:
        lines.append(f"| {row['category']} | `{row['pattern_id']}` | {row['canonical_video_count']} | {row['direct_recovered_video_count']} ({row['direct_recovered_flagged_video_count']} flagged) | {row['alternate_source_video_count']} ({row['alternate_source_flagged_video_count']} flagged) | {row['external_transcript_video_count']} ({row['external_transcript_flagged_video_count']} flagged) | {row['candidate_form']} |")
    lines += [
        "",
        "## Use protocol",
        "",
        "For any row: translate the candidate form into your communication job; draft each stage in your own words; add one bounded example; state a condition, limit, or non-fit; and ask a listener to restate the point. Treat recovery-layer hits as review leads, not validated findings.",
        "Parenthetical recovery counts identify rows with structural-quality flags; they do not mean the other rows have been human-validated.",
        "",
    ]
    (ROOT / "writeups/all-55-pattern-evidence.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"pattern_count": len(patterns), "direct": payload["direct_recovered_transcript_count"], "alternate": payload["alternate_source_transcript_count"], "external": payload["external_transcript_count"]}))


if __name__ == "__main__":
    main()
