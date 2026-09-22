#!/usr/bin/env python3
"""Mine provisional pattern leads from locally recovered machine transcripts."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    transcript_path = ROOT / "research/recovered-audio-transcripts.jsonl"
    rows = [json.loads(line) for line in transcript_path.read_text().splitlines() if line.strip()]
    registry = {row["video_id"]: row for row in (json.loads(line) for line in (ROOT / "data/metadata/video-registry.jsonl").read_text().splitlines() if line.strip())}
    inventory = json.loads((ROOT / "research/exhaustive-pattern-inventory.json").read_text())
    patterns = []
    for theme in inventory["themes"]:
        rule = re.compile(theme["matching_rule"], re.IGNORECASE)
        examples = []
        for row in rows:
            if row.get("status") != "machine_transcript_candidate":
                continue
            hits = [segment for segment in row.get("segments", []) if rule.search(segment.get("text", ""))]
            if hits:
                examples.append({
                    "video_id": row["video_id"],
                    "title": registry.get(row["video_id"], {}).get("title"),
                    "language": row.get("language"),
                    "hit_count": len(hits),
                    "excerpt": " ".join(hit["text"] for hit in hits[:2])[:400],
                })
        patterns.append({
            "theme_id": theme["theme_id"],
            "candidate_form": theme["candidate_form"],
            "matching_rule": theme["matching_rule"],
            "recovered_video_count": len(examples),
            "recovered_segment_hit_count": sum(e["hit_count"] for e in examples),
            "examples": examples[:12],
            "status": "machine_transcript_candidate_not_human_reviewed",
        })
    payload = {
        "schema_version": "1.0",
        "status": "recovered_audio_pattern_candidates_not_validated",
        "transcript_count": sum(row.get("status") == "machine_transcript_candidate" for row in rows),
        "patterns": patterns,
        "claim_boundary": "Regex hits in machine transcripts are retrieval leads only; they do not establish semantic meaning, recurrence, delivery quality, speaker intent, learner evidence, listener outcomes, or effectiveness.",
    }
    out = ROOT / "research/recovered-audio-pattern-candidates.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    active = [p for p in patterns if p["recovered_video_count"]]
    lines = [
        "# Recovered audio pattern candidates",
        "",
        "Status: `machine_transcript_candidate_not_human_reviewed`. These are provisional retrieval leads from recovered audio, not canonical findings.",
        "",
        f"- Machine transcript candidates mined: {payload['transcript_count']}",
        f"- Themes with at least one regex hit: {len(active)} / {len(patterns)}",
        "",
    ]
    for pattern in active:
        lines += [f"## {pattern['theme_id']}", "", f"Form: {pattern['candidate_form']}", "", f"Candidate coverage: {pattern['recovered_video_count']} videos; {pattern['recovered_segment_hit_count']} hits.", ""]
        lines.extend(f"- `{e['video_id']}` — {e['excerpt']}" for e in pattern["examples"][:3])
        lines.append("")
    (ROOT / "writeups/recovered-audio-pattern-candidates.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"transcript_count": payload["transcript_count"], "themes_with_hits": len(active)}))


if __name__ == "__main__":
    main()
