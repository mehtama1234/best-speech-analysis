#!/usr/bin/env python3
"""Derive five-pattern representative recurrence counts from packet records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAMES = [
    "contrast-or-disagreement",
    "example",
    "story",
    "uncertainty",
    "conclusion",
]
OUT_JSON = ROOT / "research/vertical-slice-01-cluster-recurrence.json"
OUT_MD = ROOT / "writeups/vertical-slice-01-cluster-recurrence.md"

INTERPRETATIONS = {
    "provisional-contrast_or_disagreement": (
        "The packet contains five selected representatives across four canonical "
        "video IDs; textual contrast and interpersonal disagreement remain distinct questions."
    ),
    "provisional-example": (
        "The packet contains five selected representatives across three canonical "
        "video IDs; one category list or case does not by itself establish evidence, "
        "explanation or listener understanding."
    ),
    "provisional-story_or_personal_experience": (
        "The packet contains five selected representatives across four canonical "
        "video IDs; the unavailable Parul Bansal source remains transcript-only for "
        "this packet and personal detail requires privacy and boundary review."
    ),
    "provisional-uncertainty_or_qualification": (
        "The packet contains five selected representatives across four canonical "
        "video IDs; a hedge, opinion marker or correction must be interpreted in "
        "surrounding context rather than treated as generic uncertainty."
    ),
    "provisional-conclusion_or_summary": (
        "The packet contains five selected representatives across five canonical "
        "video IDs; a marked takeaway may be a charge, transition or new claim "
        "rather than a summary."
    ),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict:
    media = json.loads((ROOT / "research/vertical-slice-01-media-audit.json").read_text())
    raw_ids = {
        occurrence["video_id"]
        for occurrence in media["occurrences"]
        if occurrence["raw_media_available"]
    }
    clusters = []
    representative_ids = set()
    for name in NAMES:
        packet = json.loads((ROOT / f"research/vertical-slice-01-{name}.json").read_text())
        representatives = packet.get("representative_examples", [])
        video_ids = {item["video_id"] for item in representatives}
        representative_ids.update(video_ids)
        clusters.append({
            "pattern_id": packet["pattern_id"],
            "representative_occurrence_count": len(representatives),
            "unique_video_id_count": len(video_ids),
            "representative_video_ids": sorted(video_ids),
            "representatives_with_raw_audio_video": sum(
                item["video_id"] in raw_ids for item in representatives
            ),
            "counterexample_occurrence_count": len(packet.get("counterexamples", [])),
            "interpretation": INTERPRETATIONS[packet["pattern_id"]],
        })
    report = {
        "schema_version": "1.0",
        "report_id": "vertical-slice-01-cluster-recurrence",
        "status": "provisional_cluster_recurrence_not_event_independent",
        "claim_boundary": "These counts summarize packet selections and source records. They do not independently validate labels, speaker identity, event independence or communication effects.",
        "packet_count": len(NAMES),
        "representative_occurrence_count": sum(
            cluster["representative_occurrence_count"] for cluster in clusters
        ),
        "unique_video_id_count_across_representatives": len(representative_ids),
        "unique_video_id_count_all_packet_occurrences": media["unique_video_ids"],
        "source_sha256": {
            **{
                f"research/vertical-slice-01-{name}.json": digest(
                    ROOT / f"research/vertical-slice-01-{name}.json"
                )
                for name in NAMES
            },
            "research/vertical-slice-01-media-audit.json": digest(
                ROOT / "research/vertical-slice-01-media-audit.json"
            ),
            "scripts/audit_vertical_slice_cluster_recurrence.py": digest(Path(__file__)),
        },
        "clusters": clusters,
        "next_actions": [
            "Verify speaker and event independence for each selected occurrence.",
            "Add event-level holdouts before treating cluster recurrence as general evidence.",
            "Have independent reviewers test whether the five cluster labels remain plausible.",
            "Keep representative counts separate from listener-outcome evidence.",
        ],
    }
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    rows = [
        "# Vertical slice 01: cluster recurrence",
        "",
        "This report counts the five pilot clusters at the packet-selection level. It",
        "does not prove that the labels are correct, that the events are independent or",
        "that a form improves audience outcomes.",
        "",
        "| Cluster | Representative occurrences | Unique video IDs | Representatives with raw audio/video | Counterexamples |",
        "|---|---:|---:|---:|---:|",
    ]
    short = {
        "provisional-contrast_or_disagreement": "Contrast/disagreement",
        "provisional-example": "Example",
        "provisional-story_or_personal_experience": "Story/personal experience",
        "provisional-uncertainty_or_qualification": "Uncertainty/qualification",
        "provisional-conclusion_or_summary": "Conclusion/summary",
    }
    for cluster in clusters:
        rows.append(
            f"| {short[cluster['pattern_id']]} | {cluster['representative_occurrence_count']} | "
            f"{cluster['unique_video_id_count']} | {cluster['representatives_with_raw_audio_video']} | "
            f"{cluster['counterexample_occurrence_count']} |"
        )
    rows += [
        "",
        f"Across the five packets there are {report['representative_occurrence_count']} representative occurrences spanning {report['unique_video_id_count_across_representatives']} unique canonical video IDs; all packet roles together span {report['unique_video_id_count_all_packet_occurrences']} IDs. The occurrence counts are not independent-event counts: some source IDs recur across packets, and the source/event audit does not yet verify speaker identity or event independence. The story packet includes the one source whose upload is unavailable, so its raw-media denominator is four of five.",
        "",
        "The report therefore supports a useful next question—whether these five",
        "higher-level jobs recur across speakers and settings—but not the conclusion",
        "that they are proven universal best practices.",
    ]
    OUT_MD.write_text("\n".join(rows) + "\n")
    print(
        f"cluster recurrence: {report['representative_occurrence_count']} representatives "
        f"across {report['unique_video_id_count_across_representatives']} IDs "
        f"({report['unique_video_id_count_all_packet_occurrences']} IDs across all packet roles)"
    )
    return report


if __name__ == "__main__":
    build()
