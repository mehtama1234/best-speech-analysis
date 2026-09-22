"""Reconcile local media availability and proxy coverage for all fixed-corpus videos."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "research/full-corpus-media-coverage.json"
PROXIES = ROOT / "research/full-delivery-proxy-index.json"
OUT = ROOT / "research/autonomous-full-media-reconciliation.json"
MD = ROOT / "writeups/autonomous-full-media-reconciliation.md"


def build() -> dict:
    media = json.loads(MEDIA.read_text(encoding="utf-8"))
    proxy_payload = json.loads(PROXIES.read_text(encoding="utf-8"))
    proxies = {item["video_id"]: item for item in proxy_payload["videos"]}
    rows = []
    for item in media["videos"]:
        proxy = proxies.get(item["video_id"])
        if proxy:
            proxy_status = "feature_proxy_available"
            observable = {
                "audio_windows": proxy.get("audio_window_count", 0),
                "sampled_frames": proxy.get("sampled_frame_count", 0),
                "aligned_transcript_segments": proxy.get("aligned_transcript_segment_count", 0),
                "face_presence_observable_frames": proxy.get("face_presence_fraction_proxy"),
            }
        else:
            proxy_status = "no_feature_proxy_report"
            observable = {"audio_windows": 0, "sampled_frames": 0, "aligned_transcript_segments": 0, "face_presence_observable_frames": None}
        row = {
            "video_id": item["video_id"],
            "title": item["title"],
            "source_url": item["source_url"],
            "media_state": item["media_state"],
            "proxy_status": proxy_status,
            "feature_file": proxy.get("feature_file") if proxy else None,
            "observable_proxy_fields": observable,
            "audio_measurement_status": proxy.get("audio_measurement_status") if proxy else "not_available",
            "visual_measurement_status": proxy.get("visual_measurement_status") if proxy else "not_available",
            "aligned_transcript_status": "aligned_proxy_available" if proxy and proxy.get("aligned_transcript_segment_count", 0) else "not_available_or_zero",
            "delivery_interpretation_status": "not_interpreted_internal_proxy_only",
            "missingness": proxy.get("missingness", []) if proxy else ["no_local_feature_report"],
            "claim_boundary": "Availability and feature measurements do not establish speaker identity, intentional delivery, emotion, gesture meaning, setting cause, audience response or effectiveness.",
        }
        rows.append(row)
    counts = {}
    for key in ("media_state", "proxy_status", "audio_measurement_status", "visual_measurement_status", "aligned_transcript_status"):
        counts[key] = {}
        for row in rows:
            value = row[key]
            counts[key][value] = counts[key].get(value, 0) + 1
    return {
        "schema_version": "1.0",
        "reconciliation_id": "autonomous-full-media-reconciliation",
        "status": "all_video_proxy_coverage_reconciled_not_delivery_interpretation",
        "video_count": len(rows),
        "claim_boundary": "This reconciles local media availability and generated feature proxies for every fixed-corpus video. It does not claim that media is the correct source, that a speaker/event is identified, or that any measured feature has social meaning or effectiveness.",
        "counts": counts,
        "rows": rows,
    }


def render(report: dict) -> str:
    c = report["counts"]
    lines = [
        "# Autonomous full-media reconciliation",
        "",
        "Status: **all-video proxy coverage reconciled; delivery interpretation is not claimed**.",
        "",
        report["claim_boundary"],
        "",
        f"The report covers **{report['video_count']} videos**. It records local media state, feature-report availability, audio/frame proxy fields, transcript alignment and missingness.",
        "",
        "## Coverage counts",
        "",
        "| Dimension | Counts |",
        "|---|---|",
    ]
    for key, values in c.items():
        lines.append(f"| `{key}` | " + "; ".join(f"`{k}`={v}" for k, v in sorted(values.items())) + " |")
    lines += [
        "",
        "## How to use it",
        "",
        "Use a row to locate a source clip or to decide that a delivery claim cannot be inspected locally. Combine it with the transcript lesson and the bounded practice questions; never turn a proxy value into a claim about emotion, confidence, intent, gesture meaning or persuasion.",
        "",
        "The [autonomous delivery reconciliation](autonomous-delivery-reconciliation.md) contains the smaller 36-sample job-linked inspection layer with bounded frame notes and practice questions.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    report = build()
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MD.write_text(render(report), encoding="utf-8")
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "markdown": str(MD.relative_to(ROOT)), "video_count": report["video_count"], "proxy_reports": sum(1 for x in report["rows"] if x["proxy_status"] == "feature_proxy_available")}, indent=2))
