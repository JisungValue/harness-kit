# Phase 1 Audit

## 목적

요구사항 감사, 계획 감사, issue 대비 plan 누락 감사를 분리해 검토한다.

## 재참조 문서

### 필수 재참조

- `docs/process/common/audit_policy.md`

### 조건부 참조

- `docs/process/common/artifact_policy.md`
- 필요한 경우 프로젝트 overlay 문서

## Phase 체크리스트

아래 체크리스트는 감사 시작 전에 빠르게 훑는 진입용 요약이다.
세부 판정은 `감사 항목`과 `승인 불가 기준`을 따른다.

- 범위와 비범위가 분리되어 있는가
- `requirements.md` 감사와 `plan.md` 감사의 판단 기준이 분리되어 있는가
- 테스트 계획과 문서 반영 계획이 `plan.md`에 포함되어 있는가
- `issue.md` 요청사항과 제약사항이 `plan.md`에 빠짐없이 반영되었는가
- stale 상태인 `requirements.md`, `plan.md`, 사용자 승인 결과를 재사용하지 않는가
- decision 반영 후보 여부가 판정되었는가
- decision 반영 후보면 관련 `docs/project/decisions/` 작업이 `plan.md`에 포함되었는가
- 승인되지 않은 범위 확장이 섞이지 않았는가

## 감사 순서

1. `requirements.md` 감사
2. `plan.md` 감사
3. `issue.md` 대비 `plan.md` 누락 감사

위 세 감사는 모두 Phase 1 내부 감사다.
사용자 승인 게이트는 세 감사가 승인 가능 상태가 된 뒤 Phase 1 종료 시점에 적용한다.

- 감사자는 최신 `issue.md`, `requirements.md`, `plan.md` 기준으로만 판정한다.
- 위 세 문서 중 하나라도 수정되면 이전 감사 결과와 사용자 승인은 stale 로 보고 승인 가능 판정에 재사용하지 않는다.

## 감사 항목

### 1. `requirements.md` 감사

- `issue.md`의 요청사항과 비범위가 반영되었는가
- `requirements.md`가 구현 가능한 수준의 요구사항, 제약, 예외, 성공 기준을 담고 있는가
- 최신 `issue.md` 변경이 반영되기 전 stale 상태의 `requirements.md`를 기준으로 판정하지 않는가
- 애매한 가정과 사용자 확인 필요 항목이 요구사항 수준에서 드러나는가
- 정책 해석이 모호하거나 구현에 필요한 외부 계약, 응답 형식, 에러 계약, 데이터 접근 방식이 비어 있으면 사용자 질의 항목으로 분리되었는가
- 연동 서버 API spec, 응답값, 에러 형식, 데이터베이스 조회 조건 또는 질의 방식 판단 근거가 빠진 상태에서 요구사항이 닫힌 것으로 처리되지 않았는가
- 이번 작업이 여러 파일 또는 레이어에 걸친 책임 배치, 장기 유지 정책, 예외 처리 규칙, 운영 규칙 변경에 해당하는지 판정이 남아 있는가
- decision 반영 후보면 기존 related decision 또는 새 decision 필요 여부가 요구사항 수준에서 드러나는가

### 2. `plan.md` 감사

- `plan.md`가 requirements 감사 통과본인 `requirements.md`를 구현하기 위한 변경 대상, 작업 순서, 테스트 계획, 문서 반영 계획, 비범위, 리스크를 담고 있는가
- stale 상태가 아닌 최신 `requirements.md`, `plan.md` 조합을 기준으로 판정하는가
- 승인되지 않은 범위 확장이 계획에 포함되지 않았는가
- 현재 TASK와 직접 관련 없는 구조 개선이나 후속 개선이 현재 계획에 섞이지 않았는가
- decision 반영 후보면 `docs/project/decisions/README.md`와 관련 `DEC-###-slug.md`의 읽기/수정/생성 계획이 문서 반영 계획에 포함되는가
- 새 decision이 필요하면 index(`docs/project/decisions/README.md`) 갱신 계획도 포함되는가

### 3. `issue.md` 대비 `plan.md` 누락 감사

- `issue.md`의 요청사항이 `plan.md`에 빠짐없이 반영되었는가
- 최신 `issue.md` 기준으로 누락을 다시 확인했는가
- `issue.md`의 제약사항과 승인 조건이 `plan.md`의 작업 순서, 테스트 계획, 문서 반영 계획에 반영되었는가
- `issue.md`의 비범위가 `plan.md`에서 유지되고 있는가
- 프로젝트 전용 문서가 필요한 판단이면 overlay 문서를 참조했는가
- issue가 구조/정책/예외/책임 위치 변경을 요구하면 관련 `docs/project/decisions/` 반영 계획이 누락되지 않았는가

## 승인 불가 기준

- 요구사항이 구현 가능한 수준으로 구체화되지 않음
- 정책 모호점 또는 구현 필수 정보 누락이 남아 있는데 사용자 질의나 요구사항 보완 없이 다음 단계로 넘어가려 함
- `requirements.md` 감사와 `plan.md` 감사의 판단 기준이 섞여 감사 포인트가 불명확함
- 비범위가 누락되어 범위 통제가 어려움
- `plan.md`에 테스트 계획 또는 문서 반영 계획이 없음
- stale 상태의 `requirements.md`, `plan.md`, 사용자 승인 결과를 최신본 대신 재사용함
- decision 반영 후보인데 관련 `docs/project/decisions/` 읽기/수정/생성 계획이 `plan.md`에 없음
- `issue.md`의 요청사항, 제약사항, 비범위 중 일부가 `plan.md`에 반영되지 않음
- 현재 TASK와 직접 관련 없는 구조 개선이 계획에 포함됨
