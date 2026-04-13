# Requirements

## 기능 요구사항

- `validate_overlay_consistency.py`는 full mode와 별도로 partial adoption 상태를 읽는 incremental mode를 제공해야 한다.
- incremental mode는 missing overlay docs, missing runtime entrypoints 같은 safe gap을 non-blocking follow-up으로 보고해야 한다.
- incremental mode는 legacy project entrypoint leftover, stale vendored path, malformed existing entrypoint/runtime contract, broken document boundary처럼 adoption continuation 전에 먼저 고쳐야 하는 구조적 문제는 blocking으로 보고해야 한다.
- existing project-facing docs는 언제 incremental mode를 쓰고 언제 full mode로 올라갈지 설명해야 한다.
- downstream bundle smoke 또는 focused test는 intermediate brownfield state에서 incremental mode가 useful signal을 주는 시나리오를 검증해야 한다.

## 비기능 요구사항 또는 품질 요구사항

- 기존 full consistency mode의 현재 성공/실패 계약은 회귀 없이 유지돼야 한다.
- adopt dry-run / safe write와 역할이 겹쳐도 중복 자동화 기능을 추가하지 않고, 출력 해석과 구조 검증 경계만 명확히 해야 한다.
- 변경은 existing script 확장, 관련 docs, focused tests, smoke validation 범위 안의 최소 수정이어야 한다.

## 입력/출력

- 입력:
  - `scripts/validate_overlay_consistency.py`
  - `docs/project_overlay/cross_document_consistency_checker.md`
  - `docs/project_overlay/adopt_dry_run.md`
  - `docs/project_overlay/adopt_safe_write.md`
  - `docs/project_overlay/local_diagnostics_and_dry_run.md`
  - `docs/quickstart.md`
  - `tests/test_validate_overlay_consistency.py`
  - `tests/test_downstream_bundle_smoke.py`
  - 필요 시 `scripts/check_harness_docs.py`
- 출력:
  - partial adoption intermediate signal을 주는 incremental consistency mode
  - incremental vs full mode 역할 경계를 설명하는 project-facing docs
  - intermediate brownfield state를 재현하는 focused test 또는 smoke coverage

## 제약사항

- missing docs 자체를 모두 green으로 완화하면 안 된다. missing은 명시적 follow-up으로 계속 보여야 한다.
- full mode는 계속 필수 문서/entrypoint를 hard fail 해야 한다.
- incremental mode도 malformed existing doc, stale vendored path, legacy leftover 같은 unsafe state는 fail 해야 한다.

## 예외 상황

- `AGENTS.md` 없이 `CLAUDE.md`/`GEMINI.md`만 있는 상태처럼 partial이라기보다 broken chain인 경우는 incremental mode에서도 fail 해야 한다.
- `docs/project_entrypoint.md`가 없고 아무 runtime entrypoint도 없다면 safe gap일 수 있지만, legacy `docs/harness_guide.md`만 남아 있으면 migration-required blocker로 분류해야 한다.
- standard docs 중 일부만 존재할 때는 missing 문서는 follow-up으로, 이미 존재하는 문서의 내부 책임 경계 위반은 blocker로 동시에 나올 수 있다.

## 성공 기준

- already-underway project가 full overlay completion 이전에도 useful intermediate signal을 받을 수 있다.
- docs가 incremental mode와 full mode의 차이, 적용 시점, 남는 수동 판단 범위를 설명한다.
- intermediate state에 대한 focused test 또는 smoke validation이 추가되고 통과한다.
