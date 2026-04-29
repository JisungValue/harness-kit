# Version And Support Scope

이 문서는 `harness-kit`의 현재 릴리스 버전과 지원 범위를 한 곳에서 관리하는 canonical 문서다.

## 현재 최신 릴리스

- 현재 최신 GitHub Release: `v0.2.1`
- release URL: `https://github.com/JisungValue/harness-kit/releases/tag/v0.2.1`

## 현재 지원 범위

- 새 프로젝트에 최소 overlay 문서 세트를 생성한다.
- first-success 경로를 로컬에서 재현한다.
- unresolved decision validation을 수행한다.
- cross-document consistency validation을 수행한다.
- 기존 프로젝트 상태를 read-only adopt dry-run으로 읽고 baseline과 비교한다.
- 기존 프로젝트에서 missing file create, unchanged refresh, explicit overwrite 중심의 selective safe write/update를 수행한다.
- task 수행 중 변경이 생기면 가장 이른 영향 Phase부터 self-healing / stale invalidation 규칙으로 재수행한다.
- task-local `phase_status.md`와 `validate_phase_gate.py`로 현재 gate와 write-set 위반을 점검한다.
- downstream bundle impact classification을 수행한다.
- consumer-facing downstream upgrade guide를 따라 bundle upgrade를 검토한다.
- human diff review checklist로 bundle upgrade 차이를 검토한다.
- maintainer는 downstream bundle generation, validation, smoke test를 release-prep 절차에 포함할 수 있다.

## 현재 아직 지원하지 않는 범위

- automatic merge-based adopt update
- semantic merge/adoption
- 프로젝트 맞춤 변경의 automatic correctness 판정
- interactive TUI
- repo-aware assisted adoption

## 0.2.1에서 추가된 핵심 범위

- runtime self-healing, stale invalidation, write-set lock 규칙 명시
- task-local `phase_status.md` runtime state file 추가
- `scripts/validate_phase_gate.py` hard-stop validator 추가
- quickstart 중심 onboarding 단순화와 doc guard 결합 완화

## 0.2.0에서 추가된 핵심 범위

- downstream bundle boundary 정의
- downstream bundle generation / validation command
- generated bundle smoke validation
- downstream bundle impact classification
- consumer-facing downstream upgrade guide
- downstream overlay diff review checklist
- 산출물 변경 시 가장 이른 영향 Phase부터 재수행하는 공통 규칙

## 읽는 방법

- `README.md`에서 현재 지원 범위가 궁금하면 이 문서를 본다.
- `bootstrap/docs/quickstart.md`, `bootstrap/docs/how_harness_kit_works.md`, `bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md`는 버전 고정 설명 대신 이 문서를 기준으로 현재 범위를 해석한다.
- maintainer release note와 release gate도 이 문서의 `현재 지원 범위`, `현재 아직 지원하지 않는 범위`와 어긋나지 않아야 한다.
