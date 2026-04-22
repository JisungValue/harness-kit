# Implementation Notes

## 진행 로그

- Phase 1: issue `#118` 기준으로 현재 문서가 earliest impacted phase 재수행 원칙은 갖고 있지만 stale invalidation, write-set lock, next-phase jump 금지는 충분히 명시하지 못한 공백을 정리했다.
- 구현: `docs/harness/common/process_policy.md`, `docs/harness/common/validation_policy.md`, `docs/harness/common/artifact_policy.md`에 self-healing runtime, stale invalidation, write-set lock, implementation_notes 기록 규칙을 추가했다.
- 구현: 추가 감사 결과를 반영해 `docs/harness/common/audit_policy.md`에 stale 재사용 금지, write-set lock 확인, 경량 예외 및 인접 지침 교차 검토 규칙을 추가했다.
- 구현: `docs/harness/common/lightweight_task_policy.md`에 경량 승인 stale 처리와 Full 전환 트리거를 보강했다.
- 구현: `docs/phase_1_requirement_and_planning/*`부터 `docs/phase_5_documentation/*`까지 phase별 재수행 규칙과 stale 상태 승인 금지 문구를 반영했다.
- 구현: `docs/harness_guide.md`, `docs/downstream_harness_flow.md`, `docs/templates/task/implementation_notes.md`를 같은 runtime contract로 정렬했다.
- self-healing 발동 시 기록: 해당 없음. 이번 작업은 self-healing 규칙 문서화 태스크이며, 현재 task runtime 중 self-healing 되돌아가기가 발생하지 않았다.

## 경량 검토 기록

- 해당 없음

## 구현 중 결정 사항

- repo-local 근거: `docs/harness/common/process_policy.md`, `docs/harness/common/validation_policy.md`, `docs/harness/common/artifact_policy.md`, `docs/harness/common/audit_policy.md`, `docs/harness/common/lightweight_task_policy.md`, `docs/harness_guide.md`, `docs/downstream_harness_flow.md`, `bootstrap/docs/quickstart.md`, `docs/project_overlay/project_entrypoint_template.md`, 각 `docs/phase_*/*` 문서를 기준으로 공통 규칙과 phase-local 규칙의 책임을 나눴다.
- repo에 없어 문서화/승인 대상으로 넘긴 결정: 없음

## 위임된 책임

- 없음

## 사용자 승인 필요 항목

- 없음

## 후속 태스크 후보

- runtime self-healing 규칙을 실제 downstream task session fixture나 문서 기반 scenario test로 고정하는 검증을 추가할 수 있다.
