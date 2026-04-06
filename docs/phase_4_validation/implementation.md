# Phase 4 Implementation

## 목적

전체 구현 결과를 검증하고 잔여 리스크를 명시적으로 남긴다.

## 재참조 문서

### 필수 재참조

- `docs/harness/common/validation_policy.md`
- 프로젝트 `docs/standard/quality_gate_profile.md`

### 조건부 참조

- `docs/harness/common/audit_policy.md`

## Phase 체크리스트

- 자동 검증과 수동 검증을 구분했는가
- 실행 방법과 결과를 함께 남겼는가
- 미실행 검증과 그 사유를 누락하지 않았는가
- `issue.md`, `requirements.md`, `plan.md`, `implementation_notes.md`, 실제 구현 결과를 교차 검토했는가
- Phase 1에서 정의한 요청사항, 제약사항, 비범위가 실제 결과와 일치하는지 확인했는가
- 구현 로그와 실제 결과가 다르면 `누락` 또는 `범위 확장`으로 기록했는가
- 불일치 원인이 이전 Phase 산출물이면 원인 Phase부터 보완 및 재수행 계획을 기록했는가
- 잔여 리스크와 후속 조치를 명시했는가

## 입력

- 전체 구현 결과
- 테스트 결과
- `issue.md`
- `requirements.md`
- `plan.md`
- `implementation_notes.md`
- 필요한 경우 수동 검증 결과

## 수행 규칙

- 자동 검증과 수동 검증을 구분해 기록한다.
- 프로젝트 `docs/standard/quality_gate_profile.md`가 현재 Phase 4 기록 시점까지 적용하도록 정의한 품질 게이트 중 무엇을 실행했고 무엇을 미실행했는지 함께 기록한다.
- 미실행 검증은 누락하지 말고 사유를 남긴다.
- Validation 단계에서는 `issue.md`, `requirements.md`, `plan.md`, `implementation_notes.md`, 실제 구현 결과를 교차 검토한다.
- Phase 1에서 정의한 요청사항, 제약사항, 비범위의 반영 여부를 확인한다.
- 구현 로그와 실제 결과가 다르면 `누락` 또는 `범위 확장`으로 구분해 기록한다.
- 불일치 원인이 이전 Phase 산출물 결함이면 원인 Phase로 되돌아가 보완하고, 영향받는 Phase를 순서대로 재수행한다.
- 되돌아가기와 재수행 범위, 사용자 승인 여부를 `validation_report.md`에 남긴다.
- 잔여 리스크와 후속 조치가 있으면 명시한다.

## 출력

- `validation_report.md`
