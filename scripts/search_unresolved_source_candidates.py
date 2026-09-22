#!/usr/bin/env python3
"""Search for possible mirrors of unresolved corpus sources.

Search results are leads only. They are never promoted to corpus evidence
without identity, content, and source-alignment review.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    audit = json.loads((ROOT / "research/corpus-coverage-audit.json").read_text())
    unresolved = audit["unresolved_after_media_recovery_video_ids"]
    registry = {
        row["video_id"]: row
        for row in (
            json.loads(line)
            for line in (ROOT / "data/metadata/video-registry.jsonl").read_text().splitlines()
            if line.strip()
        )
    }
    yt_dlp = shutil.which("yt-dlp") or str(Path.home() / ".local/bin/yt-dlp")
    results = []
    for video_id in unresolved:
        title = registry.get(video_id, {}).get("title") or video_id
        query = f"ytsearch5:{title}"
        row = {"video_id": video_id, "original_title": title, "query": query, "status": "search_failed", "candidates": []}
        try:
            proc = subprocess.run(
                [yt_dlp, "--flat-playlist", "--dump-single-json", "--no-warnings", query],
                capture_output=True, text=True, timeout=90, check=False,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                payload = json.loads(proc.stdout)
                row["status"] = "search_candidates_not_verified"
                row["candidates"] = [
                    {
                        "video_id": entry.get("id"),
                        "title": entry.get("title"),
                        "uploader": entry.get("uploader"),
                        "url": entry.get("url") or (f"https://www.youtube.com/watch?v={entry.get('id')}" if entry.get("id") else None),
                    }
                    for entry in payload.get("entries", [])
                    if entry.get("id")
                ]
            else:
                row["error"] = (proc.stderr or proc.stdout)[-1000:]
        except Exception as exc:
            row["error"] = repr(exc)
        results.append(row)
        print(json.dumps({"video_id": video_id, "status": row["status"], "candidates": len(row["candidates"])}), flush=True)
    out = ROOT / "research/unresolved-source-search-candidates.json"
    out.write_text(json.dumps({
        "schema_version": "1.0",
        "status": "alternate_source_leads_not_verified",
        "results": results,
        "claim_boundary": "Search results are leads only. No alternate source is corpus evidence until identity, content, transcript alignment, and source provenance are independently checked.",
    }, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"unresolved": len(results), "candidates": sum(len(r["candidates"]) for r in results), "output": str(out)}))


if __name__ == "__main__":
    main()
