# Requirements

## 기능 요구사항

- task workspace는 현재 Phase, 현재 gate, 마지막 승인된 Phase, 허용 write-set, 잠긴 경로, stale 상태, 다음 액션을 담는 `phase_status.md`를 가질 수 있어야 한다.
- `phase_status.md`가 있는 task에서는 runtime gate 상태와 허용 write-set 해석이 그 파일을 우선 기준으로 해야 한다.
- `scripts/validate_phase_gate.py`는 `phase_status.md`를 읽고 candidate path 또는 git 변경분이 허용 write-set과 잠긴 경로를 위반하는지 검사해야 한다.
- validator는 stale artifact가 locked path에 포함되는지, `phase_status.md` 자체가 허용 write-set에 포함되는지 같은 기본 정합성도 검사해야 한다.
- project-facing 문서와 template은 `phase_status.md`의 역할, lifecycle, validator 사용법을 설명해야 한다.

## 비기능 요구사항 또는 품질 요구사항

- validator 출력은 왜 실패했는지 바로 이해할 수 있게 명확해야 한다.
- task runtime state 구조는 현재 문서 체계 위에 얹는 최소 변경이어야 한다.
- downstream bundle에 포함되는 boundary와 테스트가 함께 갱신돼야 한다.

## 입력/출력

- 입력:
  - `docs/harness/common/process_policy.md`
  - `docs/harness/common/artifact_policy.md`
  - `docs/harness/common/audit_policy.md`
  - `docs/harness_guide.md`
  - `docs/downstream_harness_flow.md`
  - `bootstrap/docs/quickstart.md`
  - `docs/templates/task/*`
  - `maintainer/docs/downstream_bundle_boundary.md`
  - `tests/*bundle*`, `scripts/check_harness_docs.py`
- 출력:
  - `phase_status.md` template와 sample
  - `scripts/validate_phase_gate.py`
  - 관련 문서/테스트 갱신

## 제약사항

- task 종료 전에는 `phase_status.md`를 기본 유지 대상으로 본다.
- task 종료 후 삭제는 허용하지만, 그 이전에는 runtime state를 복원 가능하게 남겨야 한다.
- validator는 git repo가 있는 downstream 프로젝트를 기본 전제로 두되, `--paths`로 preflight 검사를 지원해야 한다.

## 예외 상황

- task가 완료 상태가 아니면 `Next Action`은 비어 있으면 안 된다.
- stale artifact가 locked path에 포함되지 않으면 state file 자체를 invalid로 본다.

## 성공 기준

- `phase_status.md`가 공통 artifact와 template로 추가된다.
- `scripts/validate_phase_gate.py`와 관련 테스트가 통과한다.
- bundle boundary와 bundle 테스트가 새 script를 포함하도록 갱신된다.
- `python3 scripts/check_harness_docs.py`와 관련 test suite가 통과한다.
