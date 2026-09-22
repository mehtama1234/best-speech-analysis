#!/usr/bin/env python3
"""Fail closed on a few high-risk public claims about corpus validation.

This is a wording guardrail, not a semantic fact checker. It protects the
distinction between analyst-authored transcript review, machine recovery and
independent human/outcome validation from being accidentally erased in the
top-level user-facing documents.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DOCS = (
    ROOT / "README.md",
    ROOT / "PROJECT_STATUS.md",
    ROOT / "SPEECH_ANALYSIS_END_TO_END_GOAL.md",
    ROOT / "END_TO_END_WORK_REVIEW.md",
    ROOT / "writeups/start-here.md",
    ROOT / "writeups/amazing-presentation-patterns.md",
    ROOT / "writeups/full-inventory-pattern-candidates.md",
    ROOT / "writeups/all-55-pattern-evidence.md",
    ROOT / "research/full-inventory-pattern-candidates.json",
    ROOT / "research/all-55-pattern-evidence.json",
    ROOT / "scripts/build_full_inventory_pattern_candidates.py",
    ROOT / "scripts/build_all_55_pattern_evidence.py",
    ROOT / "writeups/corpus-coverage-audit.md",
    ROOT / "writeups/amazing-presentation-patterns.html",
    ROOT / "writeups/corpus-30-day-study-route.html",
    ROOT / "scripts/build_corpus_coverage_report.py",
    ROOT / "scripts/build_amazing_presentation_patterns.py",
    ROOT / "scripts/build_corpus_30_day_route.py",
    ROOT / "writeups/corpus-pattern-atlas.html",
    ROOT / "writeups/full-corpus-delivery-inspection.html",
    ROOT / "writeups/stakeholder-tutorial.html",
    ROOT / "scripts/build_corpus_atlas_page.py",
    ROOT / "scripts/build_full_corpus_delivery_inspection.py",
)

FORBIDDEN = (
    re.compile(r"\b(?:canonical\s+)?human-reviewed\s+(?:corpus|videos?|records?)\b", re.I),
    re.compile(r"\b(?:all\s+)?(?:420|450)\s+(?:videos?|recordings?).{0,40}\b(?:analy[sz]ed|reviewed)\b", re.I | re.S),
    re.compile(r"\bfully\s+analy[sz]ed\b", re.I),
)

REQUIRED_DISCLOSURES = {
    ROOT / "README.md": ("project-generated, single-pass", "not the same as 395 independently"),
    ROOT / "PROJECT_STATUS.md": ("not independently",),
    ROOT / "writeups/start-here.md": ("not independent human validation",),
}


def audit() -> dict:
    violations = []
    missing = []
    for path in PUBLIC_DOCS:
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                violations.append({"path": str(path.relative_to(ROOT)), "line": line, "text": match.group(0)})
    for path, disclosures in REQUIRED_DISCLOSURES.items():
        text = path.read_text(encoding="utf-8").lower()
        for disclosure in disclosures:
            if disclosure.lower() not in text:
                missing.append({"path": str(path.relative_to(ROOT)), "disclosure": disclosure})
    return {
        "schema_version": "1.0",
        "audit_id": "public-claim-boundaries",
        "status": "public_claim_boundaries_valid" if not violations and not missing else "public_claim_boundaries_failed",
        "scanned_document_count": len(PUBLIC_DOCS),
        "violations": violations,
        "missing_disclosures": missing,
        "claim_boundary": "This checks selected wording guardrails; it does not validate corpus meaning, human review or communication effectiveness.",
    }


def main() -> int:
    result = audit()
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "public_claim_boundaries_valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
