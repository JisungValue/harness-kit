# Phase 1 Implementation

## 목적

구현 전에 요구사항, 범위, 가정, 제약사항, 검증 범위를 명확히 한다.

## 재참조 문서

### 필수 재참조

- `docs/process/common/artifact_policy.md`

### 조건부 참조

- `docs/process/common/audit_policy.md`
- 필요한 경우 프로젝트 overlay 문서

## Phase 체크리스트

- `issue.md`의 요청사항, 비범위, 승인 또는 제약 조건을 먼저 분석했는가
- `requirements.md`를 먼저 구현 가능한 수준으로 구체화했는가
- `requirements.md` 감사 후 `plan.md`를 작성했는가
- `plan.md` 감사 후 issue 대비 plan 누락 검토를 수행했는가
- `issue.md`, `requirements.md`, `plan.md` 중 하나라도 바뀌면 내부 감사 3종을 모두 stale 처리하고 최신본 기준으로 다시 수행하는가
- 이번 작업이 `docs/project/decisions/`에 남길 만한 결정인지 판정했는가
- `docs/project/decisions/README.md` 또는 관련 `DEC-###-slug.md`의 수정/생성이 필요하면 `plan.md`의 문서 반영 계획에 포함했는가
- 현재 TASK와 직접 관련 없는 개선 사항을 현재 범위에 넣지 않았는가

## 입력

- task workspace의 `issue.md`
- 관련 공통 정책 문서
- 필요한 경우 프로젝트 overlay 문서

## 수행 규칙

- 요청사항과 비범위를 분리해 정리한다.
- 요구사항은 구현 가능한 수준으로 구체화한다.
- `issue.md`, `requirements.md`, `plan.md` 중 하나라도 바뀌면 Phase 1 내부 절차는 `issue.md` 분석부터 다시 맞춘다.
- 위 세 문서 중 하나라도 수정되면 requirements 감사, plan 감사, issue 대비 plan 누락 감사는 모두 stale 로 본다.
- Phase 1이 다시 승인되기 전에는 `validation_report.md`, final task-local 문서, `docs/project/decisions/*`를 수정하지 않는다.
- 애매한 가정은 문서로 드러내고, 필요한 경우 사용자 확인이 필요한 항목으로 분리한다.
- 정책 해석이 모호하거나 구현에 필요한 외부 계약, 응답 형식, 에러 계약, 데이터 접근 방식이 정의되지 않았으면 추정으로 닫지 말고 사용자에게 질의한다.
- 아래 중 하나 이상이면 `docs/project/decisions/` 반영 후보로 본다.
  - 여러 파일 또는 레이어에 걸친 책임 배치가 바뀐다.
  - 장기 유지할 정책, 예외 처리 규칙, 운영 규칙이 바뀐다.
  - 다음 세션이 모르고 구현하면 쉽게 어긋날 결정이다.
  - 변경 시 관련 문서 현행화가 함께 필요한 결정이다.
- decision 반영 후보면 기존 `docs/project/decisions/README.md`와 관련 `DEC-###-slug.md`를 먼저 확인하고, 없으면 새 decision 문서 생성 필요 여부를 `plan.md`에 남긴다.
- 현재 TASK와 직접 관련 없는 개선 아이디어는 현재 범위에 넣지 않고 후속 후보로 분리한다.

## 권장 순서

1. `issue.md`를 분석해 요청사항, 비범위, 승인 또는 제약 조건을 정리한다.
2. `requirements.md`를 작성한다.
3. `requirements.md` 감사를 수행해 구현 가능한 수준인지 확인한다.
4. requirements 감사 통과본인 `requirements.md`를 기준으로 `plan.md`를 작성한다.
5. `plan.md` 감사를 수행해 작업 순서, 테스트 계획, 문서 반영 계획, 비범위를 확인한다.
6. `issue.md` 대비 `plan.md` 누락 감사를 수행해 요청사항, 제약사항, 비범위가 빠짐없이 반영되었는지 확인한다.

위 3, 5, 6 단계는 모두 Phase 1 내부 감사다.
사용자 승인 게이트는 이 내부 감사들이 승인 가능 상태가 된 뒤 Phase 1 종료 시점에 적용한다.

## 단계별 작성 규칙

### 1. `issue.md` 분석

- 요청사항, 비범위, 승인 또는 제약 조건을 먼저 식별한다.
- 구현 전에 확인이 필요한 가정은 `requirements.md` 또는 사용자 승인 필요 항목으로 올린다.
- 이번 작업이 구조, 정책, 예외 처리 규칙, 책임 배치, 운영 규칙을 바꾸는지 보고 decision 반영 후보 여부를 함께 식별한다.

### 2. `requirements.md` 작성

- 요구사항, 입력/출력, 제약사항, 예외 상황, 성공 기준을 구현 가능한 수준으로 정리한다.
- 아직 작업 순서나 변경 파일 계획이 확정되지 않았더라도 요구사항 정의를 먼저 닫는다.
- 구현에 필요한 정보가 빠져 있으면 사용자에게 먼저 질의한다.
- 예를 들어 연동 서버의 API spec, 응답값, 에러 형식이 정의되지 않았거나, 데이터베이스 연동 대상과 조회 조건만 있고 어떤 방식으로 질의해야 하는지 판단 근거가 없으면 요구사항이 닫히지 않은 것으로 본다.
- decision 반영 후보면 기존 related decision 문서 또는 새 decision 필요 여부를 요구사항에 드러낸다.
- 구현 가능한 수준이 되기 전에는 추정으로 `plan.md` 작성 단계로 넘어가지 않는다.

### 3. `requirements.md` 감사

- 요구사항이 구현 가능한 수준인지 확인한 뒤 다음 단계로 넘어간다.
- `issue.md`, `requirements.md`, `plan.md`가 바뀐 뒤에는 이전 requirements 감사 결과를 재사용하지 않는다.
- 요구사항 감사에서 승인 불가가 나오면 `requirements.md`를 먼저 보완한다.
- 정책 모호점이나 구현 필수 정보 누락이 남아 있으면 사용자 질의 또는 요구사항 보완 후 다시 감사한다.

### 4. `plan.md` 작성

- `plan.md`에는 변경 대상, 작업 순서, 테스트 계획, 문서 반영 계획, 비범위, 리스크를 남긴다.
- 계획은 requirements 감사 통과본인 `requirements.md`를 구현하는 방법에만 집중한다.
- decision 반영 후보면 `plan.md`의 문서 반영 계획에 아래를 포함한다.
  - 읽어야 할 `docs/project/decisions/README.md` 또는 관련 `DEC-###-slug.md`
  - 수정할 decision 문서 경로 또는 새로 만들 decision 문서 경로
  - index(`docs/project/decisions/README.md`) 갱신 필요 여부

### 5. `plan.md` 감사

- 계획이 요구사항을 구현할 수 있는 수준인지, 범위 확장이 섞이지 않았는지 확인한다.
- `issue.md`, `requirements.md`, `plan.md`가 바뀐 뒤에는 이전 plan 감사 결과를 재사용하지 않는다.
- decision 반영 후보인데 관련 `docs/project/decisions/` 작업이 `plan.md`에 빠졌으면 승인 불가로 본다.
- 계획 감사에서 승인 불가가 나오면 `plan.md`를 먼저 보완한다.

### 6. issue 대비 `plan.md` 누락 검토

- `issue.md`의 요청사항, 제약사항, 비범위가 `plan.md`에 빠짐없이 반영되었는지 확인한다.
- issue상 구조/정책/예외/책임 위치 변경이 있으면 관련 `docs/project/decisions/` 반영 계획도 함께 확인한다.
- 반영되지 않은 항목이 있으면 누락으로 보고 `plan.md`를 수정한 뒤 다시 확인한다.
- 앞선 산출물 중 하나라도 바뀌면 최신 `issue.md`, `requirements.md`, `plan.md` 조합으로 다시 검토한다.

## 출력

- `requirements.md`
- `plan.md`
