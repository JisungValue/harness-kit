# Harness Guide

## 빠른 시작 요약

- 구현성 작업은 이 문서를 시작점으로 사용한다.
- 먼저 `docs/task/{task-title}/issue.md`를 기준으로 작업 범위를 확정한다.
- Phase는 기본적으로 1 -> 2 -> 3 -> 4 -> 5 순서로 진행한다.
- 각 Phase는 `implementation.md` 수행 후 `audit.md` 기준으로 감사를 수행한다.
- 각 Phase는 `implementation -> audit -> 사용자 승인 -> 다음 Phase` 순서를 따른다.
- 다음 Phase로 이동하려면 현재 Phase 감사 결과가 승인 가능이고 사용자 승인이 있어야 한다.
- 각 Phase 또는 레이어의 한 작업 단위가 끝날 때마다 `docs/task/{task-title}/implementation_notes.md`의 `진행 로그`를 갱신한다.
- 공통 정책 해석과 충돌 판단은 `docs/harness/common/process_policy.md`의 우선순위 규칙을 따른다.
- 테스트와 검증은 각각 `testing_policy.md`, `validation_policy.md`를 기준으로 수행한다.
- 현재 TASK와 직접 관련 없는 기존 중복 제거, 구조 정리, 선제 추상화는 별도 리팩터링 태스크로 분리한다.
- 작은 태스크의 경량 운영 예외 가능 여부는 `docs/harness/common/lightweight_task_policy.md`를 따른다.
- 감사는 구현 주체와 분리된 서브에이전트가 수행한다.
- 작업 식별자가 있으면 브랜치 이름은 `{task_id}_{task_name}` 형식을 권장한다.
- 중요한 알고리즘, 구조, 복잡도 trade-off 결정은 사용자에게 고지하고 승인받은 뒤 진행한다.

## 공통 참조 문서

- Phase 운영 규칙: `docs/harness/common/process_policy.md`
- 산출물 규칙: `docs/harness/common/artifact_policy.md`
- 감사 운영 규칙: `docs/harness/common/audit_policy.md`
- 테스트 규칙: `docs/harness/common/testing_policy.md`
- 검증 규칙: `docs/harness/common/validation_policy.md`
- 경량 태스크 예외 규칙: `docs/harness/common/lightweight_task_policy.md`
- 공통 코드 규칙: `docs/standard/coding_guidelines_core.md`

모든 Phase의 구현과 감사는 위 문서들을 함께 참조한다.

## 공통 운영 게이트

- 각 Phase는 `implementation -> audit -> 사용자 승인 -> 다음 Phase` 순서를 따른다.
- 감사가 승인 가능이어도 사용자 승인 없이는 다음 Phase로 이동하지 않는다.
- 재감사 시에는 이전 피드백 해소 여부를 먼저 확인한다.

## 항상 먼저 읽는 문서

아래 문서는 모든 구현 태스크에서 시작 전에 먼저 확인한다.

- `docs/harness_guide.md`
- `docs/harness/common/process_policy.md`
- `docs/harness/common/artifact_policy.md`

아래 문서들은 모든 Phase에서 항상 다시 읽는 문서가 아니다.
현재 수행 중인 Phase와 판단이 필요한 상황에 따라 필요한 문서만 재참조한다.

## Phase별 필수 재참조 문서

### Phase 1. Requirement And Planning

- 구현 중 필수 재참조: `docs/harness/common/artifact_policy.md`
- 감사 직전 필수 재참조: `docs/harness/common/audit_policy.md`
- 조건부 참조: 프로젝트 overlay 문서

### Phase 2. TDD Implementation

- 구현 중 필수 재참조: `docs/harness/common/testing_policy.md`, `docs/standard/coding_guidelines_core.md`
- 감사 직전 필수 재참조: `docs/harness/common/audit_policy.md`
- 조건부 참조: `docs/harness/common/artifact_policy.md`, 프로젝트 overlay 문서

### Phase 3. Integration

- 구현 중 필수 재참조: `docs/harness/common/testing_policy.md`, `docs/harness/common/validation_policy.md`
- 감사 직전 필수 재참조: `docs/harness/common/audit_policy.md`
- 조건부 참조: 프로젝트 `testing_profile.md`

### Phase 4. Validation

- 구현 중 필수 재참조: `docs/harness/common/validation_policy.md`
- 감사 직전 필수 재참조: `docs/harness/common/audit_policy.md`
- 조건부 참조: 없음

### Phase 5. Documentation

- 구현 중 필수 재참조: `docs/harness/common/artifact_policy.md`
- 감사 직전 필수 재참조: `docs/harness/common/audit_policy.md`
- 조건부 참조: 없음

## Phase별 종료 게이트

### Phase 1 종료 게이트

- `requirements.md`가 구현 가능한 수준으로 정리되었는가
- `plan.md`에 테스트 계획, 문서 반영 계획, 비범위가 포함되었는가
- 현재 범위 밖 작업이 계획에 섞이지 않았는가

### Phase 2 종료 게이트

- 선택한 레이어가 `테스트 작성 -> 구현 -> 감사` 순서를 지켰는가
- 테스트를 통과시키는 최소 구현만 반영했는가
- 단위 테스트가 부적절한 책임을 `implementation_notes.md`에 남겼는가

### Phase 3 종료 게이트

- 위임된 책임이 실제 통합 검증 대상으로 반영되었는가
- 연결 책임, 번역 책임, 조립 책임이 검증되었는가
- 형식적 통합 테스트만 추가한 것은 아닌가

### Phase 4 종료 게이트

- 자동 검증과 수동 검증이 구분되어 있는가
- 미실행 검증과 그 사유가 기록되어 있는가
- 잔여 리스크가 누락되지 않았는가

### Phase 5 종료 게이트

- 새 계약, 구조적 결정, 사용법 변경이 관련 문서에 반영되었는가
- 작업 로그가 변경 목적과 결과를 복원 가능하게 남기는가
- 범위 밖 개선 사항이 현재 결과가 아니라 후속 후보로 분리되었는가

## Standard Phases

### Phase 1. Requirement And Planning

- 입력: `issue.md`
- 출력: `requirements.md`, `plan.md`
- 목표: 구현 범위, 제약, 비범위, 작업 계획을 확정한다.

### Phase 2. TDD Implementation

- 입력: `requirements.md`, `plan.md`
- 출력: 테스트, 구현 코드, 필요한 경우 `implementation_notes.md`
- 목표: 승인된 범위 안에서 필요한 레이어만 선택해 구현한다.

### Phase 3. Integration

- 입력: Phase 2 결과물, `implementation_notes.md`
- 출력: 통합 테스트, 연동 검증 결과
- 목표: 단위 테스트로 다루기 어려운 책임과 레이어 간 연결을 검증한다.

### Phase 4. Validation

- 입력: 전체 구현 결과
- 출력: `validation_report.md`
- 목표: 실행한 검증, 미실행 검증, 잔여 리스크를 정리한다.

### Phase 5. Documentation

- 입력: 구현 및 검증 결과
- 출력: 갱신된 문서와 작업 로그
- 목표: 구조적 결정, 사용법, 작업 요약을 복원 가능하게 남긴다.
