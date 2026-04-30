# Harness Core Guide

## 문서 역할

- 이 파일은 `harness-kit`가 제공하는 재사용 가능한 process guide다.
- downstream 프로젝트의 로컬 문서 entrypoint는 `docs/entrypoint.md`이고, 그 파일이 이 core guide와 프로젝트 전용 overlay 문서를 함께 연결한다.

## 빠른 시작 요약

- 구현성 작업은 이 문서를 시작점으로 사용한다.
- 먼저 task workspace의 `issue.md`를 기준으로 작업 범위를 확정한다.
- Phase는 기본적으로 1 -> 2 -> 3 -> 4 -> 5 순서로 진행한다.
- 각 Phase는 `implementation.md` 수행 후 `audit.md` 기준으로 감사를 수행한다.
- Phase 내부에 감사가 여러 단계로 나뉘어 있으면, 해당 내부 감사들을 모두 완료한 뒤 사용자 승인 게이트로 간다.
- 각 Phase는 `implementation -> audit 또는 내부 감사 묶음 -> 사용자 승인 -> 다음 Phase` 순서를 따른다.
- 다음 Phase로 이동하려면 현재 Phase의 필요한 감사가 모두 승인 가능이고 사용자 승인이 있어야 한다.
- 특정 입력 문서나 산출물이 바뀌어 재수행이 필요해도 무조건 처음부터 다시 시작하지 않는다.
- 재수행은 변경 영향이 걸린 가장 이른 Phase부터 시작하고, 이후 영향을 받은 Phase만 순서대로 다시 수행한다.
- 각 Phase 또는 레이어의 한 작업 단위가 끝날 때마다 task workspace의 `implementation_notes.md`의 `진행 로그`를 갱신한다.
- 공통 정책 해석과 충돌 판단은 `docs/process/common/process_policy.md`의 우선순위 규칙을 따른다.
- 작업 판단의 source-of-truth는 현재 repo 안의 `README`, `docs/*`, `docs/project/decisions/*`, `scripts/*`, `config` 같은 repo-local 근거다.
- 기억, 외부 대화, 다른 프로젝트 관행은 repo-local 근거보다 우선하지 않는다.
- 필요한 결정이나 근거가 repo에 없으면 추측으로 메우지 말고 project overlay 또는 `docs/project/decisions/` 반영 후보로 넘기며, 같은 사실을 `implementation_notes.md`나 `validation_report.md`에도 남긴다.
- 테스트, 테스트 더블 판단, 검증은 각각 `testing_policy.md`, `test_double_policy.md`, `validation_policy.md`를 기준으로 수행한다.
- 현재 TASK와 직접 관련 없는 기존 중복 제거, 구조 정리, 선제 추상화는 별도 리팩터링 태스크로 분리한다.
- 작은 태스크의 경량 운영 예외 가능 여부는 `docs/process/common/lightweight_task_policy.md`를 따른다.
- 감사는 구현 주체와 분리된 서브에이전트가 수행한다.
- 작업 식별자가 있으면 브랜치 이름은 `{task_id}_{task_name}` 형식을 권장한다.
- task workspace는 `docs/task/{task_id}_{task_name}/`를 권장하며, stable한 작업 식별자가 없으면 `docs/task/{task_name}/`를 사용할 수 있다.
- 중요한 알고리즘, 구조, 복잡도 trade-off 결정은 사용자에게 고지하고 승인받은 뒤 진행한다.

## 공통 참조 문서

- Phase 운영 규칙: `docs/process/common/process_policy.md`
- 산출물 규칙: `docs/process/common/artifact_policy.md`
- 감사 운영 규칙: `docs/process/common/audit_policy.md`
- 테스트 규칙: `docs/process/common/testing_policy.md`
- 테스트 더블 규칙: `docs/process/common/test_double_policy.md`
- 검증 규칙: `docs/process/common/validation_policy.md`
- 코드 hygiene 규칙: `docs/process/common/code_hygiene_policy.md`
- 설계 품질 규칙: `docs/process/common/design_quality_policy.md`
- 성능 검토 규칙: `docs/process/common/performance_policy.md`
- 경량 태스크 예외 규칙: `docs/process/common/lightweight_task_policy.md`
- 공통 코드 정책: `docs/process/common/coding_guidelines_policy.md`

모든 Phase의 구현과 감사는 위 문서들을 함께 참조한다.

## 공통 운영 게이트

- 작업 기준은 현재 repo 안 근거를 우선하고, 없는 결정은 추측 대신 문서화 또는 사용자 승인 대상으로 올린다.
- 각 Phase는 `implementation -> audit 또는 내부 감사 묶음 -> 사용자 승인 -> 다음 Phase` 순서를 따른다.
- 감사가 여러 단계면 필요한 내부 감사가 모두 승인 가능이어야 사용자 승인 게이트로 이동할 수 있다.
- 감사가 승인 가능이어도 사용자 승인 없이는 다음 Phase로 이동하지 않는다.
- 재감사 시에는 이전 피드백 해소 여부를 먼저 확인한다.
- task workspace에 `phase_status.md`가 있으면 현재 gate와 허용 write-set을 그 파일 기준으로 먼저 확인하고, 필요하면 `scripts/validate_phase_gate.py`로 hard-stop 위반 여부를 본다. 인자 없이 실행한 기본 모드는 현재 task workspace와 `phase_status.md`의 허용/잠금 패턴에 걸리는 dirty path만 검사하고, repo 전체 dirty path까지 포함하려면 `--git-scope repo`를 명시한다.
- 변경 요청이나 방향 변경이 들어오면 문서 수정 전에 가장 이른 영향 Phase, stale 처리할 감사/승인, 잠글 산출물을 먼저 선언한다.
- 입력 문서나 산출물 변경으로 재수행할 때는 변경 영향이 걸린 가장 이른 Phase부터 다시 수행한다.
- 어떤 Phase 산출물이 수정되면 그 Phase 감사는 stale 이 되고, 이미 승인된 상태였다면 사용자 승인도 stale 이 된다.
- stale 상태가 해소되기 전에는 다음 Phase 문서, final task-local 산출물, close-out 문서, canonical 문서를 수정하지 않는다.
- `issue.md`가 바뀌면 기본적으로 Phase 1부터 다시 시작하고, `validation_report.md`만 보완하면 기본적으로 Phase 4부터 다시 수행한다.
- 다만 현재 변경이 더 이른 Phase 산출물과 모순되면 그 원인이 있는 가장 이른 Phase까지 되돌아간다.
- 현재 Phase에서 발견한 문제의 원인이 이전 Phase 산출물에 있으면 원인 Phase로 되돌아가 보완한 뒤 영향받는 Phase를 순서대로 다시 수행한다.
- 특정 Phase의 입력 또는 핵심 산출물이 바뀌면 그 Phase의 내부 절차와 내부 감사는 최신본 기준으로 처음부터 다시 맞춘다.

## 항상 먼저 읽는 문서

아래 문서는 모든 구현 태스크에서 시작 전에 먼저 확인한다.

- `docs/entrypoint.md`
- `docs/process/common/process_policy.md`
- `docs/process/common/artifact_policy.md`

아래 문서들은 모든 Phase에서 항상 다시 읽는 문서가 아니다.
현재 수행 중인 Phase와 판단이 필요한 상황에 따라 필요한 문서만 재참조한다.

## Phase별 필수 재참조 문서

### Phase 1. Requirement And Planning

- 구현 중 필수 재참조: `docs/process/common/artifact_policy.md`
- 감사 직전 필수 재참조: `docs/process/common/audit_policy.md`
- 조건부 참조: 프로젝트 overlay 문서

### Phase 2. TDD Implementation

- 구현 중 필수 재참조: `docs/process/common/testing_policy.md`, `docs/process/common/test_double_policy.md`, `docs/process/common/code_hygiene_policy.md`, `docs/process/common/design_quality_policy.md`, `docs/process/common/performance_policy.md`, `docs/process/common/coding_guidelines_policy.md`, 프로젝트 `docs/project/standards/architecture.md`, 프로젝트 `docs/project/standards/implementation_order.md`, 프로젝트 `docs/project/standards/coding_conventions_project.md`, 프로젝트 `docs/project/standards/quality_gate_profile.md`
- 감사 직전 필수 재참조: `docs/process/common/audit_policy.md`, `docs/process/common/testing_policy.md`, `docs/process/common/test_double_policy.md`, `docs/process/common/code_hygiene_policy.md`, `docs/process/common/design_quality_policy.md`, `docs/process/common/performance_policy.md`, `docs/process/common/coding_guidelines_policy.md`, 프로젝트 `docs/project/standards/architecture.md`, 프로젝트 `docs/project/standards/implementation_order.md`, 프로젝트 `docs/project/standards/coding_conventions_project.md`, 프로젝트 `docs/project/standards/quality_gate_profile.md`
- 조건부 참조: `docs/process/common/artifact_policy.md`, `docs/process/common/audit_policy.md`

### Phase 3. Integration

- 구현 중 필수 재참조: `docs/process/common/testing_policy.md`, `docs/process/common/test_double_policy.md`, `docs/process/common/validation_policy.md`, 프로젝트 `docs/project/standards/quality_gate_profile.md`, 프로젝트 `docs/project/standards/testing_profile.md`
- 감사 직전 필수 재참조: `docs/process/common/audit_policy.md`, `docs/process/common/testing_policy.md`, `docs/process/common/test_double_policy.md`, `docs/process/common/validation_policy.md`, 프로젝트 `docs/project/standards/quality_gate_profile.md`, 프로젝트 `docs/project/standards/testing_profile.md`
- 조건부 참조: `docs/process/common/audit_policy.md`, `implementation_notes.md`

### Phase 4. Validation

- 구현 중 필수 재참조: `docs/process/common/validation_policy.md`, 프로젝트 `docs/project/standards/quality_gate_profile.md`
- 감사 직전 필수 재참조: `docs/process/common/audit_policy.md`, `docs/process/common/validation_policy.md`, 프로젝트 `docs/project/standards/quality_gate_profile.md`
- 조건부 참조: `docs/process/common/audit_policy.md`

### Phase 5. Documentation

- 구현 중 필수 재참조: `docs/process/common/artifact_policy.md`
- 감사 직전 필수 재참조: `docs/process/common/audit_policy.md`
- 조건부 참조: 없음

## Phase별 종료 게이트

### Phase 1 종료 게이트

- `requirements.md`가 구현 가능한 수준으로 정리되었는가
- `plan.md`에 테스트 계획, 문서 반영 계획, 비범위가 포함되었는가
- decision 반영 후보면 관련 `docs/project/decisions/` 계획이 `plan.md`에 포함되었는가
- `issue.md`의 요청사항, 제약사항, 비범위가 `plan.md`에 빠짐없이 반영되었는가
- 현재 범위 밖 작업이 계획에 섞이지 않았는가
- requirements 감사, plan 감사, issue 대비 plan 누락 감사가 모두 승인 가능 상태인가
- 사용자 승인 게이트가 Phase 1 종료 시점에 적용되었는가

### Phase 2 종료 게이트

- 선택한 레이어가 `테스트 작성 -> 구현 -> 감사` 순서를 지켰는가
- `docs/project/standards/implementation_order.md` 기준으로 선택 레이어 순서와 세분화 근거를 남겼는가
- 테스트를 통과시키는 최소 구현만 반영했는가
- 단위 테스트가 부적절한 책임을 `implementation_notes.md`에 남겼는가

### Phase 3 종료 게이트

- 위임된 책임이 실제 통합 검증 대상으로 반영되었는가
- 연결 책임, 번역 책임, 조립 책임이 검증되었는가
- 핵심 happy path와 주요 failure path가 통합 수준에서 검증되었는가
- entrypoint, bootstrap, adapter의 실제 연결 책임이 단위 테스트에만 남지 않았는가
- 외부 port 구현체의 실제 저장/조회 연산, 응답 또는 레코드 매핑, 저장소별 경계 책임, 에러 번역이 필요한 경우 구현체 단위 통합 테스트가 반영되었는가
- 형식적 통합 테스트만 추가한 것은 아닌가

### Phase 4 종료 게이트

- 자동 검증과 수동 검증이 구분되어 있는가
- 미실행 검증과 그 사유가 기록되어 있는가
- `issue.md`, `requirements.md`, `plan.md`, `implementation_notes.md`, 실제 구현 결과를 교차 검토했는가
- Phase 1의 요청사항, 제약사항, 비범위 대비 결과 정합성이 검증되었는가
- 불일치가 있으면 `누락` 또는 `범위 확장`으로 기록되었는가
- 불일치 원인이 이전 Phase 산출물이면 원인 Phase부터 재수행 계획과 사용자 승인 여부가 기록되었는가
- `validation_report.md`에 Phase 5에서 반영할 related decisions/가 정리되었는가
- 잔여 리스크가 누락되지 않았는가
- self-healing 이 있었다면 되돌아간 Phase, stale 처리 범위, 잠긴 문서 범위가 기록되었는가

### Phase 5 종료 게이트

- 새 계약, 구조적 결정, 사용법 변경이 관련 문서에 반영되었는가
- Phase 4가 넘긴 related decisions/가 실제 `docs/project/decisions/`에 반영되었는가
- 작업 로그가 변경 목적과 결과를 복원 가능하게 남기는가
- 범위 밖 개선 사항이 현재 결과가 아니라 후속 후보로 분리되었는가
- 이전 Phase가 stale 상태인데도 close-out 또는 canonical 문서가 먼저 수정되지 않았는가

## Standard Phases

### Phase 1. Requirement And Planning

- 입력: `issue.md`
- 출력: `requirements.md`, `plan.md`
- 목표: 구현 범위, 제약, 비범위, 작업 계획을 확정한다.
- decision 반영 후보가 있으면 `plan.md`에 관련 `docs/project/decisions/` 읽기/수정/생성 계획까지 포함한다.
- 권장 순서: `issue.md` 분석 -> `requirements.md` 작성 -> requirements 감사 -> `plan.md` 작성 -> plan 감사 -> issue 대비 plan 누락 감사
- 내부 감사: requirements 감사, plan 감사, issue 대비 plan 누락 감사
- 사용자 승인: 내부 감사가 모두 승인 가능 상태가 된 뒤 Phase 1 종료 시점에 받는다.

### Phase 2. TDD Implementation

- 입력: `requirements.md`, `plan.md`
- 출력: 테스트, 구현 코드, 필요한 경우 `implementation_notes.md`
- 목표: 승인된 범위 안에서 필요한 레이어만 선택해 구현한다.
- 프로젝트별 실제 레이어 순서와 세분화 기준은 프로젝트 `docs/project/standards/implementation_order.md`를 따르며, 이 문서는 프로젝트 `docs/project/standards/architecture.md`의 실제 구조와 의존성 방향을 기준으로 작성한다.
- `docs/project/standards/implementation_order.md`는 프로젝트 기본 레이어 순서 문서이며, 특정 기획서 기준의 API 구현 우선순위나 task별 작업 순서는 `plan.md`에 남긴다.
- 프로젝트 `docs/project/standards/implementation_order.md`가 없거나 현재 TASK 기준으로 모호하면, Phase 2 구현과 감사를 진행하지 않고 프로젝트 문서를 먼저 보강한다.

### Phase 3. Integration

- 입력: Phase 2 결과물, `implementation_notes.md`
- 출력: 통합 테스트, 연동 검증 결과
- 목표: 단위 테스트로 다루기 어려운 책임, 레이어 간 연결, 핵심 happy path와 주요 failure path를 통합 수준에서 검증한다. 필요하면 전체 앱 end-to-end가 아니라 외부 port 구현체 단위 통합 테스트로도 수행한다.

### Phase 4. Validation

- 입력: 전체 구현 결과
- 출력: `validation_report.md`
- 목표: 실행한 검증, 미실행 검증, 잔여 리스크와 Phase 5에서 반영할 related decisions/를 정리하고, 필요하면 이전 Phase 산출물을 보완해 재검증 루프를 시작한다.

### Phase 5. Documentation

- 입력: 구현 및 검증 결과
- 출력: 갱신된 문서와 작업 로그
- 목표: 구조적 결정, 사용법, 작업 요약을 복원 가능하게 남기고, 필요한 `docs/project/decisions/` 반영을 실제로 닫는다.
