# Requirements

## 기능 요구사항

- core 운영 문서는 repo-local source-of-truth 원칙을 명시적으로 선언해야 한다.
- 원칙은 repo 내부 근거 우선, 기억/외부 대화/다른 프로젝트 관행의 비우선, 누락된 결정의 추측 금지, project overlay 또는 관련 문서로의 handoff를 포함해야 한다.
- task 기록 규칙은 구현 중 판단과 검증에서 어떤 repo-local 근거를 봤는지 또는 어떤 결정이 repo에 없어 문서화 대상으로 남는지 기록할 수 있게 해야 한다.
- maintainer 감사 규칙은 source-of-truth 원칙 위반 여부를 changed-parts / whole-harness 관점에서 확인할 수 있어야 한다.
- 자동 doc guard는 핵심 문서에서 source-of-truth 원칙 설명 drift를 다시 잡을 수 있어야 한다.

## 비기능 요구사항 또는 품질 요구사항

- 기존 core/overlay 책임 경계는 유지해야 한다.
- 새로운 원칙은 모호한 선언보다 실제 체크 가능한 문구와 기록 위치를 제공해야 한다.
- 변경은 core guide, 공통 policy, task template, 관련 concept doc, doc guard 범위의 최소 수정이어야 한다.

## 입력/출력

- 입력:
  - `README.md`
  - `docs/harness_guide.md`
  - `bootstrap/docs/how_harness_kit_works.md`
  - `docs/harness/common/process_policy.md`
  - `docs/harness/common/artifact_policy.md`
  - `docs/harness/common/audit_policy.md`
  - `docs/templates/task/implementation_notes.md`
  - `docs/templates/task/validation_report.md`
  - 필요 시 sample/example 문서와 `scripts/check_harness_docs.py`
- 출력:
  - repo-local source-of-truth 원칙이 선언된 core 운영 문서
  - 해당 원칙을 기록/감사 가능한 task template와 policy
  - 원칙 drift를 감시하는 doc guard

## 제약사항

- repo-local source-of-truth를 이유로 project overlay 없이 core만으로 project-specific 결정을 대신 확정하면 안 된다.
- 기억/외부 정보 보조 사용을 전면 금지하지는 않되, repo 근거보다 우선하지 못한다는 선은 분명해야 한다.
- repo에 없는 결정은 추측으로 채우지 않고 문서화 또는 사용자 승인 대상으로 연결해야 한다.

## 예외 상황

- repo에 관련 문서가 전혀 없을 수는 있다. 이 경우는 추측으로 메우지 않고 `implementation_notes.md`, `validation_report.md`, 또는 project overlay / decisions 문서 반영 대상으로 남겨야 한다.
- 여러 repo-local 문서가 충돌하면 더 상위/구체적인 문서를 따르고, 그래도 해소되지 않으면 사용자 승인 전에는 예외 적용을 하면 안 된다.
- 외부 시스템이나 다른 프로젝트 관행을 참고할 수는 있지만, 현재 repo 근거와 다르면 repo 기준이 우선이다.

## 성공 기준

- repo-local 근거 우선 원칙이 명시적으로 선언된다.
- 누락된 결정은 추측이 아니라 문서화/승인/overlay handoff 대상으로 처리하는 기준이 생긴다.
- 감사자와 작업자가 같은 문구를 기준으로 위반 여부를 설명할 수 있다.
