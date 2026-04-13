#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path

from bootstrap_init import LANGUAGE_BOOTSTRAP_PATHS


ROOT = Path(__file__).resolve().parents[1]

LANGUAGE_TEMPLATE_REQUIRED_HEADINGS = {
    "bootstrap/language_conventions/python_coding_conventions_template.md": [
        "목적",
        "사용 방법",
        "코드 스타일과 convention 분리",
        "공통 품질 규칙 참조",
        "적용 전 결정",
        "런타임과 패키징 검토 예시",
        "참조 관점",
        "타입과 모델링",
        "객체 생성과 API 설계",
        "함수와 추상화 설계",
        "컬렉션과 데이터 처리",
        "예외와 결과 표현",
        "동시성과 비동기",
        "동적 기능, 직렬화, 런타임 경계",
        "Import 와 Dependency 사용 관례",
        "패키지와 파일 구조",
        "테스트 관례 초안",
        "자주 생기는 품질 리스크와 금지 패턴",
        "확인 필요 항목",
    ],
    "bootstrap/language_conventions/java_coding_conventions_template.md": [
        "목적",
        "사용 방법",
        "코드 스타일과 convention 분리",
        "공통 품질 규칙 참조",
        "적용 전 결정",
        "버전별 검토 예시",
        "참조 관점",
        "타입과 모델링",
        "객체 생성과 API 설계",
        "함수와 추상화 설계",
        "컬렉션과 데이터 처리",
        "예외와 결과 표현",
        "동시성과 비동기",
        "Interop, Reflection, Serialization",
        "Import 와 Dependency 사용 관례",
        "패키지와 파일 구조",
        "테스트 관례 초안",
        "자주 생기는 품질 리스크와 금지 패턴",
        "확인 필요 항목",
    ],
    "bootstrap/language_conventions/kotlin_coding_conventions_template.md": [
        "목적",
        "사용 방법",
        "코드 스타일과 convention 분리",
        "공통 품질 규칙 참조",
        "적용 전 결정",
        "런타임과 언어 기능 검토 예시",
        "참조 관점",
        "타입과 모델링",
        "객체 생성과 API 설계",
        "함수와 추상화 설계",
        "컬렉션과 데이터 처리",
        "예외와 결과 표현",
        "동시성과 비동기",
        "Interop, Reflection, Serialization",
        "Import 와 Dependency 사용 관례",
        "패키지와 파일 구조",
        "테스트 관례 초안",
        "자주 생기는 품질 리스크와 금지 패턴",
        "확인 필요 항목",
    ],
}

PROJECT_FACING_MD_GLOBS = [
    "bootstrap/**/*.md",
    "docs/examples/**/*.md",
    "docs/harness/common/**/*.md",
    "docs/harness_guide.md",
    "docs/phase_*/*.md",
    "docs/project_overlay/**/*.md",
    "docs/standard/coding_guidelines_core.md",
    "docs/templates/task/**/*.md",
]

PROJECT_FACING_LEAKAGE_EXCLUDES: set[str] = set()

MAINTAINER_ONLY_REFERENCES = [
    "harness.log",
    "docs/kit_maintenance/",
    "scripts/check_harness_docs.py",
    ".github/workflows/harness-doc-guard.yml",
]

AUDIT_SUMMARY_PLACEHOLDERS = {"pending", "todo", "tbd"}


def read_text(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def iter_globbed_files(patterns: list[str]) -> list[Path]:
    paths: set[Path] = set()
    for pattern in patterns:
        paths.update(path for path in ROOT.glob(pattern) if path.is_file())
    return sorted(paths)


def extract_h2_headings(text: str) -> list[str]:
    return [match.group(1) for match in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]


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


def extract_bullet_paths(lines: list[str], prefix: str | None = None) -> list[str]:
    result: list[str] = []
    for line in lines:
        match = re.match(r"^\s*-\s+`([^`]+)`\s*$", line)
        if not match:
            continue
        path = match.group(1)
        if prefix and not path.startswith(prefix):
            continue
        result.append(path)
    return result


def extract_codeblock_paths(lines: list[str], prefix: str | None = None) -> list[str]:
    result: list[str] = []
    in_code_block = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            continue
        match = re.match(r"^\s*-\s+`([^`]+)`\s*$", line)
        if not match:
            continue
        path = match.group(1)
        if prefix and not path.startswith(prefix):
            continue
        result.append(path)
    return result


def check_project_doc_path_consistency(errors: list[str]) -> None:
    readme = read_text("README.md")
    overlay_readme = read_text("docs/project_overlay/README.md")
    quickstart = read_text("docs/quickstart.md")
    first_success = read_text("docs/project_overlay/first_success_guide.md")
    diagnostics = read_text("docs/project_overlay/local_diagnostics_and_dry_run.md")
    first_success_example = read_text("docs/examples/bootstrap-first-success/validation_report.md")
    bundle_smoke_doc = read_text("docs/kit_maintenance/downstream_bundle_smoke_validation.md")
    project_guide_template = read_text("docs/project_overlay/project_entrypoint_template.md")
    harness_guide = read_text("docs/harness_guide.md")

    readme_min = set(extract_bullet_paths(extract_h2_section(readme, "최소 프로젝트 문서 세트")))
    overlay_required = set(
        extract_bullet_paths(extract_h2_section(overlay_readme, "필수 문서"))
    )
    if readme_min != overlay_required:
        errors.append(
            "README 최소 프로젝트 문서 세트와 project_overlay/README 필수 문서가 일치하지 않습니다."
        )

    expected_project_docs = {path for path in readme_min if path.startswith("docs/standard/")}

    template_docs = set(extract_bullet_paths(project_guide_template.splitlines(), "docs/standard/"))
    if template_docs != expected_project_docs:
        errors.append(
            "project_entrypoint_template의 docs/standard 문서 목록이 README 최소 문서 세트와 다릅니다."
        )

    overlay_local_guide_docs = set(
        extract_codeblock_paths(
            extract_h2_section(overlay_readme, "권장 로컬 `docs/project_entrypoint.md`"),
            "docs/standard/",
        )
    )
    if overlay_local_guide_docs != expected_project_docs:
        errors.append(
            "project_overlay/README의 권장 로컬 guide 예시 문서 목록이 README 최소 문서 세트와 다릅니다."
        )

    if "프로젝트 `testing_profile.md`" in harness_guide:
        errors.append("harness_guide에 구식 경로 `프로젝트 testing_profile.md` 표현이 남아 있습니다.")

    decisions_lines = extract_h2_section(project_guide_template, "프로젝트 결정 문서")
    if set(extract_bullet_paths(decisions_lines)) != {"docs/decisions/README.md"}:
        errors.append("project_entrypoint_template의 프로젝트 결정 문서 목록이 기대값과 다릅니다.")

    for rel_path, text in {
        "README.md": readme,
        "docs/project_overlay/README.md": overlay_readme,
    }.items():
        if "source repo" not in text or "bootstrap한 뒤" not in text:
            errors.append(f"{rel_path}에 source repo와 downstream bootstrap 이후 문맥 구분 설명이 없습니다.")
        if "root `AGENTS.md`" not in text:
            errors.append(f"{rel_path}에 source repo에는 root `AGENTS.md`가 아직 없다는 설명이 없습니다.")

    if "예시 명령의 `vendor/harness-kit/` 부분을 모두 같은 실제 경로로" not in quickstart:
        errors.append("docs/quickstart.md에 non-default vendoring command path localize 설명이 충분하지 않습니다.")

    overlay_completion_example = read_text("docs/examples/bootstrap-first-success/overlay_completion_validation_report.md")
    for required_path in readme_min:
        if required_path not in overlay_completion_example:
            errors.append(
                f"docs/examples/bootstrap-first-success/overlay_completion_validation_report.md에 필수 문서 `{required_path}`가 반영되지 않았습니다."
            )
    overlay_completion_targets = set(
        extract_bullet_paths(
            extract_h2_section(
                overlay_completion_example,
                "판정 대상",
            )
        )
    )
    expected_explicit_targets = {
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        "docs/project_entrypoint.md",
        "docs/decisions/README.md",
        "validate_overlay_decisions.py",
        "validate_overlay_consistency.py",
    }
    missing_targets = expected_explicit_targets - overlay_completion_targets
    if missing_targets:
        joined = ", ".join(sorted(missing_targets))
        errors.append(
            "docs/examples/bootstrap-first-success/overlay_completion_validation_report.md의 판정 대상 목록이 현재 계약과 다릅니다: "
            f"{joined}"
        )

    first_success_surfaces = {
        "docs/quickstart.md": quickstart,
        "docs/project_overlay/first_success_guide.md": first_success,
        "docs/project_overlay/local_diagnostics_and_dry_run.md": diagnostics,
        "docs/examples/bootstrap-first-success/validation_report.md": first_success_example,
        "docs/kit_maintenance/downstream_bundle_smoke_validation.md": bundle_smoke_doc,
    }
    for rel_path, text in first_success_surfaces.items():
        if "scripts/check_first_success_docs.py" in text:
            continue
        for required_path in readme_min:
            if required_path not in text:
                errors.append(f"{rel_path}에 최소 문서 세트 경로 `{required_path}`가 반영되지 않았습니다.")

    prerequisite_surfaces = {
        "docs/quickstart.md": quickstart,
        "docs/project_overlay/first_success_guide.md": first_success,
        "docs/project_overlay/local_diagnostics_and_dry_run.md": diagnostics,
        "bootstrap/README.md": read_text("bootstrap/README.md"),
    }
    for rel_path, text in prerequisite_surfaces.items():
        if "Python 3" not in text:
            errors.append(f"{rel_path}에 Python 3 prerequisite 설명이 없습니다.")

    helper_command_surfaces = {
        "docs/quickstart.md": quickstart,
        "docs/project_overlay/first_success_guide.md": first_success,
        "docs/project_overlay/local_diagnostics_and_dry_run.md": diagnostics,
        "docs/examples/bootstrap-first-success/validation_report.md": first_success_example,
        "docs/kit_maintenance/downstream_bundle_smoke_validation.md": bundle_smoke_doc,
    }
    for rel_path, text in helper_command_surfaces.items():
        if "scripts/check_first_success_docs.py" not in text:
            errors.append(f"{rel_path}에 canonical first-success helper command가 반영되지 않았습니다.")

    for token in tuple(f"`{language}`" for language in LANGUAGE_BOOTSTRAP_PATHS) + (
        "legacy entrypoint migration",
        "--migrate-legacy-entrypoint",
    ):
        if token not in bundle_smoke_doc:
            errors.append(
                "docs/kit_maintenance/downstream_bundle_smoke_validation.md에 bundle smoke coverage 설명이 부족합니다: "
                f"{token}"
            )


def check_entrypoint_role_labels(errors: list[str]) -> None:
    expected_titles = {
        "docs/harness_guide.md": "# Harness Core Guide",
        "docs/project_overlay/project_entrypoint_template.md": "# Project Harness Entry Point",
        "docs/project_overlay/agent_entrypoint_template.md": "# Agent Runtime Entry Point",
        "docs/project_overlay/claude_entrypoint_template.md": "# Claude Adapter Entry Point",
        "docs/project_overlay/gemini_entrypoint_template.md": "# Gemini Adapter Entry Point",
    }

    for rel_path, expected_title in expected_titles.items():
        first_line = read_text(rel_path).splitlines()[0].strip()
        if first_line != expected_title:
            errors.append(f"{rel_path}의 제목은 `{expected_title}`여야 합니다.")

    overlay_readme = read_text("docs/project_overlay/README.md")
    local_entrypoint_lines = extract_h2_section(overlay_readme, "권장 로컬 `docs/project_entrypoint.md`")
    if "# Project Harness Entry Point" not in "\n".join(local_entrypoint_lines):
        errors.append("project_overlay/README의 로컬 entrypoint 예시 제목이 최신 구조와 다릅니다.")

    runtime_entrypoint_lines = extract_h2_section(overlay_readme, "권장 runtime entrypoint")
    if "# Agent Runtime Entry Point" not in "\n".join(runtime_entrypoint_lines):
        errors.append("project_overlay/README의 runtime entrypoint 예시 제목이 최신 구조와 다릅니다.")

    expected_sections = {
        "docs/project_overlay/agent_entrypoint_template.md": "## 실행 계약",
        "docs/project_overlay/project_entrypoint_template.md": "## 실행 계약",
    }
    for rel_path, section in expected_sections.items():
        if section not in read_text(rel_path):
            errors.append(f"{rel_path}에 `{section}` 섹션이 없습니다.")

    traversal_phrase_sets = {
        "docs/project_overlay/agent_entrypoint_template.md": (
            "순서대로 모두 읽고 적용",
            "공통 규칙",
            "프로젝트 전용 규칙",
            "중간 문서에서 멈추지 않는다",
        ),
        "docs/project_overlay/project_entrypoint_template.md": (
            "공통 규칙",
            "프로젝트 전용 규칙",
            "순서대로 모두 읽고 적용",
            "둘 중 하나만 읽고 멈추지 않는다",
        ),
        "docs/project_overlay/claude_entrypoint_template.md": (
            "연결된 문서 체인도 끝까지 따라간다",
        ),
        "docs/project_overlay/gemini_entrypoint_template.md": (
            "연결된 문서 체인도 끝까지 따라간다",
        ),
    }
    for rel_path, phrases in traversal_phrase_sets.items():
        text = read_text(rel_path)
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{rel_path}에 traversal contract 문구 `{phrase}`가 없습니다.")

    local_entrypoint_joined = "\n".join(local_entrypoint_lines)
    if "## 실행 계약" not in local_entrypoint_joined:
        errors.append("project_overlay/README의 로컬 entrypoint 예시에 실행 계약 섹션이 없습니다.")
    for phrase in (
        "공통 규칙",
        "프로젝트 전용 규칙",
        "순서대로 모두 읽고 적용",
        "둘 중 하나만 읽고 멈추지 않는다",
    ):
        if phrase not in local_entrypoint_joined:
            errors.append(f"project_overlay/README의 로컬 entrypoint 예시에 traversal contract 문구 `{phrase}`가 없습니다.")

    runtime_entrypoint_joined = "\n".join(runtime_entrypoint_lines)
    if "## 실행 계약" not in runtime_entrypoint_joined:
        errors.append("project_overlay/README의 runtime entrypoint 예시에 실행 계약 섹션이 없습니다.")
    for phrase in (
        "순서대로 모두 읽고 적용",
        "공통 규칙",
        "프로젝트 전용 규칙",
        "중간 문서에서 멈추지 않는다",
    ):
        if phrase not in runtime_entrypoint_joined:
            errors.append(f"project_overlay/README의 runtime entrypoint 예시에 traversal contract 문구 `{phrase}`가 없습니다.")


def check_decisions_templates(errors: list[str]) -> None:
    decisions_index = read_text("docs/project_overlay/decisions_index_template.md")
    required_sections = (
        "## 문서 역할",
        "## 여기에 남기는 것",
        "## 여기에 남기지 않는 것",
        "## 번호 규칙",
        "## 읽기 방법",
        "## Current Decisions",
        "## Superseded Decisions",
    )
    for section in required_sections:
        if section not in decisions_index:
            errors.append(f"decisions_index_template에 `{section}` 섹션이 없습니다.")
    for phrase in (
        "DEC-###-slug.md",
        "최대 번호에 1",
        "renumber하지 않는다",
        "중요한 결정",
        "작은 구현 디테일",
    ):
        if phrase not in decisions_index:
            errors.append(f"decisions_index_template에 핵심 문구 `{phrase}`가 없습니다.")

    decision_record = read_text("docs/project_overlay/decision_record_template.md")
    for phrase in (
        "- Status:",
        "- Type:",
        "- Date:",
        "## Context",
        "## Decision",
        "## Rationale",
        "## Consequences",
        "## Related Docs",
        "## When To Update",
    ):
        if phrase not in decision_record:
            errors.append(f"decision_record_template에 `{phrase}`가 없습니다.")


def check_validator_explainer_docs(errors: list[str]) -> None:
    unresolved = read_text("docs/project_overlay/unresolved_decision_validator.md")
    for phrase in (
        "docs/decisions/README.md",
        "Resolve these required canonical fields first:",
        "Then resolve these blocking unresolved markers:",
        "Still allowed after the blocking items above are fixed:",
    ):
        if phrase not in unresolved:
            errors.append(f"unresolved_decision_validator에 `{phrase}` 설명이 없습니다.")

    consistency = read_text("docs/project_overlay/cross_document_consistency_checker.md")
    for phrase in (
        "필수 섹션",
        "DEC-###-slug.md",
        "listed decision 문서는 기본 record shape",
        "legacy `docs/harness_guide.md`가 남아 있으면",
    ):
        if phrase not in consistency:
            errors.append(f"cross_document_consistency_checker에 `{phrase}` 설명이 없습니다.")


def iter_harness_log_entries(lines: list[str]):
    date_header = None
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        date_match = re.match(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$", line)
        if date_match:
            date_header = date_match.group(1)
            idx += 1
            continue

        if line.startswith("- 관련 파일:"):
            start = idx
            idx += 1
            while idx < len(lines):
                if lines[idx].startswith("- 관련 파일:") or lines[idx].startswith("## "):
                    break
                idx += 1
            yield date_header, lines[start:idx]
            continue
        idx += 1


def check_harness_log(errors: list[str]) -> None:
    lines = read_text("harness.log").splitlines()
    threshold_date = "2026-04-03"

    for date_header, block_lines in iter_harness_log_entries(lines):
        if not date_header:
            errors.append("harness.log 엔트리에 날짜 헤더가 없습니다.")
            continue

        block_text = "\n".join(block_lines)
        required_fields = ["변경:", "이유:", "audit:"]
        for field in required_fields:
            if field not in block_text:
                errors.append(f"harness.log {date_header} 엔트리에 `{field}` 필드가 없습니다.")

        if date_header >= threshold_date and "audit-summary:" not in block_text:
            errors.append(
                f"harness.log {date_header} 엔트리에 `audit-summary:`가 없습니다."
            )

        audit_summary_line = next((line for line in block_lines if "audit-summary:" in line), "")
        if audit_summary_line:
            summary_value = audit_summary_line.split("audit-summary:", 1)[1].strip().lower()
            if summary_value in AUDIT_SUMMARY_PLACEHOLDERS:
                errors.append(
                    f"harness.log {date_header} 엔트리의 `audit-summary:`가 placeholder 상태입니다."
                )

        audit_line = next((line for line in block_lines if "audit:" in line), "")
        if audit_line and (
            "changed-parts" not in audit_line or "whole-harness" not in audit_line
        ):
            errors.append(
                f"harness.log {date_header} 엔트리의 audit 범위에 changed-parts/whole-harness가 모두 없습니다."
            )


def check_language_template_structure(errors: list[str]) -> None:
    for rel_path, required_headings in LANGUAGE_TEMPLATE_REQUIRED_HEADINGS.items():
        headings = extract_h2_headings(read_text(rel_path))
        positions: list[int] = []
        for heading in required_headings:
            if heading not in headings:
                errors.append(f"{rel_path}에 `## {heading}` 섹션이 없습니다.")
                continue
            positions.append(headings.index(heading))

        if positions and positions != sorted(positions):
            errors.append(f"{rel_path}의 공통 골격 섹션 순서가 맞지 않습니다.")


def check_project_facing_maintainer_leakage(errors: list[str]) -> None:
    for path in iter_globbed_files(PROJECT_FACING_MD_GLOBS):
        rel_path = path.relative_to(ROOT).as_posix()
        if rel_path in PROJECT_FACING_LEAKAGE_EXCLUDES:
            continue
        text = path.read_text(encoding="utf-8")
        for forbidden in MAINTAINER_ONLY_REFERENCES:
            if forbidden in text:
                errors.append(
                    f"{rel_path}에 maintainer 전용 경로 `{forbidden}` 참조가 남아 있습니다."
                )


def main() -> int:
    errors: list[str] = []

    check_project_doc_path_consistency(errors)
    check_entrypoint_role_labels(errors)
    check_decisions_templates(errors)
    check_validator_explainer_docs(errors)
    check_harness_log(errors)
    check_language_template_structure(errors)
    check_project_facing_maintainer_leakage(errors)

    if errors:
        print("Harness doc guard failed:")
        for idx, error in enumerate(errors, start=1):
            print(f"{idx}. {error}")
        return 1

    print("Harness doc guard passed: path consistency and harness.log rules are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
