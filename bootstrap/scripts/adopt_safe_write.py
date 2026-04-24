#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from bootstrap_init import LANGUAGE_BOOTSTRAP_PATHS

from adopt_common import (
    classify_targets,
    find_target_by_relative_path,
    render_legacy_migration_section,
    render_section,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply selective safe writes for an existing project using the bootstrap baseline.",
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
    parser.add_argument(
        "--update-unchanged",
        action="store_true",
        help="Rewrite targets that already exactly match the current bootstrap baseline.",
    )
    parser.add_argument(
        "--force-overwrite",
        action="append",
        default=[],
        metavar="RELATIVE_PATH",
        help="Explicitly overwrite a selected target path relative to the project root.",
    )
    parser.add_argument(
        "--migrate-legacy-entrypoint",
        action="store_true",
        help="Rename legacy docs/harness_guide.md to docs/project_entrypoint.md and apply safe runtime entrypoint follow-up when possible.",
    )
    return parser.parse_args(argv)


def write_target(target) -> None:
    target.path.parent.mkdir(parents=True, exist_ok=True)
    target.path.write_text(target.plan_item.content, encoding="utf-8")


def can_force_overwrite(target) -> bool:
    blocked_reasons = {
        "target path is not a directory",
        "target path is not a regular file",
        "destination path is a directory",
        "parent path is not a directory",
    }
    return target.reason not in blocked_reasons


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target_root = args.target.expanduser().resolve()
    initial = classify_targets(target_root, args.language)

    invalid_force_paths: list[str] = []
    blocked_force_paths: list[str] = []
    forced_targets = []
    migration_errors: list[str] = []
    migrated_legacy_entrypoints = []
    migration_created_targets = []
    migration_refreshed_targets = []

    allowed_force_targets = {target.path: target for target in (*initial.differing, *initial.conflicts)}

    for relative_path in args.force_overwrite:
        target = find_target_by_relative_path(initial, relative_path)
        if target is None:
            invalid_force_paths.append(relative_path)
            continue
        if target.path not in allowed_force_targets:
            invalid_force_paths.append(relative_path)
            continue
        if not can_force_overwrite(target):
            blocked_force_paths.append(relative_path)
            continue
        forced_targets.append(target)

    legacy_migration = initial.legacy_migrations[0] if initial.legacy_migrations else None
    if args.migrate_legacy_entrypoint:
        if legacy_migration is None:
            migration_errors.append(
                "- no legacy docs/harness_guide.md migration candidate was found in this project"
            )
        elif not legacy_migration.safe_to_apply:
            migration_errors.append(
                f"- legacy entrypoint migration blocked: {legacy_migration.blocked_reason}"
            )

    if invalid_force_paths or blocked_force_paths or migration_errors:
        print("adopt safe write failed.", file=sys.stderr)
        for relative_path in invalid_force_paths:
            print(
                f"- invalid force-overwrite target: {relative_path} (expected an existing differing/conflict file)",
                file=sys.stderr,
            )
        for relative_path in blocked_force_paths:
            print(
                f"- force-overwrite blocked by target path shape conflict: {relative_path}",
                file=sys.stderr,
            )
        for error in migration_errors:
            print(error, file=sys.stderr)
        return 1

    created_targets = list(initial.missing)
    refreshed_targets = list(initial.unchanged) if args.update_unchanged else []

    if args.migrate_legacy_entrypoint and legacy_migration is not None:
        legacy_migration.canonical_path.parent.mkdir(parents=True, exist_ok=True)
        legacy_migration.legacy_path.replace(legacy_migration.canonical_path)
        migrated_legacy_entrypoints.append(legacy_migration)
        for target in legacy_migration.runtime_create_targets:
            write_target(target)
            migration_created_targets.append(target)
        if legacy_migration.agents_refresh_target is not None:
            write_target(legacy_migration.agents_refresh_target)
            migration_refreshed_targets.append(legacy_migration.agents_refresh_target)

    for target in created_targets:
        write_target(target)
    for target in refreshed_targets:
        write_target(target)
    for target in forced_targets:
        write_target(target)

    final = classify_targets(target_root, args.language)

    print(f"adopt safe write for {target_root}")
    print(f"- bootstrap language baseline: {args.language}")
    print("- write mode: selective safe write")
    print(f"- created files: {len(created_targets)}")
    print(f"- refreshed unchanged targets: {len(refreshed_targets)}")
    print(f"- forced overwrites: {len(forced_targets)}")
    print(f"- migrated legacy entrypoints: {len(migrated_legacy_entrypoints)}")
    print(f"- created runtime entrypoints for migration: {len(migration_created_targets)}")
    print(f"- refreshed runtime entrypoints for migration: {len(migration_refreshed_targets)}")
    print(f"- remaining missing files: {len(final.missing)}")
    print(f"- remaining unchanged targets: {len(final.unchanged)}")
    print(f"- remaining differing files: {len(final.differing)}")
    print(f"- remaining conflict candidates: {len(final.conflicts)}")

    sections = []
    sections.extend(
        render_legacy_migration_section(
            "Migrated legacy entrypoints:",
            tuple(migrated_legacy_entrypoints),
            target_root,
        )
    )
    sections.extend(
        render_section(
            "Created runtime entrypoints for migration:",
            tuple(migration_created_targets),
            target_root,
        )
    )
    sections.extend(
        render_section(
            "Refreshed runtime entrypoints for migration:",
            tuple(migration_refreshed_targets),
            target_root,
        )
    )
    sections.extend(render_section("Created files:", tuple(created_targets), target_root))
    sections.extend(render_section("Refreshed unchanged targets:", tuple(refreshed_targets), target_root))
    sections.extend(render_section("Forced overwrites:", tuple(forced_targets), target_root))
    sections.extend(render_section("Remaining differing files (manual review):", final.differing, target_root))
    sections.extend(render_section("Remaining conflict candidates (manual decision required):", final.conflicts, target_root))
    if sections:
        print()
        for line in sections:
            print(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
