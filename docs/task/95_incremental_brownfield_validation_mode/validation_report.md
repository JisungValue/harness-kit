# Validation Report

## 실행한 검증

- 검증 항목: incremental consistency mode의 safe gap / blocker 분리
  - 대조한 입력물: `scripts/validate_overlay_consistency.py`, `tests/test_validate_overlay_consistency.py`
  - 실행 방법 또는 확인 방식: `python3 -m unittest tests.test_validate_overlay_consistency`
  - 결과: full mode strict contract는 유지되고, incremental mode는 pure-missing brownfield 상태와 partial overlay 상태를 non-blocking follow-up으로 출력했다. 동시에 adapter-only broken chain, stale vendored path, legacy `docs/harness_guide.md` leftover는 계속 fail 하는 것을 확인했다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: mixed partial state에서 일부 standard doc만 존재하고 그중 일부가 malformed인 조합은 현재 focused test보다 더 세밀하게 확장할 여지가 있다.

- 검증 항목: downstream bundle intermediate brownfield smoke
  - 대조한 입력물: `maintainer/docs/downstream_bundle_smoke_validation.md`, `tests/test_downstream_bundle_smoke.py`
  - 실행 방법 또는 확인 방식: `python3 -m unittest tests.test_downstream_bundle_smoke`
  - 결과: canonical bundle 기준 partial brownfield project에서 `validate_overlay_consistency.py --mode incremental`이 missing docs/runtime entrypoints를 follow-up으로 보고하고, brownfield dry-run/create-only/migration 시나리오도 회귀 없이 통과했다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: downstream smoke는 아직 아무 overlay도 없는 empty consumer project의 incremental path까지는 별도 fixture로 고정하지 않았다.

- 검증 항목: adopt 흐름 회귀 확인
  - 대조한 입력물: `tests/test_adopt_dry_run.py`, `tests/test_adopt_safe_write.py`
  - 실행 방법 또는 확인 방식: `python3 -m unittest tests.test_adopt_dry_run tests.test_adopt_safe_write`
  - 결과: adopt dry-run/safe write의 existing 출력과 write 제한 계약은 회귀 없이 유지됐다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 없음

- 검증 항목: project-facing docs와 doc guard 정합성
  - 대조한 입력물: `docs/project_overlay/cross_document_consistency_checker.md`, `docs/project_overlay/adopt_dry_run.md`, `docs/project_overlay/adopt_safe_write.md`, `docs/project_overlay/local_diagnostics_and_dry_run.md`, `bootstrap/docs/quickstart.md`, `maintainer/docs/downstream_bundle_smoke_validation.md`, `scripts/check_harness_docs.py`
  - 실행 방법 또는 확인 방식: `python3 scripts/check_harness_docs.py`
  - 결과: incremental mode command, safe gap 설명, brownfield docs/maintainer smoke alignment가 doc guard 기준으로 통과했다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 없음

- 검증 항목: changed-parts / whole-harness maintainer audit
  - 대조한 입력물: 변경 파일 전체, task workspace 산출물, focused test 결과
  - 실행 방법 또는 확인 방식: 분리된 subagent changed-parts audit 2회, whole-harness audit 1회 수행
  - 결과: whole-harness audit은 바로 `APPROVE`였고, changed-parts audit도 최초 `APPROVE`였다. 이후 pure-missing incremental state를 직접 고정하는 focused test를 추가한 뒤 재감사에서도 `APPROVE`가 유지됐다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: downstream bundle 관점에서 empty consumer project incremental path는 smoke 대신 focused test로만 고정돼 있다.

## 실행하지 못한 검증

- localized vendoring(`third_party/...`)과 incremental mode를 함께 쓰는 bundle-level smoke는 미실행

## 결과 요약

- brownfield partial adoption 상태를 위한 incremental consistency mode가 full mode를 약화시키지 않으면서 useful intermediate signal을 주도록 정렬됐다.

## Phase 5에서 반영할 related decisions/

- 해당 없음. 이번 작업은 downstream project-local decision record가 아니라 `harness-kit` core validation mode와 brownfield guidance 정렬 범위다.

## 남은 리스크

- incremental mode가 empty consumer project까지 허용하는 것은 의도된 safe gap이지만, bundle-level smoke는 아직 project entrypoint가 하나 남아 있는 partial fixture 위주로 검증한다.

## 후속 조치 필요 사항

- 필요하면 localized vendoring과 incremental mode 조합, mixed partial standard-doc state를 별도 regression test나 smoke로 더 보강할 수 있다.
