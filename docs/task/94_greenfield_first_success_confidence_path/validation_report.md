# Validation Report

## 실행한 검증

- 검증 항목: bootstrap CLI의 localized vendoring path 지원
  - 대조한 입력물: `scripts/bootstrap_init.py`, `tests/test_bootstrap_init.py`, `tests/test_bootstrap_e2e.py`, `tests/test_validate_overlay_consistency.py`
  - 실행 방법 또는 확인 방식: `python3 -m unittest tests.test_bootstrap_init tests.test_bootstrap_e2e tests.test_validate_overlay_consistency`
  - 결과: `bootstrap_init.py`가 `--vendor-path`로 non-default vendoring을 직접 반영하고, POSIX absolute path, Windows absolute path(`C:\...`), Windows drive-relative path(`C:...`)를 모두 fail-fast로 거부함을 확인했다. localized vendoring bootstrap은 추가 수동 편집 없이 first-success helper와 consistency validator까지 통과했다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: bootstrap 이후 vendored 경로를 다시 옮기는 경우 path update는 여전히 수동 작업이다.

- 검증 항목: first-success confidence path 문서/예시 정렬
  - 대조한 입력물: `docs/project_overlay/first_success_guide.md`, `docs/quickstart.md`, `docs/project_overlay/local_diagnostics_and_dry_run.md`, `docs/examples/bootstrap-first-success/validation_report.md`, `README.md`
  - 실행 방법 또는 확인 방식: 문서 surface를 교차 검토하고 `python3 scripts/check_harness_docs.py`로 `--vendor-path`, workflow template onboarding, bundle smoke 설명 drift를 자동 검사했다.
  - 결과: greenfield confidence path가 bootstrap output -> first-success helper -> readiness/consistency validator -> workflow template onboarding 단계로 정렬됐고, remaining manual checks도 같은 문맥으로 정리됐다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: workflow template를 실제 consumer repo에 복사한 뒤 GitHub Actions에서 end-to-end 실행하는 단계는 문서 안내와 shipped asset 수준까지만 확인했다.

- 검증 항목: downstream bundle의 workflow template shipping과 localized greenfield smoke
  - 대조한 입력물: `docs/kit_maintenance/downstream_bundle_boundary.md`, `docs/kit_maintenance/downstream_bundle_smoke_validation.md`, `scripts/generate_downstream_bundle.py`, `tests/test_generate_downstream_bundle.py`, `tests/test_validate_downstream_bundle.py`, `tests/test_downstream_bundle_smoke.py`
  - 실행 방법 또는 확인 방식: `python3 -m unittest tests.test_generate_downstream_bundle tests.test_validate_downstream_bundle tests.test_downstream_bundle_smoke`
  - 결과: bundle이 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 실제 포함하고, generated README/manifest가 새 shipped asset을 반영하며, canonical bundle 기준 `python`/`java`/`kotlin` greenfield 경로와 `third_party/harness-kit` localized vendoring 경로가 모두 통과했다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: workflow template는 bundle 포함과 placeholder 존재까지만 검증했고, remote reusable workflow 호출 자체의 외부 GitHub 실행은 미검증이다.

- 검증 항목: changed-parts / whole-harness maintainer audit
  - 대조한 입력물: 변경 파일 전체, task workspace 산출물, focused test 결과
  - 실행 방법 또는 확인 방식: 분리된 subagent changed-parts audit 3회, whole-harness audit 1회 수행
  - 결과: whole-harness audit은 바로 `APPROVE`였고, changed-parts audit은 처음에 Windows absolute path, 이어서 Windows drive-relative path 검증 공백 때문에 2회 `NEEDS_CHANGES`가 나왔다. `bootstrap_init.py`의 vendor path 정규화와 focused test를 보강한 뒤 최종 changed-parts audit도 `APPROVE`로 전환됐다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 없음

## 실행하지 못한 검증

- consumer repo에 workflow template를 실제 복사한 뒤 GitHub Actions에서 reusable workflow를 호출하는 원격 end-to-end 검증은 미실행

## 결과 요약

- greenfield first-success confidence path가 localized vendoring, staged validator signal, workflow-template onboarding까지 포함하는 실제 shipped/tested 경로로 정렬됐다.

## Phase 5에서 반영할 related decisions/

- 해당 없음. 이번 작업은 downstream project-local decision record가 아니라 `harness-kit` core greenfield bootstrap confidence path와 bundle surface 정렬 범위다.

## 남은 리스크

- workflow template를 실제 consumer CI에 설치하고 pin을 유지하는 운영 discipline은 여전히 프로젝트 측 실행이 필요하다.

## 후속 조치 필요 사항

- 다음 후보 이슈 `#95 incremental brownfield validation mode`에서 partial adoption intermediate signal을 별도 축으로 강화할 수 있다.
