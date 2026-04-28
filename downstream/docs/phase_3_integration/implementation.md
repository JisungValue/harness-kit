# Phase 3 Implementation

## 목적

단위 테스트로 충분히 검증하기 어려운 연결 책임과 통합 시나리오를 검증한다.

## 재참조 문서

### 필수 재참조

- `docs/process/common/testing_policy.md`
- `docs/process/common/test_double_policy.md`
- `docs/process/common/validation_policy.md`
- 프로젝트 `docs/project/standards/quality_gate_profile.md`
- 프로젝트 `docs/project/standards/testing_profile.md`

### 조건부 참조

- `docs/process/common/audit_policy.md`

## Phase 체크리스트

- Phase 2에서 위임된 책임을 우선 검증 대상으로 삼았는가
- 연결 책임, 외부 연동 번역, 실제 조립 책임을 검증했는가
- 핵심 happy path와 주요 failure path를 통합 수준에서 검증했는가
- entrypoint, bootstrap, adapter의 실제 연결 책임이 단위 테스트만으로 남겨지지 않았는가
- storage adapter, gateway, client adapter 같은 외부 port 구현체의 실제 연결 책임을 구현체 단위 통합 테스트로 검증할 대상을 식별했는가
- 통합 대상, 위임 책임, 연결 경계가 바뀌면 통합 절차를 처음부터 다시 맞추는가
- 통합 테스트에서 내부 협력을 `mock`으로 대체해 연결 책임을 지우지 않았는가
- 프로젝트 `docs/project/standards/quality_gate_profile.md`가 현재 Phase 3까지 적용하도록 정의한 test gate가 실행되었거나, 미실행 사유가 기록되었는가
- 단위 테스트로 충분한 책임을 중복 검증하지 않았는가
- 미확인 연동 리스크가 있으면 기록했는가

## 입력

- Phase 2 구현 결과
- `implementation_notes.md`
- 프로젝트 `docs/project/standards/quality_gate_profile.md`
- 프로젝트 `docs/project/standards/testing_profile.md`

## 수행 규칙

- 레이어 간 연결, 외부 연동 번역, 실제 조립 책임을 우선 검증한다.
- 단위 테스트로 이미 충분히 검증된 책임을 중복해서 다시 테스트하지 않는다.
- Phase 2에서 위임된 책임이 있다면 이를 우선 검증 대상으로 삼는다.
- 통합 대상, 위임 책임, 연결 경계가 바뀌면 `연결 책임 식별 -> 통합 검증 -> happy path / failure path 확인 -> 감사` 순서를 최신본 기준으로 다시 수행한다.
- Phase 3 산출물이 바뀌면 기존 Phase 3 감사와 사용자 승인은 stale 로 보고 다시 적용한다.
- Phase 3이 다시 승인되기 전에는 Phase 4 이후 산출물을 수정하지 않는다.
- 핵심 happy path와 주요 failure path를 실제 연결 책임과 함께 검증한다.
- entrypoint, bootstrap은 실제 조립과 실행 경계 검증이 필요하면 통합 테스트 우선 대상으로 삼는다.
- adapter는 순수 변환 로직과 실제 연결 책임을 분리해 보고, 실제 연결 책임은 통합 테스트에서 검증한다.
- 외부 port 구현체는 전체 애플리케이션 end-to-end 대신 구현체 단위 통합 테스트로도 검증할 수 있다.
- storage adapter, gateway, client adapter 구현체는 실제 저장/조회 연산, 실제 응답 포맷, driver 또는 client 설정, 저장소별 경계 책임, 에러 번역처럼 더블로 가리기 어려운 책임을 우선 통합 테스트 대상으로 삼는다.
- 외부 경계가 아니라면 통합 테스트 안에서 내부 협력 객체를 테스트 더블로 대체하지 않는다.
- 프로젝트 `docs/project/standards/quality_gate_profile.md`가 현재 Phase 3까지 적용하도록 정의한 test gate가 있으면, 해당 실행 또는 미실행 사유를 함께 남긴다.

## 재수행 규칙

- 재수행 범위는 변경 영향이 걸린 가장 이른 통합 책임부터 다시 정한다.
- 위임 책임 목록이 바뀌면 `implementation_notes.md`와 통합 검증 범위를 함께 최신화한 뒤 감사한다.

## 출력

- 통합 테스트 코드
- 연동 검증 결과
