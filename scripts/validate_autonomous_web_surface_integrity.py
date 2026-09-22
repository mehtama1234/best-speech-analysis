#!/usr/bin/env python3
"""Validate local web surfaces, routes and job/card coverage."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SURFACES = [
    "writeups/communication-job-curriculum.html",
    "writeups/communication-job-practice.html",
    "writeups/communication-job-learner-check.html",
    "writeups/shared-provisional-curriculum.html",
    "writeups/shared-lesson-cards.html",
]
AUXILIARY_SURFACES = {
    "writeups/communication-job-listener-record.html": "not an effectiveness claim",
    "writeups/communication-job-listener-stimulus-review-workbook.html": "does not establish that a communication pattern works",
    "writeups/communication-job-listener-stimulus-adjudication.html": "not listener outcome evidence",
}


def validate() -> list[str]:
    errors: list[str] = []
    curriculum = json.loads((ROOT / "research/communication-job-curriculum-index.json").read_text())
    jobs = [x["canonical_job"] for x in curriculum["lessons"]]
    if len(jobs) != 18 or len(set(jobs)) != 18:
        errors.append("canonical curriculum does not contain 18 unique jobs")
    for relative in SURFACES:
        path = ROOT / relative
        if not path.exists():
            errors.append(f"missing web surface: {relative}")
            continue
        source = html.unescape(path.read_text())
        if relative.endswith("communication-job-curriculum.html"):
            if not re.search(r"<html\b[^>]*\blang=['\"]en['\"]", source, flags=re.IGNORECASE):
                errors.append("curriculum surface lacks an English document language")
            if 'id="count" aria-live="polite"' not in source:
                errors.append("curriculum surface lacks an accessible live result count")
            if '<label for="search">' not in source:
                errors.append("curriculum search input is not associated with its label")
        if "provisional" not in source.lower() and "not validated" not in source.lower():
            errors.append(f"{relative} lacks provisional claim boundary")
        for job in jobs:
            if job not in source:
                errors.append(f"{relative} does not expose job {job}")
        for href in re.findall(r"(?:href|src)=[\"']([^\"']+)", source, flags=re.IGNORECASE):
            parsed = urlsplit(href)
            if parsed.scheme or href.startswith("//") or href.startswith("data:"):
                continue
            target = parsed.path
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{relative} links to missing local target {href}")
        if relative.endswith("communication-job-practice.html"):
            if source.count('lesson_id') < 18 or source.count('id="capture-start"') != 1:
                errors.append("practice surface lacks 18 embedded lessons or local capture control")
            for control_id in ("lesson", "participant", "accessibility", "consent", "capture-mode", "import-file"):
                if f'<label for="{control_id}">' not in source:
                    errors.append(f"practice control {control_id} is not associated with its label")
        if relative.endswith("communication-job-learner-check.html"):
            if source.count("<fieldset") < 18 or len(re.findall(r"name=['\"][^'\"]+_task_ids['\"]", source)) != 18 or "name='participant_code'" not in source:
                errors.append("learner surface lacks 18 job task groups or capture schema")
        if relative.endswith("shared-lesson-cards.html") and source.count('provisional-job-') < 18:
            errors.append("shared lesson-card surface lacks 18 card IDs")
    for relative, marker in AUXILIARY_SURFACES.items():
        path = ROOT / relative
        if not path.exists():
            errors.append(f"missing auxiliary web surface: {relative}")
            continue
        source = html.unescape(path.read_text())
        if not re.search(r"<html\b[^>]*\blang=['\"]en['\"]", source, flags=re.IGNORECASE):
            errors.append(f"{relative} lacks an English document language")
        if marker.lower() not in source.lower():
            errors.append(f"{relative} lacks its claim boundary marker")
        for href in re.findall(r"(?:href|src)=[\"']([^\"']+)", source, flags=re.IGNORECASE):
            parsed = urlsplit(href)
            if parsed.scheme or href.startswith("//") or href.startswith("data:"):
                continue
            target = parsed.path
            if target and not (path.parent / target).resolve().exists():
                errors.append(f"{relative} links to missing local target {href}")
    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("autonomous web-surface integrity valid: 5 pages, 18 jobs, local links resolved")
