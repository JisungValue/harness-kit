# Issue

## 배경

- self-healing, stale invalidation, write-set lock 규칙은 문서화됐지만 task runtime에서 현재 gate 상태와 허용 write-set을 즉시 읽을 수 있는 별도 state file은 없다.
- 또한 downstream task가 현재 Phase gate를 어기고 다음 산출물이나 잠긴 문서를 먼저 수정했는지 hard-stop으로 검사하는 validator가 아직 없다.

## 요청사항

- task workspace용 `phase_status.md`를 도입한다.
- `scripts/validate_phase_gate.py`를 추가해 현재 gate와 write-set 위반을 검사한다.
- 관련 공통 정책, guide, template, sample을 정렬한다.

## 비범위

- 자유로운 자동 self-repair 구현
- 기존 산출물을 audit file 3종 구조로 전면 교체
- downstream 프로젝트별 custom workflow 자동 생성

## 승인 또는 제약 조건

- `phase_status.md`는 task 종료 전까지 유지하고, close-out 완료 후 정리 가능한 구조로 둔다.
- validator는 downstream bundle에 포함되는 project-facing script여야 한다.
