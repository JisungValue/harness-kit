# Process Policy

## 목적

이 문서는 모든 구현 태스크에서 공통으로 적용되는 Phase 운영 규칙을 정의한다.

## 실무 요약

- 기본 Phase 순서는 `1 -> 2 -> 3 -> 4 -> 5` 이다.
- 각 Phase는 `implementation -> audit -> 사용자 승인 -> 다음 Phase` 순서로 진행한다.
- 변경 요청, 범위 수정, close-out 방향 변경이 들어오면 먼저 가장 이른 영향 Phase, stale 처리할 감사/승인, 잠글 산출물을 선언한다.
- `phase_status.md`가 있으면 현재 task의 gate 상태와 허용 write-set은 그 파일을 기준으로 먼저 확인한다.
- 특정 입력 문서나 산출물이 바뀌어 재수행이 필요할 때도 무조건 Phase 1부터 다시 시작하지 않는다.
- 재수행은 변경 영향이 걸린 가장 이른 Phase부터 시작하고, 그 이후 영향을 받은 Phase만 순서대로 다시 수행한다.
- 현재 Phase가 다시 승인되기 전에는 다음 Phase 문서, final task-local 산출물, close-out 문서, canonical 문서를 수정하지 않는다.
- 어떤 Phase 산출물이 수정되면 그 Phase의 감사 결과는 stale 이 되고, 이미 사용자 승인까지 끝났다면 승인 상태도 stale 이 된다.
- 현재 Phase 감사가 승인 가능이더라도 사용자 승인 전에는 다음 Phase로 이동하지 않는다.
- 승인되지 않은 범위 확장은 구현하지 않는다.
- 현재 TASK와 직접 관련 없는 리팩터링은 현재 작업에 자동 포함하지 않는다.
- 예외 적용이나 Phase 변경은 사용자 승인 후에만 가능하다.
- 작업 식별자가 있으면 브랜치 이름은 `{task_id}_{task_name}` 형식을 권장한다.
- 중요한 알고리즘, 구조, 복잡도 trade-off 결정은 사용자에게 고지하고 승인받은 뒤 진행한다.

## 공통 정책 해석 우선순위

공통 정책 문서를 함께 참조할 때 해석 우선순위는 아래와 같다.

1. `docs/entrypoint.md`
2. 현재 수행 중인 Phase의 `implementation.md`, `audit.md`
3. `docs/process/common/process_policy.md`
4. `docs/process/common/artifact_policy.md`
5. `docs/process/common/audit_policy.md`
6. `docs/process/common/testing_policy.md`
7. `docs/process/common/test_double_policy.md`
8. `docs/process/common/validation_policy.md`
9. `docs/process/common/lightweight_task_policy.md`
10. `docs/process/common/coding_guidelines_policy.md`

우선순위 해석 원칙은 아래와 같다.

- 상위 문서가 하위 문서보다 우선한다.
- 같은 수준에서는 더 구체적인 문서가 더 일반적인 문서보다 우선한다.
- 경량 태스크 예외는 명시적으로 허용된 범위에서만 적용되며, 기본 Phase 원칙을 자동으로 대체하지 않는다.
- 충돌이 해소되지 않으면 사용자 승인 없이는 예외 적용이나 Phase 변경을 하지 않는다.

## Repo-Local Source-Of-Truth 규칙

- 작업 기준은 현재 repo 안의 `README`, `docs/*`, `docs/project/decisions/*`, `scripts/*`, `config` 같은 repo-local 근거를 우선한다.
- 위 규칙은 repo-local `source-of-truth` 우선 원칙으로 본다.
- 기억, 외부 대화, 다른 프로젝트 관행, 과거 비슷한 프로젝트 경험은 참고할 수 있어도 현재 repo 근거보다 우선하지 않는다.
- repo 안 근거끼리 충돌하면 위 우선순위 규칙과 더 구체적인 문서를 먼저 적용한다.
- 그래도 해소되지 않으면 사용자 승인 없이는 예외 적용이나 Phase 변경을 하지 않는다.
- 필요한 결정이나 근거가 repo에 없으면 추측으로 메우지 않는다.
- repo에 없는 프로젝트 전용 결정은 project overlay 또는 `docs/project/decisions/` 반영 후보로 넘기고, 같은 사실을 `implementation_notes.md` 또는 `validation_report.md`에 기록한다.

## Phase 운영 원칙

- 모든 구현 태스크는 `docs/entrypoint.md`에 정의된 Phase 순서를 따른다.
- 각 Phase는 해당 `implementation.md`를 기준으로 구현한 뒤 `audit.md`를 기준으로 감사를 수행한다.
- 현재 Phase는 `implementation -> audit -> 사용자 승인 -> 다음 Phase` 순서를 지킨다.
- 수정 요청이나 산출물 변경이 생기면 어떤 문서도 수정하기 전에 아래 3가지를 먼저 선언한다.
  1. 가장 이른 영향 Phase
  2. stale 처리되는 기존 감사 또는 사용자 승인
  3. 잠금 상태로 둘 stale 산출물
- `phase_status.md`를 쓰는 task라면 선언 직후 현재 Phase, 현재 gate, 허용 write-set, 잠긴 경로, stale 산출물을 먼저 갱신한다.
- 감사 결과가 승인 불가이면, 피드백을 반영한 뒤 같은 Phase에서 다시 구현과 감사를 반복한다.
- 특정 입력 문서나 산출물이 변경되면, 그 변경 영향이 걸린 가장 이른 Phase부터 다시 수행한다.
- 특정 Phase의 입력 문서나 핵심 산출물이 바뀌면 그 Phase의 내부 절차는 최신 산출물을 기준으로 처음부터 다시 맞춘다.
- 변경이 현재 Phase 또는 더 늦은 Phase 산출물의 정합성 보완에만 머무르면 해당 Phase부터 다시 수행하고, 더 이른 Phase 산출물과 모순될 때만 원인 Phase로 되돌아간다.
- 현재 Phase에서 발견한 문제의 원인이 이전 Phase 산출물(`requirements.md`, `plan.md`, `implementation_notes.md` 등)에 있으면 원인 Phase로 되돌아가 보완한 뒤 영향받는 Phase들을 순서대로 다시 수행한다.
- 재감사 시에는 이전 감사 피드백 해소 여부를 먼저 확인한 뒤 남은 문제와 신규 문제를 구분한다.
- stale 상태가 해소되기 전에는 이후 Phase 산출물을 새로 작성하거나 갱신하지 않는다.
- write-set 위반 가능성이 보이면 구현을 계속 진행하지 않고 현재 gate 상태만 보고한 뒤 멈춘다.
- 감사 결과가 승인 가능이어도 사용자 승인 전에는 다음 Phase로 이동하지 않는다.
- Phase 생략, 순서 변경, 예외 처리는 사용자 승인 후에만 가능하다.
- 운영성 작업은 이 Phase 프로세스의 적용 대상에서 제외한다.

## Self-Healing Runtime 규칙

- self-healing은 승인 없는 자동 self-modify가 아니라, 변경 이후 Phase 순서와 감사 상태를 다시 맞추는 runtime 규칙을 뜻한다.
- 새 요청을 받거나 기존 판단 근거가 바뀌면 먼저 가장 이른 영향 Phase를 다시 찾는다.
- 가장 이른 영향 Phase가 확정되기 전에는 임의로 다음 Phase 문서나 close-out 문서를 수정하지 않는다.
- self-healing 발동 사실과 아래 항목은 `implementation_notes.md`의 `진행 로그`에 남긴다.
  - 변경 원인
  - 가장 이른 영향 Phase
  - stale 처리한 감사와 승인
  - stale 처리한 산출물
  - 다시 수행할 내부 감사
  - 현재 잠긴 문서 범위
- `phase_status.md`가 있으면 같은 사실을 runtime state에도 즉시 반영한다.

## Stale Invalidation 규칙

- 어떤 Phase 산출물이 수정되면 그 Phase의 감사 결과는 자동으로 stale 이 된다.
- 그 Phase가 이미 사용자 승인까지 받은 상태였다면 승인 상태도 stale 이 된다.
- 원인 Phase보다 뒤에서 작성된 산출물은 기본적으로 stale 후보로 보고 잠금 상태로 둔다.
- stale 후보 산출물은 원인 Phase가 다시 승인될 때까지 수정, 갱신, close-out 반영 대상으로 사용하지 않는다.
- 이전 감사 결과는 참고 기록으로는 남길 수 있지만, 최신 산출물 기준의 승인 상태를 대신하지 못한다.

## Write-Set Lock 규칙

- 재수행을 시작할 때는 현재 Phase에서 수정 가능한 파일 집합을 먼저 정한다.
- write-set 밖의 파일은 현재 Phase가 다시 승인될 때까지 잠금 상태로 본다.
- 현재 Phase보다 뒤의 문서, final task-local 산출물, close-out 문서, canonical 문서는 기본적으로 잠금 대상이다.
- `phase_status.md`를 쓰는 task라면 허용 write-set과 잠긴 경로를 그 파일에 명시하고, `scripts/validate_phase_gate.py`로 위반 여부를 검사할 수 있어야 한다. 인자 없이 실행한 기본 모드는 현재 task workspace와 `phase_status.md`의 허용/잠금 패턴에 걸리는 dirty path만 검사하고, repo 전체 dirty path까지 보려면 `--git-scope repo`를 명시한다.
- 예를 들어 Phase 1을 다시 수행할 때는 기본적으로 `issue.md`, `requirements.md`, `plan.md`, `implementation_notes.md`만 수정 대상으로 두고, `validation_report.md`, final task-local 산출물, `docs/project/decisions/*`는 잠근다.
- 예외적으로 잠금을 풀어야 하면 사용자 승인을 먼저 받는다.

## Phase 이동 규칙

- 다음 Phase로 이동하려면 현재 Phase 감사가 승인 가능이고 사용자 승인을 받아야 한다.
- 이전 Phase로 되돌아가 보완한 경우, 보완된 Phase부터 현재 Phase까지 필요한 구현, 감사, 사용자 승인 게이트를 다시 통과해야 한다.
- 입력 또는 산출물 변경으로 재수행할 때도, 변경 영향이 없는 더 이른 Phase를 자동으로 다시 수행하지 않는다.
- 현재 Phase의 내부 구현, 내부 감사, 사용자 승인이 끝나기 전에는 다음 Phase 파일을 수정하지 않는다.
- 사용자의 목표가 close-out 이더라도 현재 Phase가 닫히지 않았으면 close-out 문서를 먼저 수정하지 않는다.
- 구현 중 새 계약이나 구조적 결정이 생기면 문서 반영 대상을 식별한다.
- 승인되지 않은 범위 확장은 구현하지 않는다.

## 재수행 기준 예시

- `issue.md`가 바뀌면 Phase 1 입력이 달라진 것이므로 `requirements.md`, `plan.md`를 다시 만들고 이후 영향을 받은 Phase를 순서대로 다시 수행한다.
- `validation_report.md`만 보완하면 기본적으로 Phase 4부터 다시 수행한다.
- 다만 `validation_report.md` 보완 내용이 `issue.md`, `requirements.md`, `plan.md`, `implementation_notes.md` 같은 더 이른 Phase 산출물과 모순되면, 그 모순의 원인이 있는 가장 이른 Phase까지 되돌아가서 다시 수행한다.

## 작업 브랜치 및 중요 결정 규칙

- 작업 식별자가 있으면 브랜치 이름은 `{task_id}_{task_name}` 형식을 권장한다.
- 작업 식별자가 없으면 현재 태스크를 식별할 수 있는 일관된 브랜치 이름을 사용한다.
- 중요한 알고리즘 선택, 구조 변경, 복잡도 trade-off 결정은 구현 전에 사용자에게 고지한다.
- 중요한 알고리즘 선택, 구조 변경, 복잡도 trade-off 결정은 사용자 승인 후 진행한다.

## 범위 통제 기록 규칙

- 각 태스크의 `requirements.md` 또는 `plan.md`에는 비범위를 명시한다.
- 구현 중 새 이슈나 추가 개선점이 발견되면 현재 범위에 자동 포함하지 않는다.
- 현재 승인 범위 밖의 항목은 `implementation_notes.md`에 후속 태스크 후보로 기록한다.
- 범위 확장이 필요하면 사용자 승인 전에는 구현하지 않는다.

## 구현 범위 통제 규칙

- 현재 TASK의 요구사항, 계획, 승인 범위를 벗어나는 코드 정리는 자동으로 포함하지 않는다.
- 기존 중복 제거, 구조 개선, 네이밍 정리, 레이어 재배치는 현재 TASK 수행에 직접 필요할 때만 제한적으로 수행한다.
- 직접 필요하지 않은 리팩터링은 별도 리팩터링 태스크로 분리한다.
- 구현 중 발견한 개선 사항은 현재 TASK에서 함께 반영하지 말고 `implementation_notes.md`에 후속 태스크 후보로 기록한다.

직접 필요로 볼 수 있는 경우는 아래와 같다.

- 현재 TASK 요구사항을 구현하거나 버그를 수정하지 않으면 변경 자체가 성립하지 않는 경우
- 현재 수정 파일 내부에서 테스트 가능성이나 기존 아키텍처 규칙 준수를 위해 불가피한 경우
- 현재 변경 코드가 의존하는 바로 인접한 중복 제거 또는 함수 추출처럼 영향 범위가 국소적인 경우

별도 리팩터링 태스크로 분리해야 하는 경우는 아래와 같다.

- 현재 수정 대상과 직접 관련 없는 기존 중복 제거
- 전체 네이밍 정리, 광범위한 파일 이동, 공통 유틸 추출, 미래 확장을 위한 선제 추상화
- 현재 TASK를 수행하지 않아도 독립적으로 진행 가능한 구조 개선

## Phase 2 레이어 운영 규칙

- Phase 2는 기능 전체를 한 번에 구현하지 않고, 필요한 레이어만 선택해 진행한다.
- 선택된 레이어들 사이의 작업 순서는 의존성 안쪽부터 바깥쪽으로 진행한다.
- 프로젝트별 실제 구현 순서와 레이어 세분화 기준은 `docs/project/standards/implementation_order.md`에서 정의한다.
- 프로젝트 `docs/project/standards/implementation_order.md`는 `docs/project/standards/architecture.md`의 실제 구조와 의존성 방향을 기준으로 작성해 구조와 구현 순서 해석이 분리되지 않게 유지한다.
- 특정 TASK의 API/기능 구현 우선순위는 `plan.md`에서 정하고, `implementation_order.md`는 그 판단의 프로젝트 기본 레이어 기준으로 유지한다.
- 프로젝트 구조에 맞는 실제 레이어 명칭은 overlay 문서에서 정의한다.
- 각 선택 레이어는 아래 순서를 따른다.
  1. 테스트 작성
  2. 구현
  3. 감사
- 한 레이어 감사가 끝난 뒤 다음 레이어로 진행한다.
- 모든 선택된 레이어 구현이 끝나면 Phase 2 전체 감사를 수행한다.
- Phase 2 전체 감사가 승인 불가이면 같은 Phase에서 보완한 뒤 재감사한다.
