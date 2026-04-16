# Requirements

## 기능 요구사항

- `docs/harness/common/process_policy.md`는 변경 요청 수신 시 가장 이른 영향 Phase, stale 처리되는 감사/승인, 잠길 산출물을 먼저 선언하도록 정의해야 한다.
- 공통 정책은 어떤 Phase 산출물이 수정되면 해당 Phase 감사가 stale 이 되고, 이미 승인된 상태였다면 사용자 승인도 stale 이 된다고 명시해야 한다.
- 공통 정책은 원인 Phase보다 뒤의 산출물을 stale 후보로 잠그고, 현재 Phase가 다시 승인되기 전에는 다음 Phase 문서, final task-local 산출물, close-out 문서, canonical 문서를 수정하지 못하게 해야 한다.
- 각 Phase `implementation.md`는 입력 또는 핵심 산출물 변경 시 어떤 내부 절차를 다시 타야 하는지 phase별로 정의해야 한다.
- 각 Phase `audit.md`는 stale 상태 승인 금지와 최신 산출물 기준 판정을 명시해야 한다.
- `implementation_notes.md`에는 self-healing 발동 시 남겨야 할 최소 기록 항목이 정의돼야 한다.
- `docs/harness_guide.md`와 `docs/downstream_harness_flow.md`는 위 runtime contract를 요약해 설명해야 한다.

## 비기능 요구사항 또는 품질 요구사항

- 문안은 기존 repo-local 용어와 Phase 구조를 유지하는 최소 수정이어야 한다.
- 공통 규칙과 phase-local 규칙이 서로 모순되지 않아야 한다.
- stale, approval, lock, rerun 같은 핵심 용어가 문서 간 일관되게 사용돼야 한다.

## 입력/출력

- 입력:
  - `docs/harness/common/process_policy.md`
  - `docs/harness/common/validation_policy.md`
  - `docs/harness/common/artifact_policy.md`
  - `docs/harness_guide.md`
  - `docs/downstream_harness_flow.md`
  - `docs/phase_1_requirement_and_planning/*`
  - `docs/phase_2_tdd_implementation/*`
  - `docs/phase_3_integration/*`
  - `docs/phase_4_validation/*`
  - `docs/phase_5_documentation/*`
  - `docs/templates/task/implementation_notes.md`
- 출력:
  - self-healing runtime contract가 반영된 공통/phase 문서
  - self-healing 기록 항목이 반영된 task template

## 제약사항

- downstream upgrade guide 문제로 범위를 넓히지 않는다.
- 새 자동화 도구나 validator 구현은 포함하지 않는다.
- 기존 승인 게이트 위치를 무너뜨리지 않고 더 명확하게 만드는 범위에 머문다.

## 예외 상황

- `validation_report.md`만 보완하더라도 더 이른 Phase 산출물 해석이 바뀌면 Phase 4 단독 수정으로 닫지 않고 원인 Phase까지 되돌아가야 한다.
- 사용자 목표가 close-out 이어도 현재 Phase가 stale 이면 close-out 문서를 먼저 수정하면 안 된다.

## 성공 기준

- 공통 정책에 self-healing, stale invalidation, write-set lock, phase jump 금지 규칙이 반영된다.
- Phase 1~5 implementation과 audit 문서가 각각의 재수행 규칙과 stale 승인 금지 규칙을 담는다.
- harness guide, downstream flow, task template이 같은 runtime contract를 설명한다.
- `python3 scripts/check_harness_docs.py`가 통과한다.
