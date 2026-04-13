# Plan

## 변경 대상 파일 또는 모듈

- `docs/kit_maintenance/downstream_bundle_boundary.md`
- `docs/kit_maintenance/downstream_bundle_smoke_validation.md`
- `scripts/generate_downstream_bundle.py`
- `scripts/validate_downstream_bundle.py`
- `scripts/check_harness_docs.py`
- `tests/test_downstream_bundle_smoke.py`
- `tests/test_generate_downstream_bundle.py`
- 필요 시 `tests/test_validate_downstream_bundle.py`

## 레이어별 작업 계획

- boundary 문서와 generator/validator의 include-exclude 의미를 대조해, maintainer-only exclusion을 실제 generator 계산에도 반영하는 최소 코드를 넣는다.
- generated README/manifest/validator가 새 boundary semantics와 어긋나지 않는지 함께 정렬한다.
- downstream bundle smoke를 greenfield `python`/`java`/`kotlin` bootstrap + first-success/overlay validation coverage로 확장한다.
- maintainer smoke validation 문서를 실제 smoke 범위와 맞추고, legacy entrypoint migration surface도 문서에 명시한다.
- doc guard와 focused test를 보강해 boundary drift와 support-claim drift를 재발 시 다시 잡는다.

## 테스트 계획

- `python3 -m unittest tests.test_generate_downstream_bundle tests.test_validate_downstream_bundle tests.test_downstream_bundle_smoke`
- `python3 scripts/check_harness_docs.py`
- 필요하면 `python3 scripts/validate_downstream_bundle.py`

## 문서 반영 계획

- `docs/kit_maintenance/downstream_bundle_boundary.md`에 generator가 따르는 include/exclude 책임 경계를 실제 구현과 맞춘다.
- `docs/kit_maintenance/downstream_bundle_smoke_validation.md`에 multi-language greenfield coverage와 legacy migration surface를 반영한다.
- 관련 `docs/decisions/README.md` 또는 `DEC-###-slug.md` 읽기/수정/생성 필요 여부: 해당 없음. 이번 작업은 downstream project-local decision registry가 아니라 harness core bundle boundary와 maintainer validation 흐름 정합화 범위다.
- 새 decision이 필요하면 index 갱신 계획: 해당 없음.

## 비범위

- Java/Kotlin brownfield adoption flow까지 smoke coverage 확장
- bundle artifact packaging 방식 변경
- repo-aware adoption epic 범위 기능 추가

## 리스크 또는 확인 포인트

- exclude semantics를 코드에 올릴 때 현재 bundle contents가 무의미하게 바뀌지 않도록 overlap precedence만 추가해야 한다.
- Java/Kotlin smoke는 project-facing support claim을 고정하는 대신 테스트 시간과 brittle surface를 늘릴 수 있으므로 expectation을 bootstrap/validator 성공 신호에 집중해야 한다.
- maintainer 문서와 doc guard를 같이 안 바꾸면 다시 설명 drift가 생긴다.
