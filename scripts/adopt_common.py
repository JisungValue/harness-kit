from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from bootstrap_init import (
    PlannedFile,
    PreflightError,
    ROOT,
    build_plan,
    collect_preflight_errors,
)


@dataclass(frozen=True)
class ClassifiedTarget:
    plan_item: PlannedFile
    reason: str = ""

    @property
    def path(self) -> Path:
        return self.plan_item.destination

    @property
    def source(self) -> Path:
        return self.plan_item.source


@dataclass(frozen=True)
class AdoptClassification:
    target_root: Path
    language: str
    missing: tuple[ClassifiedTarget, ...]
    unchanged: tuple[ClassifiedTarget, ...]
    differing: tuple[ClassifiedTarget, ...]
    conflicts: tuple[ClassifiedTarget, ...]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_primary_heading(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped
    return None


def classify_difference(plan_item: PlannedFile) -> str | None:
    if not plan_item.destination.exists():
        return None
    if not plan_item.destination.is_file():
        return "target path is not a regular file"

    current_text = read_text(plan_item.destination)
    expected_heading = extract_primary_heading(plan_item.content)
    current_heading = extract_primary_heading(current_text)
    if expected_heading and current_heading != expected_heading:
        return f"primary heading differs from expected template ({expected_heading})"

    return None


def find_preflight_reason(plan_item: PlannedFile, preflight_errors: list[PreflightError]) -> str | None:
    for error in preflight_errors:
        if error.path == plan_item.destination or error.path in plan_item.destination.parents:
            return error.reason
    return None


def classify_targets(target_root: Path, language: str) -> AdoptClassification:
    plan = build_plan(target_root, language)
    preflight_errors = collect_preflight_errors(target_root, plan)

    missing: list[ClassifiedTarget] = []
    unchanged: list[ClassifiedTarget] = []
    differing: list[ClassifiedTarget] = []
    conflicts: list[ClassifiedTarget] = []

    for item in plan:
        preflight_reason = find_preflight_reason(item, preflight_errors)
        if preflight_reason:
            conflicts.append(ClassifiedTarget(plan_item=item, reason=preflight_reason))
            continue

        if not item.destination.exists():
            missing.append(ClassifiedTarget(plan_item=item))
            continue

        if not item.destination.is_file():
            conflicts.append(ClassifiedTarget(plan_item=item, reason="target path is not a regular file"))
            continue

        current_text = read_text(item.destination)
        if current_text == item.content:
            unchanged.append(ClassifiedTarget(plan_item=item))
            continue

        conflict_reason = classify_difference(item)
        if conflict_reason:
            conflicts.append(ClassifiedTarget(plan_item=item, reason=conflict_reason))
            continue

        differing.append(ClassifiedTarget(plan_item=item))

    return AdoptClassification(
        target_root=target_root,
        language=language,
        missing=tuple(missing),
        unchanged=tuple(unchanged),
        differing=tuple(differing),
        conflicts=tuple(conflicts),
    )


def render_section(title: str, items: tuple[ClassifiedTarget, ...], target_root: Path) -> list[str]:
    if not items:
        return []
    lines = [title]
    for item in items:
        relative_path = item.path.relative_to(target_root).as_posix()
        source_path = item.source.relative_to(ROOT).as_posix()
        if item.reason:
            lines.append(f"- {relative_path} <- {source_path} ({item.reason})")
        else:
            lines.append(f"- {relative_path} <- {source_path}")
    return lines


def find_target_by_relative_path(classification: AdoptClassification, relative_path: str) -> ClassifiedTarget | None:
    normalized = Path(relative_path).as_posix()
    for item in (*classification.missing, *classification.unchanged, *classification.differing, *classification.conflicts):
        if item.path.relative_to(classification.target_root).as_posix() == normalized:
            return item
    return None
