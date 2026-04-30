# Plan

## 변경 대상 파일 또는 모듈

- `docs/project/standards/implementation_order.md`
- `docs/process/examples/sample-lightweight-task/validation_report.md`

## 레이어별 작업 계획

- Phase 1 산출물은 핵심 판단 근거만 남기는 경량 형태로 작성한다.
- 대상 문장을 수정한다.
- 관련 검증과 감사 결과를 기록한다.

## 테스트 계획

- 수정 문장이 기존 문서 책임 경계를 바꾸지 않았는지 수동 검토한다.
- 문서 경로와 섹션명이 유지되는지 확인한다.

## 문서 반영 계획

- `validation_report.md`에 경량 검토 기록, 수행한 검증, 잔여 리스크를 남긴다.
- 관련 `docs/project/decisions/README.md` 또는 `DEC-###-slug.md` 읽기/수정/생성 필요 여부: 해당 없음. 이번 작업은 decision 수준의 구조 변경이 아니다.
- 새 decision이 필요하면 index 갱신 계획: 해당 없음.

## 비범위

- 다른 overlay 문서 수정
- template 구조 변경
- maintainer audit 정책 변경

## 리스크 또는 확인 포인트

- 문장 명확화가 새 규칙 추가처럼 읽히지 않게 주의해야 한다.
