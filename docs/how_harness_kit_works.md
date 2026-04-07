# How Harness Kit Works

이 문서는 `harness-kit`가 `0.1.0`에서 어떤 구조와 개념으로 동작하는지 설명한다.

## 한 줄 요약

`harness-kit`는 공통 core 문서와 프로젝트별 overlay 문서를 나누고, bootstrap / validation / dry-run 도구로 안전하게 도입을 돕는 doc-first kit다.

## 핵심 개념

### Core

- 여러 프로젝트에서 공통으로 재사용하는 규칙과 phase 기준이다.
- 이 저장소의 공통 guide와 phase/policy 문서가 여기에 속한다.
- 대표적으로 아래가 core다.
  - repo의 `docs/harness_guide.md`
  - `docs/harness/common/*`
  - `docs/phase_*`
  - `docs/templates/task/*`

### Project Overlay

- 프로젝트마다 달라져야 하는 문서 세트다.
- 여기서 말하는 문서는 downstream 프로젝트 안에 놓이는 로컬 문서다.
- 대표적으로 아래 문서가 속한다.
  - `docs/harness_guide.md`
  - `docs/standard/architecture.md`
  - `docs/standard/implementation_order.md`
  - `docs/standard/coding_conventions_project.md`
  - `docs/standard/quality_gate_profile.md`
  - `docs/standard/testing_profile.md`
  - `docs/standard/commit_rule.md`

### Bootstrap

- overlay 문서를 시작하기 위한 초기 자산과 copier다.
- `bootstrap_init.py`는 `docs/project_overlay/*` template를 source of truth로 사용해 최소 문서 세트를 생성한다.
- 언어별 convention 초안은 `bootstrap/language_conventions/*`에 있고, 프로젝트 문서로 병합해 쓴다.

### Validation

- 문서가 있느냐와, 문서가 준비됐느냐와, 문서가 서로 맞느냐를 분리해서 본다.
- 각각 도구가 다르다.
  - 존재 확인: first-success one-liner
  - readiness 확인: `validate_overlay_decisions.py`
  - 교차 정합성 확인: `validate_overlay_consistency.py`

### Adopt Dry-Run

- 기존 프로젝트에 대해 write 없이 현재 상태를 읽는 단계다.
- `adopt_dry_run.py`는 baseline 비교만 하고, merge/write는 하지 않는다.

## 사용자 흐름

### Greenfield

1. `bootstrap_init.py`로 최소 문서 세트를 만든다.
2. first-success one-liner로 존재를 확인한다.
3. `validate_overlay_decisions.py --readiness first-success`로 readiness를 확인한다.
4. `validate_overlay_consistency.py`로 구조적 정합성을 확인한다.
5. project overlay를 채우고 실제 task를 시작한다.

### Brownfield

1. `adopt_dry_run.py`로 현재 상태를 baseline과 비교한다.
2. `missing` / `differing` / `conflict`를 나눈다.
3. `missing files`를 기준으로 최소 문서 세트를 수동으로 맞춘다.
4. 최소 문서 세트가 어느 정도 맞춰진 뒤 validator를 실행한다.
5. 아직은 수동 판단과 수동 적용이 중심이다.

## 왜 여러 도구로 나누는가

- `bootstrap_init.py`
  - 생성 도구다.
- `validate_overlay_decisions.py`
  - 미결정 상태를 본다.
- `validate_overlay_consistency.py`
  - 문서 간 관계를 본다.
- `adopt_dry_run.py`
  - 기존 상태를 읽는다.

한 도구가 이 역할을 전부 담당하면, write / validation / inspection의 의미가 섞여서 사용자가 실패 원인을 해석하기 어려워진다.

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
  - 로컬 진단 경로

- 아직 지원하지 않는다.
  - automatic adopt write
  - semantic merge
  - interactive onboarding UI
  - repo-aware assisted adoption

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
- 로컬 진단이 필요하면 `docs/project_overlay/local_diagnostics_and_dry_run.md`
