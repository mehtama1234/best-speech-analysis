#!/usr/bin/env python3
"""Validate recurrence reconciliation without promoting repeated forms to evidence."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/autonomous-language-reconciliation.json"
WORKBOOK = ROOT / "research/corpus-recurrence-independent-review-workbook.json"
PHRASES = ROOT / "research/corpus-phrase-form-inventory.json"


def validate() -> list[str]:
    errors: list[str] = []
    report = json.loads(REPORT.read_text())
    workbook = json.loads(WORKBOOK.read_text())
    phrase_inventory = json.loads(PHRASES.read_text())
    candidates = report.get("recurrence_candidates", [])
    items = workbook.get("items", [])

    if "not_validation" not in report.get("status", ""):
        errors.append("language reconciliation is not explicitly non-validating")
    if report.get("phrase_form_count") != 50 or len(report.get("phrase_forms", [])) != 50:
        errors.append("phrase-form count is not exactly 50")
    if report.get("recurrence_candidate_count") != 192 or len(candidates) != 192:
        errors.append("recurrence candidate count is not exactly 192")
    if workbook.get("item_count") != 192 or len(items) != 192:
        errors.append("independent-review workbook count is not exactly 192")
    if len(phrase_inventory.get("forms", [])) != 50:
        errors.append("phrase inventory does not contain 50 forms")

    candidate_ids = [x.get("review_item_id") for x in candidates]
    workbook_ids = [x.get("review_item_id") for x in items]
    if len(set(candidate_ids)) != len(candidate_ids):
        errors.append("recurrence candidate IDs are not unique")
    if candidate_ids != workbook_ids:
        errors.append("reconciliation candidate order/IDs differ from review workbook")

    split_counts = Counter(x.get("event_split") for x in candidates)
    if split_counts != Counter({"train": 96, "holdout": 96}):
        errors.append(f"unexpected train/holdout counts: {dict(split_counts)}")

    # A video can contribute several phrase candidates, but it is one event unit.
    # No video may straddle train and holdout, and duplicate rows must never be
    # silently counted as independent recurrence.
    video_splits: dict[str, set[str]] = defaultdict(set)
    for item in candidates:
        video = item.get("video_id")
        split = item.get("event_split")
        if not video or split not in {"train", "holdout"}:
            errors.append(f"missing video or invalid split for {item.get('review_item_id')}")
        video_splits[video].add(split)
        if not item.get("source_url", "").endswith(video):
            errors.append(f"source URL does not end with video ID for {item.get('review_item_id')}")
        if not item.get("evidence_id") or not item.get("matched_forms"):
            errors.append(f"missing evidence lineage for {item.get('review_item_id')}")
        if item.get("original_independent_review_status") != "not_received":
            errors.append(f"candidate has unexpected review status for {item.get('review_item_id')}")
    cross_split = [video for video, splits in video_splits.items() if len(splits) > 1]
    if cross_split:
        errors.append(f"videos cross train/holdout boundary: {cross_split[:5]}")
    duplicate_video_rows = sum(1 for video in video_splits if sum(1 for x in candidates if x.get("video_id") == video) > 1)
    if duplicate_video_rows == 0:
        errors.append("recurrence queue unexpectedly has no repeated-video rows to guard")
    boundary = report.get("claim_boundary", "").lower()
    if "independent" not in boundary or "effectiveness" not in boundary:
        errors.append("claim boundary does not preserve independence/effectiveness limits")
    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    report = json.loads(REPORT.read_text())
    candidates = report["recurrence_candidates"]
    unique_videos = len({x["video_id"] for x in candidates})
    print(f"autonomous language reconciliation valid: 50 forms, 192 candidates, {unique_videos} event videos; independence remains unvalidated")
