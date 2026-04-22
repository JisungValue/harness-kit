# Implementation Notes

## 진행 로그

- Phase 1 시작: issue `#68` 기준으로 repo-local source-of-truth 원칙을 선언, 운영 규칙, 감사 체크포인트, task 기록 위치까지 연결하는 범위를 정리하고 요구사항/계획을 고정함.
- 구현: `README.md`, `docs/harness_guide.md`, `docs/how_harness_kit_works.md`, `docs/harness/common/process_policy.md`에 repo-local 근거 우선, 외부 관행 비우선, 추측 금지, project overlay / `docs/decisions/` / task artifact handoff 원칙을 반영함.
- 구현: `docs/harness/common/artifact_policy.md`, `docs/harness/common/audit_policy.md`, `maintainer/docs/audit_policy.md`, task templates, sample examples를 근거 기록과 감사 가능성 기준으로 정렬함.
- 구현: `scripts/check_harness_docs.py`가 source-of-truth 핵심 문구와 handoff destination, template 항목 drift를 다시 잡도록 보강함.
- 검증: `python3 scripts/check_harness_docs.py` 통과.
- 감사: 최초 changed-parts / whole-harness audit에서 sample example 경로, task 기록, handoff guard, `harness.log` 누락이 지적됐고 이를 보강한 뒤 재감사에서 둘 다 `APPROVE`로 전환됨.

## 경량 검토 기록

- 작은 태스크로 본 근거: 해당 없음
- 경량 적용 승인 여부: 미적용
- 실제 축소한 범위: 해당 없음
- 유지한 테스트: doc guard
- 유지한 감사: changed-parts / whole-harness audit 수행 완료
- 전체 흐름 영향 요약: core guide, process/audit policy, task template, doc guard가 함께 영향받는다.
- 남은 리스크: 선언만 있고 기록/감사 포인트가 약하면 source-of-truth 원칙이 실제 운영에서 희미해질 수 있다.
- Full 전환 조건 또는 승격 조건: 이미 full 흐름으로 진행 중

## 구현 중 결정 사항

- repo-local 근거: `README.md`, `docs/harness_guide.md`, `docs/how_harness_kit_works.md`, `docs/harness/common/process_policy.md`, `docs/harness/common/artifact_policy.md`, `docs/harness/common/audit_policy.md`, `maintainer/docs/audit_policy.md`, `scripts/check_harness_docs.py`를 기준으로 source-of-truth 선언, 기록 위치, 감사 체크포인트를 맞췄다.
- repo에 없어 문서화/승인 대상으로 넘긴 결정: 개별 프로젝트에서 어떤 문서가 canonical source-of-truth인지의 세부 목록은 core가 강제하지 않고 project overlay 또는 `docs/decisions/`에서 별도로 확정하도록 남겼다.

## 위임된 책임

## 사용자 승인 필요 항목

## 후속 태스크 후보

- `#69 empirical reproduction 원칙 추가`는 이번 source-of-truth 원칙 위에 bug/regression 대응 근거 규칙을 이어서 올리는 자연스러운 후속 후보다.
