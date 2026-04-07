#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
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

UNRESOLVED_PATTERNS = (
    ("[프로젝트 결정 필요]", re.compile(r"\[프로젝트 결정 필요\]")),
    ("[팀 결정 필요]", re.compile(r"\[팀 결정 필요\]")),
    ("TODO", re.compile(r"\bTODO\b", re.IGNORECASE)),
    ("TBD", re.compile(r"\bTBD\b", re.IGNORECASE)),
)

ALLOWED_MARKERS_BY_READINESS = {
    "first-success": {
        "docs/standard/coding_conventions_project.md": {"[프로젝트 결정 필요]"},
        "docs/standard/quality_gate_profile.md": {"[프로젝트 결정 필요]"},
        "docs/standard/commit_rule.md": {"[팀 결정 필요]"},
    },
    "phase2": {
        "docs/standard/commit_rule.md": {"[팀 결정 필요]"},
    },
}

IGNORED_MARKER_PATTERNS = {
    "docs/standard/coding_conventions_project.md": (
        re.compile(r"^\s*-\s+`\[프로젝트 결정 필요\]` 표시는 남길 수 있지만"),
        re.compile(r"^\s*-\s+현재 변경에 영향을 주는 항목이 아직 `\[프로젝트 결정 필요\]` 상태면"),
    ),
    "docs/standard/commit_rule.md": (
        re.compile(r"^\s*-\s+`\[팀 결정 필요\]`로 표시한 항목은 팀 정책에 맞게"),
    ),
}

REQUIRED_FIELD_RULES = {
    "first-success": {
        "docs/standard/coding_conventions_project.md": (
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


def collect_missing_docs(project_root: Path) -> list[str]:
    return [path for path in REQUIRED_DOCS if not (project_root / path).exists()]


def collect_findings(project_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for relative_path in REQUIRED_DOCS:
        path = project_root / relative_path
        if not path.exists():
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
        print(
            f"- {finding.path}:{finding.line_number} {finding.marker} -> {finding.line}",
            file=stream,
        )


def collect_required_field_failures(readiness: str, project_root: Path) -> list[Finding]:
    failures: list[Finding] = []
    for relative_path, rules in REQUIRED_FIELD_RULES[readiness].items():
        path = project_root / relative_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for label, resolved_pattern, unresolved_pattern in rules:
            if unresolved_pattern.search(text):
                failures.append(
                    Finding(
                        path=relative_path,
                        line_number=0,
                        marker="required-field",
                        line=f"unresolved canonical {label}",
                    )
                )
                continue

            if resolved_pattern.search(text):
                continue
            failures.append(
                Finding(
                    path=relative_path,
                    line_number=0,
                    marker="required-field",
                    line=f"missing resolved {label}",
                )
            )
    return failures


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    project_root = args.target.expanduser().resolve()

    missing_docs = collect_missing_docs(project_root)
    findings = collect_findings(project_root)
    blocking, allowed = partition_findings(args.readiness, findings)
    blocking.extend(collect_required_field_failures(args.readiness, project_root))

    if missing_docs or blocking:
        print(
            f"overlay decision validation failed for readiness '{args.readiness}'.",
            file=sys.stderr,
        )
        if missing_docs:
            print("Missing required overlay docs:", file=sys.stderr)
            for relative_path in missing_docs:
                print(f"- {relative_path}", file=sys.stderr)
        print_findings("Blocking unresolved markers:", blocking, sys.stderr)
        if allowed:
            print_findings("Allowed unresolved markers for this readiness:", allowed, sys.stderr)
        return 1

    print(f"overlay decision validation passed for readiness '{args.readiness}'.")
    if allowed:
        print_findings("Allowed unresolved markers for this readiness:", allowed, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
