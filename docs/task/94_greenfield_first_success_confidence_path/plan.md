# Plan

## 변경 대상 파일 또는 모듈

- `scripts/bootstrap_init.py`
- `docs/project_overlay/first_success_guide.md`
- `docs/quickstart.md`
- `docs/project_overlay/local_diagnostics_and_dry_run.md`
- `docs/examples/bootstrap-first-success/validation_report.md`
- `maintainer/docs/downstream_bundle_boundary.md`
- `maintainer/docs/downstream_bundle_smoke_validation.md`
- `scripts/check_harness_docs.py`
- `tests/test_bootstrap_init.py`
- `tests/test_bootstrap_e2e.py`
- `tests/test_validate_overlay_consistency.py`
- `tests/test_generate_downstream_bundle.py`
- `tests/test_validate_downstream_bundle.py`
- `tests/test_downstream_bundle_smoke.py`

## 레이어별 작업 계획

- bootstrap CLI에 non-default vendored path를 직접 주입할 수 있는 최소 옵션을 추가하고, generated project entrypoint/coding conventions reference를 같은 source-of-truth로 맞춘다.
- greenfield first-success를 bootstrap output, 최소 문서 세트 존재, unresolved decision readiness, cross-document consistency, CI/doc-guard onboarding의 단계형 confidence path로 재정리한다.
- downstream bundle boundary에 workflow template 같은 project-facing CI onboarding 자산을 실제 포함 대상으로 반영한다.
- bundle generation/validation/smoke test가 workflow template 포함과 localized vendoring path 시나리오를 다시 잡도록 보강한다.
- doc guard가 greenfield 문서 surface의 핵심 문구와 경로를 계속 고정하도록 맞춘다.

## 테스트 계획

- `python3 -m unittest tests.test_bootstrap_init tests.test_bootstrap_e2e tests.test_validate_overlay_consistency`
- `python3 -m unittest tests.test_generate_downstream_bundle tests.test_validate_downstream_bundle tests.test_downstream_bundle_smoke`
- `python3 scripts/check_harness_docs.py`

## 문서 반영 계획

- `docs/project_overlay/first_success_guide.md`, `docs/quickstart.md`, `docs/project_overlay/local_diagnostics_and_dry_run.md`, `docs/examples/bootstrap-first-success/validation_report.md`에 같은 confidence path와 remaining manual checks를 반영한다.
- `maintainer/docs/downstream_bundle_boundary.md`, `maintainer/docs/downstream_bundle_smoke_validation.md`에 workflow-template shipping과 localized vendoring smoke coverage를 반영한다.
- 관련 `docs/decisions/README.md` 또는 `DEC-###-slug.md` 읽기/수정/생성 필요 여부: 해당 없음. 이번 작업은 downstream project-local decision 내용이 아니라 greenfield bootstrap confidence path와 shipped surface 정렬 범위다.
- 새 decision이 필요하면 index 갱신 계획: 해당 없음.

## 비범위

- brownfield incremental validation mode 추가
- workflow generator 또는 installer 전체 추가
- full CI scaffolding 자동 생성

## 리스크 또는 확인 포인트

- `--vendor-path`가 relative path contract를 흐리면 consistency validator와 문서 예시가 다시 어긋날 수 있으므로 project-root 상대 경로만 허용해야 한다.
- workflow template를 bundle에 포함시키되 maintainer 전용 reusable workflow와 혼동되지 않게 boundary 문구를 분명히 해야 한다.
- first-success confidence path를 문서마다 다르게 쓰면 오히려 복잡해지므로 단계 이름과 보장 범위를 재사용해야 한다.
