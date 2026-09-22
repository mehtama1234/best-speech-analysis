#!/usr/bin/env python3
"""Create resumable machine-transcript candidates from recovered audio.

These transcripts are deliberately kept outside the canonical review set. They
are coverage/recovery evidence until a human validates identity, language,
transcript quality, and rhetorical interpretation.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path


def audio_files(directory: Path) -> list[Path]:
    suffixes = {".m4a", ".mp3", ".wav", ".opus", ".ogg", ".webm", ".mp4"}
    return sorted(p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in suffixes)


def load_rows(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    rows = {}
    for line in path.read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            rows[row["video_id"]] = row
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio-dir", default="data/audio-recovery")
    parser.add_argument("--output", default="research/recovered-audio-transcripts.jsonl")
    parser.add_argument("--model", default="tiny")
    parser.add_argument("--backend", choices=("faster-whisper", "openai-whisper"), default="faster-whisper")
    parser.add_argument("--language", default=None, help="Optional language code; omit for detection.")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--start", type=int, default=0)
    args = parser.parse_args()

    audio_dir = Path(args.audio_dir)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = load_rows(output)
    files = audio_files(audio_dir)[args.start:]
    if args.limit is not None:
        files = files[:args.limit]
    # Whisper shells out to ffmpeg; imageio-ffmpeg is the portable fallback on
    # this host where a system ffmpeg binary is not necessarily on PATH.
    if not shutil.which("ffmpeg"):
        try:
            import imageio_ffmpeg
            ffmpeg_exe = Path(imageio_ffmpeg.get_ffmpeg_exe())
            shim_dir = Path(tempfile.mkdtemp(prefix="speech-analysis-ffmpeg-"))
            (shim_dir / "ffmpeg").symlink_to(ffmpeg_exe)
            os.environ["PATH"] = str(shim_dir) + os.pathsep + os.environ.get("PATH", "")
        except ImportError:
            pass

    if args.backend == "faster-whisper":
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise SystemExit("faster-whisper is required: " + str(exc))
        model = WhisperModel(args.model, device="cpu", compute_type="int8")
    else:
        try:
            import whisper
        except ImportError as exc:
            raise SystemExit("openai-whisper is required: " + str(exc))
        model = whisper.load_model(args.model)

    for index, audio_path in enumerate(files):
        video_id = audio_path.stem
        if video_id in rows and rows[video_id].get("status") == "machine_transcript_candidate":
            continue
        print(json.dumps({"video_id": video_id, "index": index + 1, "total": len(files), "status": "transcribing"}), flush=True)
        try:
            if args.backend == "faster-whisper":
                segments_iter, info = model.transcribe(
                    str(audio_path), language=args.language, beam_size=1,
                    best_of=1, temperature=0, condition_on_previous_text=False,
                )
                segments = list(segments_iter)
                result = {
                    "language": info.language,
                    "text": " ".join(s.text.strip() for s in segments),
                    "segments": [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segments],
                }
            else:
                result = model.transcribe(
                    str(audio_path), language=args.language, fp16=False,
                    verbose=False, condition_on_previous_text=False,
                    beam_size=1, best_of=1, temperature=0,
                )
            rows[video_id] = {
                "video_id": video_id,
                "source_audio_file": str(audio_path),
                "status": "machine_transcript_candidate",
                "review_status": "not_human_reviewed",
                "model": f"{args.backend}:{args.model}",
                "language": result.get("language"),
                "text": result.get("text", "").strip(),
                "segments": [
                    {"start": s.get("start"), "end": s.get("end"), "text": s.get("text", "").strip()}
                    for s in result.get("segments", [])
                ],
            }
        except Exception as exc:  # preserve resumability and auditability
            rows[video_id] = {
                "video_id": video_id,
                "source_audio_file": str(audio_path),
                "status": "transcription_failed",
                "error": repr(exc),
            }
        with output.open("w") as handle:
            for key in sorted(rows):
                handle.write(json.dumps(rows[key], ensure_ascii=False) + "\n")
        print(json.dumps({"video_id": video_id, "status": rows[video_id]["status"]}), flush=True)

    print(json.dumps({"audio_files": len(files), "records": len(rows), "output": str(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
