# Implementation Notes

## 진행 로그

- Phase 1 시작: `#126` 기준으로 3축 재배치의 실제 이동 전에 필요한 inventory와 비범위 정책을 현재 repo 구조 기준으로 정리하기로 함.
- 조사: `maintainer/docs/*`, `docs/project_overlay/*`, `docs/harness/common/*`, `docs/templates/task/*`, `docs/examples/**/*`, `docs/phase_*/*`, `scripts/*`, `bootstrap/**/*`, `tests/*`를 확인해 issue 본문과 현재 파일 집합을 대조함.
- 구현: 후속 하위 이슈가 공통으로 참조할 수 있도록 canonical 문서 `maintainer/docs/three_axis_rearchi_migration_inventory.md`에 유지/비범위 정책, wrapper 정책, 테스트 expectation 원칙, dist/manifest 원칙, old path 검색 키워드, 현재 path -> target canonical path 매핑을 정리함.
- 구현: `docs/task/*`는 1차 비범위이면서 동시에 이번 이슈 산출물 위치로 계속 사용한다는 점을 명시함.
- 구현: canonical inventory는 task 폴더가 아니라 maintainer 문서 경로로 옮기고, `#125` child issue가 계속 참조할 운영 규칙과 체크리스트를 같은 문서에 추가함.
- 검증: `python3 scripts/check_harness_docs.py`를 통과함.
- 감사: 최초 subagent audit에서 `docs/project_overlay/*`의 bootstrap 축 근거와 `docs/examples/**/*` inventory 완전성 보강이 필요하다는 지적을 받음. 이후 canonical 문서 `maintainer/docs/three_axis_rearchi_migration_inventory.md`에 축 의미 경계, `project_overlay`의 bootstrap canonical source 근거, examples 전체 subtree 및 전체 파일 목록을 추가한 뒤 재감사에서 changed-parts / whole-harness 모두 `APPROVE`를 받음.

## 경량 검토 기록

- 작은 태스크로 본 근거: 해당 없음
- 경량 적용 승인 여부: 미적용
- 실제 축소한 범위: 해당 없음
- 유지한 테스트: 문서 guard, 대표 old path 검색
- 유지한 감사: changed-parts / whole-harness subagent audit 수행
- 전체 흐름 영향 요약: 실제 경로 이동 전에 공통 전제와 분류 기준을 고정해 이후 하위 이슈의 판단 분기를 줄인다.
- 남은 리스크: 이후 하위 이슈에서 새 파일이 추가되면 inventory drift가 생길 수 있다.
- Full 전환 조건 또는 승격 조건: 이미 full 흐름으로 진행 중

## 구현 중 결정 사항

- task 산출물은 `docs/task/*`에 두되, 공통 source-of-truth 역할을 하는 migration inventory는 `maintainer/docs/three_axis_rearchi_migration_inventory.md`로 옮겨 maintainer canonical 문서로 관리한다.
- 실제 파일 이동은 하지 않고 정책과 매핑만 먼저 고정한다.

## 위임된 책임

## 사용자 승인 필요 항목

## 후속 태스크 후보

- `#134`부터 inventory 기준으로 실제 path move를 시작한다.
