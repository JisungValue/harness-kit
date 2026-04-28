# Phase 4 Audit

## 목적

검증 결과가 실제 수행 내용을 복원 가능하게 남기고 있는지 검토한다.

## 재참조 문서

### 필수 재참조

- `docs/process/common/audit_policy.md`
- `docs/process/common/validation_policy.md`
- 프로젝트 `docs/project/standards/quality_gate_profile.md`

## Phase 체크리스트

아래 체크리스트는 감사 시작 전에 빠르게 훑는 진입용 요약이다.
세부 판정은 `감사 항목`과 `승인 불가 기준`을 따른다.

- 자동 검증과 수동 검증이 구분되어 있는가
- 실행 방법과 결과가 복원 가능하게 남아 있는가
- 미실행 검증과 사유가 누락되지 않았는가
- `issue.md`, `requirements.md`, `plan.md`, `implementation_notes.md`, 실제 구현 결과의 교차 검토가 수행되었는가
- Phase 1의 요청사항, 제약사항, 비범위 대비 실제 구현 결과가 일치하는가
- 구현 로그와 실제 결과 불일치가 `누락` 또는 `범위 확장`으로 기록되었는가
- 불일치 원인이 이전 Phase 산출물인 경우 원인 Phase부터의 보완 및 재수행 계획이 기록되었는가
- stale 상태의 Validation 감사 또는 사용자 승인 결과를 재사용하지 않는가
- `docs/project/decisions/` 반영 필요 여부가 검토되었는가
- `validation_report.md`에 Phase 5에서 반영할 related decision 경로 또는 `해당 없음`과 사유가 남아 있는가
- 성능 민감 변경 또는 성능 최적화 주장이 있으면 근거, 검증 방법, 미실행 사유, 잔여 리스크가 기록되었는가
- 잔여 리스크와 후속 조치가 정리되어 있는가

## 감사 항목

- 자동 검증과 수동 검증이 구분되어 있는가
- 검증 항목별 실행 방법과 결과가 남아 있는가
- 최신 입력 산출물과 최신 `validation_report.md` 기준으로만 판정했는가
- 프로젝트 `docs/project/standards/quality_gate_profile.md`가 현재 Phase 4 기록 시점까지 적용하도록 정의한 필수 게이트의 실행 여부 또는 미실행 사유가 남아 있는가
- 미실행 검증과 그 사유가 기록되어 있는가
- `issue.md`, `requirements.md`, `plan.md`, `implementation_notes.md`, 실제 구현 결과를 함께 대조했는가
- Phase 1에서 확정한 요청사항, 제약사항, 비범위의 반영 여부를 검증했는가
- 구현 로그와 실제 결과가 다르면 `누락` 또는 `범위 확장`으로 분류해 남겼는가
- 이전 Phase 산출물 결함이 원인일 때 원인 Phase로의 되돌아가기 범위와 재수행 순서가 정의되었는가
- 되돌아가기 및 재수행에도 감사와 사용자 승인 게이트를 다시 적용했는가
- 구조, 정책, 예외 처리 규칙, 책임 배치, 운영 규칙 변경 여부를 기준으로 `docs/project/decisions/` 반영 필요 여부를 판정했는가
- `validation_report.md`의 `Phase 5에서 반영할 related decisions/` 섹션이 관련 decision 경로 또는 `해당 없음`과 사유를 담는가
- 성능 민감 변경 또는 성능 최적화 주장이 있으면 `implementation_notes.md`의 근거와 검증 계획이 실제 실행 결과 또는 미실행 사유와 함께 `validation_report.md`에 반영되었는가
- 잔여 리스크 또는 후속 조치가 누락되지 않았는가

## 승인 불가 기준

- `validation_report.md`가 실제 수행 내용을 복원할 수 없을 정도로 빈약함
- 미실행 검증이 누락됨
- stale 상태의 Validation 감사 또는 이전 승인 결과를 최신 Validation 대신 재사용함
- 교차 검토 입력물(`issue.md`, `requirements.md`, `plan.md`, `implementation_notes.md`) 대비 결과 정합성 확인이 누락됨
- 구현 로그와 실제 결과 불일치가 있는데 `누락` 또는 `범위 확장`으로 기록되지 않음
- Phase 1의 요청사항, 제약사항, 비범위 반영 여부가 확인되지 않음
- 이전 Phase 산출물 결함이 확인됐는데 원인 Phase부터의 보완 및 재수행 계획이 없음
- 되돌아가기 후 감사 또는 사용자 승인 게이트 재적용이 누락됨
- `docs/project/decisions/` 반영 필요 여부 판단이 누락됨
- `validation_report.md`에 Phase 5에서 반영할 related decisions/ 또는 그 부재 사유가 없음
- 성능 민감 변경 또는 성능 최적화 주장이 있는데 근거, 검증 방법 또는 미실행 사유, 잔여 리스크가 기록되지 않음
- 잔여 리스크가 있는데 기록되지 않음
