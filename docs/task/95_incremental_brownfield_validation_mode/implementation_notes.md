# Implementation Notes

## 진행 로그

- Phase 1 시작: issue `#95` 기준으로 brownfield partial adoption intermediate state를 full consistency validator와 분리해 읽는 incremental mode 범위를 정리하고 요구사항/계획을 고정함.
- 구현: `validate_overlay_consistency.py`에 `--mode incremental`을 추가해 missing overlay docs/runtime entrypoints는 follow-up으로 보고, legacy leftover, stale vendored path, broken adapter chain, malformed existing anchor doc는 blocking으로 유지하도록 보강함.
- 구현: `cross_document_consistency_checker.md`, `adopt_dry_run.md`, `adopt_safe_write.md`, `local_diagnostics_and_dry_run.md`, `quickstart.md`, `downstream_bundle_smoke_validation.md`, `README.md`를 incremental mode와 full mode의 역할 경계에 맞게 정렬함.
- 구현: focused validator test와 downstream bundle smoke에 partial brownfield incremental scenario를 추가하고, pure-missing incremental state도 직접 고정함.
- 검증: `python3 -m unittest tests.test_validate_overlay_consistency tests.test_downstream_bundle_smoke tests.test_adopt_dry_run tests.test_adopt_safe_write`, `python3 scripts/check_harness_docs.py`를 통과함.
- 감사: changed-parts / whole-harness audit 모두 `APPROVE`였고, 이후 pure-missing incremental state focused test를 추가한 뒤 재감사에서도 `APPROVE`가 유지됨.

## 경량 검토 기록

- 작은 태스크로 본 근거: 해당 없음
- 경량 적용 승인 여부: 미적용
- 실제 축소한 범위: 해당 없음
- 유지한 테스트: consistency validator focused test, downstream bundle smoke, doc guard
- 유지한 감사: changed-parts / whole-harness audit 수행 완료
- 전체 흐름 영향 요약: brownfield project-facing docs, consistency validator, downstream smoke가 함께 영향받는다.
- 남은 리스크: localized vendoring과 incremental mode 조합은 bundle-level smoke보다 focused validation에 더 많이 기대고 있다.
- Full 전환 조건 또는 승격 조건: 이미 full 흐름으로 진행 중

## 구현 중 결정 사항

- 별도 새 validator를 만들지 않고 `validate_overlay_consistency.py --mode incremental`으로 확장해 full/incremental의 책임 경계를 같은 script 안에서 비교 가능하게 유지했다.
- incremental mode는 adopt dry-run의 file-diff classification을 대체하지 않고, current partial state가 structurally safe한지 보는 intermediate gate로만 제한했다.
- missing docs/runtime entrypoints는 follow-up으로 남기되, 이미 존재하는 anchor doc의 broken contract와 stale leftover는 계속 hard fail 하도록 정했다.

## 위임된 책임

## 사용자 승인 필요 항목

## 후속 태스크 후보

- repo-aware adoption epic의 다른 이슈는 이후 partial state classification을 더 세밀하게 확장할 수 있다.
