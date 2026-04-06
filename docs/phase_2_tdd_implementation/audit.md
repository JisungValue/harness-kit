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
- 현재 변경과 직접 관련 있는 언어별 convention 항목이 `coding_conventions_project.md`에 식별 가능하게 정리돼 있는가
- 현재 변경과 직접 관련 있는 언어별 금지 패턴을 실제로 위반하지 않았는가
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
- 현재 변경과 직접 관련 있는 언어별 규칙 범주가 `coding_conventions_project.md` 또는 그가 참조하는 언어 문서에서 식별 가능한가
- 현재 변경에 직접 영향을 주는 언어별 항목이 아직 `[프로젝트 결정 필요]` 상태로 남아 있지 않은가
- 현재 변경이 프로젝트 convention 문서의 주요 금지 패턴을 사실상 새 기본값으로 만들지 않는가
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

## 언어별 convention 감사 체크리스트

- 현재 프로젝트가 실제로 사용하는 언어/런타임이 `coding_conventions_project.md`에 명시되어 있는가
- bootstrap 템플릿을 복사했다면 현재 프로젝트에 적용하지 않는 언어/런타임 규칙이 정리되지 않은 채 남아 있지 않은가
- 언어별 상세 규칙을 별도 문서로 뺐다면 `coding_conventions_project.md`가 정확한 경로를 참조하는가
- 현재 변경과 직접 관련 있는 규칙 범주(naming, modeling, error handling, concurrency, collections, testing, interop 등)가 식별 가능하게 정리돼 있는가
- 현재 변경에 영향을 주는 항목이 아직 `[프로젝트 결정 필요]` 상태면, 그 상태를 암묵적 예외처럼 사용하지 않았는가
- 현재 변경이 프로젝트가 금지한 언어별 패턴을 새 기본값처럼 도입하지 않는가

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
