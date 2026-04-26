#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP_SCRIPT_ROOT = ROOT / "bootstrap" / "scripts"
if str(BOOTSTRAP_SCRIPT_ROOT) not in sys.path:
    sys.path.append(str(BOOTSTRAP_SCRIPT_ROOT))

import bootstrap_init
import generate_downstream_bundle as bundle


CANONICAL_BUNDLE_ROOT = bundle.DEFAULT_OUTPUT


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the canonical downstream bundle, vendor it into a target project, "
            "and run bootstrap from the vendored path."
        ),
    )
    parser.add_argument(
        "target",
        type=Path,
        help="Target downstream project directory.",
    )
    parser.add_argument(
        "--language",
        required=True,
        choices=sorted(bootstrap_init.LANGUAGE_BOOTSTRAP_PATHS),
        help="Primary project language for bootstrap convention references.",
    )
    parser.add_argument(
        "--vendor-path",
        default=bootstrap_init.DEFAULT_VENDOR_PATH,
        help="Project-root relative vendored harness-kit path.",
    )
    parser.add_argument(
        "--force-vendor",
        action="store_true",
        help="Replace an existing vendored bundle when the destination only contains bundle-owned paths.",
    )
    parser.add_argument(
        "--force-bootstrap",
        action="store_true",
        help="Overwrite generated bootstrap docs if they already exist in the target project.",
    )
    return parser.parse_args(argv)


def validate_vendor_path(vendor_path: str) -> None:
    vendor_parts = PurePosixPath(vendor_path).parts
    if vendor_parts and vendor_parts[0] == "docs":
        raise ValueError("vendor path must stay outside downstream project docs/ managed by bootstrap")


def ensure_parent_dirs(destination: Path) -> None:
    for parent in destination.parents:
        if parent.exists() and not parent.is_dir():
            raise ValueError(f"destination parent is not a directory: {parent}")


def format_bootstrap_preflight_errors(
    target_root: Path,
    preflight_errors: list[bootstrap_init.PreflightError],
) -> str:
    lines = ["bootstrap init failed: target path is not writable as a bootstrap tree."]
    lines.extend(f"- {error.path}: {error.reason}" for error in preflight_errors)
    return "\n".join(lines)


def format_bootstrap_conflicts(target_root: Path, conflicts: list[Path]) -> str:
    lines = ["bootstrap init failed: target files already exist."]
    lines.extend(f"- {path.relative_to(target_root).as_posix()}" for path in conflicts)
    lines.append("Re-run with --force-bootstrap to overwrite generated files.")
    return "\n".join(lines)


def ensure_bootstrap_preflight(
    target_root: Path,
    language: str,
    vendor_path: str,
    force_bootstrap: bool,
) -> None:
    plan = bootstrap_init.build_plan(target_root, language, vendor_path)
    preflight_errors = bootstrap_init.collect_preflight_errors(target_root, plan)
    if preflight_errors:
        raise ValueError(format_bootstrap_preflight_errors(target_root, preflight_errors))

    conflicts = bootstrap_init.find_conflicts(plan)
    if conflicts and not force_bootstrap:
        raise ValueError(format_bootstrap_conflicts(target_root, conflicts))


def prepare_vendor_destination(vendor_root: Path, bundle_files: list[bundle.BundleFile], force_vendor: bool) -> None:
    ensure_parent_dirs(vendor_root)

    if vendor_root.exists() and not vendor_root.is_dir():
        raise ValueError(f"vendoring failed: destination path is not a directory: {vendor_root}")

    if vendor_root.exists() and any(vendor_root.iterdir()):
        if not force_vendor:
            raise ValueError(
                "vendoring failed: destination already contains files. "
                "Re-run with --force-vendor to replace the existing vendored bundle."
            )

        allowed_paths = bundle.owned_bundle_paths(bundle_files) | bundle.load_existing_manifest_paths(vendor_root)
        unknown_paths = sorted(bundle.existing_output_paths(vendor_root) - allowed_paths)
        if unknown_paths:
            preview = ", ".join(unknown_paths[:5])
            raise ValueError(
                "vendoring failed: --force-vendor refused because the destination contains non-bundle paths: "
                f"{preview}"
            )

        shutil.rmtree(vendor_root)

    vendor_root.parent.mkdir(parents=True, exist_ok=True)


def generate_canonical_bundle() -> list[bundle.BundleFile]:
    bundle_files = bundle.build_bundle_files()
    bundle.prepare_output_dir(CANONICAL_BUNDLE_ROOT, bundle_files, force=True)
    bundle.write_bundle(CANONICAL_BUNDLE_ROOT, bundle_files)
    return bundle_files


def run_vendored_bootstrap(
    target_root: Path,
    vendor_path: str,
    language: str,
    force_bootstrap: bool,
) -> int:
    command = [
        sys.executable,
        str(target_root / vendor_path / "scripts" / "bootstrap_init.py"),
        str(target_root),
        "--language",
        language,
        "--vendor-path",
        vendor_path,
    ]
    if force_bootstrap:
        command.append("--force")

    return subprocess.run(command, cwd=ROOT, check=False).returncode


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target_root = args.target.expanduser().resolve()

    try:
        vendor_path = bootstrap_init.normalize_vendor_path(args.vendor_path)
        validate_vendor_path(vendor_path)
        ensure_bootstrap_preflight(target_root, args.language, vendor_path, args.force_bootstrap)

        bundle_files = generate_canonical_bundle()
        vendor_root = target_root / vendor_path
        prepare_vendor_destination(vendor_root, bundle_files, force_vendor=args.force_vendor)
        shutil.copytree(CANONICAL_BUNDLE_ROOT, vendor_root)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    print(f"Generated canonical downstream bundle in {CANONICAL_BUNDLE_ROOT}")
    print(f"Vendored downstream bundle into {vendor_root}")

    bootstrap_returncode = run_vendored_bootstrap(
        target_root,
        vendor_path,
        args.language,
        force_bootstrap=args.force_bootstrap,
    )
    if bootstrap_returncode != 0:
        return bootstrap_returncode

    print(f"Install flow completed for {target_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
