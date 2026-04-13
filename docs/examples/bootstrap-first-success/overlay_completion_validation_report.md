# Overlay Completion Validation Report

## 목적

이 문서는 project overlay completion checklist를 실제로 어떻게 읽고 판정하는지 보여 주는 sample validation 예시다.

## 판정 대상

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `docs/project_entrypoint.md`
- `docs/decisions/README.md`
- `docs/standard/*`
- `validate_overlay_decisions.py`
- `validate_overlay_consistency.py`

## 검토 전제

- greenfield first-success 경로로 최소 문서 세트가 생성됐다.
- local path 현지화와 언어/bootstrap 기준 문서는 최소한 채워져 있다.
- 자동 validator 결과를 사람이 읽는 completion checklist와 함께 판정한다.

## 체크리스트 판정

### 1. 필수 문서 세트

- 판정: 통과
- 근거:
  - `docs/project_entrypoint.md`
  - `docs/decisions/README.md`
  - `docs/standard/architecture.md`
  - `docs/standard/implementation_order.md`
  - `docs/standard/coding_conventions_project.md`
  - `docs/standard/quality_gate_profile.md`
  - `docs/standard/testing_profile.md`
  - `docs/standard/commit_rule.md`
  가 모두 존재한다.

### 2. local harness guide 연결

- 판정: 통과
- 근거:
  - `docs/project_entrypoint.md`가 vendored common guide 경로를 가진다.
  - `docs/standard/*` 문서 세트를 모두 연결한다.

### 3. 프로젝트 결정 문서 구조

- 판정: 통과
- 근거:
  - `docs/decisions/README.md`가 존재한다.
  - project-local 중요한 결정을 architecture와 별도 index로 찾을 수 있다.

### 4. runtime instruction entrypoint 연결

- 판정: 통과
- 근거:
  - `AGENTS.md`가 `docs/project_entrypoint.md`를 우선 읽을 문서로 가진다.
  - `CLAUDE.md`, `GEMINI.md`가 `AGENTS.md`를 공통 진입점으로 가진다.

### 5. 프로젝트 결정 필요 항목 해소 여부

- 판정: first-success 기준 통과, phase2 기준 미통과 가능
- 근거:
  - 활성 언어/런타임과 bootstrap 기준 문서는 채워져 있다.
  - `first-success`에서 허용되는 placeholder는 일부 남아 있을 수 있다.
  - `phase2` readiness는 별도 확인 대상이다.

### 6. profile 간 책임 분리

- 판정: 통과
- 근거:
  - `quality_gate_profile.md`와 `testing_profile.md`가 서로 책임 경계를 참조한다.
  - test 실행 명령과 gate 강제 여부는 quality gate profile 쪽에 있다.
  - 테스트 세부 범위와 환경은 testing profile 쪽에 있다.
  - `commit_rule.md`의 `커밋 전 최소 점검 항목`에 compile / type / build / test 기준이 남아 있다.

### 7. 구조와 진행 순서 연결

- 판정: 통과
- 근거:
  - `implementation_order.md`가 `architecture.md`를 기준 문서로 참조한다.
  - Phase 2에서 어떤 레이어부터 진행할지 해석 가능하다.

### 8. 자동 validator 결과

- 판정: first-success ready
- 근거:
  - `validate_overlay_decisions.py --readiness first-success` 통과
  - `validate_overlay_consistency.py` 통과
  - `phase2` readiness는 아직 추가 결정이 필요할 수 있다.

## 최종 판정

- 상태: `first-success ready`
- 이유:
  - 최소 문서 세트가 갖춰졌고
  - decisions index도 갖춰졌고
  - runtime entrypoint 연결도 갖춰졌고
  - local harness guide 연결이 맞고
  - first-success validator와 consistency checker가 통과하며
  - 사람이 읽는 checklist 기준으로도 첫 phase 시작 전 최소 상태가 확인된다.

## 아직 남은 일

- `phase2` readiness까지 요구한다면 허용 placeholder를 더 줄여야 한다.
- brownfield 프로젝트라면 `adopt_dry_run.py`의 `differing files`와 `conflict candidates`를 별도로 검토해야 한다.

## 관련 문서

- `docs/project_overlay/overlay_completion_checklist.md`
- `docs/project_overlay/unresolved_decision_validator.md`
- `docs/project_overlay/cross_document_consistency_checker.md`
