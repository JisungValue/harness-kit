# Plan

## 변경 대상 파일 또는 모듈

- `docs/task/126_three_axis_rearchi_migration_inventory/issue.md`
- `docs/task/126_three_axis_rearchi_migration_inventory/requirements.md`
- `docs/task/126_three_axis_rearchi_migration_inventory/plan.md`
- `docs/kit_maintenance/three_axis_rearchi_migration_inventory.md`
- `docs/task/126_three_axis_rearchi_migration_inventory/implementation_notes.md`
- `harness.log`

## 레이어별 작업 계획

- 현재 `docs/`, `scripts/`, `bootstrap/`, `tests/` 구조를 다시 확인해 issue 본문과 실제 파일 집합의 차이를 정리한다.
- 3축 재배치 1차 기준 문서로 사용할 migration inventory를 작성한다.
- 비범위, 루트 유지, wrapper, 테스트 path expectation, dist/manifest 검증, old path 검색 키워드 정책을 같은 문서에 고정한다.
- task 산출물과 `harness.log`를 갱신하고, 문서 guard와 경로 검색으로 최소 검증을 수행한다.

## 테스트 계획

- `python3 scripts/check_harness_docs.py`
- migration inventory에 정리한 old path 키워드 중 대표 prefix 검색

## 문서 반영 계획

- canonical migration inventory는 `docs/kit_maintenance/three_axis_rearchi_migration_inventory.md`로 유지한다.
- `docs/task/126_three_axis_rearchi_migration_inventory/`는 issue 산출물과 작업 맥락 기록만 유지한다.
- 관련 `docs/decisions/README.md` 또는 `DEC-###-slug.md` 읽기/수정/생성 필요 여부: 해당 없음
- 새 decision이 필요하면 index 갱신 계획: 해당 없음

## 비범위

- 실제 `downstream/`, `bootstrap/`, `maintainer/` 경로 생성
- 문서 링크/스크립트 import/workflow/test의 실경로 수정

## 리스크 또는 확인 포인트

- inventory가 실제 repo와 어긋나면 후속 이슈 전체가 잘못된 기준을 따를 수 있다.
- 하위 이슈에서 wrapper를 도입하더라도 canonical path와 제거 조건 기록을 빼먹지 않도록 기준 문서에 분명히 남겨야 한다.
