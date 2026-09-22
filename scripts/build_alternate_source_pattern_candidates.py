#!/usr/bin/env python3
"""Mine provisional pattern leads from alternate-source machine transcripts."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    rows = [json.loads(line) for line in (ROOT / "research/alternate-source-transcripts.jsonl").read_text().splitlines() if line.strip()]
    inventory = json.loads((ROOT / "research/exhaustive-pattern-inventory.json").read_text())
    patterns = []
    for theme in inventory["themes"]:
        rule = re.compile(theme["matching_rule"], re.IGNORECASE)
        examples = []
        for row in rows:
            hits = [s for s in row.get("segments", []) if rule.search(s.get("text", ""))]
            if hits:
                examples.append({
                    "original_video_id": row["original_video_id"],
                    "candidate_video_id": row["candidate_video_id"],
                    "hit_count": len(hits),
                    "excerpt": " ".join(h["text"] for h in hits[:2])[:400],
                })
        patterns.append({
            "theme_id": theme["theme_id"],
            "candidate_form": theme["candidate_form"],
            "recovered_video_count": len(examples),
            "recovered_segment_hit_count": sum(e["hit_count"] for e in examples),
            "examples": examples[:12],
            "status": "alternate_source_machine_candidate_not_identity_verified",
        })
    payload = {
        "schema_version": "1.0",
        "status": "alternate_source_pattern_candidates_not_validated",
        "transcript_count": len(rows),
        "patterns": patterns,
        "claim_boundary": "These regex hits are retrieval leads from alternate-source machine transcripts. They do not prove source identity, semantic interpretation, recurrence, delivery quality, learner evidence, listener outcomes, or effectiveness.",
    }
    (ROOT / "research/alternate-source-pattern-candidates.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"transcript_count": len(rows), "themes_with_hits": sum(p["recovered_video_count"] > 0 for p in patterns)}))


if __name__ == "__main__":
    main()
