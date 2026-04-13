# Unresolved Decision Validator

이 문서는 project overlay 문서에 남아 있는 미결정 placeholder를 어떤 기준으로 점검하는지 설명한다.

## 목적

- project overlay 템플릿이 존재하는 것과 프로젝트가 실제로 결정을 채운 상태를 구분한다.
- first success 시점에 허용 가능한 미결정과, Phase 2 전에 금지되는 미결정을 자동으로 나눈다.
- 로컬 실행과 CI 실행 둘 다 같은 스크립트로 처리한다.

## 실행 명령

프로젝트 루트에서 아래처럼 실행한다.

```bash
python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness first-success
python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness phase2
```

## 검사 대상 문서

- `docs/project_entrypoint.md`
- `docs/standard/architecture.md`
- `docs/standard/implementation_order.md`
- `docs/standard/coding_conventions_project.md`
- `docs/standard/quality_gate_profile.md`
- `docs/standard/testing_profile.md`
- `docs/standard/commit_rule.md`

## 검출 대상 표기

- `[프로젝트 결정 필요]`
- `[팀 결정 필요]`
- `TODO`
- `TBD`

## Readiness 규칙

### first-success

- 아래 항목은 허용된다.
  - `docs/standard/coding_conventions_project.md`의 일반 `[프로젝트 결정 필요]`
  - `docs/standard/quality_gate_profile.md`의 `[프로젝트 결정 필요]`
  - `docs/standard/commit_rule.md`의 `[팀 결정 필요]`
- 아래 항목은 금지된다.
  - `docs/standard/coding_conventions_project.md`에서 활성 언어/런타임이 아직 `[프로젝트 결정 필요]`인 상태
  - `docs/standard/coding_conventions_project.md`에서 bootstrap 기준 문서가 아직 `[프로젝트 결정 필요]`인 상태
  - `TODO`, `TBD` 같은 미완료 표기 전부
  - 허용 목록 밖 문서에 남아 있는 placeholder

### phase2

- 아래 항목만 허용된다.
  - `docs/standard/commit_rule.md`의 `[팀 결정 필요]`
- 아래 항목은 금지된다.
  - `docs/standard/coding_conventions_project.md`의 `[프로젝트 결정 필요]`
  - `docs/standard/quality_gate_profile.md`의 `[프로젝트 결정 필요]`
  - 허용 목록 밖 문서의 placeholder
  - `TODO`, `TBD` 전부

## 출력 방식

- 통과 시:
  - `overlay decision validation passed for readiness '...'`
  - 허용 가능한 미결정이 남아 있으면 함께 출력한다.
- 실패 시:
  - `overlay decision validation failed for readiness '...'`
  - 누락된 필수 문서와 blocking unresolved marker를 함께 출력한다.
  - canonical field가 비어 있으면 `Resolve these required canonical fields first:` 아래에 실제 문서 경로와 line 번호, 다음 수정 액션을 함께 출력한다.
  - 일반 blocking marker는 `Then resolve these blocking unresolved markers:` 아래에 출력한다.
  - 같은 readiness에서 허용 가능한 미결정이 있으면 `Still allowed after the blocking items above are fixed:` 아래에 참고용으로 출력한다.

## CI 사용

- 같은 스크립트를 CI step에서 실행해 된다.
- 예시:

```bash
python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness first-success
```

- 더 엄격한 게이트가 필요하면 Phase 2 진입 전 CI나 local check에서 `--readiness phase2`를 사용한다.
- unresolved placeholder와 별개로 문서 간 교차 계약도 보려면 `docs/project_overlay/cross_document_consistency_checker.md`를 함께 사용한다.
