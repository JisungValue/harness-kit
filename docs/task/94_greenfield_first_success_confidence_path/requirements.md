# Requirements

## 기능 요구사항

- first-success 경로는 bootstrap 직후 어떤 신호가 순서대로 확보되어야 하는지 문서와 예시에서 같은 단계 모델로 설명해야 한다.
- `bootstrap_init.py`는 non-default vendored path를 사용하는 greenfield 프로젝트에서도 bootstrap 산출물의 vendored reference를 직접 현지화할 수 있어야 한다.
- generated `docs/project_entrypoint.md`와 `docs/standard/coding_conventions_project.md`는 선택한 vendored path와 언어 bootstrap 기준 문서를 일관되게 반영해야 한다.
- downstream bundle은 project-facing CI/doc-guard onboarding 자산을 실제로 포함해야 하며, bundle smoke 또는 focused test가 그 경로를 다시 잡아야 한다.
- greenfield guide, quickstart, local diagnostics, bundle smoke maintainer 문서는 같은 confidence path와 남은 수동 확인 대상을 설명해야 한다.

## 비기능 요구사항 또는 품질 요구사항

- 기본 `vendor/harness-kit` 경로는 회귀 없이 계속 동작해야 한다.
- multi-language bootstrap support(`python`, `java`, `kotlin`)는 유지해야 한다.
- 변경은 bootstrap CLI, downstream bundle, focused tests, doc guard 범위에서 끝나는 최소 수정이어야 한다.

## 입력/출력

- 입력:
  - `scripts/bootstrap_init.py`
  - `docs/project_overlay/first_success_guide.md`
  - `bootstrap/docs/quickstart.md`
  - `docs/project_overlay/local_diagnostics_and_dry_run.md`
  - `docs/examples/bootstrap-first-success/validation_report.md`
  - `maintainer/docs/downstream_bundle_boundary.md`
  - `maintainer/docs/downstream_bundle_smoke_validation.md`
  - 관련 bundle/bootstrap/consistency/doc-guard 테스트
- 출력:
  - localized vendoring을 직접 지원하는 bootstrap CLI
  - greenfield confidence path를 같은 단계 모델로 설명하는 문서/예시
  - CI/doc-guard onboarding 자산이 포함된 downstream bundle과 이를 고정하는 테스트

## 제약사항

- consumer-local `docs/project_entrypoint.md`, `docs/decisions/README.md` 생성 계약은 유지한다.
- CI/doc-guard onboarding은 consumer project가 복사/핀 고정하는 템플릿 수준으로 유지하고, 원격 workflow 자체를 bundle에 중복 포함하지 않는다.
- non-default vendoring 지원은 bootstrap 시점 현지화까지만 다루고, arbitrary path rewrite 도구 전체 추가로 확대하지 않는다.

## 예외 상황

- non-default vendoring path가 절대경로이거나 project-root 상대 경로로 쓸 수 없으면 CLI에서 fail-fast 해야 한다.
- bundle boundary가 project-facing workflow template를 포함하지 않으면 docs와 shipped surface가 다시 어긋난다.
- 문서만 `--vendor-path`를 언급하고 테스트가 없으면 drift가 재발한다.

## 성공 기준

- greenfield 사용자가 bootstrap 출력, first-success helper, readiness validator, consistency validator, CI/doc-guard onboarding이 각각 무엇을 보장하는지 더 명확히 이해할 수 있다.
- `bootstrap_init.py`로 non-default vendored path를 직접 반영한 first-success 경로가 통과한다.
- downstream bundle에 workflow template가 포함되고 관련 test/doc guard/maintainer 문서가 current contract를 고정한다.
