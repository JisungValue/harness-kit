#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from bootstrap_init import (
    LANGUAGE_BOOTSTRAP_PATHS,
    ROOT,
    PlannedFile,
    PreflightError,
    build_plan,
    collect_preflight_errors,
)


@dataclass(frozen=True)
class ClassifiedTarget:
    path: Path
    source: Path
    reason: str = ""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only dry-run that compares an existing project against the bootstrap baseline.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=Path.cwd(),
        type=Path,
        help="Target project root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--language",
        required=True,
        choices=sorted(LANGUAGE_BOOTSTRAP_PATHS),
        help="Bootstrap language baseline to compare against.",
    )
    return parser.parse_args(argv)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_primary_heading(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped
    return None


def classify_difference(plan_item: PlannedFile) -> str | None:
    if not plan_item.destination.exists():
        return None
    if not plan_item.destination.is_file():
        return "target path is not a regular file"

    current_text = read_text(plan_item.destination)
    expected_heading = extract_primary_heading(plan_item.content)
    current_heading = extract_primary_heading(current_text)
    if expected_heading and current_heading != expected_heading:
        return f"primary heading differs from expected template ({expected_heading})"

    return None


def find_preflight_reason(plan_item: PlannedFile, preflight_errors: list[PreflightError]) -> str | None:
    for error in preflight_errors:
        if error.path == plan_item.destination or error.path in plan_item.destination.parents:
            return error.reason
    return None


def render_section(title: str, items: list[ClassifiedTarget], target_root: Path) -> list[str]:
    if not items:
        return []
    lines = [title]
    for item in items:
        relative_path = item.path.relative_to(target_root).as_posix()
        source_path = item.source.relative_to(ROOT).as_posix()
        if item.reason:
            lines.append(f"- {relative_path} <- {source_path} ({item.reason})")
        else:
            lines.append(f"- {relative_path} <- {source_path}")
    return lines


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target_root = args.target.expanduser().resolve()
    plan = build_plan(target_root, args.language)
    preflight_errors = collect_preflight_errors(target_root, plan)

    missing: list[ClassifiedTarget] = []
    unchanged: list[ClassifiedTarget] = []
    differing: list[ClassifiedTarget] = []
    conflicts: list[ClassifiedTarget] = []

    for item in plan:
        preflight_reason = find_preflight_reason(item, preflight_errors)
        if preflight_reason:
            conflicts.append(
                ClassifiedTarget(
                    path=item.destination,
                    source=item.source,
                    reason=preflight_reason,
                )
            )
            continue

        if not item.destination.exists():
            missing.append(ClassifiedTarget(path=item.destination, source=item.source))
            continue

        if not item.destination.is_file():
            conflicts.append(
                ClassifiedTarget(
                    path=item.destination,
                    source=item.source,
                    reason="target path is not a regular file",
                )
            )
            continue

        current_text = read_text(item.destination)
        if current_text == item.content:
            unchanged.append(ClassifiedTarget(path=item.destination, source=item.source))
            continue

        conflict_reason = classify_difference(item)
        if conflict_reason:
            conflicts.append(
                ClassifiedTarget(
                    path=item.destination,
                    source=item.source,
                    reason=conflict_reason,
                )
            )
            continue

        differing.append(ClassifiedTarget(path=item.destination, source=item.source))

    print(f"adopt dry-run for {target_root}")
    print(f"- bootstrap language baseline: {args.language}")
    print("- write mode: disabled (read-only)")
    print(f"- missing files: {len(missing)}")
    print(f"- existing but unchanged targets: {len(unchanged)}")
    print(f"- differing files: {len(differing)}")
    print(f"- conflict candidates: {len(conflicts)}")

    sections = []
    sections.extend(render_section("Missing files (safe to create):", missing, target_root))
    sections.extend(render_section("Existing but unchanged targets:", unchanged, target_root))
    sections.extend(render_section("Differing files (manual review):", differing, target_root))
    sections.extend(render_section("Conflict candidates (manual decision required):", conflicts, target_root))
    if sections:
        print()
        for line in sections:
            print(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
