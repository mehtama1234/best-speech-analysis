#!/usr/bin/env python3
"""Audit raw media and derived-feature availability for vertical slice 01."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAMES = ["contrast-or-disagreement", "example", "story", "uncertainty", "conclusion"]
OUT_JSON = ROOT / "research/vertical-slice-01-media-audit.json"
OUT_MD = ROOT / "writeups/vertical-slice-01-media-audit.md"


def load(path):
    return json.loads(path.read_text())


def media_statuses():
    result = {}
    path = ROOT / "data/media-status.jsonl"
    if not path.exists():
        return result
    for line in path.read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            result[row["video_id"]] = row
    return result


def packet_items(packet):
    """Return representative/control records without assuming one packet shape."""
    items = [("representative", item) for item in packet.get("representative_examples", [])]
    items.extend(("counterexample", item) for item in packet.get("counterexamples", []))
    for key, value in packet.get("counterexample_status", {}).items():
        if isinstance(value, list):
            items.extend((key, item) for item in value if isinstance(item, dict) and "video_id" in item)
    return items


def files_for(video_id, directory):
    return sorted(str(path.relative_to(ROOT)) for path in directory.glob(video_id + ".*") if path.is_file())


def main():
    statuses = media_statuses()
    occurrences = []
    seen = set()
    for name in NAMES:
        packet = load(ROOT / f"research/vertical-slice-01-{name}.json")
        for role, item in packet_items(packet):
            key = (name, role, item["evidence_id"])
            if key in seen:
                continue
            seen.add(key)
            video_id = item["video_id"]
            audio = files_for(video_id, ROOT / "data/audio")
            video = files_for(video_id, ROOT / "data/video")
            features = files_for(video_id, ROOT / "data/features")
            status = statuses.get(video_id, {})
            contradictions = []
            if status.get("audio_status") == "downloaded" and not audio:
                contradictions.append("media-status says audio downloaded but no raw audio file is present")
            if status.get("video_status") == "downloaded" and not video:
                contradictions.append("media-status says video downloaded but no raw video file is present")
            occurrences.append({
                "packet": name,
                "role": role,
                "evidence_id": item["evidence_id"],
                "video_id": video_id,
                "feature_files": features,
                "audio_files": audio,
                "video_files": video,
                "media_status_record": status,
                "contradictions": contradictions,
                "raw_media_available": bool(audio or video),
            })
    unique = {row["video_id"]: row for row in occurrences}
    report = {
        "schema_version": "1.0",
        "audit_id": "vertical-slice-01-media-audit",
        "status": "raw_media_audit_complete_manual_alignment_pending",
        "claim_boundary": "File presence does not establish synchronization, delivery meaning, speaker identity or listener outcome.",
        "packet_item_occurrences": len(occurrences),
        "unique_video_ids": len(unique),
        "unique_ids_with_raw_media": sum(row["raw_media_available"] for row in unique.values()),
        "unique_ids_with_features_only": sum(bool(row["feature_files"]) and not row["raw_media_available"] for row in unique.values()),
        "contradiction_count": sum(bool(row["contradictions"]) for row in occurrences),
        "occurrences": occurrences,
    }
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n")
    lines = [
        "# Vertical slice 01 media audit",
        "",
        "Status: **raw media audit complete; manual alignment pending**.",
        "",
        report["claim_boundary"],
        "",
        f"Packet item occurrences: **{report['packet_item_occurrences']}**; unique video IDs: **{report['unique_video_ids']}**.",
        f"Unique IDs with raw media: **{report['unique_ids_with_raw_media']}**; feature-only IDs: **{report['unique_ids_with_features_only']}**.",
        f"Media-status contradictions: **{report['contradiction_count']}**.",
        "",
        "A feature JSON file is a derived measurement artifact, not a substitute for inspecting the source audio/video.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")
    print(f"media audit: {report['unique_ids_with_raw_media']}/{report['unique_video_ids']} unique IDs have raw media; contradictions={report['contradiction_count']}")
    return report


if __name__ == "__main__":
    main()
