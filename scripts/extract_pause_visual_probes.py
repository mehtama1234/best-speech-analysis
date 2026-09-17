#!/usr/bin/env python3
"""Extract a small, declared still-frame probe around measured quiet intervals."""
import hashlib
import json
import subprocess
from pathlib import Path
import imageio_ffmpeg

PROBES = {
    "2fWJh-_UG5s:00035": [92.8, 93.8, 94.9],
    "fBnAMUkNM2k:00021": [196.6, 197.4, 198.2],
    "gDadfh0ZdBM:00036": [131.9, 132.8, 133.7],
}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    audio_audit = root / "research/local-pause-audio-audit.json"
    audio = {r["evidence_id"]: r for r in json.loads(audio_audit.read_text())["examples"]}
    probes = []
    hashes = {str(p.relative_to(root)): digest(p) for p in (audio_audit, Path(__file__).resolve())}
    for eid, times in PROBES.items():
        video_id = eid.split(":")[0]
        video = root / "data/video" / (video_id + ".mp4")
        record = {"evidence_id": eid, "video_path": str(video.relative_to(root)),
                  "selection": "Purposive probe of three measured low-energy intervals near caption starts, not a representative sample.",
                  "quiet_runs_minus40_dbfs": [r for r in audio[eid]["threshold_runs"]["-40"] if r["distance_from_caption_start_seconds"] < 1],
                  "frames": []}
        if not video.exists():
            record["error"] = "local_video_missing"
            probes.append(record)
            continue
        source_hash = digest(video)
        hashes[str(video.relative_to(root))] = source_hash
        directory = root / "data/cache/pause-visual-probes-v1" / video_id / source_hash[:12]
        directory.mkdir(parents=True, exist_ok=True)
        for t in times:
            path = directory / (f"{t:.3f}" + ".png")
            item = {"requested_seek_seconds": t, "path": str(path.relative_to(root))}
            if not path.exists():
                try:
                    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-ss", str(t),
                                    "-i", str(video), "-frames:v", "1", "-n", str(path)],
                                   check=True, capture_output=True, timeout=45)
                except (subprocess.SubprocessError, OSError) as exc:
                    item["error"] = type(exc).__name__
            if path.exists() and path.stat().st_size:
                item["sha256"] = digest(path)
            else:
                item["error"] = item.get("error", "no_decoded_frame")
            record["frames"].append(item)
        probes.append(record)
    report = {"schema_version": "1.0", "source_sha256": hashes,
              "policy": "Requested seek times, not verified decoded frame PTS. Audio/video timeline synchronization unverified. Three stills per interval cannot establish continuous motion, absence of intervening cuts, speech timing, emotion or intent. Raw frames are ignored cache artifacts.",
              "probes": probes}
    (root / "research/pause-visual-probes.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(probes))


if __name__ == "__main__":
    main()
