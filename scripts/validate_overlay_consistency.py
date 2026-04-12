#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_DOCS = (
    "docs/harness_guide.md",
    "docs/standard/architecture.md",
    "docs/standard/implementation_order.md",
    "docs/standard/coding_conventions_project.md",
    "docs/standard/quality_gate_profile.md",
    "docs/standard/testing_profile.md",
    "docs/standard/commit_rule.md",
)

REQUIRED_RUNTIME_ENTRYPOINTS = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
)

EXPECTED_STANDARD_DOCS = {
    "docs/standard/architecture.md",
    "docs/standard/implementation_order.md",
    "docs/standard/coding_conventions_project.md",
    "docs/standard/quality_gate_profile.md",
    "docs/standard/testing_profile.md",
    "docs/standard/commit_rule.md",
}


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
    return parser.parse_args(argv)


def read_text(project_root: Path, relative_path: str) -> str:
    return (project_root / relative_path).read_text(encoding="utf-8")


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


def validate_harness_guide(project_root: Path, errors: list[str]) -> None:
    try:
        guide = read_text(project_root, "docs/harness_guide.md")
        common_lines = extract_h2_section(guide, "공통 규칙")
        project_lines = extract_h2_section(guide, "프로젝트 전용 규칙")
    except ValueError as exc:
        errors.append(f"docs/harness_guide.md: {exc}")
        return

    common_paths = extract_bullet_paths(common_lines)
    if not any(path.endswith("/docs/harness_guide.md") and path != "docs/harness_guide.md" for path in common_paths):
        errors.append(
            "docs/harness_guide.md: 공통 규칙 섹션에 공통 harness guide 경로가 없습니다."
        )

    project_paths = set(extract_bullet_paths(project_lines))
    missing_paths = EXPECTED_STANDARD_DOCS - project_paths
    if missing_paths:
        errors.append(
            "docs/harness_guide.md: 프로젝트 전용 규칙에서 필수 standard 문서 참조가 누락됐습니다."
        )


def validate_runtime_entrypoints(project_root: Path, errors: list[str]) -> None:
    try:
        agents = read_text(project_root, "AGENTS.md")
        agent_lines = extract_h2_section(agents, "우선 읽을 문서")
    except ValueError as exc:
        errors.append(f"AGENTS.md: {exc}")
        return

    agent_paths = set(extract_bullet_paths(agent_lines))
    if "docs/harness_guide.md" not in agent_paths:
        errors.append("AGENTS.md: `docs/harness_guide.md`를 우선 읽을 문서로 연결하지 않습니다.")

    for adapter_path in ("CLAUDE.md", "GEMINI.md"):
        try:
            adapter = read_text(project_root, adapter_path)
            adapter_lines = extract_h2_section(adapter, "공통 진입점")
        except ValueError as exc:
            errors.append(f"{adapter_path}: {exc}")
            continue

        adapter_targets = set(extract_bullet_paths(adapter_lines))
        if "AGENTS.md" not in adapter_targets:
            errors.append(f"{adapter_path}: `AGENTS.md`를 공통 진입점으로 연결하지 않습니다.")


def validate_architecture_and_order(project_root: Path, errors: list[str]) -> None:
    implementation_order = read_text(project_root, "docs/standard/implementation_order.md")
    if "architecture.md" not in implementation_order:
        errors.append(
            "docs/standard/implementation_order.md: architecture.md 참조가 없어 레이어 진행 순서 기준이 불명확합니다."
        )


def validate_quality_gate_and_testing(project_root: Path, errors: list[str]) -> None:
    quality_gate = read_text(project_root, "docs/standard/quality_gate_profile.md")
    testing = read_text(project_root, "docs/standard/testing_profile.md")

    if "testing_profile.md" not in quality_gate:
        errors.append(
            "docs/standard/quality_gate_profile.md: testing_profile.md 참조가 없어 테스트 세부 기준 책임 경계가 불명확합니다."
        )
    if "quality_gate_profile.md" not in testing:
        errors.append(
            "docs/standard/testing_profile.md: quality_gate_profile.md 참조가 없어 테스트 명령 책임 경계가 불명확합니다."
        )

    try:
        testing_owner_lines = extract_h2_section(testing, "quality_gate_profile에 두는 항목")
    except ValueError as exc:
        errors.append(f"docs/standard/testing_profile.md: {exc}")
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
                f"docs/standard/testing_profile.md: quality_gate_profile 책임 항목에서 `{phrase}` 설명이 빠져 있습니다."
            )

    if "testing_profile.md" not in quality_gate or "세부 테스트 범위" not in quality_gate:
        errors.append(
            "docs/standard/quality_gate_profile.md: test 섹션이 testing_profile.md로 세부 기준을 연결하지 않습니다."
        )


def validate_coding_conventions(project_root: Path, errors: list[str]) -> None:
    coding = read_text(project_root, "docs/standard/coding_conventions_project.md")

    if "docs/standard/quality_gate_profile.md" not in coding:
        errors.append(
            "docs/standard/coding_conventions_project.md: quality_gate_profile.md 책임 경계 참조가 없습니다."
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
                "docs/standard/coding_conventions_project.md: bootstrap 기준 문서가 .md 경로가 아닙니다."
            )
        if bootstrap_reference.startswith("bootstrap/language_conventions/"):
            errors.append(
                "docs/standard/coding_conventions_project.md: bootstrap 기준 문서가 repo-local path로 남아 있습니다. vendored 또는 project-local path로 현지화해야 합니다."
            )
    else:
        errors.append(
            "docs/standard/coding_conventions_project.md: bootstrap 출처 또는 기준 언어 문서 라인이 없습니다."
        )


def validate_commit_rule(project_root: Path, errors: list[str]) -> None:
    commit_rule = read_text(project_root, "docs/standard/commit_rule.md")

    try:
        precommit_lines = extract_h2_section(commit_rule, "커밋 전 최소 점검 항목")
    except ValueError as exc:
        errors.append(f"docs/standard/commit_rule.md: {exc}")
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
                f"docs/standard/commit_rule.md: 커밋 전 최소 점검 항목에 `{label}` 기준이 없습니다."
            )


def validate_required_docs(project_root: Path, errors: list[str]) -> None:
    for relative_path in REQUIRED_DOCS:
        if not (project_root / relative_path).exists():
            errors.append(f"필수 overlay 문서가 없습니다: {relative_path}")

    for relative_path in REQUIRED_RUNTIME_ENTRYPOINTS:
        if not (project_root / relative_path).exists():
            errors.append(f"필수 runtime instruction entrypoint가 없습니다: {relative_path}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    project_root = args.target.expanduser().resolve()
    errors: list[str] = []

    validate_required_docs(project_root, errors)
    if errors:
        print("overlay consistency validation failed.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    validate_harness_guide(project_root, errors)
    validate_runtime_entrypoints(project_root, errors)
    validate_architecture_and_order(project_root, errors)
    validate_quality_gate_and_testing(project_root, errors)
    validate_coding_conventions(project_root, errors)
    validate_commit_rule(project_root, errors)

    if errors:
        print("overlay consistency validation failed.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("overlay consistency validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
