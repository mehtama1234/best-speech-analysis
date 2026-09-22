#!/usr/bin/env python3
"""Audit structural quality of recovered transcript candidates.

This is deliberately a structural audit.  It does not decide whether a
machine transcript is semantically correct, whether an alternate upload is
the same event, or whether a detected phrase is a valid speaking pattern.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "research/recovered-transcript-quality-audit.json"
MARKDOWN = ROOT / "writeups/recovered-transcript-quality-audit.md"

INPUTS = (
    (ROOT / "research/recovered-audio-transcripts.jsonl", "direct_audio"),
    (ROOT / "research/alternate-source-transcripts.jsonl", "alternate_source"),
    (ROOT / "research/external-source-transcripts.jsonl", "external_transcript"),
)

BOILERPLATE = (
    "subscribe",
    "visit our site",
    "links in the description",
    "thanks for your support",
    "englishspeechchannel",
)


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


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)?", text.lower())


def audit_row(row: dict) -> dict:
    segments = row.get("segments") or []
    text = str(row.get("text") or "")
    starts_ends = []
    malformed = 0
    for segment in segments:
        try:
            start = float(segment["start"])
            end = float(segment.get("end", start))
            if start < 0 or end < start:
                malformed += 1
            starts_ends.append((start, end))
        except (KeyError, TypeError, ValueError):
            malformed += 1

    overlaps = sum(
        1 for previous, current in zip(starts_ends, starts_ends[1:])
        if current[0] < previous[1]
    )
    nonmonotonic = sum(
        1 for previous, current in zip(starts_ends, starts_ends[1:])
        if current[0] < previous[0]
    )
    consecutive_duplicates = sum(
        1
        for previous, current in zip(segments, segments[1:])
        if str(previous.get("text", "")).strip().lower()
        == str(current.get("text", "")).strip().lower()
        and str(current.get("text", "")).strip()
    )
    lowered = text.lower()
    boilerplate_hits = sorted({phrase for phrase in BOILERPLATE if phrase in lowered})
    timestamped = bool(segments) and len(starts_ends) == len(segments)
    duration = starts_ends[-1][1] if starts_ends else None
    word_count = len(words(text))
    flags = []
    if not segments or word_count == 0:
        flags.append("empty_transcript")
    if not timestamped:
        flags.append("missing_or_malformed_timestamps")
    if overlaps:
        flags.append("overlapping_segments")
    if nonmonotonic:
        flags.append("nonmonotonic_timestamps")
    if consecutive_duplicates:
        flags.append("consecutive_duplicate_segments")
    if boilerplate_hits:
        flags.append("publisher_boilerplate_detected")
    if row["evidence_layer"] == "alternate_source":
        flags.append("source_identity_not_verified")
    if row["evidence_layer"] == "external_transcript":
        flags.append("external_transcript_candidate")

    if row["evidence_layer"] == "external_transcript":
        disposition = "external_candidate_not_timestamped"
    elif not segments or word_count == 0:
        disposition = "not_usable_for_pattern_discovery"
    elif flags:
        disposition = "machine_candidate_with_quality_flags"
    else:
        disposition = "machine_candidate_structurally_consistent"

    return {
        "video_id": row.get("video_id") or row.get("original_video_id"),
        "candidate_video_id": row.get("candidate_video_id"),
        "evidence_layer": row["evidence_layer"],
        "status": row.get("status"),
        "review_status": row.get("review_status"),
        "model": row.get("model"),
        "segment_count": len(segments),
        "word_count": word_count,
        "duration_seconds": duration,
        "timestamped_segment_count": len(starts_ends),
        "malformed_segment_count": malformed,
        "overlap_count": overlaps,
        "nonmonotonic_timestamp_count": nonmonotonic,
        "consecutive_duplicate_count": consecutive_duplicates,
        "publisher_boilerplate_hits": boilerplate_hits,
        "flags": flags,
        "disposition": disposition,
    }


def build() -> dict:
    rows = [row for path, layer in INPUTS for row in read_jsonl(path, layer)]
    audited = [audit_row(row) for row in rows]
    by_layer = Counter(row["evidence_layer"] for row in audited)
    by_disposition = Counter(row["disposition"] for row in audited)
    flag_counts = Counter(flag for row in audited for flag in row["flags"])
    result = {
        "schema_version": "1.0",
        "status": "recovered_transcript_structural_quality_audit",
        "source_files": [str(path.relative_to(ROOT)) for path, _ in INPUTS],
        "candidate_count": len(audited),
        "counts_by_evidence_layer": dict(sorted(by_layer.items())),
        "counts_by_disposition": dict(sorted(by_disposition.items())),
        "flag_counts": dict(sorted(flag_counts.items())),
        "rows": sorted(audited, key=lambda row: (row["evidence_layer"], row["video_id"] or "")),
        "claim_boundary": (
            "This audit checks transcript structure and obvious contamination only. "
            "It does not establish semantic accuracy, source identity, speaker identity, "
            "human review, recurrence, delivery meaning, or effectiveness."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    lines = [
        "# Recovered transcript quality audit",
        "",
        "This report audits structural properties of recovered transcript candidates.",
        "It is not a semantic or effectiveness validation report.",
        "",
        f"- Candidate rows: **{len(audited)}**",
        f"- Evidence layers: **{dict(sorted(by_layer.items()))}**",
        f"- Dispositions: **{dict(sorted(by_disposition.items()))}**",
        "",
        "## What this establishes",
        "",
        "The report checks timestamp shape, ordering, overlaps, duplicate segments, "
        "empty text and obvious publisher boilerplate. Direct and alternate rows "
        "remain machine-transcript candidates; alternate-source identity is not "
        "promoted by structural cleanliness.",
        "",
        "## Boundary",
        "",
        result["claim_boundary"],
        "",
        "## Reproducibility",
        "",
        "```bash",
        "python3 scripts/build_recovered_transcript_quality_audit.py",
        "```",
    ]
    MARKDOWN.write_text("\n".join(lines) + "\n")
    return result


if __name__ == "__main__":
    result = build()
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "markdown_output": str(MARKDOWN.relative_to(ROOT)),
        "candidate_count": result["candidate_count"],
        "counts_by_disposition": result["counts_by_disposition"],
        "flag_counts": result["flag_counts"],
    }, indent=2))
