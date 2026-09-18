#!/usr/bin/env python3
"""Map free-text episode labels to a provisional shared job vocabulary.

The existing full-context reviews use useful but highly specific labels. This
builder creates a comparison aid without overwriting those labels. Every
mapping remains heuristic and must be independently reviewed before it can
support a recurrence or curriculum claim.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path


# Ordered from exclusions and narrow jobs to broader jobs. A label can receive
# only one primary job here; the original free-text label remains authoritative
# for discovery and later human adjudication.
RULES = [
    ("media_or_publisher", r"publisher|advert|promotion|music|media tail|edited preview|preview|channel framing|institutional close"),
    ("opening", r"opening|introduction|intro|welcome|arrival|self-introduction|format|agenda|origin prompt"),
    ("closing", r"closing|close|closure|farewell|ending|goodbye|outro|exit|final|culmination|blessing"),
    ("question", r"question|prompt|interviewer.*ask|asked|inquiry|challenge question"),
    ("answer_or_response", r"answer|response|reply|rebuttal|reaction|response"),
    ("story_or_personal_experience", r"story|anecdote|account|narrative|biograph|origin|encounter|journey|experience|memory|childhood|episode|scene|recollection|reminisc"),
    ("example_or_case", r"example|case|instance|illustrat|scenario|sample|household|neighbor|named examples"),
    ("contrast_or_disagreement", r"contrast|versus|\bvs\b|difference|reversal|then.?now|competing|opposition|disagreement|dispute|challenged|rejected|counterargument|tension"),
    ("correction_or_reframe", r"refram|redirect|correct|clarif|redefinition|category reversal|premise|frame shift|myth correction|question redefined"),
    ("repair_or_self_correction", r"repair|restart|apolog|self.?correction|withdrawal|disavow|interruption|retraction|mistake"),
    ("qualification_or_boundary", r"qualif|boundary|limit|condition|constraint|uncertainty|exception|hedg|caveat|scope|not.?a.?cure|incomplete"),
    ("definition_or_explanation", r"definition|define|explanation|explain|meaning|model|mechanism|procedure|process|taxonomy|how it works|reasoning|rationale"),
    ("transition_or_structure", r"transition|bridge|return|pivot|shift|sequence|roadmap|agenda|digression|frame|thread|chain|ladder"),
    ("callback_or_repetition", r"callback|revisit|repeated|refrain|echo|return.*theme|anchor|recurrence|reuses|repetition"),
    ("humor_or_rapport", r"humou?r|joke|funny|laugh|play|banter|rapport|warmth|self.?deprecat|light|teasing|belonging"),
    ("credit_or_acknowledgment", r"credit|thanks|gratitude|acknowledg|praise|recognition|roll call|support chain|dedication|appreciation"),
    ("call_to_action_or_audience_role", r"action|request|instruction|invitation|pledge|commitment|participation|assignment|audience.*role|audience.*action|concrete.*checklist|ask"),
    ("persuasion_or_advocacy", r"policy|argument|advocacy|critique|vision|demand|appeal|urgency|campaign|position|pledge|responsibility|public process"),
    ("reflection_or_value_frame", r"reflection|meaning|purpose|identity|value|moral|faith|belief|human value|lesson|takeaway|principle|philosoph|legacy"),
]


def classify(raw: str) -> tuple[str, str]:
    normalized = re.sub(r"[_-]+", " ", raw or "").strip().lower()
    if not normalized:
        return "unclassified", "empty_or_unlabeled_episode_function"
    for job, pattern in RULES:
        if re.search(pattern, normalized):
            return job, f"heuristic_keyword_rule:{job}"
    return "unclassified", "no_shared_job_rule_matched"


def build(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    source = json.loads((root / "research/corpus-lesson-index.json").read_text())
    labels: dict[str, dict] = {}
    entries = []
    job_counts: Counter[str] = Counter()
    video_counts: defaultdict[str, set[str]] = defaultdict(set)
    queue = []

    for entry in source["entries"]:
        mapped = []
        for item in entry["communication_function_inventory"]:
            raw = item.get("function", "")
            job, rule = classify(raw)
            label = labels.setdefault(raw, {"raw_label": raw, "canonical_job": job, "rule": rule, "occurrence_count": 0})
            # A raw label must map consistently; this assertion catches future
            # rule changes that would silently make the inventory unstable.
            if label["canonical_job"] != job:
                raise ValueError(f"inconsistent mapping for raw label: {raw!r}")
            label["occurrence_count"] += 1
            job_counts[job] += 1
            video_counts[job].add(entry["video_id"])
            record = {
                "sequence": item["sequence"],
                "raw_label": raw,
                "canonical_job": job,
                "mapping_rule": rule,
                "evidence_ids": item["evidence_ids"],
            }
            mapped.append(record)
            if job == "unclassified":
                queue.append({
                    "queue_item_id": f"{entry['review_id']}:{item['sequence']}",
                    "review_id": entry["review_id"],
                    "video_id": entry["video_id"],
                    "title": entry["title"],
                    **record,
                    "review_status": "queued_for_human_canonical_job_review",
                })
        entries.append({
            "review_id": entry["review_id"],
            "video_id": entry["video_id"],
            "title": entry["title"],
            "writeup": entry["writeup"],
            "functions": mapped,
        })

    for label in labels.values():
        label["review_status"] = "heuristic_mapping_requires_independent_review"

    return {
        "schema_version": "1.0",
        "taxonomy_id": "provisional-shared-communication-job-taxonomy",
        "status": "heuristic_canonicalization_not_independently_validated",
        "claim_boundary": (
            "Canonical jobs are keyword-based comparison aids applied to free-text "
            "episode labels. They do not replace the original label, establish "
            "speaker intent, recurrence, delivery effects, teachability or outcomes."
        ),
        "source": "research/corpus-lesson-index.json",
        "canonical_jobs": [job for job, _ in RULES] + ["unclassified"],
        "mapping_rules": [{"canonical_job": job, "pattern": pattern} for job, pattern in RULES],
        "summary": {
            "review_count": len(entries),
            "function_item_count": sum(job_counts.values()),
            "unique_raw_label_count": len(labels),
            "heuristically_mapped_item_count": sum(count for job, count in job_counts.items() if job != "unclassified"),
            "unclassified_item_count": job_counts["unclassified"],
            "unclassified_raw_label_count": sum(1 for item in labels.values() if item["canonical_job"] == "unclassified"),
            "canonical_job_counts": dict(job_counts.most_common()),
            "canonical_job_video_counts": {job: len(video_counts[job]) for job in job_counts},
        },
        "raw_label_mappings": sorted(labels.values(), key=lambda item: (item["canonical_job"], item["raw_label"])),
        "unclassified_review_queue": queue,
        "entries": entries,
    }


def write_outputs(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    result = build(root)
    (root / "research/corpus-function-taxonomy.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    summary = result["summary"]
    lines = [
        "# Provisional shared communication-job taxonomy", "",
        "Status: **heuristic canonicalization; not independently validated**.", "",
        "This layer maps free-text episode labels to a shared vocabulary for", 
        "comparison. It preserves every original label and does not establish", 
        "speaker intent, recurrence, delivery effects, teachability or outcomes.", "",
        f"- Reviews: {summary['review_count']}",
        f"- Function items: {summary['function_item_count']}",
        f"- Unique raw labels: {summary['unique_raw_label_count']}",
        f"- Heuristically mapped items: {summary['heuristically_mapped_item_count']}",
        f"- Unclassified items queued for human review: {summary['unclassified_item_count']}",
        "",
        "## Canonical-job counts", "",
        "| Canonical job | Items | Videos |", "|---|---:|---:|",
    ]
    for job, count in summary["canonical_job_counts"].items():
        lines.append(f"| `{job}` | {count} | {summary['canonical_job_video_counts'][job]} |")
    lines += ["", "The [JSON inventory](../research/corpus-function-taxonomy.json)",
              "contains every mapped item and the explicit unclassified queue."]
    (root / "writeups/corpus-function-taxonomy.md").write_text("\n".join(lines) + "\n")
    return result


if __name__ == "__main__":
    result = write_outputs()
    print(json.dumps(result["summary"], indent=2))
