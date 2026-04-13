# Implementation Notes

## 진행 로그

- Phase 1 시작: issue `#100` 기준으로 bundle boundary, generator semantics, downstream bundle smoke coverage의 drift를 정리하고 요구사항/계획을 고정함.
- 구현: generator가 include 후보에 maintainer-only exclusion 우선순위를 실제 적용하도록 바꾸고, manifest/validator가 `excluded_patterns`를 같은 계약으로 검증하도록 맞춤.
- 구현: downstream bundle smoke를 `python`/`java`/`kotlin` greenfield bootstrap + first-success/overlay validation 경로로 확장하고, legacy entrypoint migration을 maintainer smoke 문서에 명시함.
- 검증: `python3 -m unittest tests.test_generate_downstream_bundle tests.test_validate_downstream_bundle tests.test_downstream_bundle_smoke`, `python3 scripts/check_harness_docs.py`, `python3 scripts/generate_downstream_bundle.py --force`, `python3 scripts/validate_downstream_bundle.py`를 통과함.
- 감사: changed-parts 감사는 최초 `APPROVE`였고, whole-harness 감사는 지원 언어 source-of-truth가 분산됐다는 이유로 1회 `NEEDS_CHANGES`가 나왔다. 이후 smoke test/doc guard가 `scripts/bootstrap_init.py`의 `LANGUAGE_BOOTSTRAP_PATHS`를 직접 참조하도록 보강한 뒤 whole-harness 재감사에서 `APPROVE`로 전환됨.

## 경량 검토 기록

- 작은 태스크로 본 근거: 해당 없음
- 경량 적용 승인 여부: 미적용
- 실제 축소한 범위: 해당 없음
- 유지한 테스트: downstream bundle generation/validation/smoke, doc guard
- 유지한 감사: 이후 changed-parts / whole-harness audit 예정
- 전체 흐름 영향 요약: bundle 경계 설명, generated bundle semantics, maintainer validation, project-facing support claim이 함께 영향받는다.
- 남은 리스크: Java/Kotlin smoke 범위를 어디까지 잡을지와 exclude semantics를 manifest까지 드러낼지 구현 중 판단이 필요하다.
- Full 전환 조건 또는 승격 조건: 이미 full 흐름으로 진행 중

## 구현 중 결정 사항

- section 3 maintainer-only exclusion은 문서 문구를 약화시키지 않고 generator/validator semantics로 실제 반영하는 쪽을 선택했다.
- Java/Kotlin support claim을 문서에서 줄이기보다 greenfield bundle smoke coverage를 확장해 current project-facing 약속을 테스트로 뒷받침하는 쪽을 선택했다.
- 지원 언어 source-of-truth는 `scripts/bootstrap_init.py`의 `LANGUAGE_BOOTSTRAP_PATHS`로 두고, smoke test와 doc guard가 이를 따라가게 정리했다.

## 위임된 책임

## 사용자 승인 필요 항목

## 후속 태스크 후보

- Java/Kotlin 경로는 현재 bootstrap/validator 수준 smoke까지만 보므로, 필요하면 언어별 더 깊은 ecosystem integration signal은 별도 이슈로 다룬다.
