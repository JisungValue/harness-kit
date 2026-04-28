# Phase 5 Audit

## 목적

문서화가 실제 변경과 후속 작업에 필요한 맥락을 충분히 남겼는지 검토한다.

## 재참조 문서

### 필수 재참조

- `docs/process/common/audit_policy.md`
- `docs/process/common/artifact_policy.md`

### 조건부 참조

- 없음

## Phase 체크리스트

아래 체크리스트는 감사 시작 전에 빠르게 훑는 진입용 요약이다.
세부 판정은 `감사 항목`과 `승인 불가 기준`을 따른다.

- 필요한 문서 반영이 빠지지 않았는가
- Phase 4가 넘긴 `Phase 5에서 반영할 related decisions/`가 실제 문서에 반영되었는가
- stale 상태의 Validation 결과나 Phase 5 감사/승인 결과를 재사용하지 않는가
- 작업 로그가 변경 배경과 결과를 설명할 수 있는가
- 범위 밖 개선 사항이 후속 후보로 분리되었는가

## 감사 항목

- 새 계약, 구조적 결정, 사용법 변경이 관련 문서에 반영되었는가
- 최신 `validation_report.md`와 최신 문서 상태 기준으로만 판정하는가
- decision 반영 대상이면 `docs/project/decisions/README.md`와 관련 `DEC-###-slug.md`가 실제로 수정 또는 생성되었는가
- 새 decision이 생겼다면 index(Current Decisions 또는 Superseded Decisions)도 함께 갱신되었는가
- 작업 로그가 변경 목적과 결과를 요약하고 있는가
- 현재 TASK 범위 밖 개선 사항이 후속 후보로 분리 기록되었는가

## 승인 불가 기준

- 실제 변경에 필요한 문서 반영이 누락됨
- Phase 4가 명시한 related decisions/ 반영이 누락됨
- stale 상태의 Validation 결과나 이전 Phase 5 승인 결과를 최신 문서 대신 재사용함
- 작업 로그가 작업 배경과 결과를 설명하지 못함
