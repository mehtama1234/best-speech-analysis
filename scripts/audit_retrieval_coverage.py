#!/usr/bin/env python3
"""Corpus census of stored retrieval labels, not semantic coverage or recall."""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


def census(rows, targets, contexts):
    videos = defaultdict(Counter)
    labels = Counter()
    total = Counter()
    for row in rows:
        vid, eid = row["video_id"], row["evidence_id"]
        candidates = set(row["candidate_speech_functions"])
        fallback = candidates == {"unclassified"}
        labels.update(candidates)
        for bucket in (total, videos[vid]):
            bucket["segments"] += 1
            bucket["unclassified_segments"] += int(fallback)
            bucket["contextual_target_segments"] += int(eid in targets)
            bucket["inspected_context_segments"] += int(eid in contexts)
    return {"totals": dict(total), "videos_with_segments": len(videos),
            "stored_label_occurrences": dict(sorted(labels.items())),
            "by_video": {vid: dict(counts) for vid, counts in sorted(videos.items())}}


def main():
    root = Path(__file__).resolve().parents[1]
    source = root / "research/segment-registry.jsonl"
    reviews_path = root / "research/contextual-label-reviews.json"
    reviews = json.loads(reviews_path.read_text())["reviews"]
    targets = {r["evidence_id"] for r in reviews}
    contexts = {eid for r in reviews for eid in r["context_evidence_ids"]}
    digest = hashlib.sha256()
    def rows():
        with source.open("rb") as stream:
            for line in stream:
                digest.update(line)
                if line.strip():
                    yield json.loads(line)
    report = census(rows(), targets, contexts)
    report.update({"schema_version": "1.0", "review_records": len(reviews),
                   "policy": "Census of stored heuristic retrieval labels. Unclassified is not meaningless. Context-window membership is not complete reading or semantic review of every caption. Counts do not estimate precision, recall or real-world effectiveness.",
                   "source_sha256": {"research/segment-registry.jsonl": digest.hexdigest(),
                                     "research/contextual-label-reviews.json": hashlib.sha256(reviews_path.read_bytes()).hexdigest(),
                                     "scripts/audit_retrieval_coverage.py": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}})
    (root / "research/retrieval-coverage-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    t = report["totals"]
    lines = ["# Corpus retrieval coverage", "", report["policy"], "",
             f"The stored registry has {t['segments']:,} segments in {report['videos_with_segments']} videos. "
             f"{t['unclassified_segments']:,} segments ({t['unclassified_segments']/t['segments']:.1%}) have only the unclassified fallback.", "",
             f"{t['contextual_target_segments']} distinct segments are targets of contextual assistant reviews; "
             f"{t['inspected_context_segments']} distinct segments appear in their inspected context windows. "
             "Overlapping windows are deduplicated. Neither number proves full-transcript reading.", "",
             "| Stored candidate | Segment occurrences |", "| --- | ---: |"]
    lines += [f"| `{label}` | {count:,} |" for label, count in report["stored_label_occurrences"].items()]
    lines += ["", "Labels can overlap, so the occurrence column is not additive. "
              "The JSON includes per-video denominators. The existing rules use narrow phrase patterns, so unclassified passages can contain stories, claims, transitions or other substantive functions. "
              "The three contextually inspected fallback cases demonstrate this possibility but do not estimate its frequency.", "",
              "Next sampling should include independently selected contiguous passages from both labelled and unclassified strata, balanced across videos and formats. "
              "Use complete speech episodes, establish speaker/promotion boundaries, and retain selection probabilities before estimating corpus rates. "
              "Do not use these hand-selected reviews as a held-out quality score.", ""]
    (root / "writeups/retrieval-coverage-audit.md").write_text("\n".join(lines))
    print(json.dumps({"totals": t, "videos": report["videos_with_segments"]}))


if __name__ == "__main__":
    main()
