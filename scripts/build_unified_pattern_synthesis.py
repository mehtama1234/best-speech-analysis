#!/usr/bin/env python3
"""Build a reader-facing synthesis of fixed-corpus and wave-2 candidates."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = ROOT / "research/all-55-pattern-evidence.json"
CARDS = ROOT / "research/shared-lesson-cards.json"
WAVE2 = ROOT / "research/wave-2-unified-candidate-crosswalk.json"
OUTPUT = ROOT / "writeups/unified-pattern-synthesis.md"

def main() -> int:
    patterns = json.loads(PATTERNS.read_text(encoding="utf-8"))
    cards = json.loads(CARDS.read_text(encoding="utf-8"))
    wave2 = json.loads(WAVE2.read_text(encoding="utf-8")) if WAVE2.is_file() else {"rows": []}
    lines = [
        "# Unified Speaking Pattern Synthesis",
        "",
        "Status: **candidate synthesis; not independent validation or effectiveness evidence**.",
        "",
        "This page joins the fixed speech corpus to the external communication-and-humor atlas. The fixed layer contains 55 transcript-derived presentation-pattern candidates across 395 full-context reviews. The companion guide uses selected examples from ten coaching, storytelling and humor sources. This page shows the 19 provisional rows from the Ali Siddiq, Dry Bar Comedy and TED expansion slices; it does not contain every source in the atlas.",
        "",
        "For every source, its type, transcript coverage and current integration state, read the [speech, humor and communication source map](cross-repo-communication-source-map.md).",
        "",
        "## How to use this synthesis",
        "",
        "Start with a communication problem, choose a candidate form, inspect the exact linked transcript context, read the counterexample and boundary notes, then practise the underlying choice in a new situation. Treat every form below as a hypothesis until independent function, identity, recurrence, delivery, learner, and listener gates are complete.",
        "",
        "## Fixed-corpus candidate patterns",
        "",
        "| Pattern | Category | Canonical videos | Recovered videos | Candidate form | Exact evidence anchor | Status |",
        "|---|---|---:|---:|---|---|---|",
    ]
    for item in patterns["patterns"]:
        form = item.get("candidate_form", "").replace("|", "\\|")
        writeup = item.get("example_writeup")
        link = Path(writeup).name if writeup else None
        evidence_ids = ", ".join(item.get("example_evidence_ids", [])[:3])
        anchor = f"[{item.get('example_label','evidence')}]({link}) — `{evidence_ids}`" if link else "none indexed"
        lines.append(f"| `{item['pattern_id']}` | {item.get('category','')} | {item.get('canonical_video_count',0)} | {item.get('direct_recovered_video_count',0)} | {form} | {anchor} | {item.get('status','')} |")
    lines += [
        "",
        "## Existing practice-job bridge",
        "",
        "The 18 shared lesson cards are the practice layer. They are provisional and should be selected by communication problem, not by celebrity or channel:",
        "",
        "| Job | Lesson card | Evidence state |",
        "|---|---|---|",
    ]
    for card in cards["cards"]:
        lines.append(f"| `{card['canonical_job']}` | `{card['card_id']}` | {card.get('status','')} |")
    lines += [
        "",
        "## Expansion-source candidates",
        "",
        "| Source | Candidate | Jobs | Evidence refs | Status |",
        "|---|---|---|---|---|",
    ]
    for row in wave2.get("rows", []):
        jobs = ", ".join(row.get("communication_jobs", []))
        refs = ", ".join(row.get("evidence_refs", []))
        lines.append(f"| `{row['source']}` | `{row['candidate_pattern']}` | {jobs} | {refs} | provisional; contextual review required |")
    lines += [
        "",
        "## Claim boundary",
        "",
        "Keyword hits, transcript recurrence, internal interpretations, generated lessons, browser checks, and synthetic practice records do not establish that a pattern causes understanding, trust, memory, action, or better communication. Independent reviewers must preserve disagreement and missingness. Learner records test teachability; listener studies test bounded outcomes; neither substitutes for the other.",
        "",
        "## Next evidence action",
        "",
        "Run the 162-item label-blinded priority review first, then route the 19 expansion candidates through full-context review. Do not merge the expansion rows into the fixed-corpus pattern count until the corresponding evidence gates are recorded.",
        "",
    ]
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({len(patterns['patterns'])} fixed patterns, {len(wave2.get('rows', []))} wave-2 rows)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
