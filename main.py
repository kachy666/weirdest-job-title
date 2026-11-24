#!/usr/bin/env python3
"""Weirdest Job Title: Blind Judge Showdown entry.

Writes exactly one job title (60 characters max, nothing else)
to /output/entry.txt. A job title is a few words naming an odd
job, so validate() also rejects a title with fewer than 2 words.
"""

import os
import re
import sys

TITLE = "Lost Left Sock Detective"

OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/entry.txt")


def validate(text: str) -> None:
    """Enforce the gate: 1-60 chars of clean UTF-8 text, one line."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not 1 <= len(text) <= 60:
        raise ValueError(f"entry must be 1-60 characters, got {len(text)}")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if "  " in text:
        raise ValueError("entry has double spaces")
    if re.search(r"[\t\r\n\x00-\x1f\x7f]", text):
        raise ValueError("entry has tabs, newlines or control characters")
    if re.search(r"[\u200b-\u200f\u202a-\u202e\ufeff]", text):
        raise ValueError("entry has invisible characters")
    words = [w for w in text.split(" ") if w]
    if len(words) < 2:
        raise ValueError("entry must be at least 2 words (a job title)")


def main() -> int:
    validate(TITLE)
    parent = os.path.dirname(OUTPUT_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(TITLE)
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != TITLE:
        raise ValueError(
            f"round-trip mismatch: wrote {TITLE!r}, read back {written!r}"
        )
    print(f"wrote {len(TITLE)} chars to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
