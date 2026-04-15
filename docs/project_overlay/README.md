# Project Overlay Guide

공통 Harness Kit를 가져온 프로젝트는 core를 그대로 재사용하고, 아래 문서만 프로젝트 전용으로 유지한다.

## 첫 도입 가이드

- 새 프로젝트 또는 거의 빈 프로젝트에서 first success를 빠르게 재현하려면 `docs/project_overlay/first_success_guide.md`를 먼저 본다.
- init CLI를 쓰든 수동 복사를 쓰든, 이 가이드의 최소 문서 세트와 성공 상태를 기준으로 맞춘다.
- 로컬에서 어떤 명령을 먼저 돌리고 dry-run 출력을 어떻게 읽을지는 `docs/project_overlay/local_diagnostics_and_dry_run.md`를 본다.

## Overlay Validator

- unresolved placeholder 검증 규칙과 실행 명령은 `docs/project_overlay/unresolved_decision_validator.md`를 본다.
- 같은 프로젝트라도 `first-success`와 `phase2` readiness에서 허용되는 미결정 범위가 다르다.
- 문서 간 교차 정합성 검사는 `docs/project_overlay/cross_document_consistency_checker.md`를 본다.
- 기존 프로젝트 상태를 bootstrap 기준과 비교하는 read-only adopt 흐름은 `docs/project_overlay/adopt_dry_run.md`를 본다.
- 기존 프로젝트에서 missing file create와 explicit path overwrite만 허용하는 제한적 write 흐름은 `docs/project_overlay/adopt_safe_write.md`를 본다.
- 새 harness bundle 변경을 얼마나 조심해서 반영해야 하는지 분류하는 기준은 `docs/project_overlay/harness_upgrade_impact_policy.md`를 본다.
- 새 harness bundle 변경을 실제로 어떤 순서와 기준으로 검토하고 반영할지는 `docs/project_overlay/downstream_harness_upgrade_guide.md`를 본다.
- 새 harness bundle과 현재 overlay 사이의 사람 중심 diff review 항목은 `docs/project_overlay/downstream_overlay_diff_review_checklist.md`를 본다.
- 사람이 읽는 overlay 완료 기준은 `docs/project_overlay/overlay_completion_checklist.md`를 보고, sample validation 예시는 `docs/examples/bootstrap-first-success/overlay_completion_validation_report.md`를 본다.

## 필수 문서

- `docs/project_entrypoint.md`
- `docs/decisions/README.md`
- `docs/standard/architecture.md`
- `docs/standard/implementation_order.md`
- `docs/standard/coding_conventions_project.md`
- `docs/standard/quality_gate_profile.md`
- `docs/standard/testing_profile.md`
- `docs/standard/commit_rule.md`

## Runtime Instruction Entrypoints

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`

## 권장 읽기 순서

- 이 문서는 source repo 안의 project overlay template guide다.
- 이 저장소에서는 먼저 `docs/project_overlay/first_success_guide.md`, `docs/project_overlay/local_diagnostics_and_dry_run.md`, `docs/how_harness_kit_works.md`를 본다.
- 아래 순서는 downstream 프로젝트를 bootstrap한 뒤 생성되는 문서 기준이다.
- 아래 vendored 경로 예시는 `vendor/harness-kit/` 기준이며, 다른 경로를 쓰면 같은 실제 경로로 읽는다.

- runtime 시작점: `AGENTS.md`
- project-local 문서 entrypoint: `docs/project_entrypoint.md`
- project decision index: `docs/decisions/README.md`
- reusable core guide: `<vendored-path>/docs/harness_guide.md`
- project-specific supporting docs: `docs/standard/*`
- `AGENTS.md`를 열었으면 `docs/project_entrypoint.md`에서 멈추지 말고, 그 문서가 가리키는 core guide와 supporting docs까지 순서대로 모두 읽고 적용한다.
- 현재 작업이 중요한 정책/예외/책임 위치를 다루면 `docs/decisions/README.md`에서 관련 decision 문서를 추가로 읽고 적용한다.

## source repo와 downstream 구분

- source repo에는 root `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `docs/project_entrypoint.md`, `docs/decisions/README.md`가 아직 없다.
- 이 파일들은 downstream 프로젝트를 bootstrap하거나 template를 수동 복사한 뒤에 생성되는 consumer-local 문서다.
- 따라서 source repo에서 문서를 읽는 단계에서는 `docs/project_overlay/*.md` 가이드와 template를 먼저 보고, downstream 프로젝트에서는 생성된 runtime entrypoint와 project entrypoint를 따른다.

## 역할 분리

- `vendor/harness-kit/docs/harness_guide.md`
  - vendored reusable core guide다.
  - 프로젝트 로컬 entrypoint가 먼저 이 core guide를 참조하고, 실제 프로젝트 차이는 `docs/standard/*`에서 덧붙인다.
- `docs/project_entrypoint.md`
  - 프로젝트 로컬 문서 entrypoint다.
  - vendored core guide와 프로젝트 전용 `docs/standard/*`를 함께 연결하는 index 역할만 한다.
  - runtime이나 작업자는 이 문서에 적힌 공통 규칙과 프로젝트 전용 규칙 문서를 함께 읽고 적용해야 한다.
- `docs/decisions/README.md`
  - 중요한 프로젝트 결정 문서의 index다.
  - `architecture.md`와 별도로 장기 유지되는 정책, 예외 처리 규칙, 책임 배치 결정을 찾는 진입점이다.
- `AGENTS.md`
  - agent runtime이 공통으로 먼저 읽는 canonical instruction entrypoint다.
  - 실제 규칙은 `docs/project_entrypoint.md`로 연결하고, adapter별 파일은 이 파일만 다시 가리킨다.
  - linked document chain을 끝까지 읽고 적용해야 한다는 traversal contract를 함께 둔다.
- `CLAUDE.md`, `GEMINI.md`
  - agent별 기본 파일명 차이를 흡수하는 얇은 adapter entrypoint다.
  - 규칙 본문을 중복 복사하지 않고 `AGENTS.md`로 수렴시킨다.
- `docs/standard/architecture.md`
  - 실제 레이어 구조, 모듈 경계, 주요 의존성 방향을 정의한다.
- `docs/standard/implementation_order.md`
  - Phase 2에서 사용할 프로젝트별 레이어 진행 순서와 세분화 기준을 정의한다.
  - `architecture.md`의 실제 구조와 의존성 방향을 기준으로 작성한다.
- `docs/standard/coding_conventions_project.md`
  - 프레임워크 특화 규칙, DTO postfix, 프로젝트 전용 네이밍, 트랜잭션 관례처럼 core에 두기 어려운 convention을 둔다.
  - 언어별 convention 초안이 필요하면 `bootstrap/language_conventions/`에서 해당 언어 템플릿을 골라 수동 복사 또는 병합해 시작한다.
- `docs/standard/quality_gate_profile.md`
  - formatter, linter, type checker, test, 조건부 architecture rule 같은 품질 게이트 실행 명령과 실패 기준을 정의한다.
  - 각 게이트의 필수 여부, 실행 시점, 실패 시 처리 기준을 한곳에 둔다.
- `docs/standard/testing_profile.md`
  - 테스트 환경 준비, coverage 기준, 통합 테스트 대상, 외부 의존성 기동 방식 같은 테스트 세부 기준을 정의한다.
  - 테스트 실행 명령 자체와 게이트 강제 여부는 `docs/standard/quality_gate_profile.md`에서 정의한다.
- `docs/standard/commit_rule.md`
  - 커밋 품질 최소 규칙과 원자성 운영 기준을 정의한다.
  - 알려진 compile, type, build, test 실패 상태 커밋 금지와 깨지지 않는 상태 우선 원칙을 둔다.
  - 기본 커밋 메시지 형식(`type(scope): subject`), 제목 50자 제한, 제목 동사 시작 규칙을 기본안으로 제공한다.
  - 템플릿의 `[팀 결정 필요]` 항목을 프로젝트 정책으로 확정해 사용한다.

## 권장 로컬 `docs/project_entrypoint.md`

아래 예시의 `vendor/harness-kit/`도 non-default vendoring이면 같은 실제 경로로 바꿔 쓴다.

```md
# Project Harness Entry Point

## 문서 역할

- agent runtime은 `AGENTS.md`에서 이 파일로 들어온다.
- 사람은 이 파일에서 vendored core guide와 프로젝트 전용 overlay 문서를 함께 찾는다.

## 실행 계약

- 이 문서에 들어온 runtime 또는 작업자는 `공통 규칙`, `프로젝트 전용 규칙`에 적힌 문서를 순서대로 모두 읽고 적용한 뒤에만 구현 또는 판단을 진행한다.
- vendored core guide는 공통 규칙 기준을 주고, `docs/standard/*` 문서는 프로젝트 전용 기준을 주므로 둘 중 하나만 읽고 멈추지 않는다.

## 공통 규칙

- `vendor/harness-kit/docs/harness_guide.md`

## 프로젝트 전용 규칙

- `docs/standard/architecture.md`
- `docs/standard/implementation_order.md`
- `docs/standard/coding_conventions_project.md`
- `docs/standard/quality_gate_profile.md`
- `docs/standard/testing_profile.md`
- `docs/standard/commit_rule.md`

## 프로젝트 결정 문서

- `docs/decisions/README.md`

- 현재 작업이 중요한 정책, 예외 처리 규칙, 책임 배치, 운영 결정을 건드리면 이 문서에서 관련 decision을 찾아 함께 읽고 갱신한다.
```

## 권장 CI 템플릿

- `docs/project_overlay/harness_doc_guard_workflow_template.yml`
  - 프로젝트 `.github/workflows/`로 복사해 harness-kit 문서 정합성 검사를 자동 실행한다.
  - 템플릿의 `@<pin-tag-or-sha>`를 릴리스 태그 또는 고정 커밋 SHA로 치환해 재현 가능성을 유지한다.

## 권장 runtime entrypoint

```md
# Agent Runtime Entry Point

## 우선 읽을 문서

- `docs/project_entrypoint.md`

## 실행 계약

- 이 파일에 연결된 문서는 순서대로 모두 읽고 적용한 뒤에만 다음 작업으로 넘어간다.
- `docs/project_entrypoint.md`를 열었으면 그 문서의 `공통 규칙`, `프로젝트 전용 규칙`에 연결된 문서까지 끝까지 이어서 읽고 적용한다.
- 링크만 확인하고 중간 문서에서 멈추지 않는다.
```

## 언어별 Convention Bootstrap

- `bootstrap/language_conventions/`
  - Python, Java, Kotlin 같은 언어별 convention 초안을 둔다.
  - 실제 프로젝트에 적용할 때는 필요한 언어 파일만 골라 `docs/standard/coding_conventions_project.md`에 병합하거나, 별도 언어 문서로 복사한 뒤 프로젝트 문서에서 참조한다.
  - bootstrap 자산은 편의를 위한 시작점이며, 프로젝트에 복사한 뒤에는 팀 규칙에 맞게 현지화한다.

## 작성 원칙

- project overlay는 core를 다시 설명하지 않는다.
- project overlay 템플릿은 프로젝트에 반드시 있어야 할 문서 골격을 정의한다.
- 언어별 convention이 필요할 때만 `bootstrap/` 자산을 선택해 project overlay 문서 안으로 복사 또는 병합한다.
- `bootstrap/`은 선택적 시작 자산이고, `docs/project_overlay/`는 프로젝트 문서의 기본 골격이다.
- 여러 프로젝트에서 반복되는 규칙은 overlay가 아니라 core로 승격한다.
- 특정 프로젝트에만 필요한 규칙만 overlay에 남긴다.

## decisions 구조

- `docs/project_overlay/decisions_index_template.md`
  - downstream 프로젝트의 `docs/decisions/README.md`로 생성하는 기본 index template다.
- `docs/project_overlay/decision_record_template.md`
  - 필요한 경우 `DEC-###-slug.md`로 복사해 쓰는 decision record template다.
- canonical example은 `docs/examples/project-decisions/DEC-001-authorization-validation-location.md`를 본다.
