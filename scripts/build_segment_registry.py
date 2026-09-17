#!/usr/bin/env python3
"""Normalize transcript captions into provenance-preserving research units.

Labels produced here are candidate speech-function labels. They are retrieval
and review aids, not claims that a speaker intended a particular function.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


PATTERNS = {
    "question": re.compile(r"\?\s*$|^(?:why|how|what|when|where|who|can|could|would|is|are|do|does|did|have|has|will)\b", re.I),
    "example": re.compile(r"\b(?:for example|for instance|such as|imagine|let me give you)\b", re.I),
    "definition": re.compile(r"\b(?:means|defined as|in other words|what I mean|is when)\b", re.I),
    "contrast_or_disagreement": re.compile(r"\b(?:however|although|instead|disagree|wrong|not true|on the other hand|I disagree|rather than)\b|\bnot\b[^.!?]{0,50}\bbut\b", re.I),
    "uncertainty_or_qualification": re.compile(r"\b(?:maybe|perhaps|probably|possibly|I think|I believe|might|could|it seems)\b", re.I),
    "conclusion_or_summary": re.compile(r"\b(?:in conclusion|to summarize|the point is|in short|what matters)\b", re.I),
    "call_to_action": re.compile(r"\b(?:we must|we need to|you should|let us|let's|take action|do not give up)\b", re.I),
    "story_or_personal_experience": re.compile(r"\b(?:when I was|I remember|my father|my mother|one day|years ago|I went|I saw)\b", re.I),
}


def candidate_functions(text: str) -> list[str]:
    labels = [name for name, pattern in PATTERNS.items() if pattern.search(text)]
    return labels or ["unclassified"]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry = {
        row["video_id"]: row
        for row in (
            json.loads(line)
            for line in (root / "data/metadata/video-registry.jsonl").read_text().splitlines()
            if line.strip()
        )
    }
    output = root / "research/segment-registry.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    label_counts: dict[str, int] = {}
    with output.open("w") as handle:
        for video_id in sorted(registry):
            path = root / "data/transcripts" / f"{video_id}.json"
            if not path.exists():
                continue
            payload = json.loads(path.read_text())
            video = registry[video_id]
            for ordinal, caption in enumerate(payload.get("transcript") or []):
                text = " ".join(str(caption.get("text", "")).split())
                if not text:
                    continue
                start_ms = int(float(caption.get("startMs", 0)))
                end_ms = int(float(caption.get("endMs", start_ms)))
                labels = candidate_functions(text)
                for label in labels:
                    label_counts[label] = label_counts.get(label, 0) + 1
                row = {
                    "evidence_id": f"{video_id}:{ordinal:05d}",
                    "video_id": video_id,
                    "video_url": video["url"],
                    "title": video.get("title"),
                    "channel": video.get("channel"),
                    "playlist_memberships": video.get("playlist_memberships", []),
                    "caption_ordinal": ordinal,
                    "start_seconds": round(start_ms / 1000, 3),
                    "end_seconds": round(end_ms / 1000, 3),
                    "text": text,
                    "word_count": len(re.findall(r"\b[\w’'-]+\b", text)),
                    "candidate_speech_functions": labels,
                    "label_type": "heuristic_retrieval_aid",
                    "interpretation_status": "requires_review",
                    "source_transcript_file": f"data/transcripts/{video_id}.json",
                }
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                count += 1
    summary = {"evidence_segment_count": count, "candidate_function_counts": label_counts}
    (root / "research/segment-registry-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
