#!/usr/bin/env python3
"""Validate a JSON post-series plan.

This script is deterministic and local-only. It validates the structure of the
planning JSON in assets/post-series-plan-template.json or generated specs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL = [
    "platform",
    "dimensions",
    "goal",
    "audience",
    "main_takeaway",
    "cta",
    "brand",
    "format",
    "image_count",
    "images",
]

REQUIRED_IMAGE_FIELDS = [
    "number",
    "headline",
    "supporting_text",
    "visual_direction",
]

MAX_HEADLINE_CHARS = 70
MAX_SUPPORTING_TEXT_CHARS = 180
MIN_IMAGES = 1
MAX_IMAGES = 35


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
        elif field not in {"images", "brand"} and is_blank(data[field]):
            warnings.append(f"Top-level field is blank: {field}")

    brand = data.get("brand")
    if not isinstance(brand, dict):
        errors.append("Field 'brand' must be an object.")
    else:
        colors = brand.get("colors")
        if not isinstance(colors, list) or len(colors) < 2:
            errors.append("Brand colors must include at least two values.")
        if is_blank(brand.get("style")):
            errors.append("Brand style is required.")

    image_count = data.get("image_count")
    if not isinstance(image_count, int):
        errors.append("Field 'image_count' must be an integer.")
    elif not (MIN_IMAGES <= image_count <= MAX_IMAGES):
        errors.append(f"image_count must be between {MIN_IMAGES} and {MAX_IMAGES}.")

    images = data.get("images")
    if not isinstance(images, list):
        errors.append("Field 'images' must be a list.")
        return errors, warnings

    if isinstance(image_count, int) and len(images) != image_count:
        warnings.append(f"images contains {len(images)} item(s), but image_count is {image_count}.")

    seen_numbers: set[int] = set()
    for index, item in enumerate(images, start=1):
        prefix = f"Image {index}"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: item must be an object.")
            continue
        for field in REQUIRED_IMAGE_FIELDS:
            if field not in item:
                errors.append(f"{prefix}: missing field: {field}")
            elif is_blank(item[field]):
                warnings.append(f"{prefix}: blank field: {field}")
        number = item.get("number")
        if isinstance(number, int):
            if number in seen_numbers:
                errors.append(f"{prefix}: duplicate number: {number}")
            seen_numbers.add(number)
        else:
            errors.append(f"{prefix}: number must be an integer.")
        headline = item.get("headline")
        if isinstance(headline, str) and len(headline) > MAX_HEADLINE_CHARS:
            warnings.append(f"{prefix}: headline is {len(headline)} chars; aim for {MAX_HEADLINE_CHARS} or fewer.")
        supporting = item.get("supporting_text")
        if isinstance(supporting, str) and len(supporting) > MAX_SUPPORTING_TEXT_CHARS:
            warnings.append(f"{prefix}: supporting_text is {len(supporting)} chars; aim for {MAX_SUPPORTING_TEXT_CHARS} or fewer.")

    expected = list(range(1, len(images) + 1))
    actual = [item.get("number") for item in images if isinstance(item, dict)]
    if actual != expected:
        warnings.append(f"Image numbers are {actual}; expected sequential numbering {expected}.")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a JSON post-series plan.")
    parser.add_argument("json_file", type=Path)
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
        print("OK: plan passed all checks.")
    elif not errors:
        print("OK: plan has warnings only.")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
