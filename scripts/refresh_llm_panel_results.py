#!/usr/bin/env python3
"""Reparse retained raw panel outputs after a parser-only improvement."""
from __future__ import annotations
import json
from pathlib import Path
from run_llm_panel import OUT, adjudicate, parse

def main() -> None:
    report = json.loads(OUT.read_text())
    for row in report["judgments"]:
        row["judgment"] = parse(row["raw_output"]) or {
            "decision": "indeterminate", "citations": [],
            "reason": "Model output was malformed or noncommittal.", "confidence": "low",
        }
    ids = sorted({row["blind_packet_id"] for row in report["judgments"]})
    report["adjudications"] = [adjudicate(report["judgments"], packet_id) for packet_id in ids]
    report["parser_status"] = "plain_language_recovery_with_fail_closed_fallback"
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"refreshed {len(report['judgments'])} retained raw panel judgments")

if __name__ == "__main__": main()
