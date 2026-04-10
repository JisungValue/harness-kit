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
- 사람이 읽는 overlay 완료 기준은 `docs/project_overlay/overlay_completion_checklist.md`를 보고, sample validation 예시는 `docs/examples/bootstrap-first-success/overlay_completion_validation_report.md`를 본다.

## 필수 문서

- `docs/harness_guide.md`
- `docs/standard/architecture.md`
- `docs/standard/implementation_order.md`
- `docs/standard/coding_conventions_project.md`
- `docs/standard/quality_gate_profile.md`
- `docs/standard/testing_profile.md`
- `docs/standard/commit_rule.md`

## 역할 분리

- `docs/harness_guide.md`
  - 프로젝트 로컬 진입점이다.
  - 공통 kit 문서와 프로젝트 전용 문서를 함께 연결하는 index 역할만 한다.
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

## 권장 로컬 `docs/harness_guide.md`

```md
# Project Harness Guide

## 공통 규칙

- `vendor/harness-kit/docs/harness_guide.md`

## 프로젝트 전용 규칙

- `docs/standard/architecture.md`
- `docs/standard/implementation_order.md`
- `docs/standard/coding_conventions_project.md`
- `docs/standard/quality_gate_profile.md`
- `docs/standard/testing_profile.md`
- `docs/standard/commit_rule.md`
```

## 권장 CI 템플릿

- `docs/project_overlay/harness_doc_guard_workflow_template.yml`
  - 프로젝트 `.github/workflows/`로 복사해 harness-kit 문서 정합성 검사를 자동 실행한다.
  - 템플릿의 `@<pin-tag-or-sha>`를 릴리스 태그 또는 고정 커밋 SHA로 치환해 재현 가능성을 유지한다.

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
