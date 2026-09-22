#!/usr/bin/env python3
"""Transcribe alternate-source leads while preserving original/candidate IDs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", default="research/alternate-source-transcripts.jsonl")
    parser.add_argument("--model", default="tiny")
    args = parser.parse_args()
    from faster_whisper import WhisperModel

    manifest = json.loads((ROOT / "research/unresolved-source-mirror-candidates.json").read_text())
    items = manifest["candidates"][args.start:]
    if args.limit is not None:
        items = items[:args.limit]
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if output.exists():
        for line in output.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                existing[row["original_video_id"]] = row
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    for item in items:
        original = item["original_video_id"]
        candidate = item["candidate_video_id"]
        media = sorted((ROOT / "data/alternate-source-audio").glob(f"{original}--{candidate}.*"))
        media = [p for p in media if p.suffix not in {".json", ".part"}]
        if not media or (original in existing and existing[original].get("status") == "alternate_machine_transcript_candidate"):
            continue
        print(json.dumps({"original_video_id": original, "candidate_video_id": candidate, "status": "transcribing"}), flush=True)
        try:
            segments_iter, info = model.transcribe(str(media[0]), language="en", beam_size=1, best_of=1, temperature=0, condition_on_previous_text=False)
            segments = list(segments_iter)
            existing[original] = {
                **item,
                "source_audio_file": str(media[0].relative_to(ROOT)),
                "status": "alternate_machine_transcript_candidate",
                "review_status": "identity_and_content_not_verified",
                "language": info.language,
                "text": " ".join(s.text.strip() for s in segments),
                "segments": [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segments],
            }
        except Exception as exc:
            existing[original] = {**item, "status": "alternate_transcription_failed", "error": repr(exc)}
        output.write_text("\n".join(json.dumps(existing[k], ensure_ascii=False) for k in sorted(existing)) + "\n")
        print(json.dumps({"original_video_id": original, "status": existing[original]["status"]}), flush=True)
    print(json.dumps({"records": len(existing), "output": str(output)}))


if __name__ == "__main__":
    main()
