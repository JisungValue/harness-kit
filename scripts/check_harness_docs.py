#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


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
    project_guide_template = read_text("docs/project_overlay/project_harness_guide_template.md")
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
            "project_harness_guide_template의 docs/standard 문서 목록이 README 최소 문서 세트와 다릅니다."
        )

    overlay_local_guide_docs = set(
        extract_codeblock_paths(
            extract_h2_section(overlay_readme, "권장 로컬 `docs/harness_guide.md`"),
            "docs/standard/",
        )
    )
    if overlay_local_guide_docs != expected_project_docs:
        errors.append(
            "project_overlay/README의 권장 로컬 guide 예시 문서 목록이 README 최소 문서 세트와 다릅니다."
        )

    if "프로젝트 `testing_profile.md`" in harness_guide:
        errors.append("harness_guide에 구식 경로 `프로젝트 testing_profile.md` 표현이 남아 있습니다.")


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

        audit_line = next((line for line in block_lines if "audit:" in line), "")
        if audit_line and (
            "changed-parts" not in audit_line or "whole-harness" not in audit_line
        ):
            errors.append(
                f"harness.log {date_header} 엔트리의 audit 범위에 changed-parts/whole-harness가 모두 없습니다."
            )


def main() -> int:
    errors: list[str] = []

    check_project_doc_path_consistency(errors)
    check_harness_log(errors)

    if errors:
        print("Harness doc guard failed:")
        for idx, error in enumerate(errors, start=1):
            print(f"{idx}. {error}")
        return 1

    print("Harness doc guard passed: path consistency and harness.log rules are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
