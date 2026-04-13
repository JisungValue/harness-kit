# Implementation Notes

## 진행 로그

- Phase 1 시작: issue `#94` 기준으로 greenfield first-success confidence gap, non-default vendoring friction, CI/doc-guard onboarding drift를 정리하고 요구사항/계획을 고정함.
- 구현: `bootstrap_init.py`에 `--vendor-path`를 추가해 `docs/project_entrypoint.md`, `docs/standard/coding_conventions_project.md`의 vendored reference를 bootstrap 시점에 직접 현지화하도록 보강함.
- 구현: `--vendor-path`는 project-root relative path만 허용하도록 하고, POSIX absolute path, Windows absolute path, Windows drive-relative path를 fail-fast 하도록 정규화 규칙과 focused test를 추가함.
- 구현: `docs/project_overlay/first_success_guide.md`, `docs/quickstart.md`, `docs/project_overlay/local_diagnostics_and_dry_run.md`, `docs/examples/bootstrap-first-success/validation_report.md`, `README.md`를 bootstrap output -> helper -> readiness/consistency -> workflow-template onboarding의 staged confidence path로 정렬함.
- 구현: downstream bundle boundary에 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 실제 shipped asset으로 반영하고, generated README/manifest/tests/smoke 문서를 함께 정렬함.
- 검증: `python3 -m unittest tests.test_bootstrap_init tests.test_bootstrap_e2e tests.test_validate_overlay_consistency tests.test_generate_downstream_bundle tests.test_validate_downstream_bundle tests.test_downstream_bundle_smoke`, `python3 scripts/check_harness_docs.py`를 통과함.
- 감사: whole-harness audit은 바로 `APPROVE`였고, changed-parts audit은 Windows path validation 공백 때문에 2회 `NEEDS_CHANGES`가 나왔다. 이후 `bootstrap_init.py` 정규화와 focused test를 보강한 뒤 최종 changed-parts audit도 `APPROVE`로 전환됨.

## 경량 검토 기록

- 작은 태스크로 본 근거: 해당 없음
- 경량 적용 승인 여부: 미적용
- 실제 축소한 범위: 해당 없음
- 유지한 테스트: bootstrap CLI, first-success e2e, consistency validator, downstream bundle generation/validation/smoke, doc guard
- 유지한 감사: changed-parts / whole-harness audit 수행 완료
- 전체 흐름 영향 요약: greenfield bootstrap CLI, project-facing docs, bundle boundary, maintainer smoke validation이 함께 영향받는다.
- 남은 리스크: workflow template의 실제 remote GitHub Actions 실행은 문서/asset/placeholder 수준까지만 확인했고, bootstrap 이후 vendored 경로 재이동은 여전히 수동 작업이다.
- Full 전환 조건 또는 승격 조건: 이미 full 흐름으로 진행 중

## 구현 중 결정 사항

- non-default vendoring friction은 별도 rewrite helper를 만들기보다 `bootstrap_init.py --vendor-path`로 bootstrap 시점 현지화를 지원하는 최소 구현으로 해결했다.
- future-session consistency는 maintainer reusable workflow를 bundle에 직접 넣지 않고, project-facing `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 shipped asset으로 포함하는 방식으로 강화했다.
- `--vendor-path`는 project-root relative contract를 흐리지 않도록 absolute/drive path를 모두 거부하는 쪽으로 고정했다.

## 위임된 책임

## 사용자 승인 필요 항목

## 후속 태스크 후보

- `#95 incremental brownfield validation mode`는 이번 greenfield confidence 정리와 별개로, partial adoption intermediate signal을 다루는 다음 단계 후보다.
