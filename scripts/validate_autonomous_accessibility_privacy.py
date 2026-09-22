#!/usr/bin/env python3
"""Check basic accessibility, consent and local-data boundaries on user surfaces."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "writeups/communication-job-curriculum.html",
    "writeups/communication-job-practice.html",
    "writeups/communication-job-learner-check.html",
    "writeups/communication-job-listener-record.html",
    "writeups/shared-provisional-curriculum.html",
    "writeups/shared-lesson-cards.html",
    "writeups/blinded-review-packet.html",
]
FORMS = {
    "writeups/communication-job-practice.html": ("local", "consent", "effectiveness"),
    "writeups/communication-job-learner-check.html": ("consent", "accessib", "effectiveness"),
    "writeups/communication-job-listener-record.html": ("consent", "accessib", "effectiveness"),
    "writeups/blinded-review-packet.html": ("localstorage", "not evidence", "draft"),
}


def validate() -> list[str]:
    errors: list[str] = []
    forbidden = ("fetch(", "xmlhttprequest", "sendbeacon")
    viewport = re.compile(r"<meta\b[^>]*name\s*=\s*['\"]viewport['\"]", re.I)
    for relative in PAGES:
        path = ROOT / relative
        if not path.exists():
            errors.append(f"missing page: {relative}")
            continue
        source = path.read_text().lower()
        if not viewport.search(source):
            errors.append(f"{relative} lacks a responsive viewport declaration")
        if "<h1" not in source or "<title" not in source:
            errors.append(f"{relative} lacks title or h1")
        if any(token in source for token in forbidden):
            errors.append(f"{relative} contains a network submission primitive")
        if relative in FORMS:
            for phrase in FORMS[relative]:
                if phrase not in source:
                    errors.append(f"{relative} lacks {phrase} boundary")
            if "<label" not in source or "<button" not in source:
                errors.append(f"{relative} lacks labelled control structure")
    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("autonomous accessibility/privacy audit valid: 7 pages, responsive controls, consent and local-data boundaries")
