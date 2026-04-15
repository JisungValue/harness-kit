# How Harness Kit Works

이 문서는 `harness-kit`가 `0.1.0`에서 어떤 구조와 개념으로 동작하는지 설명한다.

## 문서 역할

- 이 문서는 개념 설명 문서다.
- 처음 쓰는 사용자가 실제로 어디서 시작할지는 `README.md`와 `docs/quickstart.md`를 먼저 본다.
- downstream 프로젝트 구조와 Phase 흐름 상세는 `docs/downstream_harness_flow.md`가 더 직접적으로 설명한다.

## 한 줄 요약

`harness-kit`는 공통 core 문서와 프로젝트별 overlay 문서를 나누고, bootstrap / validation / dry-run 도구로 안전하게 도입을 돕는 doc-first kit다.

## 핵심 개념

### Core

- 여러 프로젝트에서 공통으로 재사용하는 규칙과 phase 기준이다.
- 이 저장소의 공통 guide와 phase/policy 문서가 여기에 속한다.
- core 운영 판단은 현재 repo 안의 `README`, `docs/*`, `docs/decisions/*`, `scripts/*`, `config` 같은 repo-local 근거를 source-of-truth로 우선한다.
- 대표적으로 아래가 core다.
  - repo의 `docs/harness_guide.md`
  - `docs/harness/common/*`
  - `docs/phase_*`
  - `docs/templates/task/*`

### Project Overlay

- 프로젝트마다 달라져야 하는 문서 세트다.
- 여기서 말하는 문서는 downstream 프로젝트 안에 놓이는 로컬 문서다.
- 이 문서 세트의 project-local 문서 entrypoint는 `docs/project_entrypoint.md`이고, 이 파일이 vendored core guide와 `docs/standard/*`를 함께 연결한다.
- 중요한 정책/예외/책임 배치 결정은 `docs/decisions/README.md`와 `DEC-###-slug.md` 문서로 별도 관리한다.
- repo에 아직 없는 프로젝트 전용 결정은 추측으로 메우지 않고 overlay 또는 decision 문서로 남긴다.
- 대표적으로 아래 문서가 속한다.
  - `docs/project_entrypoint.md`
  - `docs/standard/architecture.md`
  - `docs/standard/implementation_order.md`
  - `docs/standard/coding_conventions_project.md`
  - `docs/standard/quality_gate_profile.md`
  - `docs/standard/testing_profile.md`
  - `docs/standard/commit_rule.md`

### Bootstrap

- overlay 문서를 시작하기 위한 초기 자산과 copier다.
- `bootstrap_init.py`는 `docs/project_overlay/*` template를 source of truth로 사용해 최소 문서 세트와 runtime instruction entrypoint 파일을 생성한다.
- 언어별 convention 초안은 `bootstrap/language_conventions/*`에 있고, 프로젝트 문서로 병합해 쓴다.

### Runtime Instruction Entrypoint

- `AGENTS.md`는 agent runtime이 공통으로 먼저 읽는 runtime launcher entrypoint다.
- `CLAUDE.md`, `GEMINI.md`는 agent별 기본 파일명 차이를 흡수하는 얇은 adapter다.
- 이 entrypoint들은 실제 규칙 본문을 중복 복사하지 않고 documentation/policy entrypoint인 `docs/project_entrypoint.md`로 수렴한다.
- 중요한 계약은 link presence만이 아니라 traversal이다. `AGENTS.md`를 열었으면 `docs/project_entrypoint.md`, 그 문서의 core guide, project-specific supporting docs까지 순서대로 모두 읽고 적용해야 한다.
- 현재 작업이 중요한 프로젝트 결정과 관련 있으면 `docs/decisions/README.md`에서 관련 decision 문서를 찾아 함께 읽고 적용해야 한다.

### Validation

- 문서가 있느냐와, 문서가 준비됐느냐와, 문서가 서로 맞느냐를 분리해서 본다.
- 각각 도구가 다르다.
  - 존재 확인: `check_first_success_docs.py`
  - readiness 확인: `validate_overlay_decisions.py`
  - 교차 정합성 및 runtime instruction 연결 확인: `validate_overlay_consistency.py`

### Adopt Dry-Run

- 기존 프로젝트에 대해 write 없이 현재 상태를 읽는 단계다.
- `adopt_dry_run.py`는 baseline 비교만 하고, merge/write는 하지 않는다.

### Selective Safe Write

- `adopt_safe_write.py`는 `adopt_dry_run.py`와 같은 판정 규칙을 사용해 제한된 write만 수행한다.
- 기본 동작은 missing file create다.
- exact-match target refresh는 `--update-unchanged`로만 수행한다.
- user-modified 파일 overwrite는 명시적으로 선택한 `--force-overwrite` 경로에 한해 수행한다.
- automatic merge나 semantic update는 아직 지원하지 않는다.

### Upgrade Impact Classification

- downstream bundle 변경은 모두 같은 위험도로 반영하지 않는다.
- `docs/project_overlay/harness_upgrade_impact_policy.md`는 bundle 경계 안의 변경을 C0~C4 impact category로 분류한다.
- 이 분류는 adoption timing, manual review 필요성, breaking 가능성을 소비자 관점에서 해석하기 위한 기준이다.

### Repository 와 Downstream Bundle

- 이 저장소 안에는 downstream 프로젝트가 실제로 사용하는 자산과, maintainer가 core를 유지보수할 때만 쓰는 자산이 함께 존재할 수 있다.
- downstream bundle은 project-facing guide, overlay template, bootstrap 자산, deterministic script, sample/example 중심의 배포용 부분집합이다.
- maintainer 감사, 릴리스 기록, 저장소 자체 검증 자산은 downstream bundle의 기본 포함 대상이 아니다.

## 사용자 흐름

### Greenfield

1. `bootstrap_init.py`로 최소 문서 세트를 만든다.
2. runtime entrypoint chain을 따라 `AGENTS.md -> docs/project_entrypoint.md -> core guide + docs/standard/*` 순서를 확인한다.
3. `check_first_success_docs.py` helper command로 존재를 확인한다.
4. `validate_overlay_decisions.py --readiness first-success`로 readiness를 확인한다.
5. `validate_overlay_consistency.py`로 구조적 정합성과 traversal contract를 확인한다.
6. project overlay를 채우고 실제 task를 시작한다.

### Brownfield

1. `adopt_dry_run.py`로 현재 상태를 baseline과 비교한다.
2. `missing` / `differing` / `conflict`를 나눈다.
3. `missing files`가 주 문제면 `adopt_safe_write.py`로 제한적 create-only write를 먼저 적용한다.
4. exact-match target refresh 또는 특정 regular-file overwrite가 꼭 필요할 때만 `--update-unchanged`, `--force-overwrite`를 좁게 사용한다.
5. `differing files`와 path-shape conflict는 기본적으로 수동 판단 대상으로 남긴다.
6. 최소 문서 세트가 어느 정도 맞춰진 뒤 validator를 실행한다.

## 왜 여러 도구로 나누는가

- `bootstrap_init.py`
  - 생성 도구다.
- `validate_overlay_decisions.py`
  - 미결정 상태를 본다.
- `validate_overlay_consistency.py`
  - 문서 간 관계를 본다.
- `adopt_dry_run.py`
  - 기존 상태를 읽는다.
- `adopt_safe_write.py`
  - dry-run과 같은 분류를 기준으로 missing create, exact-match refresh, explicit regular-file overwrite만 수행한다.
- `harness_upgrade_impact_policy.md`
  - bundle 변경이 단순 설명 개선인지, additive update인지, review-required인지, breaking 가능성이 큰지 구분한다.
- `downstream_harness_upgrade_guide.md`
  - 소비자 프로젝트가 새 bundle 변경을 어떤 순서로 읽고, dry-run과 safe write를 어디에 쓰고, 언제 수동 개입해야 하는지 설명한다.
- `downstream_overlay_diff_review_checklist.md`
  - 사람 기준 diff review에서 필수 문서 세트, phase gate, validator, template 영향, safe write 한계를 어떤 순서로 볼지 정리한다.

한 도구가 이 역할을 전부 담당하면, write / validation / inspection의 의미가 섞여서 사용자가 실패 원인을 해석하기 어려워진다.

## Repo-Local Source Of Truth

- 현재 repo 안의 `README`, `docs/*`, `docs/decisions/*`, `scripts/*`, `config`가 작업 기준의 source-of-truth다.
- 기억, 외부 대화, 다른 프로젝트 관행은 참고할 수 있어도 현재 repo 근거보다 우선하지 않는다.
- repo에 없는 결정은 추측으로 메우지 않는다.
- 없는 결정은 project overlay, `docs/decisions/`, `implementation_notes.md`, `validation_report.md` 같은 task workspace 기록으로 handoff하고 필요하면 사용자 승인 대상으로 올린다.

## first-success 와 phase2

### first-success

- “시작 가능한 최소 상태”를 뜻한다.
- 문서 세트, 기본 참조, 최소 언어 기준이 맞는지를 본다.
- 일부 placeholder는 여전히 허용된다.

### phase2

- 실제 구현/감사에 들어갈 준비가 됐는지를 뜻한다.
- first-success보다 더 많은 프로젝트 결정을 요구한다.

## 0.1.0 지원 범위

- 지원한다.
  - 새 프로젝트 문서 세트 생성
  - first-success 경로
  - unresolved decision validation
  - cross-document consistency validation
  - existing-project adopt dry-run
  - existing-project selective safe write/update
  - 로컬 진단 경로

- 아직 지원하지 않는다.
  - automatic merge-based adopt update
  - semantic merge
  - interactive onboarding UI
  - repo-aware assisted adoption

source repo maintainer는 별도로 downstream bundle generation, bundle validation, bundle smoke validation 자산을 운영할 수 있지만, 이는 downstream 프로젝트 사용자가 직접 수행하는 기본 경로가 아니라 maintainer-side release 준비 절차에 속한다.

## 흔한 오해

- `--force`는 merge가 아니다.
  - overwrite다.
- `adopt_dry_run.py`는 write가 아니다.
  - read-only classification이다.
- decision validator와 consistency checker는 같은 게 아니다.
  - 전자는 placeholder/readiness, 후자는 문서 간 계약을 본다.

## 어디서 시작하면 되나

- 처음 쓰는 사용자라면 `docs/quickstart.md`
- 새 프로젝트라면 `docs/project_overlay/first_success_guide.md`
- 기존 프로젝트라면 `docs/project_overlay/adopt_dry_run.md`
- bundle upgrade 절차를 먼저 보려면 `docs/project_overlay/downstream_harness_upgrade_guide.md`
- 사람 기준 diff review 항목을 보려면 `docs/project_overlay/downstream_overlay_diff_review_checklist.md`
- upgrade 위험도를 먼저 판단하려면 `docs/project_overlay/harness_upgrade_impact_policy.md`
- 로컬 진단이 필요하면 `docs/project_overlay/local_diagnostics_and_dry_run.md`
