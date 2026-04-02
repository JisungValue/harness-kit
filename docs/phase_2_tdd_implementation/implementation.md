# Phase 2 Implementation

## 목적

승인된 요구사항을 TDD 원칙과 범위 통제 규칙 안에서 구현한다.

## 재참조 문서

### 필수 재참조

- `docs/harness/common/testing_policy.md`
- `docs/harness/common/test_double_policy.md`
- `docs/standard/coding_guidelines_core.md`

### 조건부 참조

- `docs/harness/common/artifact_policy.md`
- `docs/harness/common/audit_policy.md`
- 필요한 경우 프로젝트 overlay 문서

## Phase 체크리스트

- 실패하는 테스트를 먼저 작성했는가
- 테스트를 통과시키는 최소 구현만 반영했는가
- `mock`, `stub`, `fake` 선택이 현재 단위 테스트 책임에 맞는가
- 필요한 레이어만 선택해 안쪽 책임부터 진행했는가
- 현재 TASK와 직접 관련 없는 리팩터링을 함께 넣지 않았는가
- 단위 테스트가 부적절한 책임을 `implementation_notes.md`에 기록했는가

## 입력

- `requirements.md`
- `plan.md`
- 관련 공통 정책 문서
- 필요한 경우 프로젝트 overlay 문서

## 수행 규칙

- 실패하는 테스트를 먼저 작성한다.
- 테스트를 통과시키는 최소 구현을 반영한다.
- 테스트 더블은 현재 단위 테스트 책임을 설명하는 최소 수준으로 선택한다.
- 필요한 레이어만 선택해 안쪽 책임부터 바깥쪽 책임 순서로 진행한다.
- 현재 TASK 수행에 직접 필요하지 않은 리팩터링은 함께 진행하지 않는다.
- 단위 테스트가 부적절한 책임은 `implementation_notes.md`에 기록하고 Phase 3로 위임한다.

## 출력

- 실패 후 통과한 테스트
- 구현 코드
- 필요한 경우 `implementation_notes.md`
