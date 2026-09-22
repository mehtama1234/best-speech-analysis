#!/usr/bin/env python3
"""Audit lexical retrieval density and noise risk for recovered patterns."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/recovered-pattern-rule-audit.json"
MD = ROOT / "writeups/recovered-pattern-rule-audit.md"


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> int:
    matrix = json.loads((ROOT / "research/all-55-pattern-evidence.json").read_text())
    direct = jsonl(ROOT / "research/recovered-audio-transcripts.jsonl")
    alternate = jsonl(ROOT / "research/alternate-source-transcripts.jsonl")
    external = jsonl(ROOT / "research/external-source-transcripts.jsonl")
    sources = {
        "direct_audio": direct,
        "alternate_source": alternate,
        "external_transcript": external,
    }
    totals = {layer: sum(len(row.get("segments", [])) for row in rows) for layer, rows in sources.items()}
    rows = []
    for pattern in matrix["patterns"]:
        layer_rows = []
        for layer, source_rows in sources.items():
            if layer == "direct_audio":
                videos = pattern["direct_recovered_video_count"]
                hits = pattern["direct_recovered_segment_hits"]
            elif layer == "alternate_source":
                videos = pattern["alternate_source_video_count"]
                hits = pattern["alternate_source_segment_hits"]
            else:
                videos = pattern["external_transcript_video_count"]
                hits = pattern["external_transcript_segment_hits"]
            layer_rows.append({
                "evidence_layer": layer,
                "source_video_count": len(source_rows),
                "matching_video_count": videos,
                "segment_hit_count": hits,
                "segment_hit_rate": round(hits / totals[layer], 6) if totals[layer] else 0,
                "video_coverage_rate": round(videos / len(source_rows), 6) if source_rows else 0,
            })
        all_hits = sum(item["segment_hit_count"] for item in layer_rows)
        flags = ["human_context_review_required"]
        if any(item["segment_hit_rate"] >= 0.10 for item in layer_rows):
            flags.append("broad_lexical_retrieval_density")
        if any(item["video_coverage_rate"] >= 0.75 for item in layer_rows):
            flags.append("high_candidate_video_coverage")
        rows.append({
            "pattern_id": pattern["pattern_id"],
            "category": pattern["category"],
            "matching_rule": pattern["matching_rule"],
            "candidate_form": pattern["candidate_form"],
            "total_segment_hit_count": all_hits,
            "layers": layer_rows,
            "risk_flags": flags,
            "status": "lexical_retrieval_audit_not_semantic_validation",
        })
    flagged = sum("broad_lexical_retrieval_density" in row["risk_flags"] for row in rows)
    payload = {
        "schema_version": "1.0",
        "status": "recovered_pattern_lexical_rule_audit",
        "pattern_count": len(rows),
        "source_segment_totals": totals,
        "broad_density_pattern_count": flagged,
        "patterns": rows,
        "claim_boundary": (
            "This audit measures lexical retrieval density only. A hit is not a "
            "semantic match, a speech function, a recurrence finding, a source "
            "identity decision, or evidence of effectiveness. Every card remains "
            "a contextual-review candidate."
        ),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    MD.write_text("\n".join([
        "# Recovered pattern lexical-rule audit",
        "",
        f"The 55 recovered-pattern rules produced a density audit; **{flagged}** rows are flagged for broad lexical retrieval density.",
        "",
        "Every row remains a contextual-review candidate. Hit counts do not measure semantic correctness or pattern quality.",
        "",
        "| Pattern | Total hits | Risk flags |",
        "|---|---:|---|",
        *[f"| `{row['pattern_id']}` | {row['total_segment_hit_count']} | {', '.join(row['risk_flags'])} |" for row in rows],
        "",
        "## Boundary",
        "",
        payload["claim_boundary"],
        "",
        "```bash",
        "python3 scripts/build_recovered_pattern_rule_audit.py",
        "```",
    ]) + "\n")
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "pattern_count": len(rows), "broad_density_pattern_count": flagged}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
