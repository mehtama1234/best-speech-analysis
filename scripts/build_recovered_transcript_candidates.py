#!/usr/bin/env python3
"""Build an auditable provisional pattern layer from recovered alternate-language captions."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "data/transcript-recovery"
INVENTORY = ROOT / "research/exhaustive-pattern-inventory.json"
REVIEWS_OUT = ROOT / "research/recovered-transcript-review-candidates.json"
PATTERNS_OUT = ROOT / "research/recovered-transcript-pattern-candidates.json"
REPORT_OUT = ROOT / "writeups/recovered-transcript-pattern-candidates.md"
REGISTRY = ROOT / "data/metadata/video-registry.jsonl"


def registry() -> dict[str, dict]:
    return {row["video_id"]: row for row in (json.loads(line) for line in REGISTRY.read_text().splitlines() if line.strip())}


def candidate_files() -> list[Path]:
    latest: dict[str, Path] = {}
    for path in CANDIDATE_DIR.glob("*-hi-*.json"):
        video_id = path.name.split("-hi-", 1)[0]
        if video_id not in latest or path.stat().st_mtime > latest[video_id].stat().st_mtime:
            latest[video_id] = path
    return sorted(latest.values(), key=lambda path: path.name)


def load_reviews() -> list[dict]:
    meta = registry()
    rows = []
    for path in candidate_files():
        payload = json.loads(path.read_text())
        segments = payload.get("transcript", [])
        video_id = payload["video_id"]
        rows.append({
            "review_id": "recovered-transcript-candidate-" + video_id,
            "video_id": video_id,
            "title": meta.get(video_id, {}).get("title"),
            "source_url": "https://www.youtube.com/watch?v=" + video_id,
            "source_transcript_file": str(path.relative_to(ROOT)),
            "requested_language": payload.get("requested_language"),
            "provider_language": payload.get("provider_language"),
            "segment_count": len(segments),
            "caption_count": len(segments),
            "review_status": "recovered_timestamped_candidate_not_contextually_reviewed",
            "translation_status": payload.get("translation_status", "not_independently_verified"),
            "segments": [
                {
                    "sequence": index,
                    "start_seconds": round(float(row["startMs"]) / 1000, 3),
                    "end_seconds": round(float(row["endMs"]) / 1000, 3),
                    "text": str(row["text"]).strip(),
                    "evidence_id": f"{video_id}:recovered:{index:05d}",
                }
                for index, row in enumerate(segments)
                if str(row.get("text", "")).strip()
            ],
        })
    return rows


def mine(reviews: list[dict]) -> list[dict]:
    inventory = json.loads(INVENTORY.read_text())
    patterns = []
    for theme in inventory["themes"]:
        rule = re.compile(theme["matching_rule"], re.IGNORECASE)
        examples = []
        for review in reviews:
            hits = [segment for segment in review["segments"] if rule.search(segment["text"])]
            if hits:
                examples.append({
                    "review_id": review["review_id"],
                    "video_id": review["video_id"],
                    "title": review["title"],
                    "language": review["provider_language"],
                    "hit_count": len(hits),
                    "evidence_ids": [hit["evidence_id"] for hit in hits[:5]],
                    "excerpt": " ".join(hit["text"] for hit in hits[:2]),
                })
        patterns.append({
            "theme_id": theme["theme_id"],
            "candidate_form": theme["candidate_form"],
            "matching_rule": theme["matching_rule"],
            "recovered_video_count": len(examples),
            "recovered_segment_hit_count": sum(row["hit_count"] for row in examples),
            "examples": examples[:12],
            "status": "recovered_language_candidate_not_contextually_reviewed",
        })
    return patterns


def render(reviews: list[dict], patterns: list[dict]) -> str:
    active = [row for row in patterns if row["recovered_video_count"]]
    lines = [
        "# Recovered transcript pattern candidates",
        "",
        "Status: `recovered_language_candidate_not_contextually_reviewed`; alternate-language recovery candidates, not canonical full-context reviews.",
        "",
        "This report preserves recovered timestamped transcript candidates from the 85-item corpus gap. The provider supplied alternate-language caption tracks, primarily Hindi. The original provider responses are preserved, the requested language is explicit, and no row is promoted into the canonical review corpus.",
        "",
        f"- Recovered candidate videos: {len(reviews)}",
        f"- Candidate pattern themes with at least one hit: {len(active)} / {len(patterns)}",
        f"- Candidate caption rows: {sum(row['caption_count'] for row in reviews)}",
        "",
        "## Pattern candidates",
        "",
    ]
    for row in active:
        lines += [
            f"### {row['theme_id']}",
            "",
            f"Form: {row['candidate_form']}",
            "",
            f"Recovered candidate coverage: {row['recovered_video_count']} videos; {row['recovered_segment_hit_count']} caption hits.",
            "",
        ]
        for example in row["examples"][:3]:
            lines.append(f"- {example['video_id']} / {example['language']} / {example['evidence_ids'][0]} — {example['excerpt'][:240]}")
        lines.append("")
    lines += [
        "## Boundary",
        "",
        "These are retrieval leads from recovered captions. They are not independent full-context readings, verified translations, speaker-intent findings, recurrence evidence, delivery evidence, learner evidence, listener outcomes or effectiveness claims.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    reviews = load_reviews()
    patterns = mine(reviews)
    REVIEWS_OUT.write_text(json.dumps({"schema_version": "1.0", "status": "recovered_candidates_not_canonical_reviews", "reviews": reviews}, ensure_ascii=False, indent=2) + "\n")
    PATTERNS_OUT.write_text(json.dumps({"schema_version": "1.0", "status": "recovered_language_pattern_candidates_not_validated", "review_count": len(reviews), "patterns": patterns}, ensure_ascii=False, indent=2) + "\n")
    REPORT_OUT.write_text(render(reviews, patterns))
    print(json.dumps({"recovered_reviews": len(reviews), "caption_rows": sum(row["caption_count"] for row in reviews), "patterns_with_hits": sum(bool(row["recovered_video_count"]) for row in patterns)}))
