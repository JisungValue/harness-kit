# Validation Report

## 실행한 검증

- 검증 항목: repo-local source-of-truth 원칙의 core 문서 정렬
  - 대조한 입력물: `README.md`, `docs/harness_guide.md`, `bootstrap/docs/how_harness_kit_works.md`, `docs/harness/common/process_policy.md`, `docs/harness/common/artifact_policy.md`, `docs/harness/common/audit_policy.md`, `maintainer/docs/audit_policy.md`
  - 실행 방법 또는 확인 방식: source-of-truth 선언, 외부 관행 비우선, 추측 금지, project overlay / `docs/decisions/` / task artifact handoff 문구를 수동 교차 검토했다.
  - 결과: repo-local 근거 우선 원칙과 누락된 결정 handoff 경로가 core 운영 문서와 maintainer audit 기준에 함께 반영됐다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: substring 기반 doc guard가 문구 drift는 잡지만 문장 품질 전체를 의미 분석하지는 않는다.

- 검증 항목: task template와 example의 근거 기록 위치 정렬
  - 대조한 입력물: `docs/templates/task/implementation_notes.md`, `docs/templates/task/validation_report.md`, `docs/examples/sample-task/implementation_notes.md`, `docs/examples/sample-task/validation_report.md`, `docs/examples/sample-lightweight-task/implementation_notes.md`, `docs/examples/sample-lightweight-task/validation_report.md`
  - 실행 방법 또는 확인 방식: template에 새 근거/handoff 항목이 들어갔는지, examples가 이를 실제 문구로 채웠는지 수동 검토했다.
  - 결과: `implementation_notes.md`와 `validation_report.md` 템플릿에 repo-local 근거와 누락 결정 handoff 항목이 추가됐고, sample examples도 같은 구조를 따르도록 정렬됐다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 실제 downstream project task가 이 항목을 얼마나 일관되게 채우는지는 이후 운영에서 계속 봐야 한다.

- 검증 항목: doc guard drift 방지
  - 대조한 입력물: `scripts/check_harness_docs.py`
  - 실행 방법 또는 확인 방식: `python3 scripts/check_harness_docs.py`
  - 결과: source-of-truth 핵심 문구, 누락된 결정 handoff 문구, task template 근거 항목, maintainer/common audit policy 반영 여부를 자동 검사하도록 보강했고 현재 저장소 기준 통과했다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 없음

- 검증 항목: changed-parts / whole-harness maintainer audit
  - 대조한 입력물: 변경 파일 전체, task workspace 산출물, doc guard 결과
  - 실행 방법 또는 확인 방식: 분리된 subagent changed-parts audit, whole-harness audit 수행 후 피드백 반영
  - 결과: 최초 감사에서 sample example의 잘못된 repo-local 경로, 누락된 task 기록, handoff destination drift guard 부족, `harness.log` 미기록이 지적됐다. sample/example, task 산출물, doc guard, `harness.log`를 보강한 뒤 재감사했으며 changed-parts / whole-harness 모두 최종 `APPROVE`가 나왔다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: doc guard는 여전히 substring 중심이라 근거 서술의 질적 적절성은 수동 감사가 계속 필요하다.

## 실행하지 못한 검증

- downstream bootstrap 또는 bundle smoke에 이 원칙을 별도 end-to-end로 드러내는 검증은 미실행

## 결과 요약

- 이번 판단의 repo-local 근거: `README.md`, `docs/harness_guide.md`, `bootstrap/docs/how_harness_kit_works.md`, process/artifact/common audit policy, maintainer audit policy, task templates, sample examples를 기준으로 정렬했다.
- repo에 없어 후속 문서화/승인 대상으로 남긴 결정: 특정 프로젝트에서 어떤 문서가 canonical source-of-truth인지의 세부 목록은 각 project overlay 또는 `docs/decisions/`에서 별도로 확정해야 한다.

## Phase 5에서 반영할 related decisions/

- 해당 없음. 이번 작업은 project-local decision 내용이 아니라 core 운영 원칙과 기록 규칙 정렬 범위다.

## 남은 리스크

- 아직은 문서/감사/템플릿 규칙 중심이라, 실제 downstream task 작성 시 이 항목을 consistently 채우는 운영 discipline이 필요하다.

## 후속 조치 필요 사항

- `#69 empirical reproduction 원칙 추가`에서 bug/regression 근거 기록을 이번 source-of-truth 원칙과 연결해 더 강화할 수 있다.
