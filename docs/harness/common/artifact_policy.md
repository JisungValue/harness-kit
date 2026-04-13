# Artifact Policy

## 목적

이 문서는 모든 구현 태스크의 공통 산출물과 기록 위치를 정의한다.

## 언제 다시 읽는가

- 태스크를 시작할 때 산출물 위치와 최소 섹션을 확인하기 위해 읽는다.
- Phase 1에서 `requirements.md`, `plan.md`를 작성할 때 다시 확인한다.
- Phase 5에서 최종 산출물과 작업 로그 위치를 정리할 때 다시 확인한다.

## Task Workspace

- 모든 실제 태스크는 `docs/task/{task_id}_{task_name}/`를 권장 기본 workspace로 사용한다.
- stable한 작업 식별자가 없으면 `docs/task/{task_name}/`를 사용할 수 있다.
- `task_id`는 GitHub issue 번호, 티켓 번호, 날짜 기반 식별자처럼 팀이 안정적으로 추적할 수 있는 값이면 충분하며 특정 이슈 트래커 형식을 강제하지 않는다.
- 입력 문서: `issue.md`
- 요구사항 산출물: `requirements.md`
- 플랜 산출물: `plan.md`
- 구현 메모 산출물: `implementation_notes.md`
- 검증 결과 산출물: `validation_report.md`

모든 Phase의 입력, 진행 메모, 감사 결과, 검증 결과는 기본적으로 해당 task workspace 아래에 기록한다.
각 Phase 또는 레이어의 한 작업 단위가 끝날 때마다 현재 상태를 `implementation_notes.md`의 `진행 로그` 섹션에 즉시 갱신한다.
진행 로그에는 최소한 완료한 단계, 핵심 결과, 다음 단계, 보류 또는 리스크를 남겨 세션 유실 후에도 재개 가능해야 한다.
경량 운영 예외를 검토했다면 결과를 `implementation_notes.md`의 `경량 검토 기록` 섹션에 같은 작업에서 즉시 남긴다.

## 공통 산출물 최소 템플릿

각 산출물은 아래 최소 섹션을 기본으로 포함한다.
특정 태스크에서 일부 섹션이나 산출물이 실질적으로 불필요하면 삭제하지 말고 `해당 없음`으로 명시한다.

### `issue.md`

- 배경
- 요청사항
- 비범위
- 승인 또는 제약 조건

### `requirements.md`

- 기능 요구사항
- 비기능 요구사항 또는 품질 요구사항
- 입력/출력
- 제약사항
- 예외 상황
- 성공 기준

### `plan.md`

- 변경 대상 파일 또는 모듈
- 레이어별 작업 계획
- 테스트 계획
- 문서 반영 계획
- decision 반영 후보면 관련 `docs/decisions/README.md` 또는 `DEC-###-slug.md`의 읽기/수정/생성 계획
- 비범위
- 리스크 또는 확인 포인트

### `implementation_notes.md`

- 진행 로그
- 경량 검토 기록
- 구현 중 결정 사항
- 위임된 책임
- 사용자 승인 필요 항목
- 후속 태스크 후보

### `validation_report.md`

- 실행한 검증
- 실행하지 못한 검증
- 결과 요약
- Phase 5에서 반영할 related decisions/
- 남은 리스크
- 후속 조치 필요 사항

## Phase 공통 산출물 규칙

- Phase 1은 `requirements.md`, `plan.md`, 사용자 질의 및 보완 반영 내용, 감사 결과를 남긴다.
- Phase 2는 실패 후 통과한 테스트, 기능 구현 코드, 필요한 경우 `implementation_notes.md`를 남긴다.
- Phase 3은 통합 테스트 코드와 연동 검증 결과를 남긴다.
- Phase 4는 전체 검증 결과와 남은 리스크 또는 미실행 검증 목록, Phase 5에서 반영할 related decisions/를 남긴다.
- Phase 5는 갱신된 문서와 작업 로그를 남기고, 필요하면 `docs/decisions/`를 함께 갱신한다.
- 각 Phase 내부의 의미 있는 작업 단위가 끝날 때마다 `implementation_notes.md`의 `진행 로그`를 갱신한 뒤 다음 단계로 넘어간다.

## 위임 책임 기록 규칙

- 단위 테스트가 부적절한 책임은 Phase 3 통합 테스트에서 검증 대상으로 넘긴다.
- Phase 3로 넘기는 경우 위임 대상, 위임 사유, Phase 3에서 검증할 항목을 `implementation_notes.md`에 기록한다.
- Phase 3 감사는 `implementation_notes.md`에 기록된 위임 책임이 실제 통합 테스트로 검증되었는지 확인한다.

## 산출물 최소 완료 기준

- `issue.md`는 요청사항과 비범위가 함께 드러나야 한다.
- `requirements.md`는 구현 가능한 수준의 요구사항과 제약사항이 포함되어야 한다.
- `plan.md`는 작업 순서, 검증 방식, 비범위와 decision 반영 필요 시 관련 `docs/decisions/` 계획이 드러나야 한다.
- `implementation_notes.md`는 진행 로그, 구현 중 판단, 위임 또는 후속 이슈를 복원 가능하게 남겨야 한다.
- 경량 운영 예외를 검토했다면 `implementation_notes.md`에 판정 근거, 축소 범위, 유지한 테스트/감사, 남은 리스크, 승격 조건이 복원 가능하게 남아야 한다.
- `validation_report.md`는 실제 수행한 검증과 미실행 검증, Phase 5에서 반영할 related decisions/를 구분해 남겨야 한다.
