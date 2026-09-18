#!/usr/bin/env python3
"""Join lesson-function records to exact retained caption evidence.

The bank is a navigation and teaching source. It preserves caption wording as
stored, including recognition errors, and does not repair or paraphrase it.
"""

from __future__ import annotations

import html
import json
import math
from pathlib import Path


def load_registry(root: Path) -> dict[str, dict]:
    registry = {}
    with (root / "research/segment-registry.jsonl").open() as handle:
        for line in handle:
            row = json.loads(line)
            registry[row["evidence_id"]] = row
    return registry


def source_at(video_url: str | None, seconds: float | None) -> str | None:
    if not video_url or seconds is None:
        return video_url
    separator = "&" if "?" in video_url else "?"
    return f"{video_url}{separator}t={max(0, math.floor(seconds))}s"


def build(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    taxonomy = json.loads((root / "research/corpus-function-taxonomy.json").read_text())
    registry = load_registry(root)
    records = []
    missing = []
    segment_count = 0
    for entry in taxonomy["entries"]:
        for function in entry["functions"]:
            segments = []
            for evidence_id in function["evidence_ids"]:
                row = registry.get(evidence_id)
                if row is None:
                    missing.append(evidence_id)
                    continue
                segments.append({
                    "evidence_id": evidence_id,
                    "caption_ordinal": row["caption_ordinal"],
                    "start_seconds": row["start_seconds"],
                    "end_seconds": row["end_seconds"],
                    "text": row["text"],
                    "word_count": row["word_count"],
                    "source_transcript_file": row["source_transcript_file"],
                })
            segment_count += len(segments)
            start = segments[0]["start_seconds"] if segments else None
            end = segments[-1]["end_seconds"] if segments else None
            video_url = None
            if segments:
                video_url = registry[segments[0]["evidence_id"]].get("video_url")
            records.append({
                "record_id": f"{entry['review_id']}:{function['sequence']}",
                "review_id": entry["review_id"],
                "video_id": entry["video_id"],
                "title": entry["title"],
                "writeup": entry["writeup"],
                "raw_function_label": function["raw_label"],
                "canonical_job": function["canonical_job"],
                "canonicalization_status": "heuristic_or_unclassified_transcript_label",
                "start_seconds": start,
                "end_seconds": end,
                "source_url": source_at(video_url, start),
                "caption_text_status": "retained_caption_text_unrepaired",
                "assembled_caption_text": " ".join(item["text"] for item in segments),
                "segments": segments,
            })
    return {
        "schema_version": "1.0",
        "bank_id": "corpus-exact-caption-evidence-bank",
        "status": "transcript_evidence_navigation_not_validated",
        "claim_boundary": (
            "Caption wording is retained evidence for navigation and context. "
            "It may contain recognition errors and does not establish tone, "
            "intent, delivery, effectiveness, recurrence or listener outcomes. "
            "The assembled text is not a transcript repair."
        ),
        "sources": [
            "research/corpus-function-taxonomy.json",
            "research/segment-registry.jsonl",
        ],
        "summary": {
            "review_count": len({item["review_id"] for item in records}),
            "function_record_count": len(records),
            "caption_segment_record_count": segment_count,
            "missing_evidence_id_count": len(set(missing)),
        },
        "missing_evidence_ids": sorted(set(missing)),
        "records": records,
    }


def write_outputs(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    result = build(root)
    (root / "research/corpus-evidence-bank.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    s = result["summary"]
    (root / "writeups/corpus-evidence-bank.md").write_text(
        "\n".join([
            "# Corpus exact-caption evidence bank", "",
            "Status: **transcript evidence navigation; not validated delivery or outcome evidence**.", "",
            "This bank joins every indexed function record to the retained caption",
            "segments, timestamps, source URL and original transcript file. Caption",
            "wording is preserved as stored; recognition errors are not silently repaired.", "",
            f"- Reviews: {s['review_count']}",
            f"- Function records: {s['function_record_count']}",
            f"- Caption segments linked: {s['caption_segment_record_count']}",
            f"- Missing evidence IDs: {s['missing_evidence_id_count']}",
            "",
            "Use the JSON record for exact segment text and the timestamped source URL.",
            "The assembled text is a navigation convenience, not a corrected transcript.",
        ]) + "\n"
    )
    cards = []
    for record in result["records"]:
        excerpt = html.escape(record["assembled_caption_text"])
        link = html.escape(record["source_url"] or "", quote=True)
        search = html.escape(" ".join([
            record["title"], record["video_id"], record["raw_function_label"],
            record["canonical_job"], record["assembled_caption_text"],
        ]).lower(), quote=True)
        cards.append(
            f"<article class='record' data-search='{search}'><h2>{html.escape(record['title'])}</h2>"
            f"<p><code>{html.escape(record['record_id'])}</code> · <code>{html.escape(record['canonical_job'])}</code> · "
            f"<a href='{link}'>source at timestamp</a></p><p class='label'>{html.escape(record['raw_function_label'] or '[unlabeled]')}</p>"
            f"<blockquote>{excerpt or '[no retained caption text]'}</blockquote></article>"
        )
    browser = """<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Corpus exact-caption evidence bank</title><style>
body{font:16px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a}
input{width:100%;box-sizing:border-box;padding:.7rem;font:inherit;margin:1rem 0 1.5rem}.notice{background:#fff4ce;padding:1rem;border-left:4px solid #b8860b}
.record{border:1px solid #ccd3da;border-radius:8px;padding:1rem;margin:1rem 0}.record h2{margin:.1rem 0;font-size:1.05rem}.label{color:#53606c}blockquote{margin:1rem 0;padding:.8rem 1rem;background:#f5f7f9;white-space:pre-wrap}
code{overflow-wrap:anywhere}
</style><main><h1>Corpus exact-caption evidence bank</h1><div class="notice"><strong>Transcript-only evidence.</strong> Caption wording is retained as stored and may contain recognition errors. This bank does not establish delivery, intent, effectiveness or listener outcomes.</div><p>Search exact words, video IDs, raw labels or provisional canonical jobs.</p><label for="search">Search evidence</label><input id="search" type="search" placeholder="e.g. question, contrast, video ID, phrase"><p id="count" aria-live="polite"></p><section id="records">""" + "\n".join(cards) + """</section></main><script>
const input=document.querySelector('#search'),records=[...document.querySelectorAll('.record')],count=document.querySelector('#count');function filter(){const q=input.value.trim().toLowerCase();let n=0;records.forEach(r=>{const show=!q||r.dataset.search.includes(q);r.hidden=!show;if(show)n++});count.textContent=`Showing ${n} of ${records.length} records`;}input.addEventListener('input',filter);filter();</script>"""
    (root / "writeups/corpus-evidence-bank.html").write_text(browser)
    return result


if __name__ == "__main__":
    result = write_outputs()
    print(json.dumps(result["summary"], indent=2))
