# Plan

## 변경 대상 파일 또는 모듈

- `scripts/validate_overlay_consistency.py`
- `docs/project_overlay/cross_document_consistency_checker.md`
- `docs/project_overlay/adopt_dry_run.md`
- `docs/project_overlay/adopt_safe_write.md`
- `docs/project_overlay/local_diagnostics_and_dry_run.md`
- `docs/quickstart.md`
- `maintainer/docs/downstream_bundle_smoke_validation.md`
- `tests/test_validate_overlay_consistency.py`
- `tests/test_downstream_bundle_smoke.py`
- 필요 시 `scripts/check_harness_docs.py`

## 레이어별 작업 계획

- `validate_overlay_consistency.py`에 `--mode incremental`을 추가하고, safe gap과 blocking inconsistency를 분리하는 최소 출력 구조를 넣는다.
- full mode에서만 필수 문서/entrypoint hard fail을 유지하고, incremental mode에서는 missing docs/runtime entrypoints를 follow-up으로 보고 existing 문서의 broken contract만 fail 하게 정리한다.
- partial brownfield intermediate state를 focused test와 downstream bundle smoke에 추가한다.
- project-facing docs에서 adopt dry-run -> incremental mode -> safe write/full mode의 권장 흐름과 역할 경계를 정리한다.
- doc guard가 incremental mode 설명 drift를 다시 잡도록 필요한 최소 검사를 추가한다.

## 테스트 계획

- `python3 -m unittest tests.test_validate_overlay_consistency tests.test_downstream_bundle_smoke`
- 필요 시 `python3 -m unittest tests.test_adopt_dry_run tests.test_adopt_safe_write`
- `python3 scripts/check_harness_docs.py`

## 문서 반영 계획

- `cross_document_consistency_checker.md`, `adopt_dry_run.md`, `adopt_safe_write.md`, `local_diagnostics_and_dry_run.md`, `quickstart.md`에 incremental mode command와 full mode와의 차이를 반영한다.
- `downstream_bundle_smoke_validation.md`에 intermediate brownfield scenario를 추가한다.
- 관련 `docs/decisions/README.md` 또는 `DEC-###-slug.md` 읽기/수정/생성 필요 여부: 해당 없음. 이번 작업은 downstream project-local decision 내용이 아니라 overlay validation mode와 brownfield adoption guidance 범위다.
- 새 decision이 필요하면 index 갱신 계획: 해당 없음.

## 비범위

- adopt dry-run 결과를 자동으로 validator 입력으로 연결하는 새 오케스트레이터 추가
- semantic merge/update 지원
- fully custom legacy doc system mapping

## 리스크 또는 확인 포인트

- missing files를 너무 많이 non-blocking으로 두면 false confidence가 생길 수 있으므로, existing broken chain과 stale leftovers는 계속 hard fail 해야 한다.
- docs에서 incremental mode를 지나치게 강조하면 full mode 필요성이 흐려질 수 있으므로 upgrade point를 명확히 써야 한다.
- smoke/test가 partial state를 fixture로 재현하되, adopt_dry_run과 consistency validator의 역할을 혼동하지 않게 유지해야 한다.
