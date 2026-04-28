# Phase 3 Audit

## 목적

통합 테스트가 실제 연결 책임과 위임된 책임을 충분히 검증하는지 검토한다.

## 재참조 문서

### 필수 재참조

- `docs/process/common/audit_policy.md`
- `docs/process/common/testing_policy.md`
- `docs/process/common/test_double_policy.md`
- `docs/process/common/validation_policy.md`
- 프로젝트 `docs/project/standards/quality_gate_profile.md`
- 프로젝트 `docs/project/standards/testing_profile.md`

### 조건부 참조

- `implementation_notes.md`

## Phase 체크리스트

아래 체크리스트는 감사 시작 전에 빠르게 훑는 진입용 요약이다.
세부 판정은 `감사 항목`과 `승인 불가 기준`을 따른다.

- 위임된 책임이 빠지지 않았는가
- 실제 연결 책임과 번역 책임이 검증되었는가
- 핵심 happy path와 주요 failure path가 통합 수준에서 검증되었는가
- entrypoint, bootstrap, adapter의 실제 연결 책임이 통합 테스트로 확인되었는가
- storage adapter, gateway, client adapter 같은 외부 port 구현체가 구현체 단위 통합 테스트로 검증 가능한데도 불필요하게 누락되지 않았는가
- 외부 경계가 아닌 내부 협력이 `mock`으로 대체되지 않았는가
- 프로젝트 `docs/project/standards/quality_gate_profile.md`가 현재 Phase 3까지 적용하도록 정의한 필수 test gate가 실행되었거나, 미실행 사유가 남아 있는가
- stale 상태의 통합 감사 또는 사용자 승인 결과를 재사용하지 않는가
- 통합 테스트가 형식적 존재에 그치지 않는가
- 검증 범위가 과도하게 번지지 않았는가

## 감사 항목

- 단위 테스트로 다루기 어려운 책임을 실제로 검증했는가
- 재수행이 있었다면 최신 `implementation_notes.md`의 위임 책임과 최신 연결 경계를 기준으로 판정했는가
- `implementation_notes.md`에 기록된 위임 책임이 누락되지 않았는가
- 실제 경계 번역과 조립 책임이 검증되었는가
- 핵심 happy path와 주요 failure path가 실제 연결 책임과 함께 검증되었는가
- adapter의 순수 변환 검증과 실제 연결 검증이 구분되어 책임이 흐려지지 않았는가
- 외부 port 구현체의 실제 저장/조회 연산, 응답 또는 레코드 매핑, 저장소별 경계 책임, 에러 번역이 필요한 경우 구현체 단위 통합 테스트로 검증되었는가
- 외부 경계 테스트 더블이 필요하다면 `stub` 또는 `fake`가 우선이고, `mock`는 불가피한 최외곽 부수효과 검증에만 제한되었는가
- 프로젝트 `docs/project/standards/quality_gate_profile.md`가 현재 Phase 3까지 적용하도록 정의한 필수 test gate가 누락되지 않았고, 미실행이면 사유가 있는가
- 통합 테스트가 불필요하게 과도한 범위를 동시에 검증하지 않는가

## 승인 불가 기준

- 위임된 책임이 통합 테스트에서 누락됨
- stale 상태의 통합 감사 또는 이전 승인 결과를 최신 통합 검증 대신 재사용함
- 연결 책임 검증 없이 통합 테스트가 형식적으로만 존재함
- 핵심 happy path 또는 주요 failure path가 실제 연결 책임과 분리되어 검증됨
- 구현체 단위 통합 테스트로 검증할 수 있는 외부 port 책임이 빠져 실제 저장/조회 연산, 응답 또는 레코드 매핑, 저장소별 경계 책임, 에러 번역 검증이 누락됨
- 통합 테스트가 내부 협력을 `mock`으로 대체해 실제 연결 책임을 검증하지 못함
- 통합 테스트가 핵심 리스크를 설명하지 못함
