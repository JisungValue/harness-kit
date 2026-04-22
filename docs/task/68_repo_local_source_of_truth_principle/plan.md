# Plan

## 변경 대상 파일 또는 모듈

- `README.md`
- `docs/harness_guide.md`
- `bootstrap/docs/how_harness_kit_works.md`
- `docs/harness/common/process_policy.md`
- `docs/harness/common/artifact_policy.md`
- `docs/harness/common/audit_policy.md`
- `docs/templates/task/implementation_notes.md`
- `docs/templates/task/validation_report.md`
- 필요 시 `docs/examples/sample-task/implementation_notes.md`
- 필요 시 `scripts/check_harness_docs.py`

## 레이어별 작업 계획

- README, harness guide, concept doc에 repo-local source-of-truth 원칙을 선언하고 core/overlay 책임 경계와 연결한다.
- process policy와 audit policy에 repo 근거 우선, 충돌 시 처리, 누락 결정의 추측 금지를 운영 규칙과 감사 체크포인트로 반영한다.
- artifact policy와 task 템플릿에 repo-local 근거 및 누락된 결정 handoff를 기록할 위치를 추가한다.
- doc guard가 핵심 문서의 source-of-truth 원칙 drift를 다시 잡도록 필요한 최소 검사를 추가한다.

## 테스트 계획

- `python3 scripts/check_harness_docs.py`

## 문서 반영 계획

- `README.md`, `docs/harness_guide.md`, `bootstrap/docs/how_harness_kit_works.md`, `docs/harness/common/process_policy.md`, `docs/harness/common/artifact_policy.md`, `docs/harness/common/audit_policy.md`에 원칙과 책임 경계를 반영한다.
- `docs/templates/task/implementation_notes.md`, `docs/templates/task/validation_report.md`에 근거 기록 위치를 반영한다.
- 관련 `docs/decisions/README.md` 또는 `DEC-###-slug.md` 읽기/수정/생성 필요 여부: 해당 없음. 이번 작업은 project-local decision 내용이 아니라 core 운영 원칙과 기록 규칙 정렬 범위다.
- 새 decision이 필요하면 index 갱신 계획: 해당 없음.

## 비범위

- 특정 repo의 canonical 문서 목록 강제
- repo-aware adoption 기능 구현
- reproduction 원칙 전체 추가

## 리스크 또는 확인 포인트

- 선언 문구만 늘고 실제 기록/감사 포인트가 없으면 운영 원칙으로 작동하지 않는다.
- repo-local 우선 원칙이 project overlay 책임을 침범하지 않도록, 없는 결정은 overlay/decision 문서로 handoff한다는 문구가 필요하다.
- README와 process/audit/template가 다른 표현을 쓰면 오히려 session별 해석 편차가 커질 수 있다.
