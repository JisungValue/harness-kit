# Phase 2 Audit

## 목적

구현이 TDD 원칙과 승인된 범위를 지키며 진행되었는지 검토한다.

## 재참조 문서

### 필수 재참조

- `docs/harness/common/audit_policy.md`
- `docs/harness/common/testing_policy.md`
- `docs/harness/common/test_double_policy.md`
- `docs/standard/coding_guidelines_core.md`
- 프로젝트 `docs/standard/architecture.md`
- 프로젝트 `docs/standard/implementation_order.md`
- 프로젝트 `docs/standard/coding_conventions_project.md`
- 프로젝트 `docs/standard/quality_gate_profile.md`

### 조건부 참조

- 없음

## Phase 체크리스트

아래 체크리스트는 감사 시작 전에 빠르게 훑는 진입용 요약이다.
세부 판정은 `감사 항목`과 `승인 불가 기준`을 따른다.

- TDD 순서가 유지되었는가
- 최소 구현 원칙과 범위 통제가 지켜졌는가
- 테스트 더블 선택이 검증 책임과 맞는가
- 선택한 레이어 명칭, 순서, 세분화가 프로젝트 `docs/standard/implementation_order.md`와 정합한가
- 프로젝트 문서가 없거나 모호한 상태에서 임의 순서로 진행하지 않았는가
- 프로젝트 `docs/standard/coding_conventions_project.md`에 정의한 convention과 충돌하지 않는가
- 프로젝트 `docs/standard/quality_gate_profile.md`가 현재 Phase 2까지 적용하도록 정의한 품질 게이트와 모순되거나 생략된 검증이 있는가
- 불필요한 리팩터링이나 선제 추상화가 섞이지 않았는가
- 실패 경로와 핵심 예외가 검토되었는가
- 경계 번역, 민감정보 보호, 외부 에러 차단 규칙이 지켜졌는가

## 프로젝트 구현 순서 준수 감사

- 레이어 명칭, 구현 순서, 세분화 기준의 1차 기준은 프로젝트 `docs/standard/implementation_order.md`다.
- 감사자는 Phase 2 진행 순서가 프로젝트 문서와 일치하는지 먼저 확인한다.
- Core harness는 `안쪽 책임 -> 바깥쪽 책임`과 `테스트 작성 -> 구현 -> 감사` 절차 준수 여부를 확인하며, 프로젝트 상세 순서 자체를 대체하지 않는다.
- 프로젝트 문서가 없거나 현재 TASK 기준으로 모호하면, 구현 진행 정당성은 승인 가능으로 판정하지 않는다.

## 감사 항목

- 각 선택 레이어가 `테스트 작성 -> 구현 -> 감사` 순서로 진행되었는가
- 선택한 레이어 명칭, 순서, 세분화 기준이 프로젝트 `docs/standard/implementation_order.md`와 충돌하지 않는가
- 프로젝트 문서가 없거나 현재 TASK 기준으로 모호한 상태에서 임의 순서를 적용하지 않았는가
- 프로젝트 `docs/standard/coding_conventions_project.md`가 정의한 language/framework convention과 구현이 충돌하지 않는가
- 프로젝트 `docs/standard/quality_gate_profile.md`가 현재 Phase 2까지 적용하도록 정의한 formatter/linter/type checker/test 게이트가 누락되었거나 생략 사유 없이 빠지지 않았는가
- 테스트를 통과시키는 최소 구현이 반영되었는가
- `mock`, `stub`, `fake`가 현재 단위 테스트 책임에 맞게 선택되었는가
- 승인되지 않은 범위 확장이 없는가
- 현재 TASK와 직접 관련 없는 기존 중복 제거, 구조 정리, 선제 추상화를 함께 넣지 않았는가
- 실패 경로와 예외 케이스가 점검되었는가
- 원시 외부 에러가 core로 직접 유입되지 않는가
- 로그와 에러 메시지가 민감정보를 직접 노출하지 않는가
- 경계 바로 앞 레이어가 번역 책임을 수행하는가
- 테스트가 구현 세부사항보다 동작과 계약을 검증하는가
- 새 계약이나 구조 결정이 있으면 문서 반영 필요성이 식별되었는가

## 승인 불가 기준

- 테스트 없이 구현이 먼저 들어감
- 과도한 선제 구현이 포함됨
- 테스트 더블이 구현 내부 협력을 과도하게 고정하거나 현재 책임과 맞지 않게 선택됨
- 선택한 레이어 명칭, 순서, 세분화가 프로젝트 `docs/standard/implementation_order.md`와 충돌함
- 프로젝트 문서가 없거나 모호한 상태에서 기준 확정 없이 구현을 진행함
- 승인되지 않은 범위 확장이 있음
- 현재 변경과 직접 관련 없는 기존 중복 제거 또는 구조 정리가 함께 반영됨
- 외부 포맷이나 원시 에러가 core로 직접 유입됨
- 로그 또는 에러 메시지에 민감정보가 직접 포함됨
- 테스트가 핵심 동작과 계약을 설명하지 못함
