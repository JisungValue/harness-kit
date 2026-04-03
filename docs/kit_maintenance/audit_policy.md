# Kit Maintenance Audit Policy

## 목적

이 문서는 `harness-kit` core 문서를 수정할 때 적용하는 maintainer 전용 감사 기준을 정의한다.

## 운영 모드

- 본 문서는 maintainer 감사의 기본 모드를 `Strict Mode`로 사용한다.
- core 의미 변경은 `changed-parts`와 `whole-harness`를 모두 통과해야 승인 가능하다.

## 적용 범위

- 대상: `harness-kit` 저장소의 core 규칙, phase 기준, template, example, 문서 구조 변경
- 비대상: `harness-kit`를 적용한 개별 서비스 프로젝트의 task/phase 감사

## 감사 실행 원칙

- core 의미 변경이 있으면 구현 주체와 분리된 subagent audit를 수행한다.
- audit는 반드시 `changed-parts`와 `whole-harness`로 분리해 수행한다.
- 최종 판정은 두 audit가 모두 승인 가능일 때만 승인 가능으로 본다.

## Changed-Parts 감사 기준

changed-parts는 바뀐 파일과 인접 영향만 본다.

### 1) 기록 및 추적성

- `harness.log` 필수 항목(`변경`, `이유`, `audit`, `audit-summary`)이 같은 변경에서 함께 기록되었는가
- `이유`가 단순 기능 설명이 아니라 운영 리스크 감소 또는 운영 효율 개선 근거를 포함하는가
- 2026-04-03 이후 신규 항목은 `audit-summary` 형식을 준수하는가

### 2) 로컬 일관성

- 변경 의도와 실제 수정 내용이 일치하는가
- 인접 참조 경로, 문서명, 섹션명이 깨지지 않았는가
- template 변경 시 관련 phase 또는 guide 문서의 인접 영향이 반영되었는가
- "적절히", "충분히"처럼 해석 여지가 큰 표현은 가능한 한 조건문 또는 명시 기준으로 바꿨는가
- 같은 규칙이 불필요하게 중복 추가되지 않았는가
- 기존 규칙 의미를 우연히 뒤집거나 약화하지 않았는가

## Whole-Harness 감사 기준

whole-harness는 전체 문서 흐름과 core 일관성을 본다.

### 1) 아키텍처 및 경계 검사

- `README.md`, `docs/harness_guide.md`, phase-local 문서 사이에 충돌이 없는가
- core와 project overlay의 책임 경계가 흐려지지 않았는가
- 특정 기술 스택 종속 규칙을 core로 끌어오지 않았는가(How보다 What/Criterion 중심)
- 기존 프로젝트의 overlay를 대규모 재작성해야 하는 breaking 성격 변경인지 확인했는가
- Phase 게이트(implementation -> audit -> 사용자 승인 -> 다음 phase)와 충돌하지 않는가

### 2) 인지 부하 및 수행 비용

- 필수 재참조 문서 수가 늘어났다면 불필요 규칙 삭제/통합 또는 증가 근거를 기록했는가
- 문서 길이 증가와 규칙 중복이 하네스 수행 누락 위험을 키우지 않는가
- 기존 core 내에 동일/유사 규칙이 이미 있는지 중복 검사를 수행했는가
- 새 감사 단계나 산출물 추가로 태스크 리드 타임이 10% 이상 증가할 우려가 있으면 근거와 승인 사유를 남겼는가

### 3) 실무 정합성

- 규칙 변경으로 sample task 기대 산출물 또는 수행 방식이 바뀌면 `docs/examples/sample-task/`를 함께 현행화했는가
- subagent/제3자가 같은 규칙으로 유사한 감사 결론을 낼 수 있을 만큼 기준이 객관적인가
- 경량 태스크 예외 원칙과 충돌하지 않는가
- 필수/조건부 재참조 문서 목록이 상위-하위 문서 간에 모순되지 않는가

## 승인 불가 기준

아래 중 하나라도 해당하면 승인 불가다.

- 상위 문서와 하위 문서가 같은 규칙에 대해 상충 지시를 함
- core/overlay 책임 경계가 바뀌었는데 의도와 근거가 없음
- Phase 게이트를 우회하거나 약화하는 문구가 추가됨
- 필수 재참조 경로가 불일치하거나 깨짐
- `harness.log`에 `변경`, `이유`, `audit`, `audit-summary` 중 하나라도 누락됨

## Subagent 판정 기준

- P1 (Critical): changed-parts 또는 whole-harness 체크포인트 중 하나라도 실패하면 승인 불가이며 로그를 완료 상태로 확정하지 않는다.
- P2 (Major): 운영 효율 저하 우려(예: 필수 문서 수 증가, 리드 타임 10%+ 증가 가능성)가 있으면 maintainer 승인 이유를 `harness.log`에 명시한다.

## 감사 결과 형식

- verdict: APPROVE / REJECT
- findings: 핵심 근거 bullet
- risks: none / low / medium / high + 한 줄 근거
- suggested fix: REJECT일 때만 제시

## 기록 규칙

- maintainer는 같은 작업에서 `harness.log`를 갱신한다.
- `harness.log` 항목에는 `변경`, `이유`, `audit`, `audit-summary`를 포함한다.
- `audit-summary` 필수 규칙은 2026-04-03 이후 신규 항목부터 적용한다.
