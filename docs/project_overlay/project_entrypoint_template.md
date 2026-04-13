# Project Harness Entry Point

이 파일은 프로젝트 로컬 문서 entrypoint다.

## 문서 역할

- agent runtime은 `AGENTS.md`에서 이 파일로 들어온다.
- 사람은 이 파일에서 vendored core guide와 프로젝트 전용 overlay 문서를 함께 찾는다.

## 실행 계약

- 이 문서에 들어온 runtime 또는 작업자는 `공통 규칙`, `프로젝트 전용 규칙`에 적힌 문서를 순서대로 모두 읽고 적용한 뒤에만 구현 또는 판단을 진행한다.
- vendored core guide는 공통 규칙 기준을 주고, `docs/standard/*` 문서는 프로젝트 전용 기준을 주므로 둘 중 하나만 읽고 멈추지 않는다.

## 공통 규칙

- `vendor/harness-kit/docs/harness_guide.md`

## 프로젝트 전용 규칙

- `docs/standard/architecture.md`
- `docs/standard/implementation_order.md`
- `docs/standard/coding_conventions_project.md`
- `docs/standard/quality_gate_profile.md`
- `docs/standard/testing_profile.md`
- `docs/standard/commit_rule.md`
