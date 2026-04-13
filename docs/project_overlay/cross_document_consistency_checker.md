# Cross-Document Consistency Checker

이 문서는 project overlay 문서 세트가 서로 모순 없이 연결되어 있는지 확인하는 checker를 설명한다.

## 목적

- 필수 overlay 문서가 모두 있어도, 문서 간 참조와 책임 경계가 어긋난 상태를 자동으로 잡는다.
- unresolved placeholder 유무와 별개로, 문서 세트가 최소한 같은 구조와 역할 분리를 유지하는지 확인한다.
- local 실행과 CI 실행에서 같은 checker를 사용할 수 있게 한다.

## 실행 명령

프로젝트 루트에서 아래처럼 실행한다.

```bash
python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .
```

## 검사 대상 문서

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `docs/project_entrypoint.md`
- `docs/decisions/README.md`
- `docs/standard/architecture.md`
- `docs/standard/implementation_order.md`
- `docs/standard/coding_conventions_project.md`
- `docs/standard/quality_gate_profile.md`
- `docs/standard/testing_profile.md`
- `docs/standard/commit_rule.md`

## 현재 checker가 보는 교차 계약

### runtime instruction entrypoint와 local harness guide 연결

- `AGENTS.md`가 `docs/project_entrypoint.md`를 우선 읽을 문서로 연결하는지 본다.
- `CLAUDE.md`, `GEMINI.md`가 `AGENTS.md`를 공통 진입점으로 다시 가리키는지 본다.
- `AGENTS.md`가 linked document를 순서대로 모두 읽고 적용해야 한다는 traversal contract를 명시하는지 본다.
- adapter entrypoint도 `AGENTS.md` 이후 연결된 문서 체인을 끝까지 따르라고 설명하는지 본다.

### decisions index 연결

- `docs/project_entrypoint.md`가 `docs/decisions/README.md`를 프로젝트 결정 문서 entrypoint로 연결하는지 본다.
- `docs/decisions/README.md`가 architecture와 decision 문서의 역할 경계를 설명하는지 본다.
- index에 적힌 decision 문서가 실제로 존재하는지도 본다.

### harness guide와 standard 문서 세트

- `docs/project_entrypoint.md`가 project-local entrypoint 역할을 유지한 채 vendored core guide를 공통 규칙으로 참조하는지 본다.
- `docs/project_entrypoint.md`가 `공통 규칙`과 `프로젝트 전용 규칙` 문서를 함께 읽고 적용해야 한다는 contract를 명시하는지 본다.
- vendored core guide 경로가 실제 프로젝트에서 존재하는지도 본다.
- `docs/project_entrypoint.md`의 `프로젝트 전용 규칙` 섹션이 필수 standard 문서 세트를 빠짐없이 참조하는지 본다.
- `공통 규칙` 섹션이 공통 harness guide 경로를 포함하는지도 본다.

### architecture와 implementation order 연결

- `implementation_order.md`가 `architecture.md`를 기준 문서로 참조하는지 본다.

### quality gate와 testing profile의 책임 경계

- `quality_gate_profile.md`가 `testing_profile.md`를 참조하는지 본다.
- `testing_profile.md`가 `quality_gate_profile.md`를 참조하는지 본다.
- `testing_profile.md`가 test 명령, 필수 여부, 실행 시점, 실패 기준이 quality gate 문서 책임이라고 분명히 적는지 본다.
- `quality_gate_profile.md`의 test 섹션이 테스트 세부 범위를 `testing_profile.md`로 넘기는지도 본다.

### coding conventions와 language-specific 문서 참조

- `coding_conventions_project.md`가 `docs/standard/quality_gate_profile.md`를 책임 경계 문서로 참조하는지 본다.
- `bootstrap 출처 또는 기준 언어 문서`가 `.md` 경로인지 본다.
- bootstrap 기준 문서가 `bootstrap/language_conventions/...` 같은 repo-local path로 남아 있지 않은지도 본다.
- bootstrap 기준 문서 경로가 실제 프로젝트에서 존재하는지도 본다.

### commit rule과 품질/검증 흐름 연결

- `commit_rule.md`의 `커밋 전 최소 점검 항목`에 `compile`, `type`, `build`, `test` 또는 `테스트` 기준이 모두 남아 있는지 본다.

## 출력 방식

- 통과 시:
  - `overlay consistency validation passed.`
- 실패 시:
  - `overlay consistency validation failed.`
  - 어떤 문서에서 어떤 계약이 깨졌는지 bullet 목록으로 출력한다.

## unresolved decision validator와의 관계

- `validate_overlay_consistency.py`는 문서 간 연결, runtime instruction entrypoint 연결, 책임 경계를 본다.
- `validate_overlay_decisions.py`는 placeholder와 readiness 상태를 본다.
- 둘은 대체 관계가 아니라 보완 관계다.

## CI 사용

- 같은 스크립트를 CI step에서 바로 실행해 된다.
- 예시:

```bash
python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .
```
