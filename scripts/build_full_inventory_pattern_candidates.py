#!/usr/bin/env python3
"""Combine canonical findings with recovered machine-transcript leads.

The two evidence classes stay labeled separately so recovered audio cannot be
mistaken for human-validated semantic review.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    inventory = json.loads((ROOT / "research/exhaustive-pattern-inventory.json").read_text())
    recovered = json.loads((ROOT / "research/recovered-audio-pattern-candidates.json").read_text())
    alternate = json.loads((ROOT / "research/alternate-source-pattern-candidates.json").read_text())
    external = json.loads((ROOT / "research/external-transcript-pattern-candidates.json").read_text())
    coverage = json.loads((ROOT / "research/corpus-coverage-audit.json").read_text())
    recovered_by_id = {row["theme_id"]: row for row in recovered["patterns"]}
    alternate_by_id = {row["theme_id"]: row for row in alternate["patterns"]}
    external_by_id = {row["theme_id"]: row for row in external["patterns"]}
    patterns = []
    for theme in inventory["themes"]:
        machine = recovered_by_id.get(theme["theme_id"], {})
        alternate_machine = alternate_by_id.get(theme["theme_id"], {})
        external_machine = external_by_id.get(theme["theme_id"], {})
        patterns.append({
            "theme_id": theme["theme_id"],
            "candidate_form": theme["candidate_form"],
            "canonical_video_count": theme.get("video_count", 0),
            "canonical_episode_hits": theme.get("episode_hit_count", 0),
            "canonical_relation_hits": theme.get("relation_hit_count", 0),
            "recovered_machine_video_count": machine.get("recovered_video_count", 0),
            "recovered_machine_segment_hits": machine.get("recovered_segment_hit_count", 0),
            "recovered_machine_examples": machine.get("examples", []),
            "alternate_source_video_count": alternate_machine.get("recovered_video_count", 0),
            "alternate_source_segment_hits": alternate_machine.get("recovered_segment_hit_count", 0),
            "alternate_source_examples": alternate_machine.get("examples", []),
            "external_transcript_video_count": external_machine.get("external_video_count", 0),
            "external_transcript_segment_hits": external_machine.get("external_segment_hit_count", 0),
            "external_transcript_examples": external_machine.get("examples", []),
        })
    payload = {
        "schema_version": "1.0",
        "status": "full_inventory_candidate_patterns_with_separate_evidence_layers",
        "inventory_count": 480,
        "canonical_full_context_review_count": inventory.get("review_count", 395),
        "recovered_machine_transcript_count": recovered.get("transcript_count", 0),
        "alternate_source_machine_transcript_count": alternate.get("transcript_count", 0),
        "external_transcript_candidate_count": external.get("transcript_count", 0),
        "unique_text_bearing_video_count": coverage.get("unique_text_bearing_video_count"),
        "unique_text_bearing_video_count_including_external": coverage.get("unique_text_bearing_video_count_including_external"),
        "unresolved_count": coverage["unresolved_after_media_recovery_count"],
        "patterns": patterns,
        "claim_boundary": "Canonical counts are mined from project-generated single-pass full-context transcript records and are not independent human validation. Recovered counts are regex retrieval leads from machine transcripts and are not semantic validation, recurrence proof, delivery evidence, learner evidence, listener outcomes, or effectiveness evidence.",
    }
    (ROOT / "research/full-inventory-pattern-candidates.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Full-inventory pattern candidates",
        "",
        f"This is the broadest current pattern layer for the fixed {payload['inventory_count']}-video inventory. It combines the canonical {payload['canonical_full_context_review_count']}-video project-generated single-pass full-context transcript corpus (not independent human validation) with {payload['recovered_machine_transcript_count']} direct recovered machine-transcript candidates and {payload['alternate_source_machine_transcript_count']} alternate-source candidates. Evidence classes are kept separate.",
        "The complete presenter-facing taxonomy is the [55-pattern guide](amazing-presentation-patterns.md): 22 core themes, 18 structural subthemes, and 15 additional subthemes. Each pattern includes a candidate form and practical presentation use; this report adds the expanded evidence-layer counts.",
        "",
        f"- Fixed inventory: **{payload['inventory_count']}** videos",
        f"- Canonical project-generated single-pass full-context videos: **{payload['canonical_full_context_review_count']}**",
        f"- Recovered machine-transcript candidates: **{payload['recovered_machine_transcript_count']}**",
        f"- Alternate-source machine-transcript candidates: **{payload['alternate_source_machine_transcript_count']}**",
        f"- External transcript candidates: **{payload['external_transcript_candidate_count']}**",
        f"- Unique videos with at least one text-bearing layer: **{payload['unique_text_bearing_video_count']}**",
        f"- Unique videos with text-bearing layer including external candidates: **{payload['unique_text_bearing_video_count_including_external']}**",
        f"- Unresolved videos: **{payload['unresolved_count']}**",
        "",
        "## Theme map",
        "",
        "| Theme | Canonical project-generated videos | Direct recovered candidates | Alternate-source candidates | External transcript candidates | Use |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in patterns:
        lines.append(f"| `{row['theme_id']}` | {row['canonical_video_count']} | {row['recovered_machine_video_count']} | {row['alternate_source_video_count']} | {row['external_transcript_video_count']} | {row['candidate_form']} |")
    lines += [
        "",
        "## Interpretation boundary",
        "",
        "The canonical column supports the existing provisional pattern guide. The recovered column is a retrieval layer from automatic transcripts, useful for locating material to review. Neither column is independent effectiveness evidence; recovered rows must receive context, transcript-quality, and rhetorical review before semantic use.",
        "",
    ]
    (ROOT / "writeups/full-inventory-pattern-candidates.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"themes": len(patterns), "canonical": payload["canonical_full_context_review_count"], "recovered": payload["recovered_machine_transcript_count"]}))


if __name__ == "__main__":
    main()
