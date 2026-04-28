# Validation Policy

## 목적

이 문서는 전체 검증 단계에서 공통으로 적용되는 기록 원칙을 정의한다.

## 언제 다시 읽는가

- Phase 3에서 검증 결과와 연동 리스크를 기록할 때 참조한다.
- Phase 4 시작 시 반드시 재확인한다.
- `validation_report.md`에 무엇을 어떤 형식으로 남겨야 하는지 헷갈릴 때 다시 읽는다.

## 검증 대상 원칙

- 구현된 요구사항이 실제로 충족되는지 확인한다.
- 테스트 통과 여부만이 아니라 잔여 리스크와 미실행 검증도 함께 기록한다.
- 자동 검증과 수동 검증을 구분한다.

## Phase 1 대비 추적성 검증 규칙

- Validation 단계에서는 아래 입력물을 함께 놓고 교차 검토한다.
  1. `issue.md`
  2. `requirements.md`
  3. `plan.md`
  4. `implementation_notes.md`
  5. 실제 구현 결과
- `issue.md`의 요청사항, 제약사항, 비범위가 실제 구현 결과와 일치하는지 확인한다.
- `requirements.md`의 기능 요구사항, 제약사항, 예외 상황, 성공 기준이 실제 구현 결과에 반영됐는지 확인한다.
- `plan.md`의 변경 대상, 테스트 계획, 문서 반영 계획이 실제 수행 결과와 맞는지 확인한다.
- `implementation_notes.md`의 위임된 책임, 사용자 승인 필요 항목, 진행 로그가 실제 구현 및 검증 결과와 충돌하지 않는지 확인한다.
- 구현 로그와 실제 결과가 다르면 `누락` 또는 `범위 확장`으로 구분해 기록한다.

## Phase 되돌아가기 및 재수행 규칙

- Validation에서 발견한 불일치의 원인이 이전 Phase 산출물에 있으면 원인 Phase로 되돌아가 산출물을 먼저 보완한다.
- Validation에서 이전 Phase 산출물 불일치가 확인되면, 해당 원인 Phase의 감사와 사용자 승인 상태는 stale 로 본다.
- 원인 Phase보다 뒤에서 이미 작성된 `validation_report.md`, final task-local 문서, related decision 반영 초안은 stale 후보로 잠그고 재사용하지 않는다.
- 원인 Phase를 보완한 뒤에는 해당 Phase부터 현재 Phase까지 영향받는 Phase를 순서대로 다시 수행한다.
- 되돌아가기가 발생하면 `validation_report.md`에 원인 판단 근거, 되돌아간 Phase, 재수행 범위를 남긴다.
- 되돌아가기와 재수행에도 각 Phase의 감사와 사용자 승인 게이트를 동일하게 적용한다.

## 검증 결과 기록 형식

`validation_report.md`에는 검증 항목별로 아래 내용을 남긴다.

- 검증 항목
- 대조한 입력물
- 실행 방법 또는 확인 방식
- 결과
- 실패 또는 미실행 사유
- 판정 (`정합`, `누락`, `범위 확장` 중 하나)
- 잔여 리스크

검증 항목 요약 뒤에는 별도 섹션 `## Phase 5에서 반영할 related decisions/`를 두고 아래 중 하나를 남긴다.

- 수정 또는 생성해야 할 `docs/project/decisions/README.md`, `DEC-###-slug.md` 경로와 반영 이유
- decision 반영이 필요 없다는 판단과 그 사유

## 검증 결과 작성 원칙

- 단순히 `확인함`으로 끝내지 않는다.
- 자동 검증은 가능하면 실행 명령 또는 실행 단위를 남긴다.
- 프로젝트 `docs/project/standards/quality_gate_profile.md`를 기준으로 어떤 품질 게이트를 실행했는지와 미실행 사유를 남긴다.
- code hygiene 관련 자동 게이트를 실행했다면 어떤 항목을 확인했는지 또는 왜 수동 검토로 대체했는지도 남긴다.
- 성능 민감 변경 또는 성능 최적화 주장이 있으면 대상 경로, 근거, 검증 방법 또는 미실행 사유, 잔여 리스크가 `implementation_notes.md`와 `validation_report.md`에 식별 가능하게 남았는지 기록한다.
- design quality와 performance가 충돌한 경우 대안, 추천안, 근거, 검증 계획, trade-off가 `implementation_notes.md`에 정리됐는지와 `validation_report.md`에 그 요약이 남았는지도 기록한다.
- 수동 검증은 무엇을 어떻게 확인했는지 남긴다.
- 미실행 검증은 누락하지 말고 사유를 적는다.
- 추적성 검증에서 불일치가 있으면 `누락` 또는 `범위 확장`으로 명시하고 근거를 남긴다.
- 불일치 원인이 이전 Phase 산출물 결함이면 되돌아가기와 재수행 계획을 함께 기록한다.
- stale 상태가 해소되기 전에는 Validation 결과만으로 Phase 5 close-out 판단을 먼저 확정하지 않는다.
- 구조, 정책, 예외 처리 규칙, 책임 배치, 운영 규칙 변경이면 Phase 5에서 반영할 related decisions/를 빠뜨리지 않는다.
- 잔여 리스크가 없으면 `없음`으로 명시한다.
