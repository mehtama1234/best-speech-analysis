#!/usr/bin/env python3
"""Inspect short-frame acoustic energy near legacy pause targets, not intent."""
import hashlib
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np

SAMPLE_RATE = 16000
FRAME_SECONDS = 0.02
THRESHOLDS_DBFS = (-50, -40, -30)
MINIMUM_RUN_SECONDS = 0.2


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def energy_frames(samples, sample_rate=SAMPLE_RATE):
    width = round(sample_rate * FRAME_SECONDS)
    if width < 1:
        raise ValueError("Invalid frame width")
    count = len(samples) // width
    if not count:
        return []
    chunks = samples[:count * width].reshape(count, width).astype(np.float64)
    db = 20 * np.log10(np.maximum(np.sqrt(np.mean(chunks * chunks, axis=1)), 1e-12))
    return [{"start_seconds": i * width / sample_rate,
             "end_seconds": (i + 1) * width / sample_rate,
             "rms_dbfs": float(level)} for i, level in enumerate(db)]


def low_energy_runs(frames, threshold, minimum=MINIMUM_RUN_SECONDS):
    """Never bridge missing/high-energy frames; retain edge-censoring flags."""
    runs = []
    active = None
    def finish():
        if active and active["end_seconds"] - active["start_seconds"] + 1e-9 >= minimum:
            runs.append(dict(active))
    for index, row in enumerate(frames):
        contiguous = active is not None and abs(row["start_seconds"] - active["end_seconds"]) < 1e-7
        quiet = np.isfinite(row["rms_dbfs"]) and row["rms_dbfs"] < threshold
        if not quiet or (active is not None and not contiguous):
            finish()
            active = None
        if quiet:
            if active is None:
                active = {"start_seconds": row["start_seconds"], "end_seconds": row["end_seconds"],
                          "left_window_censored": index == 0,
                          "right_window_censored": False}
            else:
                active["end_seconds"] = row["end_seconds"]
            active["right_window_censored"] = index == len(frames) - 1
    finish()
    for run in runs:
        run["duration_seconds"] = round(run["end_seconds"] - run["start_seconds"], 6)
    return runs


def boundary_distance(run, boundary):
    return max(run["start_seconds"] - boundary, boundary - run["end_seconds"], 0.0)


def main():
    root = Path(__file__).resolve().parents[1]
    ledger = root / "research/annotation-ledger.jsonl"
    registry = root / "research/segment-registry.jsonl"
    targets = [json.loads(s) for s in ledger.read_text().splitlines() if s.strip()]
    targets = [r for r in targets if "pause_event" in r["candidate_labels"]]
    wanted = {r["evidence_id"] for r in targets}
    source_rows = {}
    with registry.open() as stream:
        for line in stream:
            row = json.loads(line)
            if row["evidence_id"] in wanted:
                source_rows[row["evidence_id"]] = row
    hashes = {str(p.relative_to(root)): sha256(p) for p in (ledger, registry, Path(__file__).resolve())}
    results = []
    for video_id in sorted({eid.split(":")[0] for eid in wanted}):
        audio = root / "data/audio" / (video_id + ".m4a")
        feature = root / "data/features" / (video_id + ".json")
        features = {}
        if feature.exists():
            hashes[str(feature.relative_to(root))] = sha256(feature)
            features = {r["evidence_id"]: r for r in json.loads(feature.read_text())["aligned_transcript"]}
        frames, error = [], None
        if audio.exists():
            hashes[str(audio.relative_to(root))] = sha256(audio)
            try:
                raw = subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(audio),
                        "-f", "f32le", "-ac", "1", "-ar", str(SAMPLE_RATE), "pipe:1"], timeout=90)
                frames = energy_frames(np.frombuffer(raw, dtype="<f4"))
                if not frames:
                    error = "decoded_audio_has_no_complete_frames"
            except (subprocess.SubprocessError, OSError) as exc:
                error = type(exc).__name__
        else:
            error = "local_audio_missing"
        for target in (r for r in targets if r["evidence_id"].split(":")[0] == video_id):
            eid = target["evidence_id"]
            source = source_rows.get(eid)
            item = {"annotation_id": target["annotation_id"], "evidence_id": eid,
                    "legacy_support": target["candidate_label_supported"],
                    "review_status": "acoustic_screen_only_pause_function_unadjudicated",
                    "measurement_error": error, "source": source,
                    "audio_path": str(audio.relative_to(root)),
                    "legacy_feature_caption_gaps": {k: features.get(eid, {}).get(k) for k in
                        ("transcript_gap_before_seconds", "transcript_gap_after_seconds")}}
            if source is None:
                item["measurement_error"] = "source_segment_missing"
            elif not error:
                start, end = source["start_seconds"], source["end_seconds"]
                local = [r for r in frames if r["end_seconds"] > max(0, start - 3) and r["start_seconds"] < end + 3]
                item["energy_frames"] = local
                item["threshold_runs"] = {}
                for threshold in THRESHOLDS_DBFS:
                    runs = low_energy_runs(local, threshold)
                    for run in runs:
                        run["distance_from_caption_start_seconds"] = round(boundary_distance(run, start), 6)
                        run["distance_from_caption_end_seconds"] = round(boundary_distance(run, end), 6)
                    item["threshold_runs"][str(threshold)] = runs
            results.append(item)
    report = {"schema_version": "1.0", "source_sha256": hashes,
              "settings": {"sample_rate": SAMPLE_RATE, "frame_seconds": FRAME_SECONDS,
                           "thresholds_dbfs": THRESHOLDS_DBFS, "minimum_run_seconds": MINIMUM_RUN_SECONDS,
                           "caption_padding_seconds": 3},
              "policy": "Threshold-sensitivity screen of decoded local audio; no listening or semantic pause adjudication. Quiet energy is not speech absence, intentional silence, or an audience effect. No legacy decisions overwritten.",
              "examples": results}
    (root / "research/local-pause-audio-audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    lines = ["# Local acoustic screening of pause candidates", "", report["policy"], "",
             "20 ms mono energy frames; runs at least 200 ms at three exploratory fixed thresholds. "
             "These are sensitivity settings, not calibrated speech/non-speech thresholds. Frames and run boundaries are in the JSON artifact.", "",
             "| Evidence | Local audio | Runs below -50 / -40 / -30 dBFS |", "| --- | --- | --- |"]
    for item in results:
        counts = " / ".join(str(len(item.get("threshold_runs", {}).get(str(t), []))) for t in THRESHOLDS_DBFS) if not item["measurement_error"] else "not measured"
        lines.append(f"| `{item['evidence_id']}` | {item['measurement_error'] or 'decoded'} | {counts} |")
    lines += ["", "Runs are measured over the entire caption plus three seconds either side, not necessarily immediately before speech. "
              "Distance to each caption boundary and window-censoring flags are recorded. Overlapping captions are not independent trials. "
              "Music, room noise, gain, edits and speaker changes remain confounds. Mono downmixing may also change energy. "
              "No absence of a quiet run proves continuous speech; no detected run proves a rhetorical pause.", ""]
    (root / "writeups/local-pause-audio-audit.md").write_text("\n".join(lines))
    print(json.dumps({"targets": len(results), "decoded": sum(r["measurement_error"] is None for r in results),
                      "threshold_run_counts": {r["evidence_id"]: {t: len(x) for t, x in r.get("threshold_runs", {}).items()} for r in results}}))


if __name__ == "__main__":
    main()
