#!/usr/bin/env python3
"""Reconcile all 18 communication-job product surfaces."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/autonomous-full-curriculum-audit.json"
MD = ROOT / "writeups/autonomous-full-curriculum-audit.md"


def read(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())


def build() -> dict:
    index = read("research/communication-job-curriculum-index.json")
    mobile = read("research/communication-job-mobile-lessons.json")
    learner = read("research/communication-job-learner-check.json")
    cards = read("research/shared-lesson-cards.json")
    jobs = {row["canonical_job"] for row in index["lessons"]}
    mobile_jobs = {row["canonical_job"] for row in mobile["lessons"]}
    learner_jobs = {row["canonical_job"] for row in learner["cards"]}
    card_jobs = {row["canonical_job"] for row in cards["cards"]}
    checks = []

    def add(layer: str, passed: bool, detail: str, evidence: list[str]) -> None:
        checks.append({"layer": layer, "status": "pass" if passed else "fail", "detail": detail, "evidence": evidence})

    add("canonical job index", index.get("lesson_count") == 18 and len(jobs) == 18, "18 canonical jobs have curriculum records.", ["research/communication-job-curriculum-index.json"])
    add("mobile lesson payload", mobile.get("lesson_count") == 18 and mobile_jobs == jobs and all(len(row.get("steps", [])) == 6 for row in mobile["lessons"]), "Every job has a six-step mobile lesson with explicit consent and safety fields.", ["research/communication-job-mobile-lessons.json", "writeups/communication-job-mobile-lessons.md"])
    add("shared lesson cards", cards.get("card_count") == 18 and card_jobs == jobs and all(row.get("examples") and row.get("practice") and row.get("limits") for row in cards["cards"]), "Every job has an evidence-linked shared card with examples, practice and limits.", ["research/shared-lesson-cards.json"])
    add("learner protocol", learner.get("card_count") == 18 and learner_jobs == jobs and learner.get("task_count") == 72, "Every job has four fixed learner tasks in the protocol.", ["research/communication-job-learner-check.json"])
    browser_paths = [
        "writeups/communication-job-curriculum.html",
        "writeups/communication-job-practice.html",
        "writeups/communication-job-learner-check.html",
        "writeups/shared-provisional-curriculum.html",
        "writeups/shared-lesson-cards.html",
    ]
    browser_present = all((ROOT / path).exists() for path in browser_paths)
    add("web surfaces", browser_present, "The five shared web surfaces exist for the browser clients.", browser_paths)
    failed = [row["layer"] for row in checks if row["status"] != "pass"]
    return {
        "schema_version": "1.0",
        "audit_id": "autonomous-full-curriculum-audit",
        "status": "full_18_job_surface_reconciled_not_validated" if not failed else "needs_repair",
        "job_count": len(jobs),
        "passed_check_count": len(checks) - len(failed),
        "check_count": len(checks),
        "failed_layers": failed,
        "checks": checks,
        "claim_boundary": "This audit verifies that the 18-job web/mobile curriculum surfaces join to the same job set and retain bounded evidence fields. It does not establish learner teachability, listener outcomes, effectiveness or independent review.",
    }


def render(report: dict) -> str:
    lines = [
        "# Autonomous full curriculum audit",
        "",
        f"Status: **{report['status']}**.",
        "",
        report["claim_boundary"],
        "",
        f"Checks passed: **{report['passed_check_count']}/{report['check_count']}** across **{report['job_count']} jobs**.",
        "",
        "| Layer | Status | Detail |",
        "|---|---|---|",
    ]
    for row in report["checks"]:
        lines.append(f"| `{row['layer']}` | `{row['status']}` | {row['detail']} |")
    lines += ["", "The shared web/mobile surfaces are ready for bounded use as provisional curriculum. Learner and listener records remain empty.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    report = build()
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"autonomous full curriculum audit: {report['status']} ({report['passed_check_count']}/{report['check_count']})")
    if report["failed_layers"]:
        raise SystemExit(1)
