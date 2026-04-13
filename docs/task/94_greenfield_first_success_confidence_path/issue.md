# Issue

## 배경

- current greenfield flow는 bootstrap, first-success helper, unresolved decision validator, consistency checker까지 갖췄지만, strict audit 기준에서는 first-success confidence path가 아직 약하다.
- 현재 first-success 보장은 문서마다 흩어져 있어, bootstrap 직후 무엇이 보장되고 무엇이 아직 수동 확인 대상인지 한 번에 파악하기 어렵다.
- non-default vendoring에서는 `docs/project_entrypoint.md`와 `docs/standard/coding_conventions_project.md`를 수동으로 현지화해야 해서 greenfield starter friction이 남아 있다.
- future sessions consistency를 초기에 고정하는 CI/doc-guard onboarding 자산은 문서에 언급되지만 downstream bundle과 first-success 흐름에서 충분히 전면화되어 있지 않다.

## 요청사항

- greenfield first-success가 어떤 신호를 보장하는지 단계별로 더 명확히 정의한다.
- runtime entrypoint, traversal contract, decisions index, unresolved decision readiness, consistency check, CI/doc-guard onboarding을 같은 confidence path로 정렬한다.
- non-default vendoring/manual localization friction을 줄일 수 있는 최소 구현을 추가하거나, 불가하면 fallback 경계를 더 분명히 설명한다.
- greenfield docs, downstream bundle boundary, smoke validation이 같은 confidence model을 사용하도록 맞춘다.

## 비범위

- 모든 언어의 full semantic validator 추가
- interactive installer 재설계
- brownfield incremental validation mode 전체 구현

## 승인 또는 제약 조건

- release:must-have blocker를 줄이는 최소 수정이 우선이다.
- 문서만 늘리기보다 bootstrap path, shipped bundle, smoke validation이 같은 실제 신호를 사용하도록 맞추는 쪽을 우선한다.
