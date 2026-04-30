# Overlay Completion Checklist

이 문서는 project overlay가 최소 완료 상태에 도달했는지 사람이 읽는 체크리스트로 확인하는 기준이다.

## 목적

- 자동 validator 결과와 별개로, 사람이 overlay의 최소 완료 상태를 한 번 더 점검한다.
- 필수 문서 존재, 미해결 결정, 문서 간 책임 분리, local harness guide 연결, 첫 phase 진행 가능 여부를 같은 체크리스트에서 본다.
- 자동 검사와 수동 점검이 서로 다른 기준을 말하지 않게 한다.

## 사용 시점

- first success 직후 사람이 상태를 검토할 때
- brownfield adopt dry-run 이후 최소 문서 세트를 수동으로 맞춘 뒤
- Phase 2 구현 진입 전 마지막 수동 점검이 필요할 때

## 체크리스트

### 1. 필수 문서 세트

- [ ] `docs/entrypoint.md`가 있다.
- [ ] `docs/project/decisions/README.md`가 있다.
- [ ] `docs/project/standards/architecture.md`가 있다.
- [ ] `docs/project/standards/implementation_order.md`가 있다.
- [ ] `docs/project/standards/coding_conventions_project.md`가 있다.
- [ ] `docs/project/standards/quality_gate_profile.md`가 있다.
- [ ] `docs/project/standards/testing_profile.md`가 있다.
- [ ] `docs/project/standards/commit_rule.md`가 있다.

### 2. local harness guide 연결

- [ ] `docs/entrypoint.md`의 `공통 규칙`에 `docs/process/harness_guide.md`가 있다.
- [ ] `docs/entrypoint.md`의 `프로젝트 전용 규칙`이 필수 `docs/project/standards/*` 문서를 모두 연결한다.
- [ ] `docs/entrypoint.md`의 `프로젝트 결정 문서`가 `docs/project/decisions/README.md`를 연결한다.

### 3. 프로젝트 결정 문서 구조

- [ ] `docs/project/decisions/README.md`가 있다.
- [ ] architecture와 decisions의 역할 경계가 index에서 보인다.
- [ ] 중요한 결정만 남기고 사소한 구현 디테일은 decision 문서 범위 밖이라고 명시돼 있다.
- [ ] 새 decision 번호 규칙(`DEC-###-slug.md`, max+1, renumber 금지)이 index에 적혀 있다.
- [ ] 현재 변경이 중요한 정책/예외/책임 위치를 바꿨다면 관련 decision 문서와 `Related Docs`도 함께 갱신했는지 확인했다.

### 4. runtime instruction entrypoint 연결

- [ ] `AGENTS.md`가 있다.
- [ ] `AGENTS.md`가 `docs/entrypoint.md`를 우선 읽을 문서로 연결한다.
- [ ] `CLAUDE.md`가 `AGENTS.md`를 공통 진입점으로 연결한다.
- [ ] `GEMINI.md`가 `AGENTS.md`를 공통 진입점으로 연결한다.

### 5. 프로젝트 결정 필요 항목 해소 여부

- [ ] `docs/project/standards/coding_conventions_project.md`의 활성 언어/런타임이 확정돼 있다.
- [ ] `docs/project/standards/coding_conventions_project.md`의 bootstrap 기준 문서가 확정돼 있다.
- [ ] `TODO`, `TBD` 같은 미완료 표기가 남아 있지 않다.
- [ ] first-success 시점에 허용되는 placeholder와 금지되는 placeholder를 `validate_overlay_decisions.py --readiness first-success` 결과와 맞춰 확인했다.
- [ ] Phase 2 진입 전이면 `validate_overlay_decisions.py --readiness phase2` 결과도 확인했다.

### 6. profile 간 책임 분리

- [ ] `quality_gate_profile.md`가 `testing_profile.md`를 참조한다.
- [ ] `testing_profile.md`가 `quality_gate_profile.md`를 참조한다.
- [ ] 테스트 실행 명령과 gate 강제 여부는 `quality_gate_profile.md`에 있다.
- [ ] 테스트 범위, 환경, 통합 테스트 세부 기준은 `testing_profile.md`에 있다.
- [ ] `coding_conventions_project.md`가 `quality_gate_profile.md`를 품질/검증 경계 문서로 참조한다.
- [ ] `commit_rule.md`의 `커밋 전 최소 점검 항목`에 compile, type, build, test 또는 테스트 기준이 남아 있다.

### 7. 구조와 진행 순서 연결

- [ ] `implementation_order.md`가 `architecture.md`의 실제 구조와 의존성 방향을 기준으로 작성돼 있다.
- [ ] `architecture.md`와 `implementation_order.md`를 보면 Phase 2에서 어느 레이어부터 진행할지 해석할 수 있다.
- [ ] `implementation_order.md`가 task별 API backlog처럼 쓰이지 않고, 프로젝트 기본 레이어 순서 문서로 유지돼 있다.

### 8. 자동 validator 결과

- [ ] `python3 scripts/validate_overlay_decisions.py . --readiness first-success`가 통과한다.
- [ ] `python3 scripts/validate_overlay_consistency.py .`가 통과한다.
- [ ] Phase 2에 들어갈 준비가 됐다고 주장한다면 `python3 scripts/validate_overlay_decisions.py . --readiness phase2`도 통과한다.

### 9. 첫 phase 진행 가능 여부 판정

- [ ] first-success만 통과했다면 “시작 가능하지만 일부 프로젝트 결정이 남아 있음” 상태로 판정한다.
- [ ] phase2 validator까지 통과했다면 “Phase 2 구현 진입 가능” 상태로 판정한다.
- [ ] `differing files`나 `conflict candidates`가 큰 상태의 brownfield 프로젝트라면, validator 통과 전에도 수동 판단이 더 필요하다고 기록한다.

## 판정 예시

- `first-success ready`
  - 최소 문서 세트 있음
  - decisions index 있음
  - runtime entrypoint 연결 있음
  - first-success validator 통과
  - consistency checker 통과
  - 일부 placeholder는 허용 범위 안에 남아 있음

- `phase2 ready`
  - 위 조건 충족
  - phase2 validator도 통과
  - 실제 구현 순서를 `implementation_order.md`에서 해석 가능

- `not ready`
  - 필수 문서 누락, 금지 placeholder, 교차 계약 실패, 또는 brownfield conflict가 큼

## 자동 검사와의 관계

- `validate_overlay_decisions.py`
  - placeholder와 readiness를 본다.
- `validate_overlay_consistency.py`
  - 문서 간 연결과 책임 경계를 본다.
- 이 체크리스트는 그 두 결과와 문서의 실제 해석 가능 여부를 함께 묶어 사람이 최종 판정하는 용도다.
