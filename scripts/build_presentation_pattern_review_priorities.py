#!/usr/bin/env python3
"""Build a non-promotional review-priority map for all 55 patterns."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/all-55-pattern-evidence.json"
OUT = ROOT / "research/presentation-pattern-review-priorities.json"
MD = ROOT / "writeups/presentation-pattern-review-priorities.md"


def main() -> int:
    rows = json.loads(SOURCE.read_text())["patterns"]
    priorities = []
    for row in rows:
        direct = row["direct_recovered_video_count"]
        flagged = row["direct_recovered_flagged_video_count"]
        pressure = (flagged / direct) if direct else 0.0
        if row["canonical_video_count"] <= 5 or (direct and pressure >= 0.95):
            tier = "first_review"
        elif row["canonical_video_count"] >= 100:
            tier = "broad_recurrence_review"
        else:
            tier = "standard_review"
        priorities.append({
            "pattern_id": row["pattern_id"],
            "category": row["category"],
            "tier": tier,
            "canonical_video_count": row["canonical_video_count"],
            "direct_recovered_video_count": direct,
            "direct_recovered_flagged_video_count": flagged,
            "direct_flagged_ratio": round(pressure, 4),
            "alternate_source_video_count": row["alternate_source_video_count"],
            "external_transcript_video_count": row["external_transcript_video_count"],
            "candidate_form": row["candidate_form"],
            "review_action": (
                "Check source identity, surrounding context and caption quality before using this candidate."
                if tier == "first_review" else
                "Sample across distinct speakers/events before treating the high canonical hit count as recurrence."
                if tier == "broad_recurrence_review" else
                "Review at least one distinct-source example and one counterexample before lesson use."
            ),
        })
    priorities.sort(key=lambda row: ({"first_review": 0, "broad_recurrence_review": 1, "standard_review": 2}[row["tier"]], -row["canonical_video_count"], row["pattern_id"]))
    report = {
        "schema_version": "1.0",
        "status": "presentation_pattern_review_priorities_not_effectiveness_ranking",
        "pattern_count": len(priorities),
        "priority_tier_counts": {tier: sum(row["tier"] == tier for row in priorities) for tier in ("first_review", "broad_recurrence_review", "standard_review")},
        "patterns": priorities,
        "claim_boundary": "This map prioritizes human review using canonical hit volume and recovery-layer quality flags. It is not an effectiveness ranking and does not rank pattern quality, speaker skill, learner value or listener outcomes.",
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Presentation-pattern review priorities",
        "",
        "Status: **review ordering aid; not an effectiveness ranking**.",
        "",
        report["claim_boundary"],
        "",
        f"Patterns: **{len(priorities)}** · first review: **{report['priority_tier_counts']['first_review']}** · broad recurrence review: **{report['priority_tier_counts']['broad_recurrence_review']}** · standard: **{report['priority_tier_counts']['standard_review']}**.",
        "",
        "| Tier | Pattern | Canonical videos | Direct recovered | Flagged direct | Flagged ratio | Review action |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in priorities:
        lines.append(f"| {row['tier']} | `{row['pattern_id']}` | {row['canonical_video_count']} | {row['direct_recovered_video_count']} | {row['direct_recovered_flagged_video_count']} | {row['direct_flagged_ratio']:.2f} | {row['review_action']} |")
    lines += ["", "Use this order with the [162-item priority review browser](recovered-pattern-priority-review.html). A tier is a workload decision, not a claim about what makes a great presentation.", ""]
    MD.write_text("\n".join(lines))
    print(json.dumps({"pattern_count": len(priorities), "priority_tier_counts": report["priority_tier_counts"], "promotion_eligible": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
