#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from bootstrap_init import LANGUAGE_BOOTSTRAP_PATHS

from adopt_common import classify_targets, render_legacy_migration_section, render_section


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

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target_root = args.target.expanduser().resolve()
    classification = classify_targets(target_root, args.language)

    print(f"adopt dry-run for {target_root}")
    print(f"- bootstrap language baseline: {args.language}")
    print("- write mode: disabled (read-only)")
    print(f"- missing files: {len(classification.missing)}")
    print(f"- existing but unchanged targets: {len(classification.unchanged)}")
    print(f"- differing files: {len(classification.differing)}")
    print(f"- conflict candidates: {len(classification.conflicts)}")
    print(f"- legacy entrypoint migration candidates: {len(classification.legacy_migrations)}")

    sections = []
    sections.extend(
        render_legacy_migration_section(
            "Legacy entrypoint migration candidates:",
            classification.legacy_migrations,
            target_root,
        )
    )
    sections.extend(render_section("Missing files (safe to create):", classification.missing, target_root))
    sections.extend(render_section("Existing but unchanged targets:", classification.unchanged, target_root))
    sections.extend(render_section("Differing files (manual review):", classification.differing, target_root))
    sections.extend(render_section("Conflict candidates (manual decision required):", classification.conflicts, target_root))
    if sections:
        print()
        for line in sections:
            print(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
