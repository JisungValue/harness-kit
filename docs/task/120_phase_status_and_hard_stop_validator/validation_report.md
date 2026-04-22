# Validation Report

## 실행한 검증

- 검증 항목: phase status template와 공통 policy 정렬 검토
  - 대조한 입력물: `docs/templates/task/phase_status.md`, `docs/harness/common/artifact_policy.md`, `docs/harness/common/process_policy.md`, `docs/harness/common/audit_policy.md`, `docs/harness_guide.md`, `docs/downstream_harness_flow.md`, `bootstrap/docs/quickstart.md`
  - 실행 방법 또는 확인 방식: `phase_status.md`의 lifecycle, gate state, write-set, locked path, cleanup 규칙이 문서 전반에 일관되게 반영됐는지 수동 교차 검토한다.
  - 결과: 정렬됨
  - 판정: `정합`
  - 잔여 리스크: downstream 실제 운영에서 state file을 매 단계 성실히 갱신하는 습관은 별도 운영 discipline이 필요하다.
- 검증 항목: doc guard와 validator/bundle 테스트
  - 대조한 입력물: `scripts/check_harness_docs.py`, `scripts/validate_phase_gate.py`, `tests/test_validate_phase_gate.py`, `tests/test_generate_downstream_bundle.py`, `tests/test_validate_downstream_bundle.py`
  - 실행 방법 또는 확인 방식: `python3 scripts/check_harness_docs.py`, `python3 -m unittest tests.test_validate_phase_gate tests.test_generate_downstream_bundle tests.test_validate_downstream_bundle`
  - 결과: 모두 통과
  - 판정: `정합`
  - 잔여 리스크: bundle smoke test 안에서 실제 sample task workspace로 `validate_phase_gate.py`를 실행하는 end-to-end 경로는 아직 없다.

## 실행하지 못한 검증

- downstream smoke test 안에서 실제 sample task workspace를 생성하고 `validate_phase_gate.py`를 end-to-end로 실행하는 경로는 이번 변경에서 미실행

## 결과 요약

- 이번 판단의 repo-local 근거: `docs/harness/common/process_policy.md`, `docs/harness/common/artifact_policy.md`, `docs/harness/common/audit_policy.md`, `docs/harness_guide.md`, `docs/downstream_harness_flow.md`, `bootstrap/docs/quickstart.md`, `maintainer/docs/downstream_bundle_boundary.md`, `scripts/validate_phase_gate.py`
- repo에 없어 후속 문서화/승인 대상으로 남긴 결정: 없음

## Phase 5에서 반영할 related decisions/

- 해당 없음

## 남은 리스크

- validator는 현재 task-local gate 위반을 강하게 잡지만, phase_status를 갱신하지 않은 인간/에이전트 행동 자체를 완전히 예방하지는 못한다.

## 후속 조치 필요 사항

- 필요하면 bundle smoke test나 sample workflow에 `validate_phase_gate.py` 실행 예시를 추가한다.
