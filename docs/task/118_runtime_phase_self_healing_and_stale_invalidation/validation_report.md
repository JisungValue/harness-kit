# Validation Report

## 실행한 검증

- 검증 항목: 공통 policy와 phase 문서의 self-healing runtime contract 정렬 검토
  - 대조한 입력물: `docs/harness/common/process_policy.md`, `docs/harness/common/validation_policy.md`, `docs/harness/common/artifact_policy.md`, `docs/harness/common/audit_policy.md`, `docs/harness/common/lightweight_task_policy.md`, `docs/harness_guide.md`, `docs/downstream_harness_flow.md`, `bootstrap/docs/quickstart.md`, `docs/project_overlay/project_entrypoint_template.md`, `docs/phase_1_requirement_and_planning/*`, `docs/phase_2_tdd_implementation/*`, `docs/phase_3_integration/*`, `docs/phase_4_validation/*`, `docs/phase_5_documentation/*`
  - 실행 방법 또는 확인 방식: 공통 규칙, phase별 재수행 규칙, stale 승인 금지, close-out 잠금 문구와 추가 감사한 인접 지침의 교차 참조 규칙이 같은 계약을 가리키는지 수동 교차 검토했다.
  - 결과: process policy의 공통 self-healing 규칙, common audit policy의 stale 재사용 금지와 인접 지침 교차 검토 규칙, lightweight policy의 stale/full 전환 규칙, phase-local rerun 규칙, guide/flow 요약 문안이 같은 방향으로 정렬됐다.
  - 판정: `정합`
  - 잔여 리스크: 문서 기반 규칙이라 실제 downstream session에서의 runtime drift를 자동으로 막지는 못한다.
- 검증 항목: 문서 정합성 스크립트 검증
  - 대조한 입력물: `scripts/check_harness_docs.py`, 변경된 project-facing 문서 전체
  - 실행 방법 또는 확인 방식: `python3 scripts/check_harness_docs.py`
  - 결과: 통과
  - 판정: `정합`
  - 잔여 리스크: checker는 문구 존재와 일부 경로 정합성을 잡아 주지만, 실제 운영 중 phase decision 품질 자체를 완전히 보장하지는 않는다.

## 실행하지 못한 검증

- 실제 downstream 프로젝트에서 수정 요청 -> stale invalidation -> phase rerun -> close-out unlock 흐름을 end-to-end로 재현하는 session scenario 검증은 미실행

## 결과 요약

- 이번 판단의 repo-local 근거: `docs/harness/common/process_policy.md`, `docs/harness/common/validation_policy.md`, `docs/harness/common/artifact_policy.md`, `docs/harness/common/audit_policy.md`, `docs/harness/common/lightweight_task_policy.md`, `docs/harness_guide.md`, `docs/downstream_harness_flow.md`, `bootstrap/docs/quickstart.md`, `docs/project_overlay/project_entrypoint_template.md`, 각 `docs/phase_*/*`, `docs/templates/task/implementation_notes.md`
- repo에 없어 후속 문서화/승인 대상으로 남긴 결정: 없음

## Phase 5에서 반영할 related decisions/

- 해당 없음. 이번 작업은 core process/runtime 문서 정렬 범위이며 별도 decision record를 추가할 정도의 구조 분기나 장기 정책 선택을 만들지 않았다.

## 남은 리스크

- 현재는 정책과 템플릿 중심 변경이라, 실제 downstream task 수행에서 이 규칙이 얼마나 일관되게 적용되는지는 후속 운영 검증이 필요하다.

## 후속 조치 필요 사항

- 필요하면 downstream task sample 또는 focused documentation test에 self-healing 시나리오를 추가한다.
