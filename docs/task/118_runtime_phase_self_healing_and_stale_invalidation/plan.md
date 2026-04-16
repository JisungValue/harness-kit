# Plan

## 변경 대상 파일 또는 모듈

- `docs/harness/common/process_policy.md`
- `docs/harness/common/validation_policy.md`
- `docs/harness/common/artifact_policy.md`
- `docs/harness_guide.md`
- `docs/downstream_harness_flow.md`
- `docs/phase_1_requirement_and_planning/implementation.md`
- `docs/phase_1_requirement_and_planning/audit.md`
- `docs/phase_2_tdd_implementation/implementation.md`
- `docs/phase_2_tdd_implementation/audit.md`
- `docs/phase_3_integration/implementation.md`
- `docs/phase_3_integration/audit.md`
- `docs/phase_4_validation/implementation.md`
- `docs/phase_4_validation/audit.md`
- `docs/phase_5_documentation/implementation.md`
- `docs/phase_5_documentation/audit.md`
- `docs/templates/task/implementation_notes.md`

## 레이어별 작업 계획

- 공통 policy 문서에 self-healing runtime 규칙, stale invalidation, write-set lock, close-out 잠금 규칙을 추가한다.
- Phase 1~5 implementation 문서에 입력/핵심 산출물 변경 시 다시 타야 할 내부 절차를 반영한다.
- Phase 1~5 audit 문서에 stale 상태 승인 금지와 최신 산출물 기준 판정 규칙을 반영한다.
- `docs/harness_guide.md`, `docs/downstream_harness_flow.md`, task template을 같은 runtime contract로 정렬한다.
- 현재 작업 내용을 task workspace 산출물에 남긴다.

## 테스트 계획

- `python3 scripts/check_harness_docs.py`
- 변경한 공통 policy, phase 문서, guide 사이의 용어와 gate 순서를 수동 교차 검토한다.

## 문서 반영 계획

- self-healing runtime contract를 공통 policy, phase 문서, guide, task template에 반영한다.
- 현재 작업의 task workspace 산출물(`issue.md`, `requirements.md`, `plan.md`, `implementation_notes.md`, `validation_report.md`)을 함께 작성한다.
- 관련 `docs/decisions/README.md` 또는 `DEC-###-slug.md` 읽기/수정/생성 필요 여부: 해당 없음. 이번 작업은 project-local 또는 core architectural decision보다는 process/runtime 문서 정렬 범위다.
- 새 decision이 필요하면 index 갱신 계획: 해당 없음.

## 비범위

- downstream upgrade guide 또는 bundle boundary 문서 재설계
- validator/doctor 구현
- 실제 downstream 세션에서의 end-to-end 시뮬레이터 추가

## 리스크 또는 확인 포인트

- stale, 잠금, 승인 재적용 문구가 과도하게 중복되면 문서 가독성이 떨어질 수 있으므로 공통 규칙과 phase-local 규칙 역할을 나눠야 한다.
- Phase 5의 canonical/close-out 잠금 문구가 `docs/decisions/*` 반영 규칙과 충돌하지 않게 표현을 맞춰야 한다.
