# Phase 5 Implementation

## 목적

구조적 결정, 사용법, 작업 로그를 복원 가능하게 문서화한다.

## 재참조 문서

### 필수 재참조

- `docs/process/common/artifact_policy.md`

### 조건부 참조

- 없음

## Phase 체크리스트

- 새 계약, 구조적 결정, 사용법 변경이 있으면 관련 문서를 갱신했는가
- Phase 4의 `Phase 5에서 반영할 related decisions/`를 확인했는가
- decision 반영 대상이면 `docs/project/decisions/README.md`와 관련 `DEC-###-slug.md`를 실제로 수정 또는 생성했는가
- 문서 반영 대상, canonical 역할 분담, close-out 결과가 바뀌면 Phase 5 절차를 최신 Validation 기준으로 다시 수행하는가
- 작업 로그가 변경 목적과 결과를 복원 가능하게 남기는가
- 범위 밖 개선 사항을 후속 후보로만 기록했는가

## 입력

- 구현 결과
- 검증 결과
- `validation_report.md`
- 필요한 경우 `implementation_notes.md`

## 수행 규칙

- 사용자나 후속 작업자가 변경 배경과 영향 범위를 이해할 수 있게 남긴다.
- 새 계약, 구조적 결정, 사용법 변경이 있으면 관련 문서를 갱신한다.
- Phase 4 또는 더 이른 Phase가 stale 상태면 Phase 5 문서와 close-out 문서는 잠금 상태로 두고 먼저 수정하지 않는다.
- 문서 반영 대상, canonical 역할 분담, close-out 결과가 바뀌면 `관련 문서 반영 -> related decisions 반영 -> 작업 로그 정리 -> 감사` 순서를 최신 Validation 결과 기준으로 다시 수행한다.
- `validation_report.md`의 `Phase 5에서 반영할 related decisions/`를 먼저 확인하고, listed decision 문서와 index 갱신을 실제 문서에 반영한다.
- 기존 related decision으로 설명이 안 되면 새 `DEC-###-slug.md`를 만들고 `docs/project/decisions/README.md`의 Current Decisions 또는 Superseded Decisions를 함께 갱신한다.
- decision 반영이 불필요하다고 Phase 4에서 판정됐다면 작업 로그에 그 판단이 유지됐는지만 간단히 남긴다.
- 이번 작업 요약은 프로젝트 로컬 작업 로그에 기록한다.

## 재수행 규칙

- stale 상태가 해소되기 전에는 `docs/project/decisions/*`를 포함한 canonical 문서를 close-out 목적으로 먼저 갱신하지 않는다.
- Validation 결과가 바뀌면 Phase 5 감사와 사용자 승인도 stale 로 보고 다시 수행한다.

## 출력

- 갱신된 문서
- 필요한 경우 `docs/project/decisions/README.md`, `docs/project/decisions/DEC-###-slug.md`
- 작업 로그
