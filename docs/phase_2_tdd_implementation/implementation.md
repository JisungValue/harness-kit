# Phase 2 Implementation

## 목적

승인된 요구사항을 TDD 원칙과 범위 통제 규칙 안에서 구현한다.

## 재참조 문서

### 필수 재참조

- `docs/harness/common/testing_policy.md`
- `docs/harness/common/test_double_policy.md`
- `docs/standard/coding_guidelines_core.md`
- 프로젝트 `docs/standard/architecture.md`
- 프로젝트 `docs/standard/implementation_order.md`
- 프로젝트 `docs/standard/coding_conventions_project.md`
- 프로젝트 `docs/standard/quality_gate_profile.md`

### 조건부 참조

- `docs/harness/common/artifact_policy.md`
- `docs/harness/common/audit_policy.md`

## Phase 체크리스트

- 실패하는 테스트를 먼저 작성했는가
- 테스트를 통과시키는 최소 구현만 반영했는가
- `mock`, `stub`, `fake` 선택이 현재 단위 테스트 책임에 맞는가
- 필요한 레이어만 선택해 안쪽 책임부터 진행했는가
- 선택한 레이어 명칭, 순서, 세분화 기준이 프로젝트 `docs/standard/implementation_order.md`와 일치하는가
- 현재 작업과 직접 관련 있는 언어별 convention 항목을 프로젝트 `docs/standard/coding_conventions_project.md`에서 먼저 식별했는가
- 현재 변경에 영향을 주는 언어별 항목이 아직 `[프로젝트 결정 필요]` 상태면 구현 전에 기준을 확정했는가
- 현재 TASK와 직접 관련 없는 리팩터링을 함께 넣지 않았는가
- 단위 테스트가 부적절한 책임을 `implementation_notes.md`에 기록했는가

## 프로젝트 구현 순서 책임

- 레이어 명칭, 구현 순서, 세분화 기준의 1차 책임은 프로젝트 `docs/standard/implementation_order.md`에 있다.
- Core harness는 `안쪽 책임 -> 바깥쪽 책임` 원칙과 `테스트 작성 -> 구현 -> 감사` 절차를 제공하며, 프로젝트별 상세 순서를 고정하지 않는다.
- 프로젝트 문서가 없거나 현재 TASK 기준으로 모호하면, Phase 2 구현을 진행하지 않고 프로젝트 문서를 먼저 보강해 기준을 확정한다.

## 입력

- `requirements.md`
- `plan.md`
- 관련 공통 정책 문서
- 프로젝트 `docs/standard/architecture.md`
- 프로젝트 `docs/standard/implementation_order.md`

## 수행 규칙

- 실패하는 테스트를 먼저 작성한다.
- 테스트를 통과시키는 최소 구현을 반영한다.
- 테스트 더블은 현재 단위 테스트 책임을 설명하는 최소 수준으로 선택한다.
- 필요한 레이어만 선택해 안쪽 책임부터 바깥쪽 책임 순서로 진행한다.
- 레이어 명칭, 선택 순서, 세분화 기준은 프로젝트 `docs/standard/implementation_order.md`를 단일 기준으로 따른다.
- 프로젝트 전용 framework 또는 language convention이 있으면 프로젝트 `docs/standard/coding_conventions_project.md`를 함께 참조한다.
- 현재 작업과 직접 관련 있는 언어별 규칙 범주를 `coding_conventions_project.md`에서 먼저 좁혀 읽고 구현한다.
- 언어별 상세 규칙이 별도 문서로 분리돼 있으면 `coding_conventions_project.md`가 그 경로를 정확히 가리키는지 먼저 확인한다.
- 현재 변경과 직접 관련 있는 규칙이 아직 `[프로젝트 결정 필요]` 상태면 구현 전에 프로젝트 기준을 먼저 확정한다.
- formatter, linter, type checker, test 게이트의 실제 실행 명령과 현재 Phase 2까지 적용돼야 하는 시점은 프로젝트 `docs/standard/quality_gate_profile.md`를 참조한다.
- 프로젝트 문서가 없거나 현재 TASK 기준으로 모호하면 구현 전에 프로젝트 문서를 먼저 보강해 기준을 확정한다.
- 현재 TASK 수행에 직접 필요하지 않은 리팩터링은 함께 진행하지 않는다.
- 단위 테스트가 부적절한 책임은 `implementation_notes.md`에 기록하고 Phase 3로 위임한다.

## 출력

- 실패 후 통과한 테스트
- 구현 코드
- 필요한 경우 `implementation_notes.md`
