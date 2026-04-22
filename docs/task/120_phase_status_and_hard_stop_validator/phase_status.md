# Phase Status

## Current State

- Task Status: `approval_required`
- Current Phase: `Phase 5`
- Current Gate: `documentation and validation complete`
- Last Approved Phase: `없음`

## Allowed Write Set

- `$TASK/implementation_notes.md`
- `$TASK/validation_report.md`
- `$TASK/phase_status.md`

## Locked Paths

- `docs/harness/**`
- `docs/phase_*/*`
- `docs/decisions/*`
- `bootstrap/docs/quickstart.md`
- `docs/downstream_harness_flow.md`
- `docs/harness_guide.md`
- `docs/templates/task/phase_status.md`
- `docs/examples/sample-task/phase_status.md`
- `docs/examples/sample-lightweight-task/phase_status.md`
- `scripts/validate_phase_gate.py`
- `scripts/check_harness_docs.py`
- `tests/test_validate_phase_gate.py`
- `tests/test_generate_downstream_bundle.py`
- `tests/test_validate_downstream_bundle.py`

## Stale Artifacts

- 없음

## Next Action

- 사용자 확인 전에는 task-local 상태 기록만 갱신하고, 후속 수정이 생기면 가장 이른 영향 Phase와 write-set부터 다시 판정한다.

## Cleanup

- Task 종료 전 유지: `yes`
- Task 종료 후 정리: `Phase 5` close-out 완료 뒤 최종 상태를 다른 산출물에 남기고 삭제할 수 있다.
