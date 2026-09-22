#!/usr/bin/env python3
"""Summarize canonical, recovered, and unresolved coverage without conflation."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> int:
    registry = read_jsonl(ROOT / "data/metadata/video-registry.jsonl")
    queue = json.loads((ROOT / "research/full-reading-queue.json").read_text()).get("videos", [])
    canonical = {row.get("video_id") or row.get("id") for row in queue}
    media = read_jsonl(ROOT / "data/unreviewed-corpus-media-recovery.jsonl")
    media_by_id = {row["video_id"]: row for row in media}
    audio_rows = read_jsonl(ROOT / "research/recovered-audio-transcripts.jsonl") if (ROOT / "research/recovered-audio-transcripts.jsonl").exists() else []
    audio_candidates = {row["video_id"] for row in audio_rows if row.get("status") == "machine_transcript_candidate"}
    alt_rows = read_jsonl(ROOT / "research/recovered-transcript-review-candidates.json") if False else []
    alt_path = ROOT / "research/recovered-transcript-review-candidates.json"
    if alt_path.exists():
        alt_rows = json.loads(alt_path.read_text()).get("reviews", [])
    alternate_candidates = {row["video_id"] for row in alt_rows}
    mirror_path = ROOT / "research/alternate-source-transcripts.jsonl"
    mirror_rows = read_jsonl(mirror_path) if mirror_path.exists() else []
    mirror_candidates = {row["original_video_id"] for row in mirror_rows if row.get("status") == "alternate_machine_transcript_candidate"}
    external_path = ROOT / "research/external-source-leads.json"
    external_leads = json.loads(external_path.read_text()).get("leads", []) if external_path.exists() else []
    external_transcript_path = ROOT / "research/external-source-transcripts.jsonl"
    external_transcripts = read_jsonl(external_transcript_path) if external_transcript_path.exists() else []
    external_transcript_ids = {row["video_id"] for row in external_transcripts if row.get("status") == "external_transcript_candidate"}
    all_ids = {row["video_id"] for row in registry}
    recovered_media = {
        video_id for video_id, row in media_by_id.items()
        if row.get("video_status") == "downloaded" and row.get("audio_status") == "downloaded"
    }
    unresolved = all_ids - canonical - recovered_media
    text_bearing = canonical | audio_candidates | mirror_candidates
    text_bearing_with_external = text_bearing | external_transcript_ids
    report = {
        "schema_version": "1.0",
        "status": "coverage_audit_canonical_and_recovery_layers",
        "inventory_count": len(all_ids),
        "canonical_full_context_review_count": len(canonical),
        "gap_from_canonical_count": len(all_ids - canonical),
        "recovered_complete_media_count": len(recovered_media),
        "recovered_machine_transcript_candidate_count": len(audio_candidates),
        "recovered_alternate_transcript_candidate_count": len(alternate_candidates),
        "alternate_source_machine_transcript_candidate_count": len(mirror_candidates),
        "external_source_lead_count": len(external_leads),
        "external_transcript_candidate_count": len(external_transcript_ids),
        "unique_text_bearing_video_count_including_external": len(text_bearing_with_external),
        "unique_text_bearing_gap_count_including_external": len(all_ids - text_bearing_with_external),
        "unresolved_after_media_recovery_count": len(unresolved),
        "unique_text_bearing_video_count": len(text_bearing),
        "unique_text_bearing_gap_count": len(all_ids - text_bearing),
        "unresolved_after_media_recovery_video_ids": sorted(unresolved),
        "unresolved_media_status": {
            video_id: {
                "video_status": media_by_id.get(video_id, {}).get("video_status"),
                "audio_status": media_by_id.get(video_id, {}).get("audio_status"),
            }
            for video_id in sorted(unresolved)
        },
        "layers": {
            "canonical_full_context": sorted(canonical),
            "recovered_complete_media": sorted(recovered_media),
            "machine_transcript_candidates": sorted(audio_candidates),
            "alternate_transcript_candidates": sorted(alternate_candidates),
            "alternate_source_machine_transcripts": sorted(mirror_candidates),
        },
        "claim_boundary": "Only canonical_full_context is human-reviewed semantic evidence. Recovered media and transcript layers are candidates until identity, transcript quality, context, and rhetorical interpretation are reviewed.",
    }
    (ROOT / "research/corpus-coverage-audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    md = [
        "# Corpus coverage audit",
        "",
        "This report keeps the fixed 480-video inventory separate from recovered evidence. Recovery is progress toward end-to-end analysis, not automatic semantic review.",
        "",
        f"- Inventory: **{len(all_ids)}** videos",
        f"- Canonical full-context reviews: **{len(canonical)}**",
        f"- Complete recovered media pairs: **{len(recovered_media)}**",
        f"- Machine transcript candidates: **{len(audio_candidates)}**",
        f"- Alternate transcript candidates: **{len(alternate_candidates)}**",
        f"- Alternate-source machine-transcript candidates: **{len(mirror_candidates)}**",
        f"- Unique videos with at least one text-bearing layer: **{len(text_bearing)}**",
        f"- External source leads requiring alignment review: **{len(external_leads)}**",
        f"- External transcript candidates: **{len(external_transcript_ids)}**",
        f"- Unique videos with text-bearing layer including external transcript candidates: **{len(text_bearing_with_external)}**",
        f"- Still unresolved after media recovery: **{len(unresolved)}**",
        "",
        "## Boundary",
        "",
        "The canonical layer contains project-generated single-pass full-context transcript reviews and is the source for provisional semantic and rhetorical candidates; it is not independent human validation. Recovered media/transcript rows are preserved as candidates and require human validation before promotion.",
        "",
        "## Unresolved IDs",
        "",
    ]
    md.extend(
        f"- `{video_id}` — video `{media_by_id.get(video_id, {}).get('video_status')}`; audio `{media_by_id.get(video_id, {}).get('audio_status')}`"
        for video_id in sorted(unresolved)
    )
    (ROOT / "writeups/corpus-coverage-audit.md").write_text("\n".join(md) + "\n")
    print(json.dumps({k: report[k] for k in ("inventory_count", "canonical_full_context_review_count", "recovered_complete_media_count", "recovered_machine_transcript_candidate_count", "unresolved_after_media_recovery_count")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
