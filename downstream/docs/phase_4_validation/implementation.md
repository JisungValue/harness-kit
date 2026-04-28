# Phase 4 Implementation

## 목적

전체 구현 결과를 검증하고 잔여 리스크를 명시적으로 남긴다.

## 재참조 문서

### 필수 재참조

- `docs/process/common/validation_policy.md`
- 프로젝트 `docs/project/standards/quality_gate_profile.md`

### 조건부 참조

- `docs/process/common/audit_policy.md`

## Phase 체크리스트

- 자동 검증과 수동 검증을 구분했는가
- 실행 방법과 결과를 함께 남겼는가
- 미실행 검증과 그 사유를 누락하지 않았는가
- `issue.md`, `requirements.md`, `plan.md`, `implementation_notes.md`, 실제 구현 결과를 교차 검토했는가
- Phase 1에서 정의한 요청사항, 제약사항, 비범위가 실제 결과와 일치하는지 확인했는가
- 구현 로그와 실제 결과가 다르면 `누락` 또는 `범위 확장`으로 기록했는가
- 불일치 원인이 이전 Phase 산출물이면 원인 Phase부터 보완 및 재수행 계획을 기록했는가
- 검증 기준, 입력 산출물, 미실행 사유, 잔여 리스크가 바뀌면 자동/수동 검증과 감사를 다시 수행하는가
- 이번 변경이 `docs/project/decisions/` 반영 대상인지 검토했는가
- `validation_report.md`에 `## Phase 5에서 반영할 related decisions/`를 두고 관련 decision 경로 또는 `해당 없음`과 사유를 남겼는가
- 성능 민감 변경 또는 성능 최적화 주장이 있으면 근거, 검증 방법, 미실행 사유, 잔여 리스크를 남겼는가
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
- 프로젝트 `docs/project/standards/quality_gate_profile.md`가 현재 Phase 4 기록 시점까지 적용하도록 정의한 품질 게이트 중 무엇을 실행했고 무엇을 미실행했는지 함께 기록한다.
- 미실행 검증은 누락하지 말고 사유를 남긴다.
- 검증 기준, 입력 산출물, 미실행 사유, 잔여 리스크가 바뀌면 자동 검증, 수동 검증, 감사 결과를 모두 stale 로 본다.
- Phase 4 산출물이 stale 인 동안에는 `validation_report.md`를 Phase 5 close-out 근거로 먼저 사용하지 않는다.
- Validation 단계에서는 `issue.md`, `requirements.md`, `plan.md`, `implementation_notes.md`, 실제 구현 결과를 교차 검토한다.
- Phase 1에서 정의한 요청사항, 제약사항, 비범위의 반영 여부를 확인한다.
- 구현 로그와 실제 결과가 다르면 `누락` 또는 `범위 확장`으로 구분해 기록한다.
- 불일치 원인이 이전 Phase 산출물 결함이면 원인 Phase로 되돌아가 보완하고, 영향받는 Phase를 순서대로 재수행한다.
- 되돌아가기와 재수행 범위, 사용자 승인 여부를 `validation_report.md`에 남긴다.
- Validation 단계에서는 이번 변경이 구조, 정책, 예외 처리 규칙, 책임 배치, 운영 규칙을 바꿨는지 보고 `docs/project/decisions/` 반영 필요 여부를 판정한다.
- `validation_report.md`에는 `## Phase 5에서 반영할 related decisions/` 섹션을 두고 아래 중 하나를 남긴다.
  - 수정 또는 생성해야 할 `docs/project/decisions/README.md`, `DEC-###-slug.md` 경로와 반영 이유
  - decision 반영이 필요 없다는 판단과 그 사유
- 성능 민감 변경 또는 성능 최적화 주장이 있으면 `implementation_notes.md`의 근거와 검증 계획이 실제 실행 결과 또는 미실행 사유와 함께 `validation_report.md`에 반영됐는지 확인한다.
- 잔여 리스크와 후속 조치가 있으면 명시한다.

## 재수행 규칙

- `validation_report.md`만 보완하는 경우에도 검증 기준이나 입력물 해석이 바뀌었다면 자동/수동 검증을 다시 수행한다.
- Validation 중 더 이른 Phase 산출물 모순이 발견되면 원인 Phase 승인 복구 전까지 Phase 4와 Phase 5 산출물을 잠근다.

## 출력

- `validation_report.md`
