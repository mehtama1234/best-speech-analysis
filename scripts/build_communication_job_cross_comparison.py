#!/usr/bin/env python3
"""Build a transcript-only comparison of communication jobs across videos."""

from __future__ import annotations

import html
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "research/corpus-evidence-bank.json"
ATLAS = ROOT / "research/corpus-pattern-atlas.json"
CARDS = ROOT / "research/communication-job-cards.json"
OUT_JSON = ROOT / "research/communication-job-cross-comparison.json"
OUT_MD = ROOT / "writeups/communication-job-cross-comparison.md"
OUT_HTML = ROOT / "writeups/communication-job-cross-comparison.html"


def main() -> int:
    bank = json.loads(BANK.read_text())
    atlas = json.loads(ATLAS.read_text())
    curriculum_jobs = {card["canonical_job"] for card in json.loads(CARDS.read_text())["cards"]}
    split_by_video = {row["video_id"]: row["event_split"] for row in atlas["videos"]}
    title_by_video = {row["video_id"]: row["title"] for row in atlas["videos"]}
    by_job_videos: dict[str, set[str]] = defaultdict(set)
    by_job_records: Counter[str] = Counter()
    by_job_segments: Counter[str] = Counter()
    for record in bank["records"]:
        job = record["canonical_job"]
        if job not in curriculum_jobs:
            continue
        video = record["video_id"]
        by_job_videos[job].add(video)
        by_job_records[job] += 1
        by_job_segments[job] += len(record["segments"])
    jobs = sorted(by_job_videos)
    job_rows = []
    for job in jobs:
        videos = by_job_videos[job]
        job_rows.append({
            "canonical_job": job,
            "function_record_count": by_job_records[job],
            "caption_segment_count": by_job_segments[job],
            "video_count": len(videos),
            "train_video_count": sum(split_by_video.get(v) == "train" for v in videos),
            "holdout_video_count": sum(split_by_video.get(v) == "holdout" for v in videos),
            "unassigned_video_count": sum(v not in split_by_video for v in videos),
            "sample_video_ids": sorted(videos)[:12],
        })
    pairs = []
    for left, right in itertools.combinations(jobs, 2):
        shared = by_job_videos[left] & by_job_videos[right]
        pairs.append({"left_job": left, "right_job": right, "shared_video_count": len(shared), "shared_train_video_count": sum(split_by_video.get(v) == "train" for v in shared), "shared_holdout_video_count": sum(split_by_video.get(v) == "holdout" for v in shared), "sample_shared_video_ids": sorted(shared)[:8]})
    report = {
        "schema_version": "1.0",
        "comparison_id": "communication-job-cross-comparison",
        "status": "transcript_video_level_comparison_not_independently_validated",
        "source_evidence_bank": "research/corpus-evidence-bank.json",
        "source_atlas": "research/corpus-pattern-atlas.json",
        "job_count": len(jobs),
        "pair_count": len(pairs),
        "video_denominator": atlas["eligible_video_count"],
        "claim_boundary": "This comparison describes transcript-derived coverage and same-video co-occurrence for the 18 shared curriculum jobs. A video is not an independently verified speaker/event, co-occurrence is not recurrence across independent events, and these counts do not establish effectiveness, intent, delivery meaning or audience outcomes.",
        "job_rows": job_rows,
        "pair_rows": pairs,
        "limitations": ["Speaker and event identity are not independently verified here.", "Same-video co-occurrence is not evidence that jobs are causally related.", "The fixed atlas excludes one restricted source under its source policy.", "Canonical job labels remain provisional and may be wrong or mixed.", "Unclassified and media/publisher records are excluded from the 18-job comparison rather than forced into a curriculum job."],
    }
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Communication-job cross-comparison", "", "Status: **transcript/video-level comparison; not independently validated**.", "", report["claim_boundary"], "", f"Jobs: **{len(jobs)}** · pairwise comparisons: **{len(pairs)}** · eligible video denominator: **{atlas['eligible_video_count']}**.", "", "## Job coverage", "", "| Job | Function records | Caption segments | Videos | Train | Holdout | Unassigned |", "|---|---:|---:|---:|---:|---:|---:|"]
    lines += [f"| `{r['canonical_job']}` | {r['function_record_count']} | {r['caption_segment_count']} | {r['video_count']} | {r['train_video_count']} | {r['holdout_video_count']} | {r['unassigned_video_count']} |" for r in job_rows]
    lines += ["", "## Highest same-video co-occurrence pairs", "", "| Job A | Job B | Shared videos | Train | Holdout |", "|---|---|---:|---:|---:|"]
    lines += [f"| `{r['left_job']}` | `{r['right_job']}` | {r['shared_video_count']} | {r['shared_train_video_count']} | {r['shared_holdout_video_count']} |" for r in sorted(pairs, key=lambda x: (-x['shared_video_count'], x['left_job'], x['right_job']))[:30]]
    lines += ["", "## Limits", ""] + [f"- {limit}" for limit in report["limitations"]]
    OUT_MD.write_text("\n".join(lines) + "\n")
    rows_html = "".join(f"<tr><td><code>{html.escape(r['canonical_job'])}</code></td><td>{r['function_record_count']}</td><td>{r['caption_segment_count']}</td><td>{r['video_count']}</td><td>{r['train_video_count']}</td><td>{r['holdout_video_count']}</td><td>{r['unassigned_video_count']}</td></tr>" for r in job_rows)
    OUT_HTML.write_text(f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Communication-job cross-comparison</title><style>body{{font:15px/1.45 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ccd3da;padding:.4rem;text-align:left}}.notice{{background:#fff6d6;padding:.8rem}}</style><h1>Communication-job cross-comparison</h1><div class="notice">{html.escape(report["claim_boundary"])}</div><p>{len(jobs)} jobs · {len(pairs)} pairs · {atlas["eligible_video_count"]} eligible videos.</p><table><thead><tr><th>Job</th><th>Records</th><th>Segments</th><th>Videos</th><th>Train</th><th>Holdout</th><th>Unassigned</th></tr></thead><tbody>{rows_html}</tbody></table><h2>Limits</h2><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in report['limitations'])}</ul>''')
    print(f"wrote communication-job cross-comparison ({len(jobs)} jobs, {len(pairs)} pairs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
