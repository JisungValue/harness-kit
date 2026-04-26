#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIST_ROOT = ROOT / "dist"
DEFAULT_OUTPUT = ROOT / "dist" / "harness-kit-project-bundle"
BOUNDARY_DOCUMENT = "maintainer/docs/downstream_bundle_boundary.md"
ENTRY_README = "README.md"
MANIFEST_NAME = "bundle_manifest.json"
BOUNDARY_INCLUDE_SECTIONS = (
    "### 1) Downstream 필수 자산",
    "### 2) Downstream 선택 자산",
)
BOUNDARY_EXCLUDE_SECTIONS = ("### 3) Maintainer 전용 자산",)

SOURCE_ROOTS = (ROOT / "bootstrap", ROOT / "docs", ROOT / "downstream", ROOT / "scripts")


@dataclass(frozen=True)
class BundleFile:
    source: Path
    relative_path: Path
    sha256: str
    size_bytes: int


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the downstream-facing harness-kit bundle.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Directory where the downstream bundle will be generated.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing non-empty output directory.",
    )
    return parser.parse_args(argv)


def sha256_hex(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_boundary_document() -> str:
    return (ROOT / BOUNDARY_DOCUMENT).read_text(encoding="utf-8")


def extract_markdown_section(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    start = None

    for idx, line in enumerate(lines):
        if line.strip() == heading:
            start = idx + 1
            break

    if start is None:
        raise ValueError(f"Missing boundary document section: {heading}")

    end = len(lines)
    for idx in range(start, len(lines)):
        if re.match(r"^##+#\s+", lines[idx]):
            end = idx
            break

    return lines[start:end]


def extract_boundary_paths(headings: tuple[str, ...]) -> list[str]:
    patterns: list[str] = []
    seen: set[str] = set()
    text = read_boundary_document()

    for heading in headings:
        for line in extract_markdown_section(text, heading):
            match = re.match(r"^\s*-\s+`([^`]+)`\s*$", line)
            if not match:
                continue
            pattern = match.group(1)
            if pattern in seen:
                continue
            seen.add(pattern)
            patterns.append(pattern)

    if not patterns:
        raise ValueError(f"Boundary document does not define any paths for sections: {', '.join(headings)}")

    return patterns


def extract_bundle_patterns() -> list[str]:
    return extract_boundary_paths(BOUNDARY_INCLUDE_SECTIONS)


def extract_maintainer_only_paths() -> list[str]:
    return extract_boundary_paths(BOUNDARY_EXCLUDE_SECTIONS)


def matches_any_pattern(relative_path: Path, patterns: list[str]) -> bool:
    return any(relative_path.match(pattern) for pattern in patterns)


def bundle_relative_path_for_source(relative_path: Path) -> Path:
    relative_posix = relative_path.as_posix()
    if relative_posix.startswith("bootstrap/docs/"):
        return Path("docs") / relative_path.relative_to("bootstrap/docs")
    if relative_posix.startswith("bootstrap/scripts/"):
        return Path("scripts") / relative_path.name
    if relative_posix.startswith("downstream/docs/"):
        return Path("docs") / relative_path.relative_to("downstream/docs")
    if relative_posix.startswith("downstream/scripts/"):
        return Path("downstream/scripts") / relative_path.name
    return relative_path


def build_bundle_files() -> list[BundleFile]:
    by_path: dict[str, BundleFile] = {}
    excluded_patterns = extract_maintainer_only_paths()

    for pattern in extract_bundle_patterns():
        matched_any = False
        for path in ROOT.glob(pattern):
            if not path.is_file():
                continue
            matched_any = True
            relative_path = path.relative_to(ROOT)
            if matches_any_pattern(relative_path, excluded_patterns):
                continue
            bundle_relative_path = bundle_relative_path_for_source(relative_path)
            by_path[bundle_relative_path.as_posix()] = BundleFile(
                source=path,
                relative_path=bundle_relative_path,
                sha256=sha256_hex(path),
                size_bytes=path.stat().st_size,
            )
        if not matched_any:
            raise ValueError(f"Boundary pattern matched no files: {pattern}")

    return [by_path[key] for key in sorted(by_path)]


def bundle_readme_text(bundle_files: list[BundleFile]) -> str:
    maintainer_only_paths = extract_maintainer_only_paths()
    return "\n".join(
        [
            "# Harness Kit Project Bundle",
            "",
            "이 디렉터리는 downstream 프로젝트에 전달할 project-facing 자산만 모아 생성한 bundle이다.",
            "",
            "## Start Here",
            "",
            "- `docs/quickstart.md`",
            "- `docs/how_harness_kit_works.md`",
            "- `docs/project_overlay/first_success_guide.md`",
            "- `docs/project_overlay/adopt_dry_run.md`",
            "- `docs/project_overlay/harness_doc_guard_workflow_template.yml`",
            "- `scripts/check_first_success_docs.py`",
            "",
            "## Included",
            "",
            "- project-facing docs, templates, examples, bootstrap assets",
            "- deterministic helper scripts used by downstream projects",
            "- generated manifest: `bundle_manifest.json`",
            "",
            "## Not Included",
            "",
            "- maintainer-only exclusion pattern은 include path와 겹쳐도 downstream bundle에서 우선 제외한다.",
            *[f"- `{path}`" for path in maintainer_only_paths],
            "",
            "## Bundle Facts",
            "",
            "- canonical artifact format: directory",
            f"- copied source files: `{len(bundle_files)}`",
            "",
        ]
    )


def manifest_data(bundle_files: list[BundleFile], generated_readme_sha256: str, generated_readme_size: int) -> dict:
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
        "generated_files": [
            {
                "path": ENTRY_README,
                "sha256": generated_readme_sha256,
                "size_bytes": generated_readme_size,
            }
        ],
    }


def owned_bundle_paths(bundle_files: list[BundleFile]) -> set[str]:
    owned_paths = {ENTRY_README, MANIFEST_NAME}

    for relative_path in [bundle_file.relative_path for bundle_file in bundle_files]:
        owned_paths.add(relative_path.as_posix())
        for parent in relative_path.parents:
            if parent == Path("."):
                break
            owned_paths.add(parent.as_posix())

    return owned_paths


def load_existing_manifest_paths(output_root: Path) -> set[str]:
    manifest_path = output_root / MANIFEST_NAME
    if not manifest_path.exists() or not manifest_path.is_file():
        return set()

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()

    if manifest.get("boundary_document") != BOUNDARY_DOCUMENT:
        return set()
    if manifest.get("entry_readme") != ENTRY_README:
        return set()
    if manifest.get("manifest_path") != MANIFEST_NAME:
        return set()

    owned_paths = {ENTRY_README, MANIFEST_NAME}

    for section in ("copied_files", "generated_files"):
        for entry in manifest.get(section, []):
            path = entry.get("path")
            if not isinstance(path, str) or not path:
                continue
            relative_path = Path(path)
            owned_paths.add(relative_path.as_posix())
            for parent in relative_path.parents:
                if parent == Path("."):
                    break
                owned_paths.add(parent.as_posix())

    return owned_paths


def existing_output_paths(output_root: Path) -> set[str]:
    return {path.relative_to(output_root).as_posix() for path in output_root.rglob("*")}


def ensure_output_path_is_safe(output_root: Path) -> None:
    if output_root == ROOT or output_root in ROOT.parents:
        raise ValueError("bundle output cannot overwrite the repository root or its parent directories")

    for source_root in SOURCE_ROOTS:
        if output_root == source_root or source_root in output_root.parents:
            raise ValueError(
                f"bundle output must stay outside source-of-truth paths: {source_root.relative_to(ROOT).as_posix()}"
            )


def ensure_output_parent_dirs(output_root: Path) -> None:
    for parent in output_root.parents:
        if parent.exists() and not parent.is_dir():
            raise ValueError(f"bundle output parent is not a directory: {parent}")


def output_requires_force(output_root: Path) -> bool:
    return output_root.exists() and any(output_root.iterdir())


def prepare_output_dir(output_root: Path, bundle_files: list[BundleFile], force: bool) -> None:
    ensure_output_path_is_safe(output_root)
    ensure_output_parent_dirs(output_root)

    if force and DIST_ROOT not in output_root.parents:
        raise ValueError(
            "bundle generation failed: --force can only replace bundle output directories under dist/."
        )

    if output_root.exists() and not output_root.is_dir():
        raise ValueError(f"bundle output path is not a directory: {output_root}")

    if output_requires_force(output_root):
        if not force:
            raise ValueError(
                "bundle generation failed: output directory already contains files. Re-run with --force to replace it."
            )

        allowed_paths = owned_bundle_paths(bundle_files) | load_existing_manifest_paths(output_root)
        unknown_paths = sorted(existing_output_paths(output_root) - allowed_paths)
        if unknown_paths:
            preview = ", ".join(unknown_paths[:5])
            raise ValueError(
                "bundle generation failed: --force refused because the output directory contains non-bundle paths: "
                f"{preview}"
            )

        shutil.rmtree(output_root)

    output_root.mkdir(parents=True, exist_ok=True)


def write_bundle(output_root: Path, bundle_files: list[BundleFile]) -> None:
    for bundle_file in bundle_files:
        destination = output_root / bundle_file.relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(bundle_file.source, destination)

    readme_path = output_root / ENTRY_README
    readme_text = bundle_readme_text(bundle_files)
    readme_path.write_text(readme_text + "\n", encoding="utf-8")

    manifest_path = output_root / MANIFEST_NAME
    manifest = manifest_data(
        bundle_files,
        generated_readme_sha256=sha256_hex(readme_path),
        generated_readme_size=readme_path.stat().st_size,
    )
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output_root = args.output.expanduser().resolve()

    try:
        bundle_files = build_bundle_files()
        prepare_output_dir(output_root, bundle_files, force=args.force)
        write_bundle(output_root, bundle_files)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    print(f"Generated downstream bundle in {output_root}")
    print(f"- copied files: {len(bundle_files)}")
    print(f"- generated files: {ENTRY_README}, {MANIFEST_NAME}")
    print(f"- boundary document: {BOUNDARY_DOCUMENT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
