#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from generate_downstream_bundle import (
    BOUNDARY_DOCUMENT,
    DEFAULT_OUTPUT,
    ENTRY_README,
    MANIFEST_NAME,
    build_bundle_files,
    bundle_readme_text,
    existing_output_paths,
    extract_bundle_patterns,
    extract_maintainer_only_paths,
    owned_bundle_paths,
    sha256_hex,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a generated downstream-facing harness-kit bundle.",
    )
    parser.add_argument(
        "bundle",
        nargs="?",
        default=DEFAULT_OUTPUT,
        type=Path,
        help="Bundle directory to validate. Defaults to dist/harness-kit-project-bundle.",
    )
    return parser.parse_args(argv)


def build_expected_manifest(bundle_files) -> dict:
    return {
        "schema_version": 1,
        "bundle_name": DEFAULT_OUTPUT.name,
        "artifact_format": "directory",
        "boundary_document": BOUNDARY_DOCUMENT,
        "source_patterns": extract_bundle_patterns(),
        "excluded_patterns": extract_maintainer_only_paths(),
        "entry_readme": ENTRY_README,
        "manifest_path": MANIFEST_NAME,
        "copied_files": [
            {
                "path": bundle_file.relative_path.as_posix(),
                "sha256": bundle_file.sha256,
                "size_bytes": bundle_file.size_bytes,
            }
            for bundle_file in bundle_files
        ],
    }


def load_manifest(bundle_root: Path, errors: list[str]) -> dict | None:
    manifest_path = bundle_root / MANIFEST_NAME
    if not manifest_path.is_file():
        errors.append(f"missing generated manifest: {MANIFEST_NAME}")
        return None

    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid manifest JSON {MANIFEST_NAME}: {exc}")
        return None


def validate_structure(bundle_root: Path, bundle_files, errors: list[str]) -> None:
    expected_copied_paths = {bundle_file.relative_path.as_posix() for bundle_file in bundle_files}
    actual_paths = existing_output_paths(bundle_root)
    expected_owned = owned_bundle_paths(bundle_files)

    missing_files = sorted(path for path in expected_copied_paths if path not in actual_paths)
    for path in missing_files:
        errors.append(f"missing required bundle file: {path}")

    if ENTRY_README not in actual_paths:
        errors.append(f"missing generated entry file: {ENTRY_README}")

    unexpected_paths = sorted(actual_paths - expected_owned)
    for path in unexpected_paths:
        errors.append(f"unexpected path outside downstream bundle boundary: {path}")


def validate_copied_file_contents(bundle_root: Path, bundle_files, errors: list[str]) -> None:
    for bundle_file in bundle_files:
        bundle_path = bundle_root / bundle_file.relative_path
        if not bundle_path.is_file():
            continue

        actual_sha256 = sha256_hex(bundle_path)
        actual_size = bundle_path.stat().st_size
        if actual_sha256 != bundle_file.sha256 or actual_size != bundle_file.size_bytes:
            errors.append(
                "bundle file differs from source-of-truth: "
                f"{bundle_file.relative_path.as_posix()}"
            )


def validate_generated_readme(bundle_root: Path, bundle_files, errors: list[str]) -> None:
    readme_path = bundle_root / ENTRY_README
    if not readme_path.is_file():
        return

    expected_text = bundle_readme_text(bundle_files) + "\n"
    actual_text = readme_path.read_text(encoding="utf-8")
    if actual_text != expected_text:
        errors.append(f"generated entry file content drifted: {ENTRY_README}")


def validate_manifest(bundle_root: Path, bundle_files, manifest: dict | None, errors: list[str]) -> None:
    if manifest is None:
        return

    expected_manifest = build_expected_manifest(bundle_files)

    required_scalar_fields = (
        "schema_version",
        "bundle_name",
        "artifact_format",
        "boundary_document",
        "source_patterns",
        "excluded_patterns",
        "entry_readme",
        "manifest_path",
        "copied_files",
    )
    for field in required_scalar_fields:
        if manifest.get(field) != expected_manifest[field]:
            errors.append(f"manifest field mismatch for {field}")

    generated_files = manifest.get("generated_files")
    if not isinstance(generated_files, list) or len(generated_files) != 1:
        errors.append("manifest generated_files must describe exactly one generated README entry")
        return

    generated_entry = generated_files[0]
    readme_path = bundle_root / ENTRY_README
    if not readme_path.is_file():
        return

    expected_generated_entry = {
        "path": ENTRY_README,
        "sha256": sha256_hex(readme_path),
        "size_bytes": readme_path.stat().st_size,
    }
    if generated_entry != expected_generated_entry:
        errors.append(f"manifest generated_files entry mismatch for {ENTRY_README}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    bundle_root = args.bundle.expanduser().resolve()
    errors: list[str] = []

    if not bundle_root.exists() or not bundle_root.is_dir():
        print("downstream bundle validation failed.", file=sys.stderr)
        print(f"- bundle directory does not exist: {bundle_root}", file=sys.stderr)
        return 1

    bundle_files = build_bundle_files()
    manifest = load_manifest(bundle_root, errors)
    validate_structure(bundle_root, bundle_files, errors)
    validate_copied_file_contents(bundle_root, bundle_files, errors)
    validate_generated_readme(bundle_root, bundle_files, errors)
    validate_manifest(bundle_root, bundle_files, manifest, errors)

    if errors:
        print("downstream bundle validation failed.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"downstream bundle validation passed: {bundle_root}")
    print(f"- boundary document: {BOUNDARY_DOCUMENT}")
    print(f"- validated copied files: {len(bundle_files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
