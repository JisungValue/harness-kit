#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


PHASE_RE = re.compile(r"^Phase ([1-5])$")
VALID_TASK_STATUSES = {"active", "blocked", "approval_required", "completed"}
NONE_MARKERS = {"없음", "none", "n/a"}


@dataclass(frozen=True)
class PhaseStatus:
    task_status: str
    current_phase: str
    current_gate: str
    last_approved_phase: str
    allowed_write_set: list[str]
    locked_paths: list[str]
    stale_artifacts: list[str]
    next_action: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate task phase gates and write-set violations from phase_status.md.",
    )
    parser.add_argument(
        "workspace",
        type=Path,
        help="Task workspace path that contains phase_status.md.",
    )
    parser.add_argument(
        "--paths",
        nargs="*",
        default=None,
        help="Optional repo-relative candidate paths to validate instead of git status changes.",
    )
    return parser.parse_args(argv)


def find_repo_root(start: Path) -> Path:
    resolved = start.resolve()
    for candidate in (resolved, *resolved.parents):
        if (candidate / ".git").exists():
            return candidate
    raise ValueError(f"Could not locate repository root from {start}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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
    for idx in range(start, len(lines)):
        if lines[idx].startswith("## "):
            end = idx
            break
    return lines[start:end]


def extract_field(lines: list[str], label: str) -> str:
    pattern = re.compile(rf"^\s*-\s+{re.escape(label)}:\s+`?(.+?)`?\s*$")
    for line in lines:
        match = pattern.match(line)
        if match:
            return match.group(1).strip()
    raise ValueError(f"Missing field: {label}")


def extract_code_bullets(lines: list[str]) -> list[str]:
    entries: list[str] = []
    for line in lines:
        match = re.match(r"^\s*-\s+`([^`]+)`\s*$", line)
        if match:
            entries.append(match.group(1).strip())
    return entries


def extract_freeform_bullets(lines: list[str]) -> list[str]:
    entries: list[str] = []
    for line in lines:
        match = re.match(r"^\s*-\s+(.+?)\s*$", line)
        if not match:
            continue
        value = match.group(1).strip()
        if value.startswith("`") and value.endswith("`"):
            value = value[1:-1].strip()
        entries.append(value)
    return entries


def extract_freeform_text(lines: list[str]) -> str:
    return "\n".join(line.strip() for line in lines if line.strip())


def normalize_phase_status(workspace: Path) -> tuple[Path, Path, PhaseStatus]:
    repo_root = find_repo_root(workspace)
    workspace = workspace.resolve()
    phase_status_path = workspace / "phase_status.md"
    if not phase_status_path.is_file():
        raise ValueError(f"Missing phase_status.md in workspace: {workspace}")

    text = read_text(phase_status_path)
    current_state_lines = extract_h2_section(text, "Current State")
    allowed_lines = extract_h2_section(text, "Allowed Write Set")
    locked_lines = extract_h2_section(text, "Locked Paths")
    stale_lines = extract_h2_section(text, "Stale Artifacts")
    next_action_lines = extract_h2_section(text, "Next Action")
    extract_h2_section(text, "Cleanup")

    status = PhaseStatus(
        task_status=extract_field(current_state_lines, "Task Status").lower(),
        current_phase=extract_field(current_state_lines, "Current Phase"),
        current_gate=extract_field(current_state_lines, "Current Gate"),
        last_approved_phase=extract_field(current_state_lines, "Last Approved Phase"),
        allowed_write_set=extract_code_bullets(allowed_lines),
        locked_paths=extract_code_bullets(locked_lines),
        stale_artifacts=extract_freeform_bullets(stale_lines),
        next_action=extract_freeform_text(next_action_lines),
    )
    return repo_root, workspace, status


def normalize_pattern(pattern: str, workspace_rel: Path) -> str:
    if pattern.startswith("$TASK/"):
        suffix = pattern[len("$TASK/") :]
        return (workspace_rel / suffix).as_posix()
    return pattern


def phase_number(value: str) -> int | None:
    match = PHASE_RE.match(value)
    if not match:
        return None
    return int(match.group(1))


def validate_phase_status(status: PhaseStatus, workspace_rel: Path) -> list[str]:
    errors: list[str] = []

    if status.task_status not in VALID_TASK_STATUSES:
        errors.append(f"invalid task status: {status.task_status}")

    current_phase_number = phase_number(status.current_phase)
    if current_phase_number is None:
        errors.append(f"invalid current phase: {status.current_phase}")

    if not status.current_gate:
        errors.append("current gate must not be empty")

    last_approved = status.last_approved_phase
    last_approved_number = None
    if last_approved not in NONE_MARKERS:
        last_approved_number = phase_number(last_approved)
        if last_approved_number is None:
            errors.append(f"invalid last approved phase: {last_approved}")

    if current_phase_number is not None and last_approved_number is not None and last_approved_number > current_phase_number:
        errors.append("last approved phase cannot be later than current phase")

    if not status.allowed_write_set:
        errors.append("allowed write set must not be empty")

    normalized_allowed = {normalize_pattern(pattern, workspace_rel) for pattern in status.allowed_write_set}
    expected_phase_status = (workspace_rel / "phase_status.md").as_posix()
    if expected_phase_status not in normalized_allowed:
        errors.append("allowed write set must include `$TASK/phase_status.md`")

    normalized_locked = [normalize_pattern(pattern, workspace_rel) for pattern in status.locked_paths]
    normalized_stale = [normalize_pattern(entry, workspace_rel) for entry in status.stale_artifacts if entry not in NONE_MARKERS]

    for stale_entry in normalized_stale:
        if not any(path_matches_pattern(stale_entry, locked_pattern) for locked_pattern in normalized_locked):
            errors.append(f"stale artifact must also be locked: {stale_entry}")

    if status.task_status != "completed" and not status.next_action:
        errors.append("next action must not be empty while task is active")

    if status.task_status == "completed" and normalized_stale:
        errors.append("completed task cannot keep stale artifacts in phase_status.md")

    return errors


def path_matches_pattern(path: str, pattern: str) -> bool:
    return Path(path).match(pattern)


def collect_git_status_paths(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--porcelain", "--untracked-files=all"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or "git status failed")

    paths: list[str] = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        path_field = line[3:]
        if " -> " in path_field:
            path_field = path_field.split(" -> ", 1)[1]
        paths.append(path_field.strip())
    return paths


def validate_candidate_paths(
    candidate_paths: list[str],
    workspace_rel: Path,
    status: PhaseStatus,
) -> list[str]:
    errors: list[str] = []
    allowed_patterns = [normalize_pattern(pattern, workspace_rel) for pattern in status.allowed_write_set]
    locked_patterns = [normalize_pattern(pattern, workspace_rel) for pattern in status.locked_paths]

    for candidate in sorted(set(candidate_paths)):
        if any(path_matches_pattern(candidate, pattern) for pattern in locked_patterns):
            errors.append(f"locked path violation: {candidate}")
            continue
        if not any(path_matches_pattern(candidate, pattern) for pattern in allowed_patterns):
            errors.append(f"outside allowed write set: {candidate}")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        repo_root, workspace, status = normalize_phase_status(args.workspace)
    except ValueError as exc:
        print(f"phase gate validation failed: {exc}", file=sys.stderr)
        return 1

    workspace_rel = workspace.relative_to(repo_root)
    errors = validate_phase_status(status, workspace_rel)

    candidate_paths = args.paths
    if candidate_paths is None:
        try:
            candidate_paths = collect_git_status_paths(repo_root)
        except ValueError as exc:
            print(f"phase gate validation failed: {exc}", file=sys.stderr)
            return 1

    errors.extend(validate_candidate_paths(candidate_paths, workspace_rel, status))

    if errors:
        print(
            f"phase gate validation failed for {workspace_rel.as_posix()}.",
            file=sys.stderr,
        )
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"phase gate validation passed for {workspace_rel.as_posix()}.")
    if candidate_paths:
        print("Validated paths:")
        for path in sorted(set(candidate_paths)):
            print(f"- {path}")
    else:
        print("Validated paths: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
