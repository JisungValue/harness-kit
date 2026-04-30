#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP_SCRIPT_ROOT = ROOT / "bootstrap" / "scripts"
if str(BOOTSTRAP_SCRIPT_ROOT) not in sys.path:
    sys.path.append(str(BOOTSTRAP_SCRIPT_ROOT))

import bootstrap_init
import generate_downstream_bundle as bundle


CANONICAL_BUNDLE_ROOT = bundle.DEFAULT_OUTPUT

RUNTIME_SCRIPT_SOURCES = {
    "scripts/validate_overlay_decisions.py": "scripts/validate_overlay_decisions.py",
    "scripts/validate_overlay_consistency.py": "scripts/validate_overlay_consistency.py",
    "scripts/validate_phase_gate.py": "scripts/validate_phase_gate.py",
}

INSTALL_TIME_RESIDUE_PATHS = (
    "vendor/harness-kit",
    "bootstrap",
    "bundle_manifest.json",
    "docs/project_overlay",
    "docs/quickstart.md",
    "docs/how_harness_kit_works.md",
    "docs/version_support.md",
    "scripts/bootstrap_init.py",
    "scripts/adopt_common.py",
    "scripts/adopt_dry_run.py",
    "scripts/adopt_safe_write.py",
    "scripts/check_first_success_docs.py",
)
STALE_FINAL_RUNTIME_RESIDUE_PATHS = (
    "docs/process/downstream_harness_flow.md",
)
FINAL_RUNTIME_EXAMPLE_PATHS = tuple(sorted(bootstrap_init.FINAL_RUNTIME_EXAMPLE_TARGETS))
FINAL_RUNTIME_EXAMPLE_DIRS = tuple(
    sorted(
        {
            parent.as_posix()
            for path in FINAL_RUNTIME_EXAMPLE_PATHS
            for parent in Path(path).parents
            if parent.as_posix() != "."
        }
    )
)


@dataclass(frozen=True)
class RuntimeScript:
    source: Path
    destination: Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the canonical downstream bundle, use it as an install-time input, "
            "and leave only the downstream runtime layout in the target project."
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
        help=(
            "Project-root relative legacy vendored harness-kit path to clean up. "
            "The final install does not keep a vendored runtime dependency."
        ),
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
    plan = bootstrap_init.build_plan(
        target_root,
        language,
        vendor_path,
        language_reference_mode="install-time-note",
    )
    preflight_errors = bootstrap_init.collect_preflight_errors(target_root, plan)
    if preflight_errors:
        raise ValueError(format_bootstrap_preflight_errors(target_root, preflight_errors))

    conflicts = bootstrap_init.find_conflicts(plan)
    if conflicts and not force_bootstrap:
        raise ValueError(format_bootstrap_conflicts(target_root, conflicts))


def build_runtime_script_plan(install_bundle_root: Path, target_root: Path) -> list[RuntimeScript]:
    scripts: list[RuntimeScript] = []
    for source_rel, destination_rel in RUNTIME_SCRIPT_SOURCES.items():
        source = install_bundle_root / source_rel
        if not source.is_file():
            raise ValueError(f"install bundle is missing runtime script: {source_rel}")
        scripts.append(RuntimeScript(source=source, destination=target_root / destination_rel))
    return scripts


def ensure_runtime_script_preflight(
    target_root: Path,
    runtime_scripts: list[RuntimeScript],
    force_bootstrap: bool,
) -> None:
    preflight_errors: list[bootstrap_init.PreflightError] = []
    for item in runtime_scripts:
        if item.destination.exists() and item.destination.is_dir():
            preflight_errors.append(bootstrap_init.PreflightError(item.destination, "destination path is a directory"))
        for parent in item.destination.parents:
            if parent.exists() and not parent.is_dir():
                preflight_errors.append(bootstrap_init.PreflightError(parent, "parent path is not a directory"))
            if parent == target_root.parent:
                break

    if preflight_errors:
        raise ValueError(format_bootstrap_preflight_errors(target_root, preflight_errors))

    conflicts = [item.destination for item in runtime_scripts if item.destination.exists()]
    if conflicts and not force_bootstrap:
        raise ValueError(format_bootstrap_conflicts(target_root, conflicts))


def cleanup_legacy_vendor_destination(vendor_root: Path, bundle_files: list[bundle.BundleFile], force_vendor: bool) -> None:
    ensure_parent_dirs(vendor_root)

    if vendor_root.exists() and not vendor_root.is_dir():
        raise ValueError(f"post-install cleanup failed: legacy vendor path is not a directory: {vendor_root}")

    if vendor_root.exists() and any(vendor_root.iterdir()):
        if not force_vendor:
            raise ValueError(
                "post-install cleanup failed: legacy vendor path already contains files. "
                "Re-run with --force-vendor to remove bundle-owned residue."
            )

        allowed_paths = (
            bundle.owned_bundle_paths(bundle_files)
            | bundle.load_existing_manifest_paths(vendor_root)
            | bundle.OBSOLETE_BUNDLE_PATHS
        )
        unknown_paths = sorted(
            path
            for path in bundle.existing_output_paths(vendor_root) - allowed_paths
            if not path.startswith(bundle.OBSOLETE_BUNDLE_PREFIXES)
        )
        if unknown_paths:
            preview = ", ".join(unknown_paths[:5])
            raise ValueError(
                "post-install cleanup failed: --force-vendor refused because the legacy vendor path contains non-bundle paths: "
                f"{preview}"
            )

        shutil.rmtree(vendor_root)
    elif vendor_root.exists():
        vendor_root.rmdir()


def materialize_runtime_scripts(runtime_scripts: list[RuntimeScript]) -> None:
    for item in runtime_scripts:
        item.destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item.source, item.destination)


def generate_canonical_bundle() -> list[bundle.BundleFile]:
    bundle_files = bundle.build_bundle_files()
    bundle.prepare_output_dir(CANONICAL_BUNDLE_ROOT, bundle_files, force=True)
    bundle.write_bundle(CANONICAL_BUNDLE_ROOT, bundle_files)
    return bundle_files


def run_vendored_bootstrap(
    target_root: Path,
    install_bundle_root: Path,
    language: str,
    force_bootstrap: bool,
) -> int:
    command = [
        sys.executable,
        str(install_bundle_root / "scripts" / "bootstrap_init.py"),
        str(target_root),
        "--language",
        language,
        "--language-reference-mode",
        "install-time-note",
    ]
    if force_bootstrap:
        command.append("--force")

    return subprocess.run(command, cwd=ROOT, check=False).returncode


def run_install_completion_check(target_root: Path, install_bundle_root: Path) -> int:
    command = [
        sys.executable,
        str(install_bundle_root / "scripts" / "check_first_success_docs.py"),
        str(target_root),
    ]
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def collect_install_time_residue(target_root: Path, vendor_path: str) -> list[str]:
    residue_paths = set(INSTALL_TIME_RESIDUE_PATHS)
    residue_paths.add(vendor_path)
    return sorted(path for path in residue_paths if (target_root / path).exists())


def collect_unexpected_final_runtime_examples(target_root: Path) -> list[str]:
    examples_root = target_root / "docs/process/examples"
    if not examples_root.exists():
        return []

    allowed = set(FINAL_RUNTIME_EXAMPLE_PATHS) | set(FINAL_RUNTIME_EXAMPLE_DIRS)
    return sorted(
        path.relative_to(target_root).as_posix()
        for path in examples_root.rglob("*")
        if path.relative_to(target_root).as_posix() not in allowed
    )


def ensure_no_install_time_residue(target_root: Path, vendor_path: str) -> None:
    residue = collect_install_time_residue(target_root, vendor_path)
    if residue:
        lines = ["post-install cleanup failed: install-time only assets remain in final runtime surface."]
        lines.extend(f"- {path}" for path in residue)
        raise ValueError("\n".join(lines))


def cleanup_stale_final_runtime_residue(target_root: Path) -> None:
    for relative_path in STALE_FINAL_RUNTIME_RESIDUE_PATHS:
        path = target_root / relative_path
        if not path.exists():
            continue
        if not path.is_file():
            raise ValueError(f"post-install cleanup failed: stale final runtime path is not a file: {relative_path}")
        path.unlink()


def ensure_no_unexpected_final_runtime_examples(target_root: Path) -> None:
    residue = collect_unexpected_final_runtime_examples(target_root)
    if residue:
        lines = ["post-install cleanup failed: non-runtime examples remain in final runtime surface."]
        lines.extend(f"- {path}" for path in residue)
        raise ValueError("\n".join(lines))


def ensure_required_final_runtime_examples(target_root: Path) -> None:
    missing = [path for path in FINAL_RUNTIME_EXAMPLE_PATHS if not (target_root / path).is_file()]
    if missing:
        lines = ["post-install validation failed: required final runtime examples are missing."]
        lines.extend(f"- {path}" for path in missing)
        raise ValueError("\n".join(lines))


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target_root = args.target.expanduser().resolve()

    try:
        vendor_path = bootstrap_init.normalize_vendor_path(args.vendor_path)
        validate_vendor_path(vendor_path)
        ensure_bootstrap_preflight(target_root, args.language, vendor_path, args.force_bootstrap)
        ensure_no_unexpected_final_runtime_examples(target_root)

        bundle_files = generate_canonical_bundle()
        vendor_root = target_root / vendor_path
        cleanup_legacy_vendor_destination(vendor_root, bundle_files, force_vendor=args.force_vendor)
        ensure_no_install_time_residue(target_root, vendor_path)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    print(f"Generated canonical downstream bundle in {CANONICAL_BUNDLE_ROOT}")

    with tempfile.TemporaryDirectory(prefix="harness-kit-install-") as tmp_dir:
        install_bundle_root = Path(tmp_dir) / "harness-kit"
        shutil.copytree(CANONICAL_BUNDLE_ROOT, install_bundle_root)
        try:
            runtime_scripts = build_runtime_script_plan(install_bundle_root, target_root)
            ensure_runtime_script_preflight(target_root, runtime_scripts, args.force_bootstrap)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 1

        bootstrap_returncode = run_vendored_bootstrap(
            target_root,
            install_bundle_root,
            args.language,
            force_bootstrap=args.force_bootstrap,
        )
        if bootstrap_returncode != 0:
            return bootstrap_returncode

        try:
            cleanup_stale_final_runtime_residue(target_root)
            ensure_no_unexpected_final_runtime_examples(target_root)
            ensure_required_final_runtime_examples(target_root)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 1

        completion_returncode = run_install_completion_check(target_root, install_bundle_root)
        if completion_returncode != 0:
            return completion_returncode

        materialize_runtime_scripts(runtime_scripts)

    try:
        ensure_no_install_time_residue(target_root, vendor_path)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    print(f"Install-time bundle inputs removed from final runtime surface")
    print(f"Install flow completed for {target_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
