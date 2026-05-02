#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
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

UNRESOLVED_PATTERNS = (
    ("[프로젝트 결정 필요]", re.compile(r"\[프로젝트 결정 필요\]")),
    ("[팀 결정 필요]", re.compile(r"\[팀 결정 필요\]")),
    ("TODO", re.compile(r"\bTODO\b", re.IGNORECASE)),
    ("TBD", re.compile(r"\bTBD\b", re.IGNORECASE)),
)

ALLOWED_MARKERS_BY_READINESS = {
    "first-success": {
        "docs/project/standards/coding_conventions_project.md": {"[프로젝트 결정 필요]"},
        "docs/project/standards/quality_gate_profile.md": {"[프로젝트 결정 필요]"},
        "docs/project/standards/commit_rule.md": {"[팀 결정 필요]"},
    },
    "phase2": {
        "docs/project/standards/commit_rule.md": {"[팀 결정 필요]"},
    },
}

IGNORED_MARKER_PATTERNS = {
    "docs/project/standards/architecture.md": (
        re.compile(r"^\s*-\s+`레이어/책임: \[프로젝트 결정 필요\]`\s*$"),
        re.compile(r"^\s*-\s+`패키지/경로: \[프로젝트 결정 필요; 기획서만 보고 추론하지 않음\]`\s*$"),
    ),
    "docs/project/standards/implementation_order.md": (
        re.compile(r"^\s*-\s+허용 예: `경계 번역 책임: \[프로젝트 결정 필요\]`\s*$"),
    ),
    "docs/project/standards/coding_conventions_project.md": (
        re.compile(r"^\s*-\s+`\[프로젝트 결정 필요\]` 표시는 남길 수 있지만"),
        re.compile(r"^\s*-\s+현재 변경에 영향을 주는 항목이 아직 `\[프로젝트 결정 필요\]` 상태면"),
    ),
    "docs/project/standards/commit_rule.md": (
        re.compile(r"^\s*-\s+`\[팀 결정 필요\]`로 표시한 항목은 팀 정책에 맞게"),
    ),
}

REQUIRED_FIELD_RULES = {
    "first-success": {
        "docs/project/standards/coding_conventions_project.md": (
            (
                "활성 언어/런타임 필드",
                re.compile(
                    r"^- 현재 프로젝트의 활성 언어/런타임:\s+`(?!\[프로젝트 결정 필요\]).+`$",
                    re.MULTILINE,
                ),
                re.compile(
                    r"^- 현재 프로젝트의 활성 언어/런타임:\s+`\[프로젝트 결정 필요\]`$",
                    re.MULTILINE,
                ),
                re.compile(r"^- .*활성 언어.*$", re.MULTILINE),
                "Replace the canonical active runtime line with a resolved value.",
            ),
            (
                "bootstrap 기준 문서 필드",
                re.compile(
                    r"^- bootstrap 출처 또는 기준 언어 문서:\s+`(?!\[프로젝트 결정 필요\]).+`$",
                    re.MULTILINE,
                ),
                re.compile(
                    r"^- bootstrap 출처 또는 기준 언어 문서:\s+`\[프로젝트 결정 필요\]`$",
                    re.MULTILINE,
                ),
                re.compile(r"^- .*bootstrap 출처 또는 기준 언어 문서.*$", re.MULTILINE),
                "Fill the canonical bootstrap reference line with the actual project baseline document.",
            ),
        ),
    },
    "phase2": {},
}


@dataclass(frozen=True)
class Finding:
    path: str
    line_number: int
    marker: str
    line: str
    remediation: str = ""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate unresolved project-overlay decisions for a target project.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=Path.cwd(),
        type=Path,
        help="Target project root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--readiness",
        choices=("first-success", "phase2"),
        default="first-success",
        help="Readiness gate to validate against.",
    )
    return parser.parse_args(argv)


def iter_content_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    in_code_block = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        lines.append((line_number, line))
    return lines


def describe_invalid_doc_shape(path: Path) -> str:
    if path.is_dir():
        return "expected a file but found a directory"
    return "expected a file but found a non-file path"


def collect_required_doc_failures(project_root: Path) -> tuple[list[str], list[Finding]]:
    missing: list[str] = []
    invalid_shapes: list[Finding] = []
    for relative_path in REQUIRED_DOCS:
        path = project_root / relative_path
        if not path.exists():
            missing.append(relative_path)
            continue
        if path.is_file():
            continue
        invalid_shapes.append(
            Finding(
                path=relative_path,
                line_number=0,
                marker="invalid-path",
                line=describe_invalid_doc_shape(path),
            )
        )
    return missing, invalid_shapes


def collect_findings(project_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for relative_path in REQUIRED_DOCS:
        path = project_root / relative_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for line_number, line in iter_content_lines(text):
            for marker, pattern in UNRESOLVED_PATTERNS:
                if pattern.search(line):
                    if should_ignore_line(relative_path, line):
                        continue
                    findings.append(
                        Finding(
                            path=relative_path,
                            line_number=line_number,
                            marker=marker,
                            line=line.strip(),
                        )
                    )
    return findings


def should_ignore_line(relative_path: str, line: str) -> bool:
    for pattern in IGNORED_MARKER_PATTERNS.get(relative_path, ()):
        if pattern.search(line):
            return True
    return False


def is_allowed_finding(readiness: str, finding: Finding) -> bool:
    if finding.marker in {"TODO", "TBD"}:
        return False

    allowed_markers = ALLOWED_MARKERS_BY_READINESS[readiness].get(finding.path, set())
    if finding.marker not in allowed_markers:
        return False

    return True


def partition_findings(readiness: str, findings: list[Finding]) -> tuple[list[Finding], list[Finding]]:
    blocking: list[Finding] = []
    allowed: list[Finding] = []
    for finding in findings:
        if is_allowed_finding(readiness, finding):
            allowed.append(finding)
        else:
            blocking.append(finding)
    return blocking, allowed


def print_findings(header: str, findings: list[Finding], stream) -> None:
    if not findings:
        return
    print(header, file=stream)
    for finding in findings:
        location = f"{finding.path}:{finding.line_number}" if finding.line_number > 0 else finding.path
        next_step = f" | next: {finding.remediation}" if finding.remediation else ""
        print(
            f"- {location} {finding.marker} -> {finding.line}{next_step}",
            file=stream,
        )


def locate_pattern(text: str, pattern: re.Pattern[str]) -> tuple[int, str]:
    match = pattern.search(text)
    if not match:
        return 0, ""

    line_number = text.count("\n", 0, match.start()) + 1
    line = text.splitlines()[line_number - 1].strip()
    return line_number, line


def collect_required_field_failures(readiness: str, project_root: Path) -> list[Finding]:
    failures: list[Finding] = []
    for relative_path, rules in REQUIRED_FIELD_RULES[readiness].items():
        path = project_root / relative_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for label, resolved_pattern, unresolved_pattern, locator_pattern, remediation in rules:
            if unresolved_pattern.search(text):
                line_number, line = locate_pattern(text, unresolved_pattern)
                failures.append(
                    Finding(
                        path=relative_path,
                        line_number=line_number,
                        marker="required-field",
                        line=f"unresolved canonical {label}" if not line else line,
                        remediation=remediation,
                    )
                )
                continue

            if resolved_pattern.search(text):
                continue
            line_number, line = locate_pattern(text, locator_pattern)
            failures.append(
                Finding(
                    path=relative_path,
                    line_number=line_number,
                    marker="required-field",
                    line=f"missing resolved {label}" if not line else line,
                    remediation=remediation,
                )
            )
    return failures


def suppress_duplicate_required_field_markers(
    blocking: list[Finding],
    allowed: list[Finding],
    required_field_failures: list[Finding],
) -> tuple[list[Finding], list[Finding]]:
    duplicate_locations = {
        (finding.path, finding.line_number)
        for finding in required_field_failures
        if finding.line_number > 0
    }

    def keep(finding: Finding) -> bool:
        if finding.marker == "required-field":
            return True
        if finding.marker != "[프로젝트 결정 필요]":
            return True
        return (finding.path, finding.line_number) not in duplicate_locations

    return [finding for finding in blocking if keep(finding)], [finding for finding in allowed if keep(finding)]


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    project_root = args.target.expanduser().resolve()

    missing_docs, invalid_doc_shapes = collect_required_doc_failures(project_root)
    findings = collect_findings(project_root)
    blocking, allowed = partition_findings(args.readiness, findings)
    required_field_failures = collect_required_field_failures(args.readiness, project_root)
    blocking.extend(required_field_failures)
    blocking, allowed = suppress_duplicate_required_field_markers(blocking, allowed, required_field_failures)

    if missing_docs or invalid_doc_shapes or blocking:
        print(
            f"overlay decision validation failed for readiness '{args.readiness}'.",
            file=sys.stderr,
        )
        if missing_docs:
            print("Missing required overlay docs:", file=sys.stderr)
            for relative_path in missing_docs:
                print(f"- {relative_path}", file=sys.stderr)
        if invalid_doc_shapes:
            print_findings("Required overlay docs with invalid path shapes:", invalid_doc_shapes, sys.stderr)
        required_field_blocking = [finding for finding in blocking if finding.marker == "required-field"]
        unresolved_blocking = [finding for finding in blocking if finding.marker != "required-field"]
        if required_field_blocking:
            print_findings("Resolve these required canonical fields first:", required_field_blocking, sys.stderr)
        if unresolved_blocking:
            print_findings("Then resolve these blocking unresolved markers:", unresolved_blocking, sys.stderr)
        if allowed:
            print_findings("Still allowed after the blocking items above are fixed:", allowed, sys.stderr)
        return 1

    print(f"overlay decision validation passed for readiness '{args.readiness}'.")
    if allowed:
        print_findings("Allowed unresolved markers for this readiness:", allowed, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
