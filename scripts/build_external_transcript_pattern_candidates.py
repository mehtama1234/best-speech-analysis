#!/usr/bin/env python3
"""Mine provisional pattern leads from externally hosted transcript candidates."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    rows = [json.loads(line) for line in (ROOT / "research/external-source-transcripts.jsonl").read_text().splitlines() if line.strip()]
    inventory = json.loads((ROOT / "research/exhaustive-pattern-inventory.json").read_text())
    patterns = []
    for theme in inventory["themes"]:
        rule = re.compile(theme["matching_rule"], re.IGNORECASE)
        examples = []
        for row in rows:
            hits = [s for s in row.get("segments", []) if rule.search(s.get("text", ""))]
            if hits:
                examples.append({"video_id": row["video_id"], "hit_count": len(hits), "excerpt": " ".join(h["text"] for h in hits[:2])[:400]})
        patterns.append({
            "theme_id": theme["theme_id"],
            "candidate_form": theme["candidate_form"],
            "external_video_count": len(examples),
            "external_segment_hit_count": sum(e["hit_count"] for e in examples),
            "examples": examples,
            "status": "external_transcript_candidate_not_human_reviewed",
        })
    payload = {
        "schema_version": "1.0",
        "status": "external_transcript_pattern_candidates_not_validated",
        "transcript_count": len(rows),
        "patterns": patterns,
        "claim_boundary": "External transcript regex hits are retrieval leads only; source identity, timestamp alignment, semantic interpretation, recurrence, delivery quality, learner evidence, listener outcomes, and effectiveness remain unverified.",
    }
    (ROOT / "research/external-transcript-pattern-candidates.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"transcript_count": len(rows), "themes_with_hits": sum(p["external_video_count"] > 0 for p in patterns)}))


if __name__ == "__main__":
    main()
