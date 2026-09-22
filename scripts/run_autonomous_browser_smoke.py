#!/usr/bin/env python3
"""Run the core browser smoke checks and write a reproducible receipt."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/autonomous-browser-smoke.json"
MD = ROOT / "writeups/autonomous-browser-smoke.md"
CHECKS = [
    "scripts/check_shared_curriculum_browser.py",
    "scripts/check_communication_job_practice_browser.py",
    "scripts/check_communication_job_learner_browser.py",
    "scripts/check_communication_job_listener_browser.py",
    "scripts/check_vertical_slice_lesson_browser.py",
    "scripts/check_vertical_slice_02_learner_browser.py",
    "scripts/check_independent_review_forms_browser.py",
    "scripts/check_communication_job_delivery_browser.py",
    "scripts/check_multimodal_independent_review_browser.py",
    "scripts/check_listener_stimulus_adjudication_browser.py",
    "scripts/check_listener_stimulus_review_browser.py",
    "scripts/check_vertical_slice_02_review_browser.py",
    "scripts/check_practice_pwa_browser.py",
    "scripts/check_recovered_pattern_priority_review_browser.py",
    "scripts/check_unified_pattern_library_browser.py",
    "scripts/check_presentation_builder_browser.py",
    "scripts/check_professional_pattern_fieldbook_browser.py",
]


def run() -> dict:
    env = os.environ.copy()
    user_libs = Path("/tmp/best-speech-libs/usr/lib/x86_64-linux-gnu")
    if user_libs.exists():
        env["LD_LIBRARY_PATH"] = f"{user_libs}:{env.get('LD_LIBRARY_PATH', '')}".rstrip(":")
    results = []
    for relative in CHECKS:
        completed = subprocess.run([sys.executable, relative], cwd=ROOT, env=env, text=True, capture_output=True)
        results.append({
            "script": relative,
            "return_code": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        })
    failed = [x["script"] for x in results if x["return_code"] != 0]
    return {
        "schema_version": "1.0",
        "receipt_id": "autonomous-browser-smoke",
        "status": "core_browser_smoke_passed" if not failed else "browser_smoke_failed",
        "check_count": len(results),
        "passed_check_count": len(results) - len(failed),
        "failed_checks": failed,
        "checks": results,
        "claim_boundary": "This receipt verifies local rendering, navigation, export and bounded browser interactions. It does not establish learner outcomes, listener outcomes, evidence validity or communication effectiveness.",
        "environment_note": "Uses Playwright Chromium; when present, /tmp/best-speech-libs supplies user-space shared libraries and is not a repository artifact.",
    }


def render(report: dict) -> str:
    lines = ["# Autonomous browser smoke receipt", "", f"Status: **{report['status']}**.", "", report["claim_boundary"], "", f"Checks passed: **{report['passed_check_count']}/{report['check_count']}**.", "", "| Script | Result | Output |", "|---|---|---|"]
    for check in report["checks"]:
        lines.append(f"| `{check['script']}` | `{check['return_code']}` | {check['stdout'] or check['stderr']} |")
    lines += ["", report["environment_note"], ""]
    return "\n".join(lines)


if __name__ == "__main__":
    report = run()
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    MD.write_text(render(report))
    print(f"autonomous browser smoke: {report['status']} ({report['passed_check_count']}/{report['check_count']})")
    raise SystemExit(0 if not report["failed_checks"] else 1)
