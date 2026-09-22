#!/usr/bin/env python3
"""Download selected alternate-source leads without promoting them."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = json.loads((ROOT / "research/unresolved-source-mirror-candidates.json").read_text())
    audio_dir = ROOT / "data/alternate-source-audio"
    metadata_dir = ROOT / "research/alternate-source-metadata"
    audio_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    yt_dlp = shutil.which("yt-dlp") or str(Path.home() / ".local/bin/yt-dlp")
    results = []
    for item in manifest["candidates"]:
        original = item["original_video_id"]
        candidate = item["candidate_video_id"]
        output = audio_dir / f"{original}--{candidate}.%(ext)s"
        command = [
            yt_dlp, "--no-playlist", "--no-part", "--retries", "1",
            "--write-info-json", "--format", "worstaudio[protocol=https]/worstaudio",
            "--output", str(output), f"https://www.youtube.com/watch?v={candidate}",
        ]
        proc = subprocess.run(command, capture_output=True, text=True, timeout=180, check=False)
        files = sorted(audio_dir.glob(f"{original}--{candidate}.*"))
        media = [str(p.relative_to(ROOT)) for p in files if p.suffix not in {".json", ".part"}]
        row = {**item, "media_files": media, "download_status": "downloaded" if media else f"failed:{proc.returncode}"}
        if not media:
            row["error"] = (proc.stderr or proc.stdout)[-1000:]
        results.append(row)
        print(json.dumps({"original_video_id": original, "candidate_video_id": candidate, "status": row["download_status"]}), flush=True)
    (ROOT / "research/alternate-source-recovery.json").write_text(json.dumps({
        "schema_version": "1.0",
        "status": "alternate_source_media_candidates_not_verified",
        "results": results,
        "claim_boundary": manifest["claim_boundary"],
    }, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"attempted": len(results), "downloaded": sum(r["download_status"] == "downloaded" for r in results)}))


if __name__ == "__main__":
    main()
