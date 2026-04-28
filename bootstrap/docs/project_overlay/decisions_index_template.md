# Project Decision Index

이 문서는 프로젝트에서 장기적으로 유지해야 하는 중요한 결정 문서를 찾는 진입점이다.

## 문서 역할

- `docs/project/standards/architecture.md`는 현재 구조, 경계, 큰 그림을 설명한다.
- `docs/decisions/*.md`는 중요한 Architecture/Policy/Operational 결정을 기록한다.
- 다음 작업이 관련 결정을 건드리면 이 index에서 관련 decision 문서를 찾아 함께 읽고 갱신한다.

## 여기에 남기는 것

- 아래 중 하나 이상이면 decision 후보로 본다.
- 다음 세션이 모르고 구현하면 쉽게 어긋나는 중요한 결정
- 여러 파일 또는 레이어에 영향을 주는 책임 배치
- 장기 유지돼야 하는 정책, 예외 처리 규칙, 운영 규칙
- 변경 시 관련 문서 현행화가 필요한 결정
- 한 파일 안의 국소 수정이 아니라 architecture, standard 문서, 테스트, 운영 방식에 함께 영향을 주는 결정
- 기존 구현을 계속 따라야 하는지 새 원칙으로 바꿔야 하는지 후속 작업자가 반복 판단하게 될 결정

## 여기에 남기지 않는 것

- 메서드명 같은 작은 구현 디테일
- 일회성 리팩터링 편의 선택
- 테스트 fixture 이름 같은 국소 구현 사항
- 다음 세션에 반복 적용되지 않는 임시 판단
- 관련 문서 현행화가 필요 없는 단발성 구현 메모
- 로컬 코드 블록 안에서만 닫히는 미세한 표현 선택

## 번호 규칙

- 새 decision 문서는 `DEC-###-slug.md` 형식을 사용한다.
- 번호는 현재 index의 최대 번호에 1을 더해 정한다.
- 중간 번호 gap은 허용하고 기존 문서를 renumber하지 않는다.

## 읽기 방법

- `docs/entrypoint.md`에서 이 문서로 들어왔으면, 현재 작업과 직접 관련 있는 decision부터 읽는다.
- 구조 설명이 필요하면 `architecture.md`를 함께 읽고, 정책/책임/예외 규칙이 필요하면 관련 decision 문서를 함께 읽는다.
- 관련 decision이 바뀌면 `Related Docs`, `When To Update`에 적힌 문서도 같은 작업에서 함께 갱신한다.
- Phase 1에서는 이번 작업이 decision 후보인지 먼저 판정하고, 필요하면 plan에 decision 수정/생성을 넣는다.
- Phase 4에서는 `validation_report.md`에 Phase 5에서 반영할 related decisions/를 명시한다.
- Phase 5에서는 그 목록을 기준으로 decision 문서와 index를 실제로 갱신한다.

## Current Decisions

- 아직 active decision 없음. 새 decision을 추가하면 여기에 기록한다.

## Superseded Decisions

- 아직 superseded decision 없음.
