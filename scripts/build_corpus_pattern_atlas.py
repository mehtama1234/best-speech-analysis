#!/usr/bin/env python3
"""Build a corpus-wide, explicitly provisional pattern and phrase atlas.

This is a retrieval and coverage artifact.  It does not promote heuristic
labels to reviewed findings.  Each phrase occurrence remains linked to its
caption evidence ID and keeps the transcript-only boundary visible.
"""

from __future__ import annotations

import json
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path

if __package__:
    from .source_restrictions import load_restrictions
else:
    from source_restrictions import load_restrictions


PHRASE_FORMS = {
    "contrast_or_disagreement": [
        r"\bbut\b", r"\bhowever\b", r"\binstead\b", r"\brather than\b",
        r"\bon the other hand\b", r"\bused to\b", r"\bnow I\b",
    ],
    "example": [r"\bfor example\b", r"\bfor instance\b", r"\bsuch as\b", r"\bone example\b"],
    "story_or_personal_experience": [
        r"\bwhen I\b", r"\bI remember\b", r"\byears ago\b", r"\bone day\b",
        r"\bI was\b", r"\bmy first\b", r"\bgrowing up\b",
    ],
    "uncertainty_or_qualification": [
        r"\bmaybe\b", r"\bperhaps\b", r"\bI think\b", r"\bI'm not sure\b",
        r"\bit depends\b", r"\bto some extent\b", r"\bnot necessarily\b",
    ],
    "conclusion_or_summary": [
        r"\bthe point is\b", r"\bwhat matters\b", r"\bin conclusion\b",
        r"\bultimately\b", r"\bin short\b", r"\bso the\b", r"\bthe lesson\b",
    ],
    "question": [r"\bwhy\b", r"\bhow\b", r"\bwhat if\b", r"\bcan we\b", r"\?"],
    "definition": [
        r"\bin other words\b", r"\bmeans that\b", r"\bdefined as\b",
        r"\bis when\b", r"\bwhat I mean\b", r"\bthe definition\b",
    ],
    "call_to_action": [
        r"\bwe need to\b", r"\byou can\b", r"\blet's\b", r"\bdo not\b",
        r"\bdon't\b", r"\bjoin us\b", r"\btake action\b",
    ],
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u2019", "'")).strip()


def phrase_hits(text: str, patterns: list[str]) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text, re.I)]


def event_split(video_id: str) -> str:
    """Assign a video to a stable, event-level 80/20 split."""
    bucket = int(hashlib.sha256(video_id.encode("utf-8")).hexdigest()[:2], 16)
    return "holdout" if bucket < 51 else "train"


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    restrictions = load_restrictions(root)
    registry_path = root / "research/segment-registry.jsonl"
    cards = json.loads((root / "research/reviewed-pattern-cards.json").read_text())["cards"]
    reviewed_by_video: dict[str, Counter] = defaultdict(Counter)
    reviewed_evidence: set[str] = set()
    for card in cards:
        evidence_id = card.get("evidence_id")
        if not evidence_id:
            continue
        video_id = evidence_id.split(":", 1)[0]
        reviewed_by_video[video_id][card.get("reviewed_speech_function", "unclassified")] += 1
        reviewed_evidence.add(evidence_id)

    videos: dict[str, dict] = {}
    global_candidates: dict[str, list[dict]] = defaultdict(list)
    global_segment_counts: Counter = Counter()
    global_form_counts: Counter = Counter()
    global_video_ids: dict[str, set[str]] = defaultdict(set)
    global_reviewed_segment_counts: Counter = Counter()
    global_function_segment_counts: Counter = Counter()
    global_function_video_ids: dict[str, set[str]] = defaultdict(set)
    global_reviewed_function_counts: Counter = Counter()
    function_first_candidate: dict[str, dict[str, dict]] = defaultdict(dict)
    per_video_first_candidate: dict[str, dict[str, dict]] = defaultdict(dict)
    split_stats: dict[str, dict[str, dict]] = defaultdict(
        lambda: {
            "train": {"video_ids": set(), "segment_hit_count": 0, "reviewed_segment_hit_count": 0, "form_hit_counts": Counter()},
            "holdout": {"video_ids": set(), "segment_hit_count": 0, "reviewed_segment_hit_count": 0, "form_hit_counts": Counter()},
        }
    )
    excluded_segments = Counter()
    total_segments = 0
    for line in registry_path.open():
        row = json.loads(line)
        video_id = row["video_id"]
        if video_id in restrictions:
            excluded_segments[video_id] += 1
            continue
        total_segments += 1
        video = videos.setdefault(video_id, {
            "video_id": video_id,
            "title": row.get("title"),
            "video_url": row.get("video_url"),
            "channel": row.get("channel"),
            "event_split": event_split(video_id),
            "transcript_evidence_status": "full_retained_transcript_reviewed",
            "segment_count": 0,
            "candidate_function_counts": Counter(),
            "phrase_candidates": defaultdict(list),
            "reviewed_annotation_count": sum(reviewed_by_video[video_id].values()),
            "reviewed_functions": dict(reviewed_by_video[video_id]),
            "phrase_segment_counts": Counter(),
            "phrase_form_counts": defaultdict(Counter),
        })
        video["segment_count"] += 1
        for label in row.get("candidate_speech_functions", []):
            video["candidate_function_counts"][label] += 1
            global_function_segment_counts[label] += 1
            global_function_video_ids[label].add(video_id)
            if row["evidence_id"] in reviewed_evidence:
                global_reviewed_function_counts[label] += 1
            if label != "unclassified":
                function_first_candidate[label].setdefault(video_id, {
                    "evidence_id": row["evidence_id"],
                    "video_id": video_id,
                    "title": row.get("title"),
                    "start_seconds": row.get("start_seconds"),
                    "end_seconds": row.get("end_seconds"),
                    "text": normalize(row.get("text", "")),
                    "event_split": event_split(video_id),
                    "reviewed_evidence": row["evidence_id"] in reviewed_evidence,
                })
        text = normalize(row.get("text", ""))
        if not text:
            continue
        for label, patterns in PHRASE_FORMS.items():
            hits = phrase_hits(text, patterns)
            if not hits:
                continue
            global_segment_counts[label] += 1
            global_video_ids[label].add(video_id)
            split = video["event_split"]
            split_stats[label][split]["video_ids"].add(video_id)
            split_stats[label][split]["segment_hit_count"] += 1
            if row["evidence_id"] in reviewed_evidence:
                global_reviewed_segment_counts[label] += 1
                split_stats[label][split]["reviewed_segment_hit_count"] += 1
            video["phrase_segment_counts"][label] += 1
            for form in hits:
                global_form_counts[(label, form)] += 1
                split_stats[label][split]["form_hit_counts"][form] += 1
                video["phrase_form_counts"][label][form] += 1
            item = {
                "evidence_id": row["evidence_id"],
                "start_seconds": row["start_seconds"],
                "end_seconds": row["end_seconds"],
                "text": text,
                "matched_forms": hits,
                "candidate_label_status": "heuristic_phrase_retrieval_aid",
                "reviewed_evidence": row["evidence_id"] in reviewed_evidence,
            }
            per_video_first_candidate[label].setdefault(video_id, {
                **item,
                "video_id": video_id,
                "title": row.get("title"),
                "event_split": split,
            })
            # Keep a bounded, deterministic sample per video and globally.
            if len(video["phrase_candidates"][label]) < 8:
                video["phrase_candidates"][label].append(item)
            if len(global_candidates[label]) < 40:
                global_candidates[label].append({**item, "video_id": video_id, "title": row.get("title")})

    serialized_videos = []
    for video in sorted(videos.values(), key=lambda item: (item["title"] or "", item["video_id"])):
        serialized_videos.append({
            **video,
            "candidate_function_counts": dict(sorted(video["candidate_function_counts"].items())),
            "phrase_candidates": {k: v for k, v in sorted(video["phrase_candidates"].items())},
            "phrase_segment_counts": dict(sorted(video["phrase_segment_counts"].items())),
            "phrase_form_counts": {
                label: dict(sorted(counts.items()))
                for label, counts in sorted(video["phrase_form_counts"].items())
            },
        })
    global_summary = {}
    recurrence_review_queue = []
    for label, patterns in PHRASE_FORMS.items():
        stratified_candidates = []
        for split in ("train", "holdout"):
            candidates = sorted(
                (item for item in per_video_first_candidate[label].values() if item["event_split"] == split),
                key=lambda item: (item["video_id"], item["evidence_id"]),
            )
            stratified_candidates.extend(candidates[:12])
        for item in stratified_candidates:
            recurrence_review_queue.append({
                "queue_item_id": f"{label}:{item['evidence_id']}",
                "phrase_family": label,
                **item,
                "review_status": "queued_for_manual_recurrence_review",
                "required_checks": [
                    "confirm phrase in full surrounding context",
                    "assign primary speech function without relying on phrase form",
                    "record alternate function or non-fit if present",
                    "verify speaker/event identity and duplicate status",
                    "add delivery evidence only when source media is available",
                ],
            })
        global_summary[label] = {
            "phrase_forms": patterns,
            "status": "heuristic_retrieval_aid_requires_manual_review",
            "segment_hit_count": global_segment_counts[label],
            "video_hit_count": len(global_video_ids[label]),
            "reviewed_segment_hit_count": global_reviewed_segment_counts[label],
            "form_hit_counts": {
                form: global_form_counts[(label, form)] for form in patterns
            },
            "event_level_holdout": {
                split: {
                    "video_hit_count": len(split_stats[label][split]["video_ids"]),
                    "segment_hit_count": split_stats[label][split]["segment_hit_count"],
                    "reviewed_segment_hit_count": split_stats[label][split]["reviewed_segment_hit_count"],
                    "form_hit_counts": {
                        form: split_stats[label][split]["form_hit_counts"][form]
                        for form in patterns
                    },
                }
                for split in ("train", "holdout")
            },
            "sample_occurrences": global_candidates[label],
            "stratified_review_queue_item_count": len(stratified_candidates),
        }
    function_review_queue = []
    for label in sorted(function_first_candidate):
        candidates = []
        for split in ("train", "holdout"):
            candidates.extend(sorted(
                (item for item in function_first_candidate[label].values() if item["event_split"] == split),
                key=lambda item: (item["video_id"], item["evidence_id"]),
            )[:12])
        for item in candidates:
            function_review_queue.append({
                "queue_item_id": f"function:{label}:{item['evidence_id']}",
                "candidate_function": label,
                **item,
                "review_status": "queued_for_manual_function_review",
                "required_checks": [
                    "read surrounding context",
                    "assign primary speech function independently of the candidate label",
                    "record alternate function or indeterminate status",
                    "verify speaker/event identity and duplicate status",
                ],
            })
    output = {
        "schema_version": "0.1",
        "generated_from": "research/segment-registry.jsonl",
        "scope": (
            "Corpus-wide transcript retrieval atlas for exact phrase forms and "
            "candidate speech functions. Full retained-transcript coverage is "
            "not audiovisual review, causal evidence, or independent semantic validation."
        ),
        "transcript_boundary": "transcript_only",
        "event_level_split": {
            "method": "sha256(video_id) first byte; bucket < 51 is holdout",
            "purpose": "prevent caption-level leakage when selecting recurrence candidates for later review",
            "train_video_count": sum(event_split(video["video_id"]) == "train" for video in serialized_videos),
            "holdout_video_count": sum(event_split(video["video_id"]) == "holdout" for video in serialized_videos),
        },
        "eligible_video_count": len(serialized_videos),
        "eligible_segment_count": total_segments,
        "reviewed_annotation_video_count": sum(bool(v["reviewed_annotation_count"]) for v in serialized_videos),
        "reviewed_evidence_count": len(reviewed_evidence),
        "phrase_forms": global_summary,
        "candidate_function_summary": {
            label: {
                "status": "heuristic_candidate_label_requires_manual_review",
                "segment_hit_count": global_function_segment_counts[label],
                "video_hit_count": len(global_function_video_ids[label]),
                "reviewed_segment_hit_count": global_reviewed_function_counts[label],
                "stratified_review_queue_item_count": len([item for item in function_review_queue if item["candidate_function"] == label]),
            }
            for label in sorted(global_function_segment_counts)
        },
        "candidate_function_review_queue": {
            "policy": "one earliest retained candidate segment per video, up to 12 train and 12 holdout videos per non-unclassified function; sorted by video ID",
            "item_count": len(function_review_queue),
            "items": function_review_queue,
        },
        "recurrence_review_queue": {
            "policy": "one earliest retained hit per video, up to 12 train and 12 holdout videos per phrase family; sorted by video ID for deterministic selection",
            "item_count": len(recurrence_review_queue),
            "items": recurrence_review_queue,
        },
        "recurrence_review_workbook": "research/corpus-recurrence-independent-review-workbook.json",
        "videos": serialized_videos,
        "excluded_source_segments": dict(sorted(excluded_segments.items())),
        "source_restrictions": restrictions,
    }
    out = root / "research/corpus-pattern-atlas.json"
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    md = root / "writeups/corpus-pattern-atlas.md"
    lines = [
        "# Corpus pattern atlas",
        "",
        "This is a transcript retrieval and coverage artifact, not a set of validated universal rules.",
        "",
        f"- Eligible videos: **{len(serialized_videos)}**",
        f"- Eligible caption segments: **{total_segments}**",
        f"- Videos with prior contextual/manual annotations: **{output['reviewed_annotation_video_count']}**",
        f"- Exact evidence IDs in prior reviewed cards: **{len(reviewed_evidence)}**",
        "- Boundary: transcript-only; phrase hits and candidate labels require manual review.",
        "- Counts below are retrieval denominators (caption-segment and video hits), not validated speech-function or effectiveness findings.",
        "- The train/holdout counts use a stable video-level split; they are not a statistical performance evaluation.",
        "- The recurrence-review queue is stratified by phrase family and event split; queued items still require contextual, audiovisual and independent review.",
        "",
        "## Phrase-form families",
        "",
    ]
    for label, info in global_summary.items():
        lines.append(
            f"- `{label}` — **{info['video_hit_count']}** videos / "
            f"**{info['segment_hit_count']}** caption segments; "
            f"event holdout **{info['event_level_holdout']['holdout']['video_hit_count']}** videos / "
            f"**{info['event_level_holdout']['holdout']['segment_hit_count']}** segments; "
            + ", ".join(
                f"`{p}` ({info['form_hit_counts'][p]})"
                for p in info["phrase_forms"]
            )
        )
    lines += ["", "## Candidate speech-function inventory", "", "These labels are transcript retrieval aids, not validated semantic annotations.", ""]
    for label, info in output["candidate_function_summary"].items():
        lines.append(f"- `{label}` — **{info['video_hit_count']}** videos / **{info['segment_hit_count']}** segments; reviewed segments: **{info['reviewed_segment_hit_count']}**")
    lines += ["", f"The candidate-function review queue contains **{len(function_review_queue)}** stratified intervals for non-`unclassified` labels (up to 12 train and 12 holdout videos per label)."]
    lines += [
        "",
        "## How to use this atlas",
        "",
        "Use the JSON to select cross-speaker, cross-event samples for manual review. Preserve the exact evidence ID and timestamp, inspect surrounding context, then add audiovisual evidence, counterexamples, and practice only after the candidate survives review.",
        "",
        "A phrase hit is not proof that the speaker performed the associated function; the same words can serve different jobs.",
        "",
        f"The generated recurrence-review queue contains **{len(recurrence_review_queue)}** balanced candidate intervals (up to 12 train and 12 holdout videos per phrase family).",
        "",
    ]
    md.write_text("\n".join(lines))
    print(json.dumps({
        "output": str(out),
        "markdown": str(md),
        "eligible_videos": len(serialized_videos),
        "eligible_segments": total_segments,
        "reviewed_evidence": len(reviewed_evidence),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
