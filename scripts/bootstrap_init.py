#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from pathlib import PurePosixPath
from pathlib import PureWindowsPath


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VENDOR_PATH = "vendor/harness-kit"

TEMPLATE_TARGETS = {
    "bootstrap/docs/project_overlay/agent_entrypoint_template.md": "AGENTS.md",
    "bootstrap/docs/project_overlay/claude_entrypoint_template.md": "CLAUDE.md",
    "bootstrap/docs/project_overlay/gemini_entrypoint_template.md": "GEMINI.md",
    "bootstrap/docs/project_overlay/project_entrypoint_template.md": "docs/project_entrypoint.md",
    "bootstrap/docs/project_overlay/decisions_index_template.md": "docs/decisions/README.md",
    "bootstrap/docs/project_overlay/architecture_template.md": "docs/standard/architecture.md",
    "bootstrap/docs/project_overlay/implementation_order_template.md": "docs/standard/implementation_order.md",
    "bootstrap/docs/project_overlay/coding_conventions_project_template.md": "docs/standard/coding_conventions_project.md",
    "bootstrap/docs/project_overlay/quality_gate_profile_template.md": "docs/standard/quality_gate_profile.md",
    "bootstrap/docs/project_overlay/testing_profile_template.md": "docs/standard/testing_profile.md",
    "bootstrap/docs/project_overlay/commit_rule_template.md": "docs/standard/commit_rule.md",
}

MATERIALIZED_PROJECT_OVERLAY_ROOT = "docs/project_overlay"

LANGUAGE_BOOTSTRAP_PATHS = {
    "python": "vendor/harness-kit/bootstrap/language_conventions/python_coding_conventions_template.md",
    "java": "vendor/harness-kit/bootstrap/language_conventions/java_coding_conventions_template.md",
    "kotlin": "vendor/harness-kit/bootstrap/language_conventions/kotlin_coding_conventions_template.md",
}


@dataclass(frozen=True)
class PlannedFile:
    source: Path
    destination: Path
    content: str


@dataclass(frozen=True)
class PreflightError:
    path: Path
    reason: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create deterministic harness bootstrap docs in a target directory.",
    )
    parser.add_argument(
        "target",
        type=Path,
        help="Target project directory to initialize.",
    )
    parser.add_argument(
        "--language",
        required=True,
        choices=sorted(LANGUAGE_BOOTSTRAP_PATHS),
        help="Primary project language for bootstrap convention references.",
    )
    parser.add_argument(
        "--vendor-path",
        default=DEFAULT_VENDOR_PATH,
        help="Project-root relative vendored harness-kit path used in generated references.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated files if they already exist.",
    )
    return parser.parse_args(argv)


def normalize_vendor_path(raw_path: str) -> str:
    candidate = raw_path.replace("\\", "/").strip()
    windows_path = PureWindowsPath(candidate)
    if candidate.startswith("/") or windows_path.is_absolute() or windows_path.drive:
        raise ValueError("vendor path must be project-root relative, not absolute")

    normalized = candidate.strip("/")
    vendor_path = PurePosixPath(normalized)

    if not normalized or normalized == ".":
        raise ValueError("vendor path must be a non-empty project-root relative path")
    if any(part in {"", ".", ".."} for part in vendor_path.parts):
        raise ValueError("vendor path must stay inside the project root")

    return vendor_path.as_posix()


def resolve_template_source(source_rel: str) -> Path:
    source = ROOT / source_rel
    if source.exists():
        return source

    canonical_prefix = "bootstrap/docs/project_overlay/"
    if source_rel.startswith(canonical_prefix):
        materialized_source = ROOT / MATERIALIZED_PROJECT_OVERLAY_ROOT / source_rel.removeprefix(canonical_prefix)
        if materialized_source.exists():
            return materialized_source

    raise FileNotFoundError(f"Bootstrap template not found: {source_rel}")


def build_plan(target_root: Path, language: str, vendor_path: str = DEFAULT_VENDOR_PATH) -> list[PlannedFile]:
    plan: list[PlannedFile] = []
    bootstrap_ref = f"{vendor_path}/bootstrap/language_conventions/{Path(LANGUAGE_BOOTSTRAP_PATHS[language]).name}"
    harness_guide_ref = f"{vendor_path}/docs/harness_guide.md"

    for source_rel, destination_rel in TEMPLATE_TARGETS.items():
        source = resolve_template_source(source_rel)
        destination = target_root / destination_rel
        content = source.read_text(encoding="utf-8")
        if destination_rel == "docs/project_entrypoint.md":
            content = customize_project_entrypoint_template(content, harness_guide_ref)
        if destination_rel == "docs/standard/coding_conventions_project.md":
            content = customize_coding_conventions_template(content, language, bootstrap_ref)
        plan.append(PlannedFile(source=source, destination=destination, content=content))

    return plan


def customize_project_entrypoint_template(content: str, harness_guide_ref: str) -> str:
    default_reference = f"{DEFAULT_VENDOR_PATH}/docs/harness_guide.md"
    if default_reference not in content:
        raise ValueError(f"Expected template snippet not found: {default_reference}")
    return content.replace(default_reference, harness_guide_ref, 1)


def customize_coding_conventions_template(content: str, language: str, bootstrap_ref: str) -> str:
    replacements = {
        "- 언어별 convention 초안이 필요하면 `bootstrap/language_conventions/`에서 해당 언어 템플릿을 골라 이 문서에 병합한다.": (
            "- 언어별 convention 초안이 필요하면 "
            f"`{bootstrap_ref.rsplit('/', 1)[0]}/`에서 해당 언어 템플릿을 골라 이 문서에 병합한다."
        ),
        "- bootstrap 템플릿을 복사했다면 어떤 언어 템플릿을 기준으로 병합했는지 적는다.": (
            "- bootstrap 템플릿을 복사했다면 어떤 언어 템플릿을 기준으로 병합했는지 적는다.\n"
            f"- init 기본값은 `{bootstrap_ref}`를 첫 기준 문서로 참조한다."
        ),
        "- 현재 프로젝트의 활성 언어/런타임: `[프로젝트 결정 필요]`": (
            f"- 현재 프로젝트의 활성 언어/런타임: `{language}`"
        ),
        "- bootstrap 출처 또는 기준 언어 문서: `[프로젝트 결정 필요]`": (
            f"- bootstrap 출처 또는 기준 언어 문서: `{bootstrap_ref}`"
        ),
    }

    for old, new in replacements.items():
        if old not in content:
            raise ValueError(f"Expected template snippet not found: {old}")
        content = content.replace(old, new, 1)

    return content


def find_conflicts(plan: list[PlannedFile]) -> list[Path]:
    return [item.destination for item in plan if item.destination.exists()]


def collect_preflight_errors(target_root: Path, plan: list[PlannedFile]) -> list[PreflightError]:
    errors: list[PreflightError] = []
    seen: set[tuple[Path, str]] = set()

    def add_error(path: Path, reason: str) -> None:
        key = (path, reason)
        if key in seen:
            return
        seen.add(key)
        errors.append(PreflightError(path=path, reason=reason))

    if target_root.exists() and not target_root.is_dir():
        add_error(target_root, "target path is not a directory")

    for item in plan:
        if item.destination.exists() and item.destination.is_dir():
            add_error(item.destination, "destination path is a directory")

        for parent in item.destination.parents:
            if parent.exists() and not parent.is_dir():
                add_error(parent, "parent path is not a directory")
            if parent == target_root.parent:
                break

    return errors


def write_plan(plan: list[PlannedFile]) -> None:
    for item in plan:
        item.destination.parent.mkdir(parents=True, exist_ok=True)
        item.destination.write_text(item.content, encoding="utf-8")


def print_plan(plan: list[PlannedFile], target_root: Path, overwritten: bool) -> None:
    action = "Overwrote" if overwritten else "Created"
    print(f"{action} harness bootstrap docs in {target_root}")
    for item in plan:
        print(f"- {item.destination.relative_to(target_root).as_posix()} <- {item.source.relative_to(ROOT).as_posix()}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target_root = args.target.expanduser().resolve()
    try:
        vendor_path = normalize_vendor_path(args.vendor_path)
        plan = build_plan(target_root, args.language, vendor_path)
    except ValueError as exc:
        print(f"bootstrap init failed: {exc}", file=sys.stderr)
        return 1
    preflight_errors = collect_preflight_errors(target_root, plan)
    conflicts = find_conflicts(plan)

    if preflight_errors:
        print("bootstrap init failed: target path is not writable as a bootstrap tree.", file=sys.stderr)
        for error in preflight_errors:
            print(
                f"- {error.path}: {error.reason}",
                file=sys.stderr,
            )
        return 1

    if conflicts and not args.force:
        print("bootstrap init failed: target files already exist.", file=sys.stderr)
        for path in conflicts:
            print(f"- {path.relative_to(target_root).as_posix()}", file=sys.stderr)
        print("Re-run with --force to overwrite generated files.", file=sys.stderr)
        return 1

    write_plan(plan)
    print_plan(plan, target_root, overwritten=bool(conflicts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
