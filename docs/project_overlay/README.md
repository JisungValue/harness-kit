# Project Overlay Guide

공통 Harness Kit를 가져온 프로젝트는 core를 그대로 재사용하고, 아래 문서만 프로젝트 전용으로 유지한다.

## 필수 문서

- `docs/harness_guide.md`
- `docs/standard/architecture.md`
- `docs/standard/implementation_order.md`
- `docs/standard/coding_guidelines_project.md`
- `docs/standard/testing_profile.md`

## 역할 분리

- `docs/harness_guide.md`
  - 프로젝트 로컬 진입점이다.
  - 공통 kit 문서와 프로젝트 전용 문서를 함께 연결하는 index 역할만 한다.
- `docs/standard/architecture.md`
  - 실제 레이어 구조, 모듈 경계, 주요 의존성 방향을 정의한다.
- `docs/standard/implementation_order.md`
  - Phase 2에서 사용할 프로젝트별 레이어 진행 순서와 세분화 기준을 정의한다.
  - `architecture.md`에서 반드시 참조한다.
- `docs/standard/coding_guidelines_project.md`
  - 프레임워크 특화 규칙, DTO postfix, 프로젝트 전용 네이밍, 트랜잭션 관례처럼 core에 두기 어려운 내용을 둔다.
- `docs/standard/testing_profile.md`
  - 테스트 실행 명령, 환경 준비, coverage 기준, 통합 테스트 의존성을 정의한다.

## 권장 로컬 `docs/harness_guide.md`

```md
# Project Harness Guide

## 공통 규칙

- `vendor/harness-kit/docs/harness_guide.md`

## 프로젝트 전용 규칙

- `docs/standard/architecture.md`
- `docs/standard/implementation_order.md`
- `docs/standard/coding_guidelines_project.md`
- `docs/standard/testing_profile.md`
```

## 작성 원칙

- project overlay는 core를 다시 설명하지 않는다.
- 여러 프로젝트에서 반복되는 규칙은 overlay가 아니라 core로 승격한다.
- 특정 프로젝트에만 필요한 규칙만 overlay에 남긴다.
