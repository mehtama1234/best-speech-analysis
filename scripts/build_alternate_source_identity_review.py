#!/usr/bin/env python3
"""Build an explicit identity-review queue for alternate source candidates."""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tokens(value: str) -> set[str]:
    return {x for x in re.findall(r"[a-z0-9]+", value.lower()) if len(x) > 2}


def main() -> int:
    manifest = json.loads((ROOT / "research/unresolved-source-mirror-candidates.json").read_text())
    registry = {
        row["video_id"]: row
        for row in (
            json.loads(line)
            for line in (ROOT / "data/metadata/video-registry.jsonl").read_text().splitlines()
            if line.strip()
        )
    }
    records = {json.loads(line)["original_video_id"]: json.loads(line) for line in (ROOT / "research/alternate-source-transcripts.jsonl").read_text().splitlines() if line.strip()}
    output = []
    for item in manifest["candidates"]:
        original_title = registry.get(item["original_video_id"], {}).get("title") or item["original_video_id"]
        metadata_files = sorted((ROOT / "data/alternate-source-audio").glob(f"{item['original_video_id']}--{item['candidate_video_id']}.info.json"))
        candidate_title = None
        duration = None
        uploader = None
        if metadata_files:
            metadata = json.loads(metadata_files[0].read_text())
            candidate_title, duration, uploader = metadata.get("title"), metadata.get("duration"), metadata.get("uploader")
        a, b = tokens(original_title), tokens(candidate_title or "")
        overlap = len(a & b) / len(a | b) if a | b else 0.0
        sequence = SequenceMatcher(None, original_title.lower(), (candidate_title or "").lower()).ratio()
        row = {
            **item,
            "original_title": original_title,
            "candidate_title": candidate_title,
            "candidate_uploader": uploader,
            "candidate_duration_seconds": duration,
            "title_token_overlap": round(overlap, 3),
            "title_sequence_similarity": round(sequence, 3),
            "transcript_status": records.get(item["original_video_id"], {}).get("status"),
            "identity_decision": "manual_identity_review_required",
        }
        output.append(row)
    payload = {
        "schema_version": "1.0",
        "status": "alternate_source_identity_review_queue",
        "records": output,
        "claim_boundary": "Title similarity and transcript availability are triage signals, not proof that a mirror is the original source or has identical scene boundaries.",
    }
    (ROOT / "research/alternate-source-identity-review.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Alternate-source identity review queue", "", "These 11 recovered mirrors are triage candidates, not promoted corpus evidence. Review the title, uploader, duration, transcript excerpt, and scene boundaries before promotion.", "", "| Original | Candidate | Candidate title | Uploader | Title token overlap | Decision |", "|---|---|---|---|---:|---|"]
    for r in output:
        lines.append(f"| `{r['original_video_id']}` | `{r['candidate_video_id']}` | {r.get('candidate_title') or '—'} | {r.get('candidate_uploader') or '—'} | {r['title_token_overlap']:.3f} | `{r['identity_decision']}` |")
    (ROOT / "writeups/alternate-source-identity-review.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"records": len(output), "transcribed": sum(r.get("transcript_status") == "alternate_machine_transcript_candidate" for r in output)}))


if __name__ == "__main__":
    main()
