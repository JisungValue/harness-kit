# Downstream Final Layout Contract

## 목적

이 문서는 Epic #153의 downstream greenfield final install 결과를 정의하는 maintainer source-of-truth다.

Issue #154의 범위는 계약 확정이다. 이 문서는 source repo의 물리 구조를 바꾸지 않고, 후속 이슈 #155-#159가 같은 final path와 asset lifecycle 용어를 사용하게 하는 기준을 고정한다.

## 적용 범위

- 대상: greenfield install 완료 뒤 downstream 프로젝트에 남는 runtime-only final surface
- 비대상: source repo의 `bootstrap/`, `downstream/`, `maintainer/` 물리 구조 재배치
- 비대상: brownfield 자동 migration 전체 재설계
- 비대상: package registry 배포와 framework별 semantic migration 자동화

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
      downstream_harness_flow.md
      common/
      phases/
      standard/
        coding_guidelines_core.md
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
  - `docs/process/downstream_harness_flow.md`
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

### Runtime / Operation-Time

install 완료 뒤 downstream 프로젝트가 task 수행, phase 운영, validation에 계속 사용하는 자산이다. final surface에는 root-local canonical path로 남긴다.

- `docs/process/harness_guide.md`
- `docs/process/downstream_harness_flow.md`
- `docs/process/common/*`
- `docs/process/phases/*`
- `docs/process/standard/coding_guidelines_core.md`
- `docs/process/templates/task/*`
- `docs/process/examples/*`
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
| `downstream/docs/downstream_harness_flow.md` | runtime / operation-time | `docs/process/downstream_harness_flow.md` |
| `downstream/docs/harness/common/*` | runtime / operation-time | `docs/process/common/*` |
| `downstream/docs/phase_*/*` | runtime / operation-time | `docs/process/phases/<existing-phase-dir>/*` |
| `downstream/docs/standard/coding_guidelines_core.md` | runtime / operation-time | `docs/process/standard/coding_guidelines_core.md` |
| `downstream/docs/templates/task/*` | runtime / operation-time | `docs/process/templates/task/*` |
| `downstream/docs/examples/*` | runtime / operation-time | `docs/process/examples/*` |
| `bootstrap/scripts/validate_overlay_decisions.py` | runtime / operation-time | `scripts/validate_overlay_decisions.py` |
| `bootstrap/scripts/validate_overlay_consistency.py` | runtime / operation-time | `scripts/validate_overlay_consistency.py` |
| `downstream/scripts/validate_phase_gate.py` | runtime / operation-time | `scripts/validate_phase_gate.py` |
| `bootstrap/scripts/bootstrap_init.py` | install-time only | no final runtime path |
| `bootstrap/scripts/adopt_common.py` | install-time only | no final runtime path |
| `bootstrap/scripts/adopt_dry_run.py` | install-time only | no final runtime path |
| `bootstrap/scripts/adopt_safe_write.py` | install-time only | no final runtime path |
| `bootstrap/scripts/check_first_success_docs.py` | install-time only by default | no final runtime path unless #157 defines an exception |
| `bootstrap/docs/quickstart.md` | install-time only | no final runtime path |
| `bootstrap/docs/how_harness_kit_works.md` | install-time only | no final runtime path |
| `bootstrap/docs/version_support.md` | install-time only | no final runtime path |
| `bootstrap/docs/project_overlay/*` guide/checklist assets | install-time only | no final runtime path |
| `maintainer/docs/*`, `maintainer/scripts/*`, `harness.log`, `tests/*` | maintainer-only | no final runtime path |

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
- `docs/process/standard/coding_guidelines_core.md`
- `scripts/validate_overlay_decisions.py`
- `scripts/validate_overlay_consistency.py`

`CLAUDE.md`와 `GEMINI.md`는 supported adapter entrypoint로 생성하되, first-success의 핵심 chain은 `AGENTS.md -> docs/entrypoint.md`다.

### Runtime Operation Minimum

Runtime operation은 first-success minimum에 phase/task execution surface를 더한 상태다.

- first-success minimum 전체
- `docs/process/downstream_harness_flow.md`
- `docs/process/common/*`
- `docs/process/phases/*`
- `docs/process/templates/task/*`
- `scripts/validate_phase_gate.py`

`docs/process/examples/*`는 runtime reference로 설치해도 되지만, phase/task 실행의 최소 hard dependency는 아니다. final install에 포함하는지 여부는 #156과 #159에서 smoke 기준과 함께 확정한다.

## 후속 이슈 기준

- #155는 project-local generated target을 `docs/entrypoint.md`와 `docs/project/*`로 바꾼다.
- #156은 process/runtime docs target을 `docs/process/*`로 바꾼다.
- #157은 install-time only 자산이 install 중 어디서 쓰이고 install 완료 뒤 무엇이 제거되는지 검증한다.
- #158은 runtime validators와 command examples를 root `scripts/*` 기준으로 바꾼다.
- #159는 greenfield install smoke와 user-facing canonical path surface가 이 문서의 final layout과 일치하는지 확인한다.

후속 이슈에서 이 문서와 다른 path 또는 lifecycle이 필요해지면, 구현보다 먼저 이 계약 문서를 갱신하고 변경 이유를 `harness.log`에 남긴다.
