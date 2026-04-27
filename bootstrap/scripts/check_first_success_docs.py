#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_DOCS = (
    "docs/project_entrypoint.md",
    "docs/decisions/README.md",
    "docs/standard/architecture.md",
    "docs/standard/implementation_order.md",
    "docs/standard/coding_conventions_project.md",
    "docs/standard/quality_gate_profile.md",
    "docs/standard/testing_profile.md",
    "docs/standard/commit_rule.md",
)


def describe_invalid_doc_shape(path: Path) -> str:
    if path.is_dir():
        return "expected a file but found a directory"
    return "expected a file but found a non-file path"


def collect_required_doc_failures(project_root: Path) -> tuple[list[str], list[tuple[str, str]]]:
    missing: list[str] = []
    invalid_shapes: list[tuple[str, str]] = []
    for relative_path in REQUIRED_DOCS:
        path = project_root / relative_path
        if not path.exists():
            missing.append(relative_path)
            continue
        if path.is_file():
            continue
        invalid_shapes.append((relative_path, describe_invalid_doc_shape(path)))
    return missing, invalid_shapes


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check that the first-success document set exists in a target project.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=Path.cwd(),
        type=Path,
        help="Target project root. Defaults to the current directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    project_root = args.target.expanduser().resolve()
    missing, invalid_shapes = collect_required_doc_failures(project_root)
    if missing or invalid_shapes:
        print("first-success doc check failed:", file=sys.stderr)
        if missing:
            print("Missing required docs:", file=sys.stderr)
            for path in missing:
                print(f"- {path}", file=sys.stderr)
        if invalid_shapes:
            print("Required docs with invalid path shapes:", file=sys.stderr)
            for path, detail in invalid_shapes:
                print(f"- {path}: {detail}", file=sys.stderr)
        return 1

    print("first success docs are present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
