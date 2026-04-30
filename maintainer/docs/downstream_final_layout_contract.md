# Downstream Final Layout Contract

## 목적

이 문서는 Epic #153의 downstream greenfield final install 결과와 Epic #166의 final runtime docs surface 경량화 목표를 정의하는 maintainer source-of-truth다.

Issue #154의 범위는 계약 확정이다. 이 문서는 source repo의 물리 구조를 바꾸지 않고, 후속 이슈 #155-#159가 같은 final path와 asset lifecycle 용어를 사용하게 하는 기준을 고정한다.

Issue #167의 범위도 계약 확정이다. 이 단계에서는 실제 파일 이동과 generated/final install 구현을 수행하지 않고, #168-#170이 따라야 할 coding guideline policy path, examples taxonomy, stale path cleanup acceptance를 먼저 고정한다.

## 적용 범위

- 대상: greenfield install 완료 뒤 downstream 프로젝트에 남는 runtime-only final surface
- 비대상: source repo의 `bootstrap/`, `downstream/`, `maintainer/` 물리 구조 재배치
- 비대상: brownfield 자동 migration 전체 재설계
- 비대상: package registry 배포와 framework별 semantic migration 자동화
- 비대상: 기존 brownfield 프로젝트 안의 legacy path를 자동 rename 또는 semantic merge 하는 upgrade migration

source repo에서는 현재 3축 구조를 유지한다.

- `bootstrap/`: install-time source, project-local generated doc template, adoption/readiness helper
- `downstream/`: runtime/process doc와 validator source-of-truth
- `maintainer/`: maintainer-only release, audit, generation, validation source-of-truth

downstream final install은 위 source-of-truth를 consumer-friendly runtime path로 materialize 한 결과다. source repo 자체를 downstream final tree처럼 재배치하지 않는다.

## Downstream Final Canonical Layout

greenfield install 완료 뒤 downstream 프로젝트의 canonical runtime-only layout은 아래 구조다.

```text
project-root/
  AGENTS.md
  CLAUDE.md
  GEMINI.md
  docs/
    entrypoint.md
    project/
      decisions/
        README.md
      standards/
        architecture.md
        implementation_order.md
        coding_conventions_project.md
        quality_gate_profile.md
        testing_profile.md
        commit_rule.md
    process/
      harness_guide.md
      common/
        coding_guidelines_policy.md
      phases/
      templates/
        task/
      examples/
  scripts/
    validate_overlay_decisions.py
    validate_overlay_consistency.py
    validate_phase_gate.py
```

`vendor/harness-kit/...`는 final runtime canonical path가 아니다. greenfield install이 transient delivery 또는 source input으로 bundle을 사용하더라도, install 완료 뒤 runtime/operation-time 명령과 문서 체인은 root-local `docs/*`와 `scripts/*`를 기준으로 설명되어야 한다.

## Entrypoint Contract

- runtime launcher entrypoint는 `AGENTS.md`다.
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`는 모두 `docs/entrypoint.md`를 가리킨다.
- `docs/entrypoint.md`는 `docs/` 바로 아래 top-level docs entrypoint다.
- `docs/entrypoint.md`는 아래 문서를 함께 읽게 해야 한다.
  - `docs/process/harness_guide.md`
  - `docs/project/standards/*`
  - `docs/project/decisions/README.md`
- `docs/project/*`는 project-owned docs다. downstream project가 채우고 유지하는 프로젝트별 결정, 표준, 품질 게이트, 테스트 정책을 둔다.
- `docs/process/*`는 shipped runtime/process docs다. harness-kit가 제공하는 공통 운영 규칙, phase, template, example을 둔다.

## Asset Taxonomy

### Maintainer-Only

`harness-kit` source repo를 유지보수할 때만 쓰는 자산이다. downstream final install surface에 남기지 않는다.

- `maintainer/docs/*`
- `maintainer/scripts/*`
- `harness.log`
- `.github/workflows/harness-doc-guard.yml`
- `tests/*`
- `.git*`

`dist/harness-kit-project-bundle/` 같은 generated delivery artifact는 final runtime surface에 남지 않지만 maintainer-only 자산으로 단정하지 않는다. delivery artifact의 include/exclude 경계는 `maintainer/docs/downstream_bundle_boundary.md`가 관할한다.

### Install-Time Only

greenfield install을 수행하거나 install 직전 이해를 돕는 데 쓰는 자산이다. 명시적 예외가 없는 한 install 완료 뒤 runtime dependency surface에 남기지 않는다.

- `bootstrap/scripts/bootstrap_init.py`
- `bootstrap/scripts/adopt_common.py`
- `bootstrap/scripts/adopt_dry_run.py`
- `bootstrap/scripts/adopt_safe_write.py`
- `bootstrap/scripts/check_first_success_docs.py`
- `bootstrap/docs/project_overlay/*`
- `bootstrap/docs/quickstart.md`
- `bootstrap/docs/how_harness_kit_works.md`
- `bootstrap/docs/version_support.md`
- `bootstrap/language_conventions/*`
- downstream upgrade/adoption guide and checklist assets under `bootstrap/docs/project_overlay/*`

`check_first_success_docs.py`의 final lifecycle은 #157에서 확정한다. #154 기준 기본값은 install-completion helper이며 runtime validator가 아니다. #157이 root `scripts/*` 유지로 예외 처리한다면 이 문서와 후속 command surface를 함께 갱신해야 한다.

Issue #157 기준으로 `check_first_success_docs.py`는 install-completion helper로 확정한다. greenfield install은 bundle을 임시 입력으로 사용하는 동안 이 helper를 실행해 최소 문서 세트 생성을 확인하고, install 완료 뒤에는 root `scripts/*` runtime surface에 남기지 않는다.

### Runtime / Operation-Time

install 완료 뒤 downstream 프로젝트가 task 수행, phase 운영, validation에 계속 사용하는 자산이다. final surface에는 root-local canonical path로 남긴다.

- `docs/process/harness_guide.md`
- `docs/process/common/*`
- `docs/process/common/coding_guidelines_policy.md`
- `docs/process/phases/*`
- `docs/process/templates/task/*`
- final runtime minimum examples defined in the Examples Taxonomy section
- `scripts/validate_overlay_decisions.py`
- `scripts/validate_overlay_consistency.py`
- `scripts/validate_phase_gate.py`

### Project-Local Generated

install 중 template에서 생성되고, install 완료 뒤 downstream project가 직접 소유해 채우는 자산이다.

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `docs/entrypoint.md`
- `docs/project/decisions/README.md`
- `docs/project/standards/architecture.md`
- `docs/project/standards/implementation_order.md`
- `docs/project/standards/coding_conventions_project.md`
- `docs/project/standards/quality_gate_profile.md`
- `docs/project/standards/testing_profile.md`
- `docs/project/standards/commit_rule.md`

## Source To Final Mapping

| source-of-truth path | asset class | final installed path |
| --- | --- | --- |
| `bootstrap/docs/project_overlay/agent_entrypoint_template.md` | project-local generated | `AGENTS.md` |
| `bootstrap/docs/project_overlay/claude_entrypoint_template.md` | project-local generated | `CLAUDE.md` |
| `bootstrap/docs/project_overlay/gemini_entrypoint_template.md` | project-local generated | `GEMINI.md` |
| `bootstrap/docs/project_overlay/project_entrypoint_template.md` | project-local generated | `docs/entrypoint.md` |
| `bootstrap/docs/project_overlay/decisions_index_template.md` | project-local generated | `docs/project/decisions/README.md` |
| `bootstrap/docs/project_overlay/architecture_template.md` | project-local generated | `docs/project/standards/architecture.md` |
| `bootstrap/docs/project_overlay/implementation_order_template.md` | project-local generated | `docs/project/standards/implementation_order.md` |
| `bootstrap/docs/project_overlay/coding_conventions_project_template.md` plus selected `bootstrap/language_conventions/*` | project-local generated | `docs/project/standards/coding_conventions_project.md` |
| `bootstrap/docs/project_overlay/quality_gate_profile_template.md` | project-local generated | `docs/project/standards/quality_gate_profile.md` |
| `bootstrap/docs/project_overlay/testing_profile_template.md` | project-local generated | `docs/project/standards/testing_profile.md` |
| `bootstrap/docs/project_overlay/commit_rule_template.md` | project-local generated | `docs/project/standards/commit_rule.md` |
| `downstream/docs/harness_guide.md` | runtime / operation-time | `docs/process/harness_guide.md` |
| `downstream/docs/harness/common/*` | runtime / operation-time | `docs/process/common/*` |
| `downstream/docs/phase_*/*` | runtime / operation-time | `docs/process/phases/<existing-phase-dir>/*` |
| `downstream/docs/harness/common/coding_guidelines_policy.md` | runtime / operation-time | `docs/process/common/coding_guidelines_policy.md` |
| `downstream/docs/templates/task/*` | runtime / operation-time | `docs/process/templates/task/*` |
| final runtime minimum examples from `downstream/docs/examples/*` | runtime / operation-time | `docs/process/examples/*` |
| `bootstrap/scripts/validate_overlay_decisions.py` | runtime / operation-time | `scripts/validate_overlay_decisions.py` |
| `bootstrap/scripts/validate_overlay_consistency.py` | runtime / operation-time | `scripts/validate_overlay_consistency.py` |
| `downstream/scripts/validate_phase_gate.py` | runtime / operation-time | `scripts/validate_phase_gate.py` |
| `bootstrap/scripts/bootstrap_init.py` | install-time only | no final runtime path |
| `bootstrap/scripts/adopt_common.py` | install-time only | no final runtime path |
| `bootstrap/scripts/adopt_dry_run.py` | install-time only | no final runtime path |
| `bootstrap/scripts/adopt_safe_write.py` | install-time only | no final runtime path |
| `bootstrap/scripts/check_first_success_docs.py` | install-time only install-completion helper | no final runtime path |
| `bootstrap/docs/quickstart.md` | install-time only | no final runtime path |
| `bootstrap/docs/how_harness_kit_works.md` | install-time only | no final runtime path |
| `bootstrap/docs/version_support.md` | install-time only | no final runtime path |
| `bootstrap/docs/project_overlay/*` guide/checklist assets | install-time only | no final runtime path |
| `maintainer/docs/*`, `maintainer/scripts/*`, `harness.log`, `tests/*` | maintainer-only | no final runtime path |

## Coding Guideline Policy Contract

Epic #166 removes the separate final `standard` axis from the downstream runtime docs surface. The common coding baseline is a common process policy, not a standalone `standard` namespace.

- source repo canonical path: `downstream/docs/harness/common/coding_guidelines_policy.md`
- generated bundle path: `docs/process/common/coding_guidelines_policy.md`
- final installed runtime path: `docs/process/common/coding_guidelines_policy.md`

The following names and paths are legacy-only and must disappear from project-facing, generated bundle, and final runtime surfaces except in explicit migration inventory or stale-path audit text:

- `coding_guidelines_core.md`
- `downstream/docs/standard/coding_guidelines_core.md`
- `docs/process/standard/coding_guidelines_core.md`
- `docs/process/standard/`

The source repo may mention those legacy strings only where the purpose is to define removal, stale cleanup, or historical migration context. User-facing runtime docs, generated bundle README/manifest content, bootstrap output, and final install smoke expectations must use `docs/process/common/coding_guidelines_policy.md`.

## Examples Taxonomy

Examples are split by lifecycle. Delivery bundle inclusion and final install inclusion are separate decisions: an example may be shipped in the delivery bundle for reference and still be excluded from the final installed runtime tree.

### Final Runtime Minimum Examples

These examples may remain in the final installed runtime surface because they are small, directly useful during task execution, and do not require maintainer context.

| source path | final path | keep criteria |
| --- | --- | --- |
| `downstream/docs/examples/project-decisions/DEC-001-authorization-validation-location.md` | `docs/process/examples/project-decisions/DEC-001-authorization-validation-location.md` | one-file project decision record example |
| `downstream/docs/examples/sample-lightweight-task/issue.md` | `docs/process/examples/sample-lightweight-task/issue.md` | compact task framing example |
| `downstream/docs/examples/sample-lightweight-task/plan.md` | `docs/process/examples/sample-lightweight-task/plan.md` | compact planning example |
| `downstream/docs/examples/sample-lightweight-task/validation_report.md` | `docs/process/examples/sample-lightweight-task/validation_report.md` | compact validation/audit evidence example |

If #169 finds that even this set adds too much runtime surface, it may reduce the lightweight task example further, but it must keep at least one task-execution example and one decision-record example or explicitly update this contract first.

### Delivery Bundle Reference-Only Examples

These examples may be useful in the generated delivery bundle as optional reference material, but they are not final runtime dependencies and should not be copied into the final installed tree by default.

| source path | bundle path | final install |
| --- | --- | --- |
| `downstream/docs/examples/sample-task/issue.md` | `docs/process/examples/sample-task/issue.md` | excluded by default |
| `downstream/docs/examples/sample-task/requirements.md` | `docs/process/examples/sample-task/requirements.md` | excluded by default |
| `downstream/docs/examples/sample-task/plan.md` | `docs/process/examples/sample-task/plan.md` | excluded by default |
| `downstream/docs/examples/sample-task/phase_status.md` | `docs/process/examples/sample-task/phase_status.md` | excluded by default |
| `downstream/docs/examples/sample-task/implementation_notes.md` | `docs/process/examples/sample-task/implementation_notes.md` | excluded by default |
| `downstream/docs/examples/sample-task/validation_report.md` | `docs/process/examples/sample-task/validation_report.md` | excluded by default |
| `downstream/docs/examples/sample-task/coding_conventions_project_example.md` | `docs/process/examples/sample-task/coding_conventions_project_example.md` | excluded by default |
| `downstream/docs/examples/sample-lightweight-task/requirements.md` | `docs/process/examples/sample-lightweight-task/requirements.md` | excluded by default |
| `downstream/docs/examples/sample-lightweight-task/phase_status.md` | `docs/process/examples/sample-lightweight-task/phase_status.md` | excluded by default |
| `downstream/docs/examples/sample-lightweight-task/implementation_notes.md` | `docs/process/examples/sample-lightweight-task/implementation_notes.md` | excluded by default |

The full `sample-task` subtree is the heavy reference example. It should remain outside the default final runtime tree unless a later contract update proves that a specific file is needed during normal downstream operation.

### Install-Time / Reference Examples

Install-time reference examples explain bootstrap or overlay completion behavior. They are not runtime process docs, and a greenfield install must not require them after install completion.

Current policy: do not add new install-time examples under final `docs/process/examples/*`. If install-time examples are needed, prefer `bootstrap/docs/project_overlay/*` or maintainer docs, and make the final install exclusion explicit in #169.

### Maintainer Smoke / Reference Examples

These files validate maintainer smoke scenarios or document test evidence. They are not final runtime examples and must not be final install dependencies.

| source path | lifecycle | final install |
| --- | --- | --- |
| `downstream/docs/examples/bootstrap-first-success/validation_report.md` | maintainer smoke/reference | excluded |
| `downstream/docs/examples/bootstrap-first-success/overlay_completion_validation_report.md` | maintainer smoke/reference | excluded |

The `bootstrap-first-success/*` validation reports may remain as maintainer reference material only if #169 keeps them out of the final installed runtime surface and prevents downstream operation docs from treating them as required reading.

## Minimum File Sets

### First-Success Minimum

First-success는 downstream project가 runtime entrypoint와 project-owned minimum docs를 갖추고, root-local validator를 실행할 수 있는 상태다.

- `AGENTS.md`
- `docs/entrypoint.md`
- `docs/project/decisions/README.md`
- `docs/project/standards/architecture.md`
- `docs/project/standards/implementation_order.md`
- `docs/project/standards/coding_conventions_project.md`
- `docs/project/standards/quality_gate_profile.md`
- `docs/project/standards/testing_profile.md`
- `docs/project/standards/commit_rule.md`
- `docs/process/harness_guide.md`
- `docs/process/common/coding_guidelines_policy.md`
- `scripts/validate_overlay_decisions.py`
- `scripts/validate_overlay_consistency.py`

`CLAUDE.md`와 `GEMINI.md`는 supported adapter entrypoint로 생성하되, first-success의 핵심 chain은 `AGENTS.md -> docs/entrypoint.md`다.

### Runtime Operation Minimum

Runtime operation은 first-success minimum에 phase/task execution surface를 더한 상태다.

- first-success minimum 전체
- `docs/process/common/*`
- `docs/process/phases/*`
- `docs/process/templates/task/*`
- `scripts/validate_phase_gate.py`

`docs/process/examples/*`는 phase/task 실행의 hard dependency가 아니다. #169는 위 Examples Taxonomy의 final runtime minimum만 default final install에 남기고, delivery bundle reference-only 또는 maintainer smoke/reference 파일은 final install에서 제외해야 한다.

## 후속 이슈 기준

- #155는 project-local generated target을 `docs/entrypoint.md`와 `docs/project/*`로 바꾼다.
- #156은 process/runtime docs target을 `docs/process/*`로 바꾼다.
- #157은 install-time only 자산이 install 중 어디서 쓰이고 install 완료 뒤 무엇이 제거되는지 검증한다.
- #158은 runtime validators와 command examples를 root `scripts/*` 기준으로 바꾼다.
- #159는 greenfield install smoke와 user-facing canonical path surface가 이 문서의 final layout과 일치하는지 확인한다.

후속 이슈에서 이 문서와 다른 path 또는 lifecycle이 필요해지면, 구현보다 먼저 이 계약 문서를 갱신하고 변경 이유를 `harness.log`에 남긴다.

## Epic #166 Acceptance Matrix

| issue | implementation scope | required acceptance |
| --- | --- | --- |
| #168 | move/rename coding guideline policy and remove final standard axis | source path is `downstream/docs/harness/common/coding_guidelines_policy.md`; generated and final path is `docs/process/common/coding_guidelines_policy.md`; `docs/process/standard/` and `coding_guidelines_core.md` are absent from generated/final surfaces; stale bundle cleanup handles old `docs/process/standard/*` output |
| #169 | minimize final examples surface | final install contains only the Final Runtime Minimum Examples or a contract-approved smaller set; `sample-task/*` is not copied into final install by default; `bootstrap-first-success/*` reports are excluded from final install; delivery bundle inclusion is tested separately from final install exclusion |
| #170 | final smoke and docs guard closeout | generated bundle manifest, final installed tree, old path absence, excluded example absence, root validators, doc guard, and full tests all pass against the same contract |

Brownfield/upgrade automatic migration is outside Epic #166. Existing projects with legacy `docs/process/standard/coding_guidelines_core.md` or heavyweight examples need a separate adoption/upgrade task; this epic only defines new generated/final surfaces and stale generated artifact cleanup in bundle/install tooling.

## Install-Time Lifecycle

Issue #157 이후 greenfield install은 아래 순서를 따른다.

1. maintainer source repo에서 canonical delivery bundle을 생성한다.
2. install process가 bundle을 임시 작업 디렉터리로 복사한다.
3. 임시 bundle의 `scripts/bootstrap_init.py`가 project-local generated docs와 `docs/process/*` runtime docs를 target project에 작성한다.
4. 임시 bundle의 `scripts/check_first_success_docs.py`가 install-completion helper로 최소 생성 상태를 확인한다.
5. runtime validator만 target project root의 `scripts/*`로 materialize 한다.
6. 임시 bundle을 폐기하고, target project에 install-time only 자산이 남아 있지 않은지 audit 한다.

final runtime surface에 남으면 안 되는 대표 residue는 아래와 같다.

- `vendor/harness-kit`
- `bootstrap/`
- `bundle_manifest.json`
- `docs/project_overlay/`
- `docs/quickstart.md`
- `docs/how_harness_kit_works.md`
- `docs/version_support.md`
- `scripts/bootstrap_init.py`
- `scripts/adopt_common.py`
- `scripts/adopt_dry_run.py`
- `scripts/adopt_safe_write.py`
- `scripts/check_first_success_docs.py`

기존 `vendor/harness-kit`가 이미 있는 target project에 no-vendor install을 다시 적용할 때는 기본적으로 실패한다. `--force-vendor`는 manifest 또는 bundle-owned path로 판정 가능한 legacy residue만 제거하며, 알 수 없는 사용자 파일이 섞여 있으면 제거하지 않는다.
