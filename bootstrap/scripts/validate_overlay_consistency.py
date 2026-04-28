#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_DOCS = (
    "docs/entrypoint.md",
    "docs/project/decisions/README.md",
    "docs/project/standards/architecture.md",
    "docs/project/standards/implementation_order.md",
    "docs/project/standards/coding_conventions_project.md",
    "docs/project/standards/quality_gate_profile.md",
    "docs/project/standards/testing_profile.md",
    "docs/project/standards/commit_rule.md",
)

REQUIRED_RUNTIME_ENTRYPOINTS = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
)

LEGACY_PROJECT_ENTRYPOINT = "docs/harness_guide.md"

EXPECTED_STANDARD_DOCS = {
    "docs/project/standards/architecture.md",
    "docs/project/standards/implementation_order.md",
    "docs/project/standards/coding_conventions_project.md",
    "docs/project/standards/quality_gate_profile.md",
    "docs/project/standards/testing_profile.md",
    "docs/project/standards/commit_rule.md",
}

DECISION_RECORD_REQUIRED_HEADINGS = (
    "Context",
    "Decision",
    "Rationale",
    "Consequences",
    "Related Docs",
    "When To Update",
)

INSTALL_TIME_BOOTSTRAP_REFERENCE_RE = re.compile(r"^install-time-only:[A-Za-z0-9_.-]+\.md$")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check cross-document consistency for project overlay docs.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=Path.cwd(),
        type=Path,
        help="Target project root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--mode",
        choices=("full", "incremental"),
        default="full",
        help="Validation mode. `full` requires the complete overlay set, `incremental` allows safe adoption gaps.",
    )
    return parser.parse_args(argv)


def read_text(project_root: Path, relative_path: str) -> str:
    return (project_root / relative_path).read_text(encoding="utf-8")


def path_exists(project_root: Path, relative_path: str) -> bool:
    return (project_root / relative_path).is_file()


def extract_h2_section(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.strip() == f"## {heading}":
            start = idx + 1
            break
    if start is None:
        raise ValueError(f"Missing section: ## {heading}")

    end = len(lines)
    in_code_block = False
    for idx in range(start, len(lines)):
        if lines[idx].strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block and lines[idx].startswith("## "):
            end = idx
            break
    return lines[start:end]


def extract_bullet_paths(lines: list[str]) -> list[str]:
    paths: list[str] = []
    for line in lines:
        match = re.match(r"^\s*-\s+`([^`]+)`\s*$", line)
        if match:
            paths.append(match.group(1))
    return paths


def require_phrases(text: str, phrases: tuple[str, ...], error_prefix: str, errors: list[str]) -> None:
    for phrase in phrases:
        if phrase not in text:
            errors.append(f"{error_prefix}: `{phrase}` 설명이 없습니다.")


def partition_existing_file_paths(project_root: Path, paths: list[str]) -> tuple[list[str], list[str]]:
    existing: list[str] = []
    missing: list[str] = []
    for path in paths:
        if (project_root / path).is_file():
            existing.append(path)
        else:
            missing.append(path)
    return existing, missing


def validate_project_entrypoint(project_root: Path, errors: list[str], mode: str) -> None:
    if mode == "incremental" and not path_exists(project_root, "docs/entrypoint.md"):
        return

    try:
        guide = read_text(project_root, "docs/entrypoint.md")
        traversal_lines = extract_h2_section(guide, "실행 계약")
        common_lines = extract_h2_section(guide, "공통 규칙")
        project_lines = extract_h2_section(guide, "프로젝트 전용 규칙")
        decisions_lines = extract_h2_section(guide, "프로젝트 결정 문서")
    except (FileNotFoundError, ValueError) as exc:
        errors.append(f"docs/entrypoint.md: {exc}")
        return

    require_phrases(
        "\n".join(traversal_lines),
        (
            "공통 규칙",
            "프로젝트 전용 규칙",
            "순서대로 모두 읽고 적용",
            "둘 중 하나만 읽고 멈추지 않는다",
        ),
        "docs/entrypoint.md 실행 계약",
        errors,
    )

    common_paths = extract_bullet_paths(common_lines)
    required_common_paths = {
        "docs/process/harness_guide.md",
        "docs/process/downstream_harness_flow.md",
    }
    missing_required_common_paths = sorted(required_common_paths - set(common_paths))
    if missing_required_common_paths:
        joined = ", ".join(missing_required_common_paths)
        errors.append(
            "docs/entrypoint.md: 공통 규칙 섹션에 필수 process docs 경로가 없습니다: "
            f"{joined}"
        )
    candidate_common_paths = [
        path
        for path in common_paths
        if path in required_common_paths or path.endswith("/docs/harness_guide.md")
    ]
    if not candidate_common_paths:
        errors.append(
            "docs/entrypoint.md: 공통 규칙 섹션에 공통 harness guide 경로가 없습니다."
        )
    else:
        existing_paths, missing_paths = partition_existing_file_paths(project_root, candidate_common_paths)
        planned_process_paths = {
            "docs/process/harness_guide.md",
            "docs/process/downstream_harness_flow.md",
        }
        missing_planned_paths = [path for path in missing_paths if path in planned_process_paths]
        if missing_planned_paths:
            joined = ", ".join(missing_planned_paths)
            errors.append(
                "docs/entrypoint.md: 공통 규칙의 필수 process docs 경로가 실제 프로젝트에서 존재하지 않습니다: "
                f"{joined}"
            )
            return
        missing_non_planned_paths = [path for path in missing_paths if path not in planned_process_paths]
        if missing_non_planned_paths and any(path in planned_process_paths for path in candidate_common_paths):
            joined = ", ".join(missing_non_planned_paths)
            errors.append(
                "docs/entrypoint.md: 공통 규칙에 stale harness guide 경로가 남아 있습니다. "
                f"존재하지 않는 경로를 정리하거나 현지화하세요: {joined}"
            )
        elif not existing_paths and not all(path in planned_process_paths for path in candidate_common_paths):
            joined = ", ".join(candidate_common_paths)
            errors.append(
                "docs/entrypoint.md: 공통 규칙의 harness guide 경로가 실제 프로젝트에서 존재하지 않습니다. "
                f"먼저 vendored 경로를 현지화하거나 배치 상태를 확인하세요: {joined}"
            )
        elif missing_non_planned_paths:
            joined = ", ".join(missing_non_planned_paths)
            errors.append(
                "docs/entrypoint.md: 공통 규칙에 stale harness guide 경로가 남아 있습니다. "
                f"존재하지 않는 경로를 정리하거나 현지화하세요: {joined}"
            )

    project_paths = set(extract_bullet_paths(project_lines))
    missing_paths = EXPECTED_STANDARD_DOCS - project_paths
    if missing_paths:
        errors.append(
            "docs/entrypoint.md: 프로젝트 전용 규칙에서 필수 project standard 문서 참조가 누락됐습니다."
        )

    decisions_paths = set(extract_bullet_paths(decisions_lines))
    if "docs/project/decisions/README.md" not in decisions_paths:
        errors.append("docs/entrypoint.md: `docs/project/decisions/README.md`를 프로젝트 결정 문서 진입점으로 연결하지 않습니다.")


def validate_decisions_index(project_root: Path, errors: list[str], mode: str) -> None:
    if mode == "incremental" and not path_exists(project_root, "docs/project/decisions/README.md"):
        return

    try:
        decisions_index = read_text(project_root, "docs/project/decisions/README.md")
        extract_h2_section(decisions_index, "문서 역할")
        extract_h2_section(decisions_index, "여기에 남기는 것")
        extract_h2_section(decisions_index, "여기에 남기지 않는 것")
        numbering_lines = extract_h2_section(decisions_index, "번호 규칙")
        extract_h2_section(decisions_index, "읽기 방법")
        current_lines = extract_h2_section(decisions_index, "Current Decisions")
        superseded_lines = extract_h2_section(decisions_index, "Superseded Decisions")
    except (FileNotFoundError, ValueError) as exc:
        errors.append(f"docs/project/decisions/README.md: {exc}")
        return

    if "DEC-###-slug.md" not in "\n".join(numbering_lines):
        errors.append("docs/project/decisions/README.md: 번호 규칙에 `DEC-###-slug.md` 형식이 없습니다.")

    listed_paths = extract_bullet_paths(current_lines) + extract_bullet_paths(superseded_lines)
    for path in listed_paths:
        if not (project_root / path).is_file():
            errors.append(f"docs/project/decisions/README.md: index에 적힌 decision 문서가 실제 프로젝트에 없습니다: {path}")
            continue
        validate_decision_record(project_root, path, errors)


def validate_decision_record(project_root: Path, relative_path: str, errors: list[str]) -> None:
    text = read_text(project_root, relative_path)
    front_matter_phrases = (
        "- Status:",
        "- Type:",
        "- Date:",
        "- Related Docs:",
        "- When To Update:",
    )
    for phrase in front_matter_phrases:
        if phrase not in text:
            errors.append(f"{relative_path}: `{phrase}` 메타데이터가 없습니다.")
    for heading in DECISION_RECORD_REQUIRED_HEADINGS:
        if f"## {heading}" not in text:
            errors.append(f"{relative_path}: `## {heading}` 섹션이 없습니다.")


def validate_runtime_entrypoints(project_root: Path, errors: list[str], mode: str) -> None:
    if mode == "incremental" and not path_exists(project_root, "AGENTS.md"):
        for adapter_path in ("CLAUDE.md", "GEMINI.md"):
            if path_exists(project_root, adapter_path):
                errors.append(f"{adapter_path}: `AGENTS.md` 없이 adapter entrypoint만 부분 도입된 상태는 허용되지 않습니다.")
        return

    try:
        agents = read_text(project_root, "AGENTS.md")
        agent_lines = extract_h2_section(agents, "우선 읽을 문서")
        traversal_lines = extract_h2_section(agents, "실행 계약")
    except (FileNotFoundError, ValueError) as exc:
        errors.append(f"AGENTS.md: {exc}")
        return

    require_phrases(
        "\n".join(traversal_lines),
        (
            "순서대로 모두 읽고 적용",
            "공통 규칙",
            "프로젝트 전용 규칙",
            "중간 문서에서 멈추지 않는다",
        ),
        "AGENTS.md 실행 계약",
        errors,
    )

    agent_paths = set(extract_bullet_paths(agent_lines))
    if "docs/entrypoint.md" not in agent_paths:
        errors.append("AGENTS.md: `docs/entrypoint.md`를 우선 읽을 문서로 연결하지 않습니다.")
    elif not path_exists(project_root, "docs/entrypoint.md"):
        errors.append("AGENTS.md: `docs/entrypoint.md`를 가리키지만 실제 파일이 없습니다.")

    for adapter_path in ("CLAUDE.md", "GEMINI.md"):
        if mode == "incremental" and not path_exists(project_root, adapter_path):
            continue
        try:
            adapter = read_text(project_root, adapter_path)
            adapter_lines = extract_h2_section(adapter, "공통 진입점")
        except (FileNotFoundError, ValueError) as exc:
            errors.append(f"{adapter_path}: {exc}")
            continue

        adapter_targets = set(extract_bullet_paths(adapter_lines))
        if "AGENTS.md" not in adapter_targets:
            errors.append(f"{adapter_path}: `AGENTS.md`를 공통 진입점으로 연결하지 않습니다.")
        if "연결된 문서 체인도 끝까지 따라간다" not in adapter:
            errors.append(f"{adapter_path}: `AGENTS.md` 이후 연결된 문서 체인을 끝까지 따르라는 설명이 없습니다.")


def validate_legacy_project_entrypoint_absence(project_root: Path, errors: list[str]) -> None:
    legacy_path = project_root / LEGACY_PROJECT_ENTRYPOINT
    if legacy_path.exists():
        errors.append(
            "legacy project-local entrypoint가 남아 있습니다: docs/harness_guide.md -> docs/entrypoint.md로 migrate하고 기존 파일을 retire해야 합니다."
        )


def validate_architecture_and_order(project_root: Path, errors: list[str], mode: str) -> None:
    if mode == "incremental" and not path_exists(project_root, "docs/project/standards/implementation_order.md"):
        return

    if mode == "incremental" and not path_exists(project_root, "docs/project/standards/architecture.md"):
        errors.append(
            "docs/project/standards/implementation_order.md: implementation_order 문서가 있으면 architecture.md도 함께 있어야 합니다."
        )
        return

    implementation_order = read_text(project_root, "docs/project/standards/implementation_order.md")
    if "architecture.md" not in implementation_order:
        errors.append(
            "docs/project/standards/implementation_order.md: architecture.md 참조가 없어 레이어 진행 순서 기준이 불명확합니다."
        )


def validate_quality_gate_and_testing(project_root: Path, errors: list[str], mode: str) -> None:
    has_quality_gate = path_exists(project_root, "docs/project/standards/quality_gate_profile.md")
    has_testing = path_exists(project_root, "docs/project/standards/testing_profile.md")

    if mode == "incremental" and not has_quality_gate and not has_testing:
        return

    quality_gate = read_text(project_root, "docs/project/standards/quality_gate_profile.md") if has_quality_gate else ""
    testing = read_text(project_root, "docs/project/standards/testing_profile.md") if has_testing else ""

    if has_quality_gate and "testing_profile.md" not in quality_gate:
        errors.append(
            "docs/project/standards/quality_gate_profile.md: testing_profile.md 참조가 없어 테스트 세부 기준 책임 경계가 불명확합니다."
        )
    if has_testing and "quality_gate_profile.md" not in testing:
        errors.append(
            "docs/project/standards/testing_profile.md: quality_gate_profile.md 참조가 없어 테스트 명령 책임 경계가 불명확합니다."
        )

    if has_testing:
        try:
            testing_owner_lines = extract_h2_section(testing, "quality_gate_profile에 두는 항목")
        except ValueError as exc:
            errors.append(f"docs/project/standards/testing_profile.md: {exc}")
            return

        joined = "\n".join(testing_owner_lines)
        required_keywords = (
            "실행 명령",
            "필수 여부",
            "언제 test를 반드시 돌려야 하는지",
            "테스트 실패 시 커밋/승인 불가 기준",
        )
        for phrase in required_keywords:
            if phrase not in joined:
                errors.append(
                    f"docs/project/standards/testing_profile.md: quality_gate_profile 책임 항목에서 `{phrase}` 설명이 빠져 있습니다."
                )

    if has_quality_gate and ("testing_profile.md" not in quality_gate or "세부 테스트 범위" not in quality_gate):
        errors.append(
            "docs/project/standards/quality_gate_profile.md: test 섹션이 testing_profile.md로 세부 기준을 연결하지 않습니다."
        )


def validate_coding_conventions(project_root: Path, errors: list[str], mode: str) -> None:
    if mode == "incremental" and not path_exists(project_root, "docs/project/standards/coding_conventions_project.md"):
        return

    coding = read_text(project_root, "docs/project/standards/coding_conventions_project.md")

    if "docs/project/standards/quality_gate_profile.md" not in coding:
        errors.append(
            "docs/project/standards/coding_conventions_project.md: quality_gate_profile.md 책임 경계 참조가 없습니다."
        )

    bootstrap_match = re.search(
        r"^- bootstrap 출처 또는 기준 언어 문서:\s+`([^`]+)`$",
        coding,
        re.MULTILINE,
    )
    if bootstrap_match:
        bootstrap_reference = bootstrap_match.group(1)
        if not bootstrap_reference.endswith(".md"):
            errors.append(
                "docs/project/standards/coding_conventions_project.md: bootstrap 기준 문서가 .md 경로가 아닙니다."
            )
        if bootstrap_reference.startswith("install-time-only:"):
            if not INSTALL_TIME_BOOTSTRAP_REFERENCE_RE.match(bootstrap_reference):
                errors.append(
                    "docs/project/standards/coding_conventions_project.md: install-time bootstrap 기준 문서 표기가 올바르지 않습니다."
                )
        elif bootstrap_reference.startswith("bootstrap/language_conventions/"):
            errors.append(
                "docs/project/standards/coding_conventions_project.md: bootstrap 기준 문서가 repo-local path로 남아 있습니다. vendored 또는 project-local path로 현지화해야 합니다."
            )
        elif not (project_root / bootstrap_reference).is_file():
            errors.append(
                "docs/project/standards/coding_conventions_project.md: bootstrap 기준 문서 경로가 실제 프로젝트에서 존재하지 않습니다. "
                f"먼저 vendored 경로를 현지화하거나 배치 상태를 확인하세요: {bootstrap_reference}"
            )
    else:
        errors.append(
            "docs/project/standards/coding_conventions_project.md: bootstrap 출처 또는 기준 언어 문서 라인이 없습니다."
        )


def validate_commit_rule(project_root: Path, errors: list[str], mode: str) -> None:
    if mode == "incremental" and not path_exists(project_root, "docs/project/standards/commit_rule.md"):
        return

    commit_rule = read_text(project_root, "docs/project/standards/commit_rule.md")

    try:
        precommit_lines = extract_h2_section(commit_rule, "커밋 전 최소 점검 항목")
    except ValueError as exc:
        errors.append(f"docs/project/standards/commit_rule.md: {exc}")
        return

    joined = "\n".join(precommit_lines)
    required_term_patterns = {
        "compile": re.compile(r"compile", re.IGNORECASE),
        "type": re.compile(r"type", re.IGNORECASE),
        "build": re.compile(r"build", re.IGNORECASE),
        "test": re.compile(r"test|테스트", re.IGNORECASE),
    }
    for label, pattern in required_term_patterns.items():
        if not pattern.search(joined):
            errors.append(
                f"docs/project/standards/commit_rule.md: 커밋 전 최소 점검 항목에 `{label}` 기준이 없습니다."
            )


def collect_missing_required_paths(project_root: Path) -> tuple[list[str], list[str]]:
    missing_docs = [relative_path for relative_path in REQUIRED_DOCS if not path_exists(project_root, relative_path)]
    missing_runtime = [relative_path for relative_path in REQUIRED_RUNTIME_ENTRYPOINTS if not path_exists(project_root, relative_path)]
    return missing_docs, missing_runtime


def validate_required_docs(project_root: Path, errors: list[str], mode: str) -> tuple[list[str], list[str]]:
    missing_docs, missing_runtime = collect_missing_required_paths(project_root)

    if mode == "full":
        for relative_path in missing_docs:
            errors.append(f"필수 overlay 문서가 없습니다: {relative_path}")

        for relative_path in missing_runtime:
            errors.append(f"필수 runtime instruction entrypoint가 없습니다: {relative_path}")

    return missing_docs, missing_runtime


def print_missing_paths(header: str, paths: list[str], stream) -> None:
    if not paths:
        return
    print(header, file=stream)
    for relative_path in paths:
        print(f"- {relative_path}", file=stream)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    project_root = args.target.expanduser().resolve()
    errors: list[str] = []

    missing_docs, missing_runtime = validate_required_docs(project_root, errors, args.mode)
    if errors:
        print("overlay consistency validation failed.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    validate_project_entrypoint(project_root, errors, args.mode)
    validate_decisions_index(project_root, errors, args.mode)
    validate_runtime_entrypoints(project_root, errors, args.mode)
    validate_legacy_project_entrypoint_absence(project_root, errors)
    validate_architecture_and_order(project_root, errors, args.mode)
    validate_quality_gate_and_testing(project_root, errors, args.mode)
    validate_coding_conventions(project_root, errors, args.mode)
    validate_commit_rule(project_root, errors, args.mode)

    if errors:
        if args.mode == "incremental":
            print("overlay consistency validation failed for mode 'incremental'.", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            print_missing_paths(
                "Still missing overlay docs allowed in incremental mode:",
                missing_docs,
                sys.stderr,
            )
            print_missing_paths(
                "Still missing runtime instruction entrypoints allowed in incremental mode:",
                missing_runtime,
                sys.stderr,
            )
            return 1

        print("overlay consistency validation failed.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if args.mode == "incremental":
        print("overlay consistency validation passed for mode 'incremental'.")
        print_missing_paths(
            "Still missing overlay docs allowed in incremental mode:",
            missing_docs,
            sys.stdout,
        )
        print_missing_paths(
            "Still missing runtime instruction entrypoints allowed in incremental mode:",
            missing_runtime,
            sys.stdout,
        )
        if not missing_docs and not missing_runtime:
            print("No incremental follow-ups remain. Re-run without `--mode incremental` to confirm the full overlay shape.")
        return 0

    print("overlay consistency validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
