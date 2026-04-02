# Phase 3 Implementation

## 목적

단위 테스트로 충분히 검증하기 어려운 연결 책임과 통합 시나리오를 검증한다.

## 재참조 문서

### 필수 재참조

- `docs/harness/common/testing_policy.md`
- `docs/harness/common/test_double_policy.md`
- `docs/harness/common/validation_policy.md`

### 조건부 참조

- `docs/harness/common/audit_policy.md`
- 프로젝트 `testing_profile.md`

## Phase 체크리스트

- Phase 2에서 위임된 책임을 우선 검증 대상으로 삼았는가
- 연결 책임, 외부 연동 번역, 실제 조립 책임을 검증했는가
- 통합 테스트에서 내부 협력을 `mock`으로 대체해 연결 책임을 지우지 않았는가
- 단위 테스트로 충분한 책임을 중복 검증하지 않았는가
- 미확인 연동 리스크가 있으면 기록했는가

## 입력

- Phase 2 구현 결과
- `implementation_notes.md`
- 프로젝트 `testing_profile.md`

## 수행 규칙

- 레이어 간 연결, 외부 연동 번역, 실제 조립 책임을 우선 검증한다.
- 단위 테스트로 이미 충분히 검증된 책임을 중복해서 다시 테스트하지 않는다.
- Phase 2에서 위임된 책임이 있다면 이를 우선 검증 대상으로 삼는다.
- 외부 경계가 아니라면 통합 테스트 안에서 내부 협력 객체를 테스트 더블로 대체하지 않는다.

## 출력

- 통합 테스트 코드
- 연동 검증 결과
