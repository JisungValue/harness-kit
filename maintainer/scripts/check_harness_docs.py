#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP_SCRIPT_ROOT = ROOT / "bootstrap" / "scripts"
if str(BOOTSTRAP_SCRIPT_ROOT) not in sys.path:
    sys.path.append(str(BOOTSTRAP_SCRIPT_ROOT))

from bootstrap_init import LANGUAGE_BOOTSTRAP_PATHS


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
    "downstream/docs/downstream_harness_flow.md",
    "downstream/docs/examples/**/*.md",
    "downstream/docs/harness/common/**/*.md",
    "downstream/docs/harness_guide.md",
    "downstream/docs/phase_*/*.md",
    "bootstrap/docs/project_overlay/**/*.md",
    "downstream/docs/standard/coding_guidelines_core.md",
    "downstream/docs/templates/task/**/*.md",
    "bootstrap/docs/how_harness_kit_works.md",
    "bootstrap/docs/quickstart.md",
    "bootstrap/docs/version_support.md",
]

PROJECT_FACING_LEAKAGE_EXCLUDES: set[str] = set()

MAINTAINER_ONLY_REFERENCES = [
    "harness.log",
    "maintainer/docs/",
    "maintainer/scripts/",
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
    overlay_readme = read_text("bootstrap/docs/project_overlay/README.md")
    quickstart = read_text("bootstrap/docs/quickstart.md")
    first_success = read_text("bootstrap/docs/project_overlay/first_success_guide.md")
    diagnostics = read_text("bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md")
    bundle_smoke_doc = read_text("maintainer/docs/downstream_bundle_smoke_validation.md")
    bundle_boundary = read_text("maintainer/docs/downstream_bundle_boundary.md")
    project_guide_template = read_text("bootstrap/docs/project_overlay/project_entrypoint_template.md")
    harness_guide = read_text("downstream/docs/harness_guide.md")

    readme_min = set(extract_bullet_paths(extract_h2_section(readme, "최소 프로젝트 문서 세트")))
    overlay_required = set(
        extract_bullet_paths(extract_h2_section(overlay_readme, "필수 문서"))
    )
    if readme_min != overlay_required:
        errors.append(
            "README 최소 프로젝트 문서 세트와 project_overlay/README 필수 문서가 일치하지 않습니다."
        )

    expected_project_docs = {path for path in readme_min if path.startswith("docs/project/standards/")}

    template_docs = set(extract_bullet_paths(project_guide_template.splitlines(), "docs/project/standards/"))
    if template_docs != expected_project_docs:
        errors.append(
            "project_entrypoint_template의 docs/project/standards 문서 목록이 README 최소 문서 세트와 다릅니다."
        )

    common_rule_docs = set(
        extract_bullet_paths(extract_h2_section(project_guide_template, "공통 규칙"))
    )
    if common_rule_docs != {
        "docs/process/harness_guide.md",
        "docs/process/downstream_harness_flow.md",
    }:
        errors.append("project_entrypoint_template의 공통 규칙 문서 목록이 final layout contract와 다릅니다.")

    overlay_local_guide_docs = set(
        extract_codeblock_paths(
            extract_h2_section(overlay_readme, "권장 로컬 `docs/entrypoint.md`"),
            "docs/project/standards/",
        )
    )
    if overlay_local_guide_docs != expected_project_docs:
        errors.append(
            "project_overlay/README의 권장 로컬 guide 예시 문서 목록이 README 최소 문서 세트와 다릅니다."
        )

    if "프로젝트 `testing_profile.md`" in harness_guide:
        errors.append("harness_guide에 구식 경로 `프로젝트 testing_profile.md` 표현이 남아 있습니다.")

    decisions_lines = extract_h2_section(project_guide_template, "프로젝트 결정 문서")
    if set(extract_bullet_paths(decisions_lines)) != {"docs/project/decisions/README.md"}:
        errors.append("project_entrypoint_template의 프로젝트 결정 문서 목록이 기대값과 다릅니다.")

    for rel_path, text in {
        "README.md": readme,
        "bootstrap/docs/project_overlay/README.md": overlay_readme,
    }.items():
        if "source repo" not in text or "bootstrap한 뒤" not in text:
            errors.append(f"{rel_path}에 source repo와 downstream bootstrap 이후 문맥 구분 설명이 없습니다.")
        if "root `AGENTS.md`" not in text:
            errors.append(f"{rel_path}에 source repo에는 root `AGENTS.md`가 아직 없다는 설명이 없습니다.")

    if "예시 명령의 `vendor/harness-kit/` 부분을 모두 같은 실제 경로로" not in quickstart:
        errors.append("bootstrap/docs/quickstart.md에 non-default vendoring command path localize 설명이 충분하지 않습니다.")

    prerequisite_surfaces = {
        "bootstrap/docs/quickstart.md": quickstart,
        "bootstrap/docs/project_overlay/first_success_guide.md": first_success,
        "bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md": diagnostics,
        "bootstrap/README.md": read_text("bootstrap/README.md"),
    }
    for rel_path, text in prerequisite_surfaces.items():
        if "Python 3" not in text:
            errors.append(f"{rel_path}에 Python 3 prerequisite 설명이 없습니다.")

    helper_command_surfaces = {
        "bootstrap/docs/quickstart.md": quickstart,
        "bootstrap/docs/project_overlay/first_success_guide.md": first_success,
        "bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md": diagnostics,
    }
    for rel_path, text in helper_command_surfaces.items():
        if "check_first_success_docs.py" not in text or "install" not in text:
            errors.append(f"{rel_path}에 install-time first-success helper lifecycle 설명이 없습니다.")

    incremental_surfaces = {
        "bootstrap/docs/quickstart.md": quickstart,
        "bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md": diagnostics,
        "bootstrap/docs/project_overlay/adopt_dry_run.md": read_text("bootstrap/docs/project_overlay/adopt_dry_run.md"),
        "bootstrap/docs/project_overlay/adopt_safe_write.md": read_text("bootstrap/docs/project_overlay/adopt_safe_write.md"),
        "bootstrap/docs/project_overlay/cross_document_consistency_checker.md": read_text(
            "bootstrap/docs/project_overlay/cross_document_consistency_checker.md"
        ),
    }
    for rel_path, text in incremental_surfaces.items():
        if "--mode incremental" not in text:
            errors.append(f"{rel_path}에 incremental consistency mode command 설명이 없습니다.")

    localized_vendoring_surfaces = {
        "bootstrap/docs/quickstart.md": quickstart,
        "bootstrap/docs/project_overlay/first_success_guide.md": first_success,
        "bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md": diagnostics,
    }
    for rel_path, text in localized_vendoring_surfaces.items():
        if "--vendor-path" not in text:
            errors.append(f"{rel_path}에 non-default vendoring `--vendor-path` 경로 설명이 없습니다.")

    workflow_template_surfaces = {
        "README.md": readme,
        "bootstrap/docs/quickstart.md": quickstart,
        "bootstrap/docs/project_overlay/first_success_guide.md": first_success,
        "bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md": diagnostics,
    }
    for rel_path, text in workflow_template_surfaces.items():
        for token in ("docs/project_overlay/harness_doc_guard_workflow_template.yml", "@<pin-tag-or-sha>"):
            if token not in text:
                errors.append(f"{rel_path}에 future-session doc guard onboarding 설명이 부족합니다: {token}")

    if "docs/project_overlay/harness_doc_guard_workflow_template.yml" not in bundle_boundary:
        errors.append(
            "maintainer/docs/downstream_bundle_boundary.md에 project-facing workflow template 경로가 반영되지 않았습니다."
        )

def check_entrypoint_role_labels(errors: list[str]) -> None:
    expected_titles = {
        "downstream/docs/harness_guide.md": "# Harness Core Guide",
        "bootstrap/docs/project_overlay/project_entrypoint_template.md": "# Project Harness Entry Point",
        "bootstrap/docs/project_overlay/agent_entrypoint_template.md": "# Agent Runtime Entry Point",
        "bootstrap/docs/project_overlay/claude_entrypoint_template.md": "# Claude Adapter Entry Point",
        "bootstrap/docs/project_overlay/gemini_entrypoint_template.md": "# Gemini Adapter Entry Point",
    }

    for rel_path, expected_title in expected_titles.items():
        first_line = read_text(rel_path).splitlines()[0].strip()
        if first_line != expected_title:
            errors.append(f"{rel_path}의 제목은 `{expected_title}`여야 합니다.")

    overlay_readme = read_text("bootstrap/docs/project_overlay/README.md")
    local_entrypoint_lines = extract_h2_section(overlay_readme, "권장 로컬 `docs/entrypoint.md`")
    if "# Project Harness Entry Point" not in "\n".join(local_entrypoint_lines):
        errors.append("project_overlay/README의 로컬 entrypoint 예시 제목이 최신 구조와 다릅니다.")

    runtime_entrypoint_lines = extract_h2_section(overlay_readme, "권장 runtime entrypoint")
    if "# Agent Runtime Entry Point" not in "\n".join(runtime_entrypoint_lines):
        errors.append("project_overlay/README의 runtime entrypoint 예시 제목이 최신 구조와 다릅니다.")

    expected_sections = {
        "bootstrap/docs/project_overlay/agent_entrypoint_template.md": "## 실행 계약",
        "bootstrap/docs/project_overlay/project_entrypoint_template.md": "## 실행 계약",
    }
    for rel_path, section in expected_sections.items():
        if section not in read_text(rel_path):
            errors.append(f"{rel_path}에 `{section}` 섹션이 없습니다.")

    traversal_phrase_sets = {
        "bootstrap/docs/project_overlay/agent_entrypoint_template.md": (
            "순서대로 모두 읽고 적용",
            "공통 규칙",
            "프로젝트 전용 규칙",
            "중간 문서에서 멈추지 않는다",
        ),
        "bootstrap/docs/project_overlay/project_entrypoint_template.md": (
            "공통 규칙",
            "프로젝트 전용 규칙",
            "docs/process/downstream_harness_flow.md",
            "순서대로 모두 읽고 적용",
            "둘 중 하나만 읽고 멈추지 않는다",
        ),
        "bootstrap/docs/project_overlay/claude_entrypoint_template.md": (
            "연결된 문서 체인도 끝까지 따라간다",
        ),
        "bootstrap/docs/project_overlay/gemini_entrypoint_template.md": (
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

    runtime_entrypoint_joined = "\n".join(runtime_entrypoint_lines)
    if "## 실행 계약" not in runtime_entrypoint_joined:
        errors.append("project_overlay/README의 runtime entrypoint 예시에 실행 계약 섹션이 없습니다.")


def check_decisions_templates(errors: list[str]) -> None:
    decisions_index = read_text("bootstrap/docs/project_overlay/decisions_index_template.md")
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

    decision_record = read_text("bootstrap/docs/project_overlay/decision_record_template.md")
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
    unresolved = read_text("bootstrap/docs/project_overlay/unresolved_decision_validator.md")
    for phrase in (
        "docs/project/decisions/README.md",
        "Resolve these required canonical fields first:",
        "Then resolve these blocking unresolved markers:",
        "Still allowed after the blocking items above are fixed:",
    ):
        if phrase not in unresolved:
            errors.append(f"unresolved_decision_validator에 `{phrase}` 설명이 없습니다.")

    consistency = read_text("bootstrap/docs/project_overlay/cross_document_consistency_checker.md")
    for phrase in (
        "필수 섹션",
        "DEC-###-slug.md",
        "listed decision 문서는 기본 record shape",
        "legacy `docs/harness_guide.md`가 남아 있으면",
        "--mode incremental",
        "safe gap",
    ):
        if phrase not in consistency:
            errors.append(f"cross_document_consistency_checker에 `{phrase}` 설명이 없습니다.")


def check_repo_local_source_of_truth_docs(errors: list[str]) -> None:
    required_phrases = (
        "repo-local",
        "source-of-truth",
        "기억, 외부 대화, 다른 프로젝트 관행",
        "추측으로 메우지",
    )

    for rel_path in (
        "README.md",
        "downstream/docs/harness_guide.md",
        "bootstrap/docs/how_harness_kit_works.md",
        "downstream/docs/harness/common/process_policy.md",
    ):
        text = read_text(rel_path)
        for phrase in required_phrases:
            if phrase not in text:
                errors.append(f"{rel_path}에 repo-local source-of-truth 핵심 문구 `{phrase}`가 없습니다.")
        handoff_phrase_groups = (
            ("project overlay",),
            ("docs/project/decisions/", "docs/decisions/"),
            ("implementation_notes.md",),
            ("validation_report.md",),
        )
        for handoff_phrases in handoff_phrase_groups:
            if not any(handoff_phrase in text for handoff_phrase in handoff_phrases):
                label = " 또는 ".join(f"`{handoff_phrase}`" for handoff_phrase in handoff_phrases)
                errors.append(f"{rel_path}에 누락된 결정 handoff 문구 {label}가 없습니다.")

    artifact_policy = read_text("downstream/docs/harness/common/artifact_policy.md")
    for phrase in (
        "repo-local source-of-truth",
        "구현 중 결정 사항",
        "결과 요약",
        "문서화/승인 대상으로",
    ):
        if phrase not in artifact_policy:
            errors.append(f"artifact_policy에 repo-local 근거 기록 규칙 `{phrase}`가 없습니다.")

    common_audit_policy = read_text("downstream/docs/harness/common/audit_policy.md")
    if "기억/외부 대화/다른 프로젝트 관행" not in common_audit_policy:
        errors.append("common audit_policy에 repo-local source-of-truth 감사 문구가 없습니다.")

    maintainer_audit_policy = read_text("maintainer/docs/audit_policy.md")
    for phrase in (
        "source-of-truth",
        "repo-local",
        "추측으로 메우지",
    ):
        if phrase not in maintainer_audit_policy:
            errors.append(f"kit_maintenance audit_policy에 `{phrase}` 문구가 없습니다.")

    implementation_template = read_text("downstream/docs/templates/task/implementation_notes.md")
    for phrase in (
        "- repo-local 근거:",
        "- repo에 없어 문서화/승인 대상으로 넘긴 결정:",
    ):
        if phrase not in implementation_template:
            errors.append(f"implementation_notes template에 `{phrase}` 항목이 없습니다.")

    phase_status_template = read_text("downstream/docs/templates/task/phase_status.md")
    for phrase in (
        "## Current State",
        "## Allowed Write Set",
        "## Locked Paths",
        "## Stale Artifacts",
        "## Next Action",
        "## Cleanup",
        "$TASK/phase_status.md",
    ):
        if phrase not in phase_status_template:
            errors.append(f"phase_status template에 `{phrase}` 항목이 없습니다.")

    validation_template = read_text("downstream/docs/templates/task/validation_report.md")
    for phrase in (
        "- 이번 판단의 repo-local 근거:",
        "- repo에 없어 후속 문서화/승인 대상으로 남긴 결정:",
    ):
        if phrase not in validation_template:
            errors.append(f"validation_report template에 `{phrase}` 항목이 없습니다.")


def check_downstream_final_layout_contract(errors: list[str]) -> None:
    contract_path = "maintainer/docs/downstream_final_layout_contract.md"
    contract = read_text(contract_path)
    bundle_boundary = read_text("maintainer/docs/downstream_bundle_boundary.md")
    readme = read_text("README.md")

    required_phrases = (
        "Epic #153",
        "runtime-only final surface",
        "source repo의 물리 구조를 바꾸지",
        "docs/entrypoint.md",
        "docs/project/",
        "docs/process/",
        "scripts/validate_overlay_decisions.py",
        "scripts/validate_overlay_consistency.py",
        "scripts/validate_phase_gate.py",
        "Maintainer-Only",
        "Install-Time Only",
        "Runtime / Operation-Time",
        "Project-Local Generated",
        "First-Success Minimum",
        "Runtime Operation Minimum",
    )
    for phrase in required_phrases:
        if phrase not in contract:
            errors.append(f"{contract_path}에 final layout contract 핵심 문구 `{phrase}`가 없습니다.")

    required_final_paths = (
        "AGENTS.md",
        "docs/project/decisions/README.md",
        "docs/project/standards/coding_conventions_project.md",
        "docs/process/harness_guide.md",
        "docs/process/standard/coding_guidelines_core.md",
        "docs/process/templates/task/*",
        "no final runtime path",
    )
    for path in required_final_paths:
        if path not in contract:
            errors.append(f"{contract_path}에 source-to-final mapping 또는 minimum set 경로 `{path}`가 없습니다.")

    for rel_path, text in {
        "README.md": readme,
        "maintainer/docs/downstream_bundle_boundary.md": bundle_boundary,
    }.items():
        if "maintainer/docs/downstream_final_layout_contract.md" not in text:
            errors.append(f"{rel_path}에서 downstream final layout contract를 참조하지 않습니다.")


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
    check_repo_local_source_of_truth_docs(errors)
    check_downstream_final_layout_contract(errors)
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
