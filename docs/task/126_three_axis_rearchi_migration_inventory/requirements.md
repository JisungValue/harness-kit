# Requirements

## 기능 요구사항

- migration inventory는 현재 저장소의 실제 자산을 `downstream`, `bootstrap`, `maintainer`, `루트 유지/비범위`로 분류해야 한다.
- inventory는 각 자산군의 현재 경로와 1차 목표 canonical path를 함께 보여줘야 한다.
- `docs/task/*`가 1차 구조 재배치 범위 밖이라는 점과 `harness.log`가 루트 유지라는 점을 명시해야 한다.
- wrapper는 허용 가능한 전이 수단이지만 canonical path를 대체하지 못하며, 제거 조건 또는 후속 추적 조건을 남겨야 한다.
- 테스트는 물리 이동과 별개로 path expectation을 자산 이동 단계에서 즉시 갱신해야 한다는 원칙을 포함해야 한다.
- bundle boundary나 canonical path가 바뀌는 단계에서는 `dist/harness-kit-project-bundle/` 재생성과 `bundle_manifest.json` 검증이 완료 조건에 포함돼야 한다.
- old path 문자열 검색 키워드 목록이 단계별 검증에 바로 사용할 수 있는 수준으로 정리돼야 한다.

## 비기능 요구사항 또는 품질 요구사항

- inventory는 실제 repo 상태와 맞아야 하며, issue 본문을 그대로 복사한 문서가 아니라 현재 파일 집합을 반영해야 한다.
- 이후 하위 이슈가 그대로 참조할 수 있도록 directory-level 분류와 대표 파일 목록이 모두 드러나야 한다.
- 정책 문구는 실행 순서를 혼동하지 않도록 `이번 이슈에서 확정`과 `후속 이슈에서 실행`을 구분해야 한다.

## 입력/출력

- 입력:
  - `#125`, `#126` 이슈 본문
  - 현재 저장소의 `docs/`, `scripts/`, `bootstrap/`, `tests/`, `README.md`
- 출력:
  - 3축 재배치용 migration inventory 문서
  - 비범위/유지 정책, wrapper 정책, 테스트 경로 원칙, dist 검증 원칙, old path 검색 키워드 목록

## 제약사항

- 이번 이슈에서는 실제 파일 이동을 하지 않는다.
- 1차 목표 구조는 `#125`의 큰 방향을 따르되, 현재 repo에 있는 실제 파일만 inventory에 포함한다.

## 예외 상황

- 실제 파일명이나 경로가 에픽 예시와 다르면 현재 저장소 기준으로 기록하고, 후속 이슈에서 그 차이를 해소한다.
- 테스트 물리 이동은 뒤로 미뤄도 되지만 경로 기대값 변경은 뒤로 미루지 않는다.

## 성공 기준

- 하위 이슈가 참조할 수 있는 maintainer canonical migration inventory가 생긴다.
- 비범위와 루트 유지 정책이 누락 없이 정리된다.
- wrapper, 테스트 path expectation, dist/manifest 검증 원칙이 문서화된다.
- old path 검색 키워드를 단계별 검증에 바로 사용할 수 있다.
