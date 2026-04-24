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
    missing = [path for path in REQUIRED_DOCS if not (project_root / path).exists()]
    if missing:
        print("first-success docs are missing:", file=sys.stderr)
        for path in missing:
            print(f"- {path}", file=sys.stderr)
        return 1

    print("first success docs are present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
