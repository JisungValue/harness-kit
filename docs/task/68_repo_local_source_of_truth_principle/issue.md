# Issue

## 배경

- `harness-kit`는 project overlay를 통해 프로젝트별 규칙을 repo-local 문서로 수렴시키는 구조다.
- 하지만 현재는 기억, 외부 대화, 다른 프로젝트 관행보다 repo 안 근거를 우선한다는 운영 원칙의 명시도가 약하다.
- strict audit 관점에서도 이 원칙이 약하면 session마다 다른 판단 기준이 섞이고, 누락된 결정을 추측으로 메우는 drift가 생길 수 있다.

## 요청사항

- repo-local source-of-truth 원칙을 core 운영 문서에 추가한다.
- 최소한 아래 규칙을 포함한다.
  - 작업 기준은 repo 안의 README, docs, ADR, scripts, config를 우선한다.
  - 기억, 외부 대화, 다른 프로젝트 관행은 repo 근거보다 우선하지 않는다.
  - 필요한 결정이 repo에 없으면 추측으로 메우지 않는다.
  - 없는 결정은 project overlay 또는 관련 문서에 남기도록 유도한다.
  - overlay 철학과 충돌하지 않도록 책임 경계를 정리한다.

## 비범위

- 특정 프로젝트의 canonical 문서 목록 강제
- 메모리 기반 보조 판단 전체 금지
- repo 외부 시스템과의 동기화 정책 추가

## 승인 또는 제약 조건

- 선언만 추가하는 데서 끝나지 않고, 감사 가능성과 task 기록 흐름에도 연결되어야 한다.
- project-facing 원칙과 maintainer-facing 감사 규칙이 같은 방향을 가리켜야 한다.
