# Phase 2 Implementation

## 목적

승인된 요구사항을 TDD 원칙과 범위 통제 규칙 안에서 구현한다.

## 재참조 문서

### 필수 재참조

- `docs/process/common/testing_policy.md`
- `docs/process/common/test_double_policy.md`
- `docs/process/common/code_hygiene_policy.md`
- `docs/process/common/design_quality_policy.md`
- `docs/process/common/performance_policy.md`
- `docs/process/common/coding_guidelines_policy.md`
- 프로젝트 `docs/project/standards/architecture.md`
- 프로젝트 `docs/project/standards/implementation_order.md`
- 프로젝트 `docs/project/standards/coding_conventions_project.md`
- 프로젝트 `docs/project/standards/quality_gate_profile.md`

### 조건부 참조

- `docs/process/common/artifact_policy.md`
- `docs/process/common/audit_policy.md`

## Phase 체크리스트

- 실패하는 테스트를 먼저 작성했는가
- 테스트를 통과시키는 최소 구현만 반영했는가
- `mock`, `stub`, `fake` 선택이 현재 단위 테스트 책임에 맞는가
- 필요한 레이어만 선택해 안쪽 책임부터 진행했는가
- 선택한 레이어 명칭, 순서, 세분화 기준이 프로젝트 `docs/project/standards/implementation_order.md`와 일치하는가
- 현재 작업과 직접 관련 있는 언어별 convention 항목을 프로젝트 `docs/project/standards/coding_conventions_project.md`에서 먼저 식별했는가
- 현재 변경에 영향을 주는 언어별 항목이 아직 `[프로젝트 결정 필요]` 상태면 구현 전에 기준을 확정했는가
- 현재 변경과 직접 관련 있는 import/unused/dead code/debug 흔적을 함께 정리했는가
- 현재 변경이 책임 분리, 추상화 수준, 응집도, 경계 분리를 악화시키지 않는가
- 현재 변경이 시간복잡도, 메모리 사용, 중간 컬렉션, 반복 호출, 과도한 I/O를 불필요하게 악화시키지 않는가
- 승인된 입력이나 현재 레이어 산출물이 바뀌면 해당 레이어부터 `테스트 -> 구현 -> 감사`를 다시 수행하는가
- 현재 TASK와 직접 관련 없는 리팩터링을 함께 넣지 않았는가
- 단위 테스트가 부적절한 책임을 `implementation_notes.md`에 기록했는가
- 성능 이슈나 최적화 주장이 있다면 근거와 검증 계획을 `implementation_notes.md`에 남겼는가

## 프로젝트 구현 순서 책임

- 레이어 명칭, 구현 순서, 세분화 기준의 1차 책임은 프로젝트 `docs/project/standards/implementation_order.md`에 있다.
- Core harness는 `안쪽 책임 -> 바깥쪽 책임` 원칙과 `테스트 작성 -> 구현 -> 감사` 절차를 제공하며, 프로젝트별 상세 순서를 고정하지 않는다.
- 특정 TASK에서 어떤 API, use case, 화면, 배치 작업부터 구현할지는 승인된 `plan.md`가 정하고, `implementation_order.md`는 그 판단의 프로젝트 기본 레이어 기준을 제공한다.
- 프로젝트 문서가 없거나 현재 TASK 기준으로 모호하면, Phase 2 구현을 진행하지 않고 프로젝트 문서를 먼저 보강해 기준을 확정한다.

## 입력

- `requirements.md`
- `plan.md`
- 관련 공통 정책 문서
- 프로젝트 `docs/project/standards/architecture.md`
- 프로젝트 `docs/project/standards/implementation_order.md`

## 수행 규칙

- 실패하는 테스트를 먼저 작성한다.
- 테스트를 통과시키는 최소 구현을 반영한다.
- 테스트 더블은 현재 단위 테스트 책임을 설명하는 최소 수준으로 선택한다.
- 승인된 `requirements.md`, `plan.md`, 선택 레이어의 테스트/구현/경계가 바뀌면 가장 이른 영향 레이어부터 `테스트 작성 -> 구현 -> 현재 레이어 감사`를 다시 수행한다.
- 특정 레이어를 다시 수행하면 그 레이어 이후의 감사 결과와 `Phase 2 전체 감사`는 stale 로 본다.
- Phase 2가 다시 승인되기 전에는 Phase 3 이후 문서와 close-out 문서를 수정하지 않는다.
- 필요한 레이어만 선택해 안쪽 책임부터 바깥쪽 책임 순서로 진행한다.
- 레이어 명칭, 선택 순서, 세분화 기준은 프로젝트 `docs/project/standards/implementation_order.md`를 단일 기준으로 따른다.
- `implementation_order.md`를 이번 기획서의 API 구현 체크리스트처럼 다시 쓰지 않는다.
- API/기능 단위의 실제 작업 순서는 `plan.md`에 남기고, 그 순서가 프로젝트 기본 레이어 순서와 충돌하지 않게 맞춘다.
- 프로젝트 전용 framework 또는 language convention이 있으면 프로젝트 `docs/project/standards/coding_conventions_project.md`를 함께 참조한다.
- 현재 작업과 직접 관련 있는 언어별 규칙 범주를 `coding_conventions_project.md`에서 먼저 좁혀 읽고 구현한다.
- 언어별 상세 규칙이 별도 문서로 분리돼 있으면 `coding_conventions_project.md`가 그 경로를 정확히 가리키는지 먼저 확인한다.
- 현재 변경과 직접 관련 있는 규칙이 아직 `[프로젝트 결정 필요]` 상태면 구현 전에 프로젝트 기준을 먼저 확정한다.
- 현재 변경과 직접 관련 있는 import, dead code, 임시 디버깅 흔적은 함께 정리하되, 대규모 hygiene 정리는 별도 태스크로 분리한다.
- 현재 변경이 책임 분리, 추상화 수준, 응집도, 경계 분리를 악화시키지 않는지 `docs/process/common/design_quality_policy.md`의 판정 질문과 빠른 체크리스트 기준으로 함께 확인한다.
- 현재 변경이 시간복잡도, 메모리 사용, 중간 컬렉션, 반복 호출, 과도한 I/O를 불필요하게 악화시키지 않는지 `docs/process/common/performance_policy.md`의 판정 질문과 빠른 체크리스트 기준으로 함께 확인한다.
- 성능 민감 경로이거나 성능 이슈 또는 최적화 주장이 있으면 대상 경로, 근거, 검토 항목, 검증 방법 또는 후속 검증 계획을 `implementation_notes.md`에 기록한다.
- design quality와 performance가 실제로 충돌하면 상세 판정 질문, 대안, 추천안, 근거, 검증 계획, trade-off를 `docs/process/common/performance_policy.md` 기준으로 `implementation_notes.md`에 기록하고 필요하면 사용자 승인 또는 후속 태스크 분리로 넘긴다.
- formatter, linter, type checker, test 게이트의 실제 실행 명령과 현재 Phase 2까지 적용돼야 하는 시점은 프로젝트 `docs/project/standards/quality_gate_profile.md`를 참조한다.
- 프로젝트 문서가 없거나 현재 TASK 기준으로 모호하면 구현 전에 프로젝트 문서를 먼저 보강해 기준을 확정한다.
- 현재 TASK 수행에 직접 필요하지 않은 리팩터링은 함께 진행하지 않는다.
- 단위 테스트가 부적절한 책임은 `implementation_notes.md`에 기록하고 Phase 3로 위임한다.

## 재수행 규칙

- 재수행 범위는 변경 영향이 걸린 가장 이른 레이어부터 시작한다.
- 다시 수행하는 레이어마다 `테스트 작성 -> 구현 -> 감사` 순서를 그대로 적용한다.
- 하나라도 레이어가 다시 수행되면 `Phase 2 전체 감사`는 최신본 기준으로 다시 수행한다.

## 출력

- 실패 후 통과한 테스트
- 구현 코드
- 필요한 경우 `implementation_notes.md`
