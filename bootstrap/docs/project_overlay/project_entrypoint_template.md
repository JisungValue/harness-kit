# Project Harness Entry Point

이 파일은 프로젝트 로컬 문서 entrypoint다.

## 문서 역할

- agent runtime은 `AGENTS.md`에서 이 파일로 들어온다.
- 사람은 이 파일에서 shipped process guide와 프로젝트 전용 overlay 문서를 함께 찾는다.

## 실행 계약

- 이 문서에 들어온 runtime 또는 작업자는 `공통 규칙`, `프로젝트 전용 규칙`에 적힌 문서를 순서대로 모두 읽고 적용한 뒤에만 구현 또는 판단을 진행한다.
- process guide는 공통 규칙 기준을 주고, `docs/project/standards/*` 문서는 프로젝트 전용 기준을 주므로 둘 중 하나만 읽고 멈추지 않는다.

## 공통 규칙

- `docs/process/harness_guide.md`

## 프로젝트 전용 규칙

- `docs/project/standards/architecture.md`
- `docs/project/standards/implementation_order.md`
- `docs/project/standards/coding_conventions_project.md`
- `docs/project/standards/quality_gate_profile.md`
- `docs/project/standards/testing_profile.md`
- `docs/project/standards/commit_rule.md`

## 프로젝트 결정 문서

- `docs/project/decisions/README.md`

- 현재 작업이 중요한 정책, 예외 처리 규칙, 책임 배치, 운영 결정을 건드리면 이 문서에서 관련 decision을 찾아 함께 읽고 갱신한다.
