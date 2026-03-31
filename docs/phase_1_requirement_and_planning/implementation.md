# Phase 1 Implementation

## 목적

구현 전에 요구사항, 범위, 가정, 제약사항, 검증 범위를 명확히 한다.

## 재참조 문서

### 필수 재참조

- `docs/harness/common/artifact_policy.md`

### 조건부 참조

- `docs/harness/common/audit_policy.md`
- 필요한 경우 프로젝트 overlay 문서

## Phase 체크리스트

- 요청사항과 비범위를 분리했는가
- `requirements.md`를 구현 가능한 수준으로 구체화했는가
- `plan.md`에 변경 대상, 작업 순서, 테스트 계획, 문서 반영 계획, 리스크를 남겼는가
- 현재 TASK와 직접 관련 없는 개선 사항을 현재 범위에 넣지 않았는가

## 입력

- `docs/task/{task-title}/issue.md`
- 관련 공통 정책 문서
- 필요한 경우 프로젝트 overlay 문서

## 수행 규칙

- 요청사항과 비범위를 분리해 정리한다.
- 요구사항은 구현 가능한 수준으로 구체화한다.
- 애매한 가정은 문서로 드러내고, 필요한 경우 사용자 확인이 필요한 항목으로 분리한다.
- `plan.md`에는 변경 대상, 작업 순서, 테스트 계획, 문서 반영 계획, 리스크를 남긴다.
- 현재 TASK와 직접 관련 없는 개선 아이디어는 현재 범위에 넣지 않고 후속 후보로 분리한다.

## 출력

- `requirements.md`
- `plan.md`
