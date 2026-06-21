#!/usr/bin/env python3
"""Validate a JSON carousel specification.

This script is deterministic and local-only. It performs structure and readability
checks for carousel specs produced by the Content To Carousel skill.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL = [
    "platform",
    "audience",
    "goal",
    "angle",
    "content_promise",
    "slides",
    "caption",
    "cta",
]

REQUIRED_SLIDE_FIELDS = [
    "number",
    "role",
    "headline",
    "body",
    "visual_direction",
    "creator_note",
    "alt_text",
]

MAX_HEADLINE_CHARS = 90
MAX_BODY_CHARS = 260
MAX_ALT_TEXT_CHARS = 220
MIN_RECOMMENDED_SLIDES = 3
MAX_RECOMMENDED_SLIDES = 12


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"ERROR: file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")


def is_blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def validate(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ["Root value must be a JSON object."], []

    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            errors.append(f"Missing top-level field: {field}")
        elif field != "slides" and is_blank(data[field]):
            warnings.append(f"Top-level field is blank: {field}")

    slides = data.get("slides")
    if not isinstance(slides, list):
        errors.append("Field 'slides' must be a list.")
        return errors, warnings

    if len(slides) < MIN_RECOMMENDED_SLIDES:
        warnings.append(f"Carousel has {len(slides)} slides; most carousels need at least {MIN_RECOMMENDED_SLIDES}.")
    if len(slides) > MAX_RECOMMENDED_SLIDES:
        warnings.append(f"Carousel has {len(slides)} slides; consider tightening to {MAX_RECOMMENDED_SLIDES} or fewer.")

    seen_numbers: set[int] = set()
    for index, slide in enumerate(slides, start=1):
        prefix = f"Slide {index}"
        if not isinstance(slide, dict):
            errors.append(f"{prefix}: slide must be an object.")
            continue

        for field in REQUIRED_SLIDE_FIELDS:
            if field not in slide:
                errors.append(f"{prefix}: missing field: {field}")
            elif is_blank(slide[field]):
                warnings.append(f"{prefix}: blank field: {field}")

        number = slide.get("number")
        if isinstance(number, int):
            if number in seen_numbers:
                errors.append(f"{prefix}: duplicate slide number: {number}")
            seen_numbers.add(number)
        else:
            errors.append(f"{prefix}: number must be an integer.")

        headline = slide.get("headline")
        if isinstance(headline, str) and len(headline) > MAX_HEADLINE_CHARS:
            warnings.append(f"{prefix}: headline is {len(headline)} chars; aim for {MAX_HEADLINE_CHARS} or fewer.")

        body = slide.get("body")
        if isinstance(body, str) and len(body) > MAX_BODY_CHARS:
            warnings.append(f"{prefix}: body is {len(body)} chars; aim for {MAX_BODY_CHARS} or fewer.")

        alt_text = slide.get("alt_text")
        if isinstance(alt_text, str) and len(alt_text) > MAX_ALT_TEXT_CHARS:
            warnings.append(f"{prefix}: alt_text is {len(alt_text)} chars; aim for {MAX_ALT_TEXT_CHARS} or fewer.")

    expected = list(range(1, len(slides) + 1))
    actual = [slide.get("number") for slide in slides if isinstance(slide, dict)]
    if actual != expected:
        warnings.append(f"Slide numbers are {actual}; expected sequential numbering {expected}.")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a JSON carousel specification.")
    parser.add_argument("json_file", type=Path, help="Path to a carousel JSON spec.")
    args = parser.parse_args(argv)

    data = load_json(args.json_file)
    errors, warnings = validate(data)

    if errors:
        print("ERRORS:")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("WARNINGS:")
        for item in warnings:
            print(f"- {item}")
    if not errors and not warnings:
        print("OK: carousel spec passed all checks.")
    elif not errors:
        print("OK: carousel spec has warnings only.")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
