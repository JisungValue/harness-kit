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


LEGACY_PROJECT_ENTRYPOINT = Path("docs/harness_guide.md")
CANONICAL_PROJECT_ENTRYPOINT = Path("docs/project_entrypoint.md")
RUNTIME_ENTRYPOINTS = (
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path("GEMINI.md"),
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
    legacy_migrations: tuple["LegacyEntrypointMigration", ...]


@dataclass(frozen=True)
class LegacyEntrypointMigration:
    legacy_path: Path
    canonical_target: ClassifiedTarget
    runtime_create_targets: tuple[ClassifiedTarget, ...]
    agents_refresh_target: ClassifiedTarget | None
    reason: str
    blocked_reason: str | None

    @property
    def canonical_path(self) -> Path:
        return self.canonical_target.path

    @property
    def safe_to_apply(self) -> bool:
        return self.blocked_reason is None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_primary_heading(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped
    return None


def normalize_legacy_agents_text(text: str) -> str:
    return (
        text.replace("# Agent Entry Point", "# Agent Runtime Entry Point", 1)
        .replace("docs/harness_guide.md", "docs/project_entrypoint.md")
    )


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


def find_item_by_path(
    items: tuple[ClassifiedTarget, ...] | list[ClassifiedTarget],
    path: Path,
) -> ClassifiedTarget | None:
    for item in items:
        if item.path == path:
            return item
    return None


def detect_legacy_entrypoint_migration(
    target_root: Path,
    missing: list[ClassifiedTarget],
    unchanged: list[ClassifiedTarget],
    differing: list[ClassifiedTarget],
    conflicts: list[ClassifiedTarget],
) -> LegacyEntrypointMigration | None:
    legacy_path = target_root / LEGACY_PROJECT_ENTRYPOINT
    if not legacy_path.exists():
        return None

    canonical_path = target_root / CANONICAL_PROJECT_ENTRYPOINT
    canonical_target = (
        find_item_by_path(missing, canonical_path)
        or find_item_by_path(unchanged, canonical_path)
        or find_item_by_path(differing, canonical_path)
        or find_item_by_path(conflicts, canonical_path)
    )
    if canonical_target is None:
        return None

    runtime_create_targets: list[ClassifiedTarget] = []
    for relative_path in RUNTIME_ENTRYPOINTS:
        target = find_item_by_path(missing, target_root / relative_path)
        if target is not None:
            runtime_create_targets.append(target)

    agents_refresh_target: ClassifiedTarget | None = None
    blocked_reason: str | None = None
    reason = "rename preserves the current localized project entrypoint content"

    if not legacy_path.is_file():
        blocked_reason = "legacy project entrypoint path is not a regular file"
    elif canonical_path.exists():
        blocked_reason = (
            "canonical docs/project_entrypoint.md already exists; compare the two files and retire the stale legacy file manually"
        )
    elif canonical_target.reason:
        blocked_reason = f"canonical target path is blocked: {canonical_target.reason}"

    agents_path = target_root / RUNTIME_ENTRYPOINTS[0]
    agents_target = (
        find_item_by_path(unchanged, agents_path)
        or find_item_by_path(differing, agents_path)
        or find_item_by_path(conflicts, agents_path)
        or find_item_by_path(missing, agents_path)
    )
    if agents_target is not None and agents_path.exists() and agents_path.is_file():
        current_agents = read_text(agents_path)
        expected_agents = agents_target.plan_item.content
        if current_agents == expected_agents:
            pass
        elif normalize_legacy_agents_text(current_agents) == expected_agents:
            agents_refresh_target = agents_target
        elif "docs/harness_guide.md" in current_agents:
            blocked_reason = (
                blocked_reason
                or "AGENTS.md still points to docs/harness_guide.md and needs manual review"
            )

    return LegacyEntrypointMigration(
        legacy_path=legacy_path,
        canonical_target=canonical_target,
        runtime_create_targets=tuple(runtime_create_targets),
        agents_refresh_target=agents_refresh_target,
        reason=reason,
        blocked_reason=blocked_reason,
    )


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

    legacy_migration = detect_legacy_entrypoint_migration(
        target_root,
        missing,
        unchanged,
        differing,
        conflicts,
    )
    legacy_migrations: tuple[LegacyEntrypointMigration, ...] = ()
    if legacy_migration is not None:
        legacy_migrations = (legacy_migration,)
        if legacy_migration.safe_to_apply:
            suppressed_paths = {legacy_migration.canonical_path}
            suppressed_paths.update(target.path for target in legacy_migration.runtime_create_targets)
            if legacy_migration.agents_refresh_target is not None:
                suppressed_paths.add(legacy_migration.agents_refresh_target.path)

            missing = [item for item in missing if item.path not in suppressed_paths]
            differing = [item for item in differing if item.path not in suppressed_paths]
            conflicts = [item for item in conflicts if item.path not in suppressed_paths]

    return AdoptClassification(
        target_root=target_root,
        language=language,
        missing=tuple(missing),
        unchanged=tuple(unchanged),
        differing=tuple(differing),
        conflicts=tuple(conflicts),
        legacy_migrations=legacy_migrations,
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


def render_legacy_migration_section(
    title: str,
    items: tuple[LegacyEntrypointMigration, ...],
    target_root: Path,
) -> list[str]:
    if not items:
        return []

    lines = [title]
    for item in items:
        legacy_path = item.legacy_path.relative_to(target_root).as_posix()
        canonical_path = item.canonical_path.relative_to(target_root).as_posix()
        details = [item.reason]

        if item.runtime_create_targets:
            runtime_paths = ", ".join(
                target.path.relative_to(target_root).as_posix()
                for target in item.runtime_create_targets
            )
            details.append(f"also create runtime entrypoints: {runtime_paths}")
        if item.agents_refresh_target is not None:
            details.append("refresh AGENTS.md to the canonical template")
        if item.blocked_reason:
            details.append(item.blocked_reason)

        lines.append(f"- {legacy_path} -> {canonical_path} ({'; '.join(details)})")
    return lines


def find_target_by_relative_path(classification: AdoptClassification, relative_path: str) -> ClassifiedTarget | None:
    normalized = Path(relative_path).as_posix()
    for item in (*classification.missing, *classification.unchanged, *classification.differing, *classification.conflicts):
        if item.path.relative_to(classification.target_root).as_posix() == normalized:
            return item
    return None
