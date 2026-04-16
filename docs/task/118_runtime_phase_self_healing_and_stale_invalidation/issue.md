# Issue

## 배경

- 현재 harness 문서에는 가장 이른 영향 Phase부터 재수행한다는 원칙은 있으나, 수정 요청 수신 시 stale audit, stale approval, stale artifact를 어떻게 무효화하고 잠글지에 대한 runtime 규칙이 충분히 명시돼 있지 않다.
- 이 공백 때문에 downstream 프로젝트가 harness를 실제 task 수행 중 사용할 때 Phase jump, close-out 선행 수정, 이전 승인 재사용 같은 drift가 생길 수 있다.
- 이 문제는 downstream bundle upgrade 절차가 아니라, downstream task runtime contract 문제다.

## 요청사항

- 공통 self-healing runtime 규칙을 정의한다.
- earliest impacted phase, stale invalidation, write-set lock, next-phase jump 금지 규칙을 명시한다.
- Phase 1~5 implementation과 audit 문서에 phase별 재수행 규칙과 stale 상태 승인 금지 규칙을 반영한다.
- `docs/harness_guide.md`, `docs/downstream_harness_flow.md`, task artifact template을 같은 계약으로 정렬한다.

## 비범위

- downstream bundle upgrade 절차 재설계
- 승인 없는 자동 self-modify 허용
- doctor, scheduler, autonomous repair 구현
- 자유로운 semantic merge 또는 문서 rewrite 자동화

## 승인 또는 제약 조건

- 기존 `1 -> 2 -> 3 -> 4 -> 5` Phase 순서는 유지한다.
- 문안은 현재 repo-local 용어와 기존 process policy 구조를 최대한 유지한다.
- 변경은 문서와 task artifact 범위에서 끝낸다.
