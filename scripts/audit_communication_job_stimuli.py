#!/usr/bin/env python3
"""Run bounded automated checks on draft listener stimulus pairs."""

from __future__ import annotations

import json
import re
from pathlib import Path


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "before", "but", "by", "can", "could", "does", "for", "from", "if", "in", "is", "it", "its", "may", "more", "not", "of", "on", "one", "or", "should", "that", "the", "their", "them", "there", "this", "to", "we", "what", "when", "who", "will", "with", "you", "your",
}

TARGET_MARKERS = {
    "opening": ["explain", "why", "where"],
    "closing": ["takeaway", "simple", "if you can"],
    "question": ["which", "?", "ask"],
    "answer_or_response": ["short answer", "useful question", "if it is not"],
    "story_or_personal_experience": ["during one", "missed", "event illustrates"],
    "example_or_case": ["for example", "case illustrates"],
    "contrast_or_disagreement": ["expected", "but", "change explains"],
    "correction_or_reframe": ["more useful question", "before we treat"],
    "repair_or_self_correction": ["sorry", "i mean"],
    "qualification_or_boundary": ["suggest", "may", "sample is small"],
    "definition_or_explanation": ["by a", "i mean", "not simply"],
    "transition_or_structure": ["now we can move", "choice it creates"],
    "callback_or_repetition": ["at the start", "return to", "safety check"],
    "humor_or_rapport": ["stage manager", "fire exit"],
    "credit_or_acknowledgment": ["collected", "checked", "their work"],
    "call_to_action_or_audience_role": ["if you need", "request", "coordinator"],
    "persuasion_or_advocacy": ["pilot", "measure", "revise or stop"],
    "reflection_or_value_frame": ["value", "interpretations", "alongside"],
}


def tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z]+", text.lower()) if token not in STOPWORDS and len(token) > 2}


def audit_record(record: dict) -> dict:
    control = tokens(record["control_text"])
    pattern = tokens(record["pattern_informed_text"])
    union = control | pattern
    overlap = control & pattern
    job = record["canonical_job"]
    lowered = record["pattern_informed_text"].lower()
    markers = TARGET_MARKERS[job]
    marker_hits = [marker for marker in markers if marker in lowered]
    safety_text = f"{record['control_text']} {record['pattern_informed_text']}".lower()
    safety_flags = []
    for term in ("suicide", "self-harm", "private medical", "identifiable patient", "trauma", "force", "must disclose"):
        if term in safety_text:
            safety_flags.append(term)
    return {
        "stimulus_id": record["stimulus_id"],
        "canonical_job": job,
        "word_count_delta": record["word_count_delta"],
        "non_stopword_jaccard": round(len(overlap) / len(union), 3) if union else 0.0,
        "shared_content_token_count": len(overlap),
        "control_content_token_count": len(control),
        "pattern_content_token_count": len(pattern),
        "target_marker_hits": marker_hits,
        "target_marker_status": "present" if marker_hits else "manual_review_required",
        "safety_flags": safety_flags,
        "automated_status": "screened_not_independently_equated",
        "manual_checks_required": [
            "same proposition and no extra outcome claim",
            "readability and vocabulary match",
            "target form is the intended manipulation",
            "accessibility and safety",
        ],
    }


def build(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    bank = json.loads((root / "research/communication-job-listener-stimuli-draft.json").read_text())
    records = [audit_record(record) for record in bank["records"]]
    return {
        "schema_version": "1.0",
        "audit_id": "communication-job-stimulus-automated-preflight",
        "status": "automated_screening_not_independent_review",
        "claim_boundary": "Token overlap, word counts, marker checks and keyword safety flags are screening aids. They cannot establish proposition equivalence, readability, accessibility, causal isolation or listener outcomes.",
        "source": "research/communication-job-listener-stimuli-draft.json",
        "pair_count": len(records),
        "records": records,
        "summary": {
            "pair_count": len(records),
            "max_absolute_word_count_delta": max(abs(item["word_count_delta"]) for item in records),
            "min_non_stopword_jaccard": min(item["non_stopword_jaccard"] for item in records),
            "pairs_with_marker_flag": sum(item["target_marker_status"] != "present" for item in records),
            "pairs_with_safety_flags": sum(bool(item["safety_flags"]) for item in records),
            "pairs_requiring_manual_review": len(records),
        },
    }


def write_outputs(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    result = build(root)
    (root / "research/communication-job-stimuli-preflight.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    s = result["summary"]
    lines = ["# Draft listener-stimulus automated preflight", "", "Status: **automated screening; not independent review**.", "", result["claim_boundary"], "", f"- Pairs: {s['pair_count']}", f"- Maximum absolute word-count delta: {s['max_absolute_word_count_delta']}", f"- Minimum non-stopword Jaccard overlap: {s['min_non_stopword_jaccard']}", f"- Marker flags: {s['pairs_with_marker_flag']}", f"- Safety flags: {s['pairs_with_safety_flags']}", f"- Pairs still requiring manual review: {s['pairs_requiring_manual_review']}", "", "| Job | Word delta | Token overlap | Marker | Safety flags |", "|---|---:|---:|---|---|"]
    lines += [f"| `{item['canonical_job']}` | {item['word_count_delta']:+d} | {item['non_stopword_jaccard']:.3f} | `{item['target_marker_status']}` | {', '.join(item['safety_flags']) or 'none'} |" for item in result["records"]]
    (root / "writeups/communication-job-stimuli-preflight.md").write_text("\n".join(lines) + "\n")
    return result


if __name__ == "__main__":
    result = write_outputs()
    print(json.dumps(result["summary"], indent=2))
