# Issue

## 배경

- `#125`는 `downstream/`, `bootstrap/`, `maintainer/` 3축 구조를 실제 디렉터리 레이아웃으로 드러내는 에픽이다.
- 실제 파일 이동에 들어가기 전에 무엇을 어느 축으로 옮길지, 무엇은 1차 범위 밖으로 둘지, 각 단계가 어떤 공통 원칙을 따라야 하는지 먼저 고정해야 한다.
- 특히 이후 하위 이슈들이 같은 전제를 공유하지 못하면 문서 이동, 스크립트 이동, bundle/dist 갱신, 테스트 경로 수정이 서로 어긋날 가능성이 크다.

## 요청사항

- 현재 저장소 기준의 migration inventory를 정리한다.
- `docs/harness/common/*`, `docs/templates/task/*`, `docs/examples/*`, `docs/task/*`의 분류를 명시한다.
- `docs/task/*` 1차 비범위 정책과 `harness.log` 루트 유지 정책을 명시한다.
- wrapper 허용 여부와 제거 조건을 정한다.
- 테스트 path expectation을 각 단계에서 즉시 수정한다는 원칙을 명시한다.
- `dist/` 재생성과 manifest 검증을 관련 단계의 완료 조건으로 명시한다.
- old path 문자열 검색 키워드 목록을 정리한다.

## 비범위

- 실제 파일 이동 또는 rename 수행
- 스크립트 import/path 상수 실제 수정
- bundle/dist artifact 재생성 자체
- root README 재작성 자체

## 승인 또는 제약 조건

- inventory는 현재 저장소 구조를 기준으로 작성한다.
- 하위 이슈가 재사용할 수 있도록 source path와 target canonical path를 함께 남긴다.
- `docs/task/*`는 이번 이슈에서 이동 대상이 아니라 작업 산출물 저장 위치로 계속 사용한다.
- canonical migration inventory는 maintainer 문서 `docs/kit_maintenance/three_axis_rearchi_migration_inventory.md`에 둔다.
