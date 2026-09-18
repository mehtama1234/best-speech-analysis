#!/usr/bin/env python3
"""Consolidate delivery measurements and bounded multimodal observations."""

from __future__ import annotations

import json
from pathlib import Path


def build(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    coverage = json.loads((root / "research/multimodal-coverage-audit.json").read_text())
    delivery = json.loads((root / "research/reviewed-delivery-patterns.json").read_text())
    manual_items = []
    for filename in ("research/multimodal-expansion-manual-review.json", "research/multimodal-expansion-manual-review-02.json"):
        report = json.loads((root / filename).read_text())
        for item in report["items"]:
            manual_items.append({
                "evidence_id": item["evidence_id"],
                "video_id": item["video_id"],
                "title": item["title"],
                "pattern_id": item.get("pattern_id"),
                "sampled_time_seconds": item.get("sampled_time_seconds"),
                "transcript_text": item.get("transcript_text"),
                "frame_observation": item.get("frame_observation"),
                "alignment_decision": item.get("alignment_decision"),
                "measured_audio_proxy": item.get("measured_audio_proxy", {}),
                "nearest_frame_measurement": item.get("nearest_frame_measurement", {}),
                "feature_limit": item.get("feature_limit"),
                "review_status": item.get("review_status"),
                "source_report": filename,
            })
    feature_files = []
    media_by_video = {item["video_id"]: item for item in coverage["videos"]}
    for path in sorted((root / "data/features").glob("*.json")):
        report = json.loads(path.read_text())
        video_id = path.stem
        feature_files.append({
            "video_id": video_id,
            "feature_file": str(path.relative_to(root)),
            "feature_record_count": len(report.get("aligned_transcript", [])),
            "video_feature_keys": sorted(report.get("video_features", {}).keys()) if isinstance(report.get("video_features"), dict) else [],
            "raw_media_state": media_by_video.get(video_id, {}).get("raw_media_state", "not_in_selected_audit"),
            "manual_observation_count": sum(item["video_id"] == video_id for item in manual_items),
        })
    return {
        "schema_version": "1.0",
        "index_id": "delivery-evidence-index",
        "status": "delivery_evidence_reconciled_independent_review_pending",
        "claim_boundary": "This index distinguishes raw media, derived measurements, internal visual/audio observations and independent review. Proxies do not establish emotion, intent, confidence, nonverbal meaning, audience response or effectiveness.",
        "coverage_source": "research/multimodal-coverage-audit.json",
        "coverage": {
            "selected_video_count": coverage["selected_video_count"],
            "raw_audio_video_present_count": coverage["raw_audio_video_present_count"],
            "raw_audio_video_with_transcript_count": coverage["raw_audio_video_with_transcript_count"],
            "raw_audio_video_without_transcript_count": coverage["raw_audio_video_without_transcript_count"],
            "derived_features_only_count": coverage["derived_features_only_count"],
            "raw_media_missing_count": coverage["raw_media_missing_count"],
            "internal_manual_observation_count": len(manual_items),
            "independent_review_count": 0,
        },
        "feature_files": feature_files,
        "internal_multimodal_observations": manual_items,
        "transcript_reviewed_delivery_patterns": {
            "source": "research/reviewed-delivery-patterns.json",
            "supported_annotation_count": delivery["supported_annotation_count"],
            "feature_record_count": delivery["feature_record_count"],
            "review_provenance": delivery["review_provenance"],
            "patterns_by_reviewed_function": delivery["patterns_by_reviewed_function"],
        },
        "independent_review": {
            "status": "blank_workbook_no_records",
            "workbook": "research/multimodal-independent-review-workbook.json",
            "validator": "scripts/validate_multimodal_independent_review.py",
        },
        "limits": coverage["limits"],
    }


def write_outputs(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    result = build(root)
    (root / "research/delivery-evidence-index.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    c = result["coverage"]
    lines = ["# Delivery evidence index", "", "Status: **delivery reconciled; independent review pending**.", "", result["claim_boundary"], "", "| Evidence layer | Count |", "|---|---:|", f"| Selected videos | {c['selected_video_count']} |", f"| Raw audio/video present | {c['raw_audio_video_present_count']} |", f"| Raw audio/video with transcript | {c['raw_audio_video_with_transcript_count']} |", f"| Raw audio/video without transcript | {c['raw_audio_video_without_transcript_count']} |", f"| Derived-features-only | {c['derived_features_only_count']} |", f"| Raw media missing | {c['raw_media_missing_count']} |", f"| Internal multimodal observations | {c['internal_manual_observation_count']} |", f"| Independent observations | {c['independent_review_count']} |", "", "The [multimodal independent workbook](multimodal-independent-review-workbook.html) remains blank. Internal observations and derived proxies are not delivery or effectiveness findings.", ""]
    (root / "writeups/delivery-evidence-index.md").write_text("\n".join(lines))
    return result


if __name__ == "__main__":
    result = write_outputs()
    print(json.dumps(result["coverage"], indent=2))
