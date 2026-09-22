#!/usr/bin/env python3
"""Import externally hosted transcript leads with explicit provenance."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_URL = "https://service.unibas.it/documenti/docenti_materiale_didattico/010934_81240_Transcript%20-%20Justin%20Timberlake.pdf"


def main() -> int:
    from pypdf import PdfReader

    raw_dir = ROOT / "data/external-source-recovery"
    raw_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = raw_dir / "tWhHf7IeFmo-justin-timberlake-transcript.pdf"
    if not pdf_path.exists():
        urllib.request.urlretrieve(PDF_URL, pdf_path)
    reader = PdfReader(str(pdf_path))
    segments = []
    for page_number, page in enumerate(reader.pages):
        text = (page.extract_text() or "").strip()
        for sequence, paragraph in enumerate(p for p in text.split("\n") if p.strip()):
            segments.append({
                "sequence": len(segments),
                "page": page_number,
                "text": paragraph.strip(),
            })
    row = {
        "video_id": "tWhHf7IeFmo",
        "source_url": "https://youtu.be/tWhHf7IeFmo",
        "external_transcript_url": PDF_URL,
        "source_file": str(pdf_path.relative_to(ROOT)),
        "status": "external_transcript_candidate",
        "review_status": "source_identity_and_alignment_not_human_verified",
        "language": "en",
        "timestamp_status": "not_available_in_external_pdf",
        "segments": segments,
        "claim_boundary": "External transcript candidate; not canonical review evidence and not counted as timestamped direct recovery.",
    }
    out = ROOT / "research/external-source-transcripts.jsonl"
    out.write_text(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"video_id": row["video_id"], "pages": len(reader.pages), "segments": len(segments), "output": str(out)}))


if __name__ == "__main__":
    main()
