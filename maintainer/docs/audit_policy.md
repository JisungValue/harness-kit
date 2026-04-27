# Kit Maintenance Audit Policy

## 목적

이 문서는 `harness-kit` core 문서를 수정할 때 적용하는 maintainer 전용 감사 기준을 정의한다.

## 운영 모드

- 본 문서는 maintainer 감사의 기본 모드를 `Strict Mode`로 사용한다.
- core 의미 변경은 `changed-parts`와 `whole-harness`를 모두 통과해야 승인 가능하다.

## 적용 범위

- 대상: `harness-kit` 저장소의 core 규칙, phase 기준, template, example, bootstrap 자산, 문서 구조 변경
- 비대상: `harness-kit`를 적용한 개별 서비스 프로젝트의 task/phase 감사

## Downstream 프로젝트와의 경계

이 문서는 `harness-kit`를 사용하는 개별 프로젝트의 일반 task 수행 규칙이 아니다.

- 개별 프로젝트의 task/phase 운영은 프로젝트 로컬 `docs/project_entrypoint.md`와 project overlay 문서가 담당한다.
- 본 문서는 `harness-kit` 저장소의 core 규칙, 공통 phase 기준, template, example, bootstrap 자산, overlay template, 문서 구조를 수정할 때만 적용한다.
- downstream 프로젝트에서 kit를 사용해 구현하거나 감사하는 일만으로는 본 maintainer 절차를 적용하지 않는다.
- 단, downstream 프로젝트 요구를 반영하기 위해 `harness-kit` core 또는 overlay template 자체를 수정하는 순간부터 본 문서를 적용한다.

## 프로젝트 문서 변경과 Kit 변경의 판별 기준

- 비대상: downstream 프로젝트 로컬 `docs/project_entrypoint.md`, `docs/standard/*`, 프로젝트 저장소 안의 task 산출물 변경
- 대상: 이 저장소의 `downstream/docs/harness_guide.md`, `downstream/docs/harness/common/*`, `docs/phase_*`, `bootstrap/docs/project_overlay/*` template, `bootstrap/*`, `README.md`, `maintainer/scripts/check_harness_docs.py`, `bootstrap/scripts/bootstrap_init.py`, `harness.log` 변경
- downstream 프로젝트에서 복사해 간 overlay 문서를 수정하는 일은 프로젝트 문서 변경이지 `harness-kit` 유지보수가 아니다.
- 반대로 이 저장소의 overlay template를 수정해 모든 프로젝트의 기본값을 바꾸는 일은 `harness-kit` 유지보수다.

## 문서 집합 경계

- 프로젝트 영향 문서: `downstream/docs/harness_guide.md`, `downstream/docs/harness/common/*`, `downstream/docs/phase_*`, `bootstrap/docs/project_overlay/*`, `downstream/docs/standard/coding_guidelines_core.md`, `downstream/docs/templates/task/*`, `downstream/docs/examples/*`, `bootstrap/*`, `bootstrap/scripts/bootstrap_init.py`
- maintainer 전용 문서: `maintainer/docs/*`, `maintainer/scripts/*`, `harness.log`, `.github/workflows/harness-doc-guard.yml`
- maintainer 전용 지침을 수정하는 작업은 maintainer 전용 문서 집합 안에서만 끝나야 한다.
- 예외: 모든 감사에 공통으로 적용할 audit 운영 규칙을 바꾸는 경우 `downstream/docs/harness/common/audit_policy.md`를 함께 수정할 수 있다. 이때도 maintainer 전용 경로, `harness.log` 규칙, drift 대응 절차는 프로젝트 영향 문서 본문으로 복제하지 않는다.
- 프로젝트 영향 문서와 overlay template를 수정하는 작업은 프로젝트 영향 문서 집합 안에서만 끝나야 하며, maintainer 전용 문서는 `harness.log` 기록 외에는 함께 수정하지 않는다.
- `README.md`는 저장소 진입 문서라 project-facing 안내와 maintainer 안내가 함께 존재할 수 있으므로, maintainer 전용 경로 substring 자동 누수 검사는 기본적으로 `README.md`를 제외하고 whole-harness 수동 감사로 확인한다.

## 감사 실행 원칙

- maintainer가 GitHub issue를 해결하기 위해 `harness-kit` core를 수정할 때는 issue마다 전용 브랜치를 따로 잡아 진행한다.
- 이 규칙은 maintainer의 issue 기반 core 작업에서 일반 task 브랜치 권장 형식인 `{task_id}_{task_name}`보다 우선한다.
- issue 기반 maintainer 브랜치 이름은 `{issue_num}_{title}` 형식을 사용한다.
- `issue_num`은 숫자 issue 번호만 사용하고, `title`은 issue 제목을 branch-safe 문자열로 정리해 사용한다.
- 공백은 `_`로 치환하고, 브랜치 구분을 깨는 문자는 제거하거나 같은 수준의 안전한 문자로 치환한다.
- 하나의 issue 해결에 사용한 maintainer 브랜치를 다른 issue 작업에 재사용하지 않는다.
- maintainer 감사에서는 현재 작업 브랜치가 대상 issue의 `{issue_num}_{title}` 형식을 따르는지와, 작업이 기본 브랜치가 아니라 issue 전용 브랜치에서 진행 중인지 확인한다.
- 브랜치 생성 시점이나 과거 재사용 이력은 자동 또는 저장소 상태만으로 완전 검증하기 어려우므로, 이 둘은 maintainer 운영 원칙으로 관리한다.
- core 의미 변경이 있으면 구현 주체와 분리된 subagent audit를 수행한다.
- GitHub issue 기반 maintainer 작업이면, changed-parts / whole-harness와 별도로 최소 한 번은 subagent가 issue 본문과 acceptance criteria를 현재 diff, 테스트, 실패/성공 동작과 직접 대조해 구현 누락이나 범위 이탈이 없는지 확인한다.
- 위 issue 대조 점검은 findings가 없더라도 "누락 없음" 또는 남은 testing gap을 명시적으로 남긴다.
- audit는 반드시 `changed-parts`와 `whole-harness`로 분리해 수행한다.
- `changed-parts`와 `whole-harness`는 각각 독립된 subagent 세션으로 수행하고 self-audit만으로 대체하지 않는다.
- 최종 판정은 두 audit가 모두 승인 가능일 때만 승인 가능으로 본다.
- 새 운영 경계, 승인 기준, 배포 단위, validator 판정 규칙처럼 이후 maintainer audit의 판정 기준 자체를 바꿀 수 있는 변경이라면, 이번 작업에서 기존 audit 체크포인트 보강이 필요한지도 명시적으로 판단한다.
- audit 체크포인트 보강이 필요하면 같은 작업에서 `maintainer/docs/audit_policy.md`를 함께 갱신하는 것을 기본으로 하고, 범위를 분리해야 하면 follow-up issue와 분리 이유를 남긴다.

## Changed-Parts 감사 기준

changed-parts는 바뀐 파일과 인접 영향만 본다.

### 1) 기록 및 추적성

- `harness.log` 필수 항목(`변경`, `이유`, `audit`, `audit-summary`)이 같은 변경에서 함께 기록되었는가
- `이유`가 단순 기능 설명이 아니라 운영 리스크 감소 또는 운영 효율 개선 근거를 포함하는가
- 2026-04-03 이후 신규 항목은 `audit-summary` 형식을 준수하는가

### 2) 로컬 일관성

- 변경 의도와 실제 수정 내용이 일치하는가
- GitHub issue 기반 작업이면 issue 본문/acceptance criteria의 요구와 현재 수정/테스트가 일치하고, 남은 gap이 명시적으로 분류되었는가
- 인접 참조 경로, 문서명, 섹션명이 깨지지 않았는가
- template 변경 시 관련 phase 또는 guide 문서의 인접 영향이 반영되었는가
- "적절히", "충분히"처럼 해석 여지가 큰 표현은 가능한 한 조건문 또는 명시 기준으로 바꿨는가
- "직접 관련 있는", "과도한", "단순한", "충분한"처럼 판단 편차가 큰 표현을 새로 도입했다면, 체크 질문, 승인 불가 예시, 긍정 예시, 결정 규칙 중 하나 이상으로 해석 범위를 좁혔는가
- 같은 규칙이 불필요하게 중복 추가되지 않았는가
- 기존 규칙 의미를 우연히 뒤집거나 약화하지 않았는가
- 현재 판단의 source-of-truth가 repo-local 문서/스크립트/설정인지, repo에 없는 결정을 추측으로 메우지 않았는지 기록상 확인 가능한가
- maintainer 전용 지침 변경인데 프로젝트 영향 문서 본문에 maintainer 전용 경로, `harness.log` 규칙, drift 대응 절차가 추가되지 않았는가
- 프로젝트 영향 문서 변경인데 `harness.log` 외의 maintainer 전용 문서 수정이 불필요하게 섞이지 않았는가
- downstream bundle 포함/제외 경계를 바꾸는 변경이라면 `maintainer/docs/downstream_bundle_boundary.md`, 인접 project-facing 문서, 관련 release 문서가 같은 경계를 가리키는가
- downstream bundle에 포함될 자산이 배포 후 존재하지 않을 maintainer 전용 문서를 canonical reference로 요구하지 않는가
- downstream canonical path rename 또는 migration 경로를 바꾸는 변경이라면 legacy-only 상태, stale coexistence 상태, canonical target 상태를 dry-run, write 경로, validator, project-facing 문서가 같은 계약으로 설명하는가
- 새 project-facing migration flag 또는 upgrade 자동화 경로를 추가했다면 source-tree unit test만이 아니라 vendored downstream bundle smoke까지 같은 경로를 실제로 검증하는가

## Whole-Harness 감사 기준

whole-harness는 전체 문서 흐름과 core 일관성을 본다.

### 1) 아키텍처 및 경계 검사

- `README.md`, `downstream/docs/harness_guide.md`, downstream `docs/project_entrypoint.md` 설명, phase-local 문서 사이에 충돌이 없는가
- core와 project overlay의 책임 경계가 흐려지지 않았는가
- repo source-of-truth 자산, downstream bundle 자산, maintainer 전용 자산의 경계가 서로 충돌하지 않는가
- maintainer 전용 규칙이 프로젝트 영향 문서 본문으로 새어 들어가지 않았는가
- 프로젝트 수행 규칙이 maintainer 전용 문서에 불필요하게 복제되지 않았는가
- 현재 작업 범위와 무관한 실제 downstream 프로젝트 폴더 또는 로컬 문서 변경이 섞이지 않았는가
- 특정 기술 스택 종속 규칙을 core로 끌어오지 않았는가(How보다 What/Criterion 중심)
- 기존 프로젝트의 overlay를 대규모 재작성해야 하는 breaking 성격 변경인지 확인했는가
- Phase 게이트(implementation -> audit -> 사용자 승인 -> 다음 phase)와 충돌하지 않는가

### 2) 인지 부하 및 수행 비용

- 필수 재참조 문서 수가 늘어났다면 불필요 규칙 삭제/통합 또는 증가 근거를 기록했는가
- 문서 길이 증가와 규칙 중복이 하네스 수행 누락 위험을 키우지 않는가
- 기존 core 내에 동일/유사 규칙이 이미 있는지 중복 검사를 수행했는가
- 새 감사 단계나 산출물 추가로 태스크 리드 타임이 10% 이상 증가할 우려가 있으면 근거와 승인 사유를 남겼는가

### 3) 실무 정합성

- 규칙 변경으로 sample task 기대 산출물 또는 수행 방식이 바뀌면 `downstream/docs/examples/` 아래 관련 예시를 함께 현행화했는가
- subagent/제3자가 같은 규칙으로 유사한 감사 결론을 낼 수 있을 만큼 기준이 객관적인가
- `downstream/docs/standard/coding_guidelines_core.md`의 공통 품질 기준과 project convention 참조 구조가 phase 문서, template, example, bootstrap 자산 전반에서 같은 방식으로 유지되는가
- 여러 구현 에이전트가 같은 입력으로 작업해도 동일한 필수 재참조 문서, 체크리스트, 감사 게이트를 따라 유사한 품질 결론에 수렴할 수 있게 기준이 재현 가능한가
- 같은 입력에서 서로 다른 session이 기억이나 외부 관행보다 repo-local 근거를 먼저 보게 만드는 운영 원칙이 충분히 명시적인가
- 새 지침이나 정책이 너무 넓거나 모호해서 서로 다른 session이 같은 입력을 보고 다른 결론에 도달할 위험이 있는지 직접 점검했는가
- 편차 위험이 있다면 yes/no 질문, 명시적 판정 단위, 승인 불가 예시, 긍정 예시, sample artifact 중 하나 이상으로 해석 범위를 좁혔는가
- bundle generation, bundle validation, release 절차, upgrade 판단이 생기거나 바뀌면 ad hoc 목록이 아니라 같은 boundary source-of-truth에 묶여 있는가
- downstream migration automation이나 rename migration을 지원한다고 project-facing 문서에 적었다면, generated bundle consumer 경로에서도 같은 계약이 재현되는지 확인했는가
- 이번 변경이 기존 changed-parts/whole-harness 체크포인트만으로 충분히 통제되는지 판단했고, 부족하면 audit policy 또는 후속 issue에 보강 근거를 남겼는가
- 새 규칙이나 템플릿이 책임 혼합, 과도한 추상화, 테스트 없는 핵심 변경, 원시 외부 에러 유입 같은 금지 패턴을 사실상 새 기본값으로 만들지 않는가
- 코드 생성 품질 목표가 단기 작성 편의보다 장기 유지보수성, 책임 분리, 변경 용이성, 안전한 확장 가능성을 높이는 방향으로 유지되는가
- 새 규칙이나 템플릿이 convention, 품질 기준, 구조 패턴 drift를 키워 프로젝트별 산출물 품질 편차를 늘리지 않는가
- 경량 태스크 예외 원칙과 충돌하지 않는가
- 필수/조건부 재참조 문서 목록이 상위-하위 문서 간에 모순되지 않는가

## 승인 불가 기준

아래 중 하나라도 해당하면 승인 불가다.

- 상위 문서와 하위 문서가 같은 규칙에 대해 상충 지시를 함
- core/overlay 책임 경계가 바뀌었는데 의도와 근거가 없음
- maintainer 전용 경로, `harness.log` 규칙, drift 대응 절차가 프로젝트 영향 문서 본문에 추가됨
- 프로젝트 영향 문서 변경과 무관한 maintainer 전용 문서 수정이 `harness.log` 외에 섞임
- 공통 품질 기준(`downstream/docs/standard/coding_guidelines_core.md`) 또는 project convention 참조 구조가 phase 문서, template, example, bootstrap 자산 사이에서 불일치함
- 규칙 변경으로 여러 에이전트가 따라야 할 필수 재참조 문서, 체크리스트, 감사 게이트가 달라져 산출물 품질 편차가 커질 가능성이 높은데 완화 기준이나 근거가 없음
- 새 지침이 넓거나 모호해 서로 다른 session/agent가 같은 입력으로도 다른 판정에 도달할 가능성이 높은데, 해석 범위를 좁히는 질문/예시/결정 규칙이 없음
- 책임 혼합, 과도한 추상화, 테스트 없는 핵심 변경, 원시 외부 에러 유입 같은 금지 패턴을 새 기본값처럼 허용하거나 묵인함
- 규칙 변경이 장기 유지보수성보다 단기 작성 편의만 강화해 책임 분리, 변경 용이성, 안전한 확장 가능성을 약화함
- convention, 품질 기준, 구조 패턴 drift를 키워 프로젝트별 결과 품질 일관성을 해칠 가능성이 높은데 보완이 없음
- Phase 게이트를 우회하거나 약화하는 문구가 추가됨
- 필수 재참조 경로가 불일치하거나 깨짐
- `harness.log`에 `변경`, `이유`, `audit`, `audit-summary` 중 하나라도 누락됨
- 새 운영 경계나 판정 규칙이 추가됐는데, 이번 변경으로 기존 audit 체크포인트가 부족해졌는지 판단하지 않았고 보강 근거도 없음

## Subagent 판정 기준

- P1 (Critical): changed-parts 또는 whole-harness 체크포인트 중 하나라도 실패하면 승인 불가이며 로그를 완료 상태로 확정하지 않는다.
- P2 (Major): 운영 효율 저하 우려(예: 필수 문서 수 증가, 리드 타임 10%+ 증가 가능성)가 있으면 maintainer 승인 이유를 `harness.log`에 명시한다.

## 감사 결과 형식

- verdict: APPROVE / REJECT
- findings: 핵심 근거 bullet
- risks: none / low / medium / high + 한 줄 근거
- suggested fix: REJECT일 때만 제시

## 기록 규칙

- maintainer는 같은 작업에서 `harness.log`를 갱신한다.
- `harness.log` 항목에는 `변경`, `이유`, `audit`, `audit-summary`를 포함한다.
- `audit-summary` 필수 규칙은 2026-04-03 이후 신규 항목부터 적용한다.

## 자동검사 실패 대응

- Harness Doc Guard CI가 실패하면 `maintainer/docs/drift_response_guide.md` 순서로 보완한다.

## 릴리스 절차

- 버전 릴리스 준비와 tag / GitHub Release 생성 순서는 `maintainer/docs/release_process.md`를 따른다.

## 자동검사 실행 기준

- 기본 검사 스크립트는 `maintainer/scripts/check_harness_docs.py`를 사용한다.
- 기본 워크플로우는 `.github/workflows/harness-doc-guard.yml`을 사용한다.
- downsteam 프로젝트는 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 복사해 재사용 워크플로우를 호출한다.
