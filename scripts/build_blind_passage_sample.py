#!/usr/bin/env python3
"""Select contiguous caption blocks independently of keyword hits or judgments."""
import hashlib
import itertools
import json
import random
from pathlib import Path

SEED = 20260917
VIDEO_COUNT = 24
BLOCK_SIZE = 50
PADDING = 5


def choose(block_counts, count=VIDEO_COUNT, seed=SEED):
    if count < 1 or any(n < 1 for n in block_counts.values()):
        raise ValueError("Positive sample size and block counts required")
    rng = random.Random(seed)
    videos = sorted(block_counts)
    selected = rng.sample(videos, min(count, len(videos)))
    return {vid: rng.randrange(block_counts[vid]) for vid in selected}


def read_groups(path):
    with path.open() as stream:
        rows = (json.loads(s) for s in stream if s.strip())
        previous = None
        for vid, group in itertools.groupby(rows, key=lambda r: r["video_id"]):
            if previous is not None and vid <= previous:
                raise ValueError("Registry must be grouped in increasing video-ID order")
            previous = vid
            batch = list(group)
            ordinals = [r["caption_ordinal"] for r in batch]
            if ordinals != sorted(set(ordinals)):
                raise ValueError("Caption ordinals must be unique and increasing")
            yield vid, batch


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    registry = root / "research/segment-registry.jsonl"
    review_path = root / "research/contextual-label-reviews.json"
    frame = {}
    for vid, rows in read_groups(registry):
        frame[vid] = {"segment_count": len(rows), "block_count": (len(rows) + BLOCK_SIZE - 1) // BLOCK_SIZE}
    chosen = choose({vid: r["block_count"] for vid, r in frame.items()})
    reviews = json.loads(review_path.read_text())["reviews"]
    prior_context = {eid for r in reviews for eid in r["context_evidence_ids"]}
    passages = []
    fields = ("evidence_id", "start_seconds", "end_seconds", "text")
    for vid, rows in read_groups(registry):
        if vid not in chosen:
            continue
        block = chosen[vid]
        first = block * BLOCK_SIZE
        core = rows[first:first + BLOCK_SIZE]
        context = rows[max(0, first - PADDING):first + BLOCK_SIZE + PADDING]
        core_ids = {r["evidence_id"] for r in core}
        passages.append({"passage_id": f"blind-v1:{vid}:{block:04d}",
                         "video_id": vid, "title": rows[0].get("title"),
                         "block_index": block, "core_count": len(core),
                         "video_block_count": frame[vid]["block_count"],
                         "design_video_probability": len(chosen) / len(frame),
                         "design_core_block_probability": len(chosen) / len(frame) / frame[vid]["block_count"],
                         "core_evidence_ids": [r["evidence_id"] for r in core],
                         "prior_context_overlap_ids": sorted(core_ids & prior_context),
                         "review_status": "unreviewed_at_selection_see_separate_passage_reviews",
                         "rows": [{**{k: r[k] for k in fields}, "role": "core" if r["evidence_id"] in core_ids else "boundary_context"} for r in context],
                         "post_selection_fallback_count": sum(r["candidate_speech_functions"] == ["unclassified"] for r in core)})
    passages.sort(key=lambda p: list(chosen).index(p["video_id"]))
    report = {"schema_version": "1.0", "seed": SEED, "video_sample_size": len(chosen),
              "block_size_captions": BLOCK_SIZE, "boundary_padding_captions": PADDING,
              "sampling_frame": frame, "passages": passages,
              "policy": "Two-stage seeded uniform selection: videos, then one fixed nonoverlapping caption block per selected video. All nonempty registry videos eligible. No keyword, reviewed-support, media-availability or title filter. Padding aids interpretation but is not probability-sampled core. Block boundaries are not speech-episode boundaries. Blind means selection ignores labels; this is not blinded independent adjudication.",
              "source_sha256": {str(p.relative_to(root)): digest(p) for p in (registry, review_path, Path(__file__).resolve())}}
    (root / "research/blind-passage-sample.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    lines = ["# Label-independent passage review packet", "", report["policy"], "",
             f"Seed {SEED}; {len(chosen)} of {len(frame)} transcript-bearing videos selected. "
             "Core blocks contain up to 50 retained captions; five surrounding captions are supplied on each side when available. "
             "Keywords and legacy judgments are hidden in this packet, not erased from the source.", "",
             "This is the selection-time packet, not a live review-status tracker; consult research/passage-context-reviews.json for completed reviews. Record speaker turns, promotional boundaries, transcription defects, "
             "speech functions, claims, supporting examples and counterexamples. Expand incomplete episodes before interpreting them. "
             "Do not turn self-description into visible behavior or internal-state facts.", ""]
    for p in passages:
        lines += [f"## {p['passage_id']}", "", f"Source title (unverified metadata): {p['title']}",
                  f"Core: {p['core_count']} captions; prior reviewed-context overlap: {len(p['prior_context_overlap_ids'])}.", ""]
        for r in p["rows"]:
            lines.append(f"- **{r['role']}** `{r['evidence_id']}` {r['start_seconds']}–{r['end_seconds']} s: {r['text']}")
        lines.append("")
    lines += ["## Limits of the design", "", "This is a discovery pilot, not a completed corpus analysis. "
              "Equal video selection differs from equal-time or equal-caption sampling. Within-video block probabilities differ with video length; short tail blocks are retained. "
              "The manifest records model-based inclusion probabilities for core blocks, not padding. A fixed pseudorandom seed provides reproducibility; no population rate is inferred here. "
              "Missing transcripts, duplicate uploads, repeated speakers, edits and unknown formats limit generalization. "
              "Prior-review overlap is disclosed, not filtered out or treated as a held-out test.", ""]
    (root / "writeups/blind-passage-review-packet.md").write_text("\n".join(lines))
    print(json.dumps({"videos": len(chosen), "eligible_videos": len(frame),
                      "core_captions": sum(p["core_count"] for p in passages),
                      "fallback_core_captions": sum(p["post_selection_fallback_count"] for p in passages),
                      "first_passage_ids": [p["passage_id"] for p in passages[:3]]}))


if __name__ == "__main__":
    main()
