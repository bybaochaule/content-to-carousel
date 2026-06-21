#!/usr/bin/env python3
"""Check image-generation prompts for forbidden terms.

This script is deterministic and local-only. It is intended for prompts that will
be sent to an image-generation model, not for full skill documentation.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FORBIDDEN_TERMS = [
    "carousel",
    "slide",
    "slides",
    "slide deck",
    "multi-slide",
    "swipe",
    "sequence",
    "series",
    "panel",
    "set of",
    "collection",
    "contact sheet",
    "grid",
    "collage",
    "mockup",
    "preview",
    "part 1 of",
    "one of eight",
    "batch",
]

REQUIRED_START = "You are creating ONE standalone social media post design."


def find_forbidden(text: str) -> list[str]:
    lowered = text.lower()
    hits: list[str] = []
    for term in FORBIDDEN_TERMS:
        pattern = r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, lowered):
            hits.append(term)
    return hits


def lint_prompt(text: str, require_start: bool = True) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    stripped = text.lstrip()
    if require_start and not stripped.startswith(REQUIRED_START):
        errors.append(f"Prompt must start with: {REQUIRED_START}")

    hits = find_forbidden(text)
    for term in hits:
        errors.append(f"Forbidden image prompt term found: {term}")

    if "one standalone social media post design" not in text.lower():
        warnings.append("Prompt should include: one standalone social media post design")

    if len(text) > 2000:
        warnings.append("Prompt is longer than 2000 characters; consider simplifying it.")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint image-generation prompt text.")
    parser.add_argument("prompt_file", type=Path)
    parser.add_argument("--no-require-start", action="store_true")
    args = parser.parse_args(argv)

    try:
        text = args.prompt_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.prompt_file}", file=sys.stderr)
        return 1

    errors, warnings = lint_prompt(text, require_start=not args.no_require_start)

    if errors:
        print("ERRORS:")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("WARNINGS:")
        for item in warnings:
            print(f"- {item}")
    if not errors and not warnings:
        print("OK: image prompt passed all checks.")
    elif not errors:
        print("OK: image prompt has warnings only.")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
