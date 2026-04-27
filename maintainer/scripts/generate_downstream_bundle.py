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

SOURCE_ROOTS = (ROOT / "bootstrap", ROOT / "docs", ROOT / "downstream")


@dataclass(frozen=True)
class BundleFile:
    source: Path
    relative_path: Path
    content: bytes
    sha256: str
    size_bytes: int


BUNDLE_TEXT_REPLACEMENTS = (
    ("bootstrap/docs/", "docs/"),
    ("downstream/docs/", "docs/"),
    ("bootstrap/scripts/", "scripts/"),
)


BUNDLE_TEXT_REPLACEMENTS_BY_PATH: dict[str, tuple[tuple[str, str], ...]] = {
    "bootstrap/README.md": (
        (
            "- source repo canonical CLI는 `scripts/bootstrap_init.py`, `scripts/check_first_success_docs.py`, `scripts/validate_overlay_decisions.py`, `scripts/validate_overlay_consistency.py`이며 모두 Python 3 runtime으로 실행한다.",
            "- bundle에서는 `scripts/bootstrap_init.py`, `scripts/check_first_success_docs.py`, `scripts/validate_overlay_decisions.py`, `scripts/validate_overlay_consistency.py`를 모두 Python 3 runtime으로 실행한다.",
        ),
        (
            "- `scripts/bootstrap_init.py`는 `docs/project_overlay/*` 템플릿을 source of truth로 삼고, generated bundle에서는 같은 자산을 `docs/project_overlay/*`와 `scripts/*`로 materialize 한 뒤 새 프로젝트 또는 거의 빈 대상 디렉터리에 최소 project overlay 문서 세트를 그대로 복사해 생성한다.",
            "- `scripts/bootstrap_init.py`는 이 bundle 안의 `docs/project_overlay/*` 템플릿을 기준으로 최소 project overlay 문서 세트를 그대로 복사해 생성한다.",
        ),
        (
            "- `scripts/check_first_success_docs.py`는 source repo canonical helper command다. generated bundle에서는 `scripts/check_first_success_docs.py`로 materialize 된다.",
            "- `scripts/check_first_success_docs.py`는 bundle helper command다.",
        ),
    ),
    "docs/downstream_harness_flow.md": (
        (
            "- source repo 자산과 downstream 생성 문서의 대응 관계가 먼저 필요하면 `README.md`의 `Source Repo 와 Downstream 관계` 표를 함께 본다.",
            "- bootstrap 전후 구조 설명이 더 필요하면 `docs/quickstart.md`와 `docs/how_harness_kit_works.md`를 함께 본다.",
        ),
        (
            "- 이 저장소는 bootstrap 전 source repo이고, 실제로 동작하는 하네스는 downstream 프로젝트 안에서 맞물린다.",
            "- 이 bundle은 downstream 프로젝트에 vendoring하기 전의 delivery unit이고, 실제로 동작하는 하네스는 downstream 프로젝트 안에서 맞물린다.",
        ),
    ),
    "docs/how_harness_kit_works.md": (
        (
            "- `bootstrap_init.py`는 source repo 기준 `docs/project_overlay/*` template를 source of truth로 사용하고, generated bundle에서는 이를 `docs/project_overlay/*`로 materialize 해 최소 문서 세트와 runtime instruction entrypoint 파일을 생성한다.",
            "- `bootstrap_init.py`는 이 bundle 안의 `docs/project_overlay/*` template를 기준으로 최소 문서 세트와 runtime instruction entrypoint 파일을 생성한다.",
        ),
    ),
    "docs/project_overlay/README.md": (
        (
            "- 이 문서는 source repo 안의 project overlay template guide다.",
            "- 이 문서는 downstream bundle 안의 project overlay guide다.",
        ),
        (
            "- 이 저장소에서는 먼저 `docs/quickstart.md`를 보고, 필요할 때만 `docs/project_overlay/first_success_guide.md`, `docs/project_overlay/local_diagnostics_and_dry_run.md`, `docs/how_harness_kit_works.md`로 이어진다.",
            "- 이 bundle에서는 먼저 `docs/quickstart.md`를 보고, 필요할 때만 `docs/project_overlay/first_success_guide.md`, `docs/project_overlay/local_diagnostics_and_dry_run.md`, `docs/how_harness_kit_works.md`로 이어진다.",
        ),
        (
            "## source repo와 downstream 구분",
            "## bundle과 downstream 구분",
        ),
        (
            "- source repo에는 root `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `docs/project_entrypoint.md`, `docs/decisions/README.md`가 아직 없다.",
            "- 이 bundle 자체에는 root `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `docs/project_entrypoint.md`, `docs/decisions/README.md`가 아직 없다.",
        ),
        (
            "- 따라서 source repo에서 문서를 읽는 단계에서는 `docs/project_overlay/*` canonical source를 먼저 보고, downstream 프로젝트에서는 generated bundle의 `docs/project_overlay/*`와 생성된 runtime entrypoint, project entrypoint를 따른다.",
            "- 이 bundle 안에서는 `docs/project_overlay/*`를 직접 읽고, 실제 downstream 프로젝트에서는 여기서 생성한 runtime entrypoint와 project entrypoint를 따른다.",
        ),
        (
            "  - source repo canonical workflow template이다.",
            "  - bundle 안에서 바로 복사해 쓰는 workflow template이다.",
        ),
        (
            "  - generated bundle에서는 `docs/project_overlay/harness_doc_guard_workflow_template.yml`로 materialize 되고, 프로젝트 `.github/workflows/`로 복사해 harness-kit 문서 정합성 검사를 자동 실행한다.",
            "  - 프로젝트 `.github/workflows/`로 복사해 harness-kit 문서 정합성 검사를 자동 실행한다.",
        ),
        (
            "- `docs/project_overlay/`는 guide, template, workflow의 canonical source다.\n- generated downstream bundle은 이 자산을 `docs/project_overlay/` 아래로 materialize 해 consumer-facing 경로를 유지한다.",
            "- 이 bundle에서는 `docs/project_overlay/` 아래 자산을 guide, template, workflow 기준 경로로 사용한다.",
        ),
    ),
}


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


def bundle_pattern_for_source_pattern(pattern: str) -> str:
    return bundle_relative_path_for_source(Path(pattern)).as_posix()


def extract_bundle_layout_patterns() -> list[str]:
    return [bundle_pattern_for_source_pattern(pattern) for pattern in extract_bundle_patterns()]


def matches_any_pattern(relative_path: Path, patterns: list[str]) -> bool:
    return any(relative_path.match(pattern) for pattern in patterns)


def is_shippable_bundle_source(relative_path: Path) -> bool:
    return "__pycache__" not in relative_path.parts and relative_path.suffix != ".pyc"


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


def render_bundle_text(relative_path: Path, text: str) -> str:
    rendered = text
    for source_prefix, bundle_prefix in BUNDLE_TEXT_REPLACEMENTS:
        rendered = rendered.replace(source_prefix, bundle_prefix)

    for old, new in BUNDLE_TEXT_REPLACEMENTS_BY_PATH.get(relative_path.as_posix(), ()):  # pragma: no branch
        rendered = rendered.replace(old, new)

    return rendered


def render_bundle_file_content(source: Path, relative_path: Path) -> bytes:
    if source.suffix != ".md":
        return source.read_bytes()

    rendered_text = render_bundle_text(relative_path, source.read_text(encoding="utf-8"))
    return rendered_text.encode("utf-8")


def build_bundle_files() -> list[BundleFile]:
    by_path: dict[str, BundleFile] = {}
    excluded_patterns = extract_maintainer_only_paths()

    for pattern in extract_bundle_patterns():
        matched_any = False
        for path in ROOT.glob(pattern):
            if not path.is_file():
                continue
            relative_path = path.relative_to(ROOT)
            if not is_shippable_bundle_source(relative_path):
                continue
            matched_any = True
            if matches_any_pattern(relative_path, excluded_patterns):
                continue
            bundle_relative_path = bundle_relative_path_for_source(relative_path)
            bundle_content = render_bundle_file_content(path, bundle_relative_path)
            by_path[bundle_relative_path.as_posix()] = BundleFile(
                source=path,
                relative_path=bundle_relative_path,
                content=bundle_content,
                sha256=hashlib.sha256(bundle_content).hexdigest(),
                size_bytes=len(bundle_content),
            )
        if not matched_any:
            raise ValueError(f"Boundary pattern matched no files: {pattern}")

    return [by_path[key] for key in sorted(by_path)]


def bundle_readme_text(bundle_files: list[BundleFile]) -> str:
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
            "- maintainer-only docs, release procedures, and audit records",
            "- maintainer-only generation and validation scripts",
            "- repository tests and git metadata",
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
        "schema_version": 2,
        "bundle_name": DEFAULT_OUTPUT.name,
        "artifact_format": "directory",
        "bundle_patterns": extract_bundle_layout_patterns(),
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

    if manifest.get("schema_version") != 2:
        return set()
    if manifest.get("bundle_name") != DEFAULT_OUTPUT.name:
        return set()
    if manifest.get("artifact_format") != "directory":
        return set()
    if manifest.get("bundle_patterns") != extract_bundle_layout_patterns():
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
        destination.write_bytes(bundle_file.content)
        shutil.copystat(bundle_file.source, destination)

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
