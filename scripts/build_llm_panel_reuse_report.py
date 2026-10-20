#!/usr/bin/env python3
"""Write a reader-facing inventory of the reusable LLM panel queues."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETS = (
    ("Fieldbook", ROOT / "research/llm-panel-fixed-fieldbook-packets.json"),
    ("Humor/TED expansion", ROOT / "research/llm-panel-expansion-packets.json"),
)
OUT = ROOT / "writeups/llm-panel-reuse-queues.md"


def main() -> None:
    lines = [
        "# Reusable LLM-panel queues",
        "",
        "These are evidence packets prepared for the same two-model, four-rubric review used in the five-job vertical slice. Source identity and internal labels are held in separate keys. A panel result reviews supplied evidence; it does not prove audience response, learning, transfer, or effectiveness.",
        "",
        "| Queue | Packets | Ready to run | Held before model review | What blocks promotion |",
        "|---|---:|---:|---:|---|",
    ]
    for label, path in SETS:
        report = json.loads(path.read_text())
        counts = Counter(packet["review_readiness"] for packet in report["packets"])
        ready = sum(count for state, count in counts.items() if not state.startswith("not_panel_ready"))
        held = report["packet_count"] - ready
        blocker = "Evidence-linked counterexamples are absent." if label == "Fieldbook" else "Two items need five distinct contextual excerpts; all items still need counterexamples."
        lines.append(f"| {label} | {report['packet_count']} | {ready} | {held} | {blocker} |")
    lines += [
        "",
        "## What is ready now",
        "",
        "- All 55 fieldbook cards have five retained-caption excerpts, a bounded lesson, a media caveat, and a private packet key. They may be run to identify wording and evidence problems, but lack controls and therefore cannot be promoted.",
        "- Seventeen of 19 humor/TED candidates have five bounded transcript excerpts and can enter the panel. Two are explicitly held until more distinct source context is retrieved.",
        "- The runner accepts any blinded packet set: `python3 scripts/run_llm_panel.py --packets research/<packet-set>.json --output research/<results>.json`.",
        "",
        "## Decision rule",
        "",
        "Each packet receives source/context, counterexample/scope, lesson-transfer/safety, and adversarial reviews from two local models. Any disagreement, indeterminate answer, absent citation, malformed output, or explicit evidence gap produces `model_panel_revision_or_more_evidence_needed`. No automated result is treated as an effectiveness claim.",
        "",
    ]
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
