# Plan

## 변경 대상 파일 또는 모듈

- `docs/templates/task/phase_status.md`
- `docs/harness/common/artifact_policy.md`
- `docs/harness/common/process_policy.md`
- `docs/harness/common/audit_policy.md`
- `docs/harness_guide.md`
- `docs/downstream_harness_flow.md`
- `bootstrap/docs/quickstart.md`
- `maintainer/docs/downstream_bundle_boundary.md`
- `scripts/validate_phase_gate.py`
- `scripts/check_harness_docs.py`
- `tests/test_validate_phase_gate.py`
- `tests/test_generate_downstream_bundle.py`
- 필요한 sample/task workspace 문서

## 레이어별 작업 계획

- `phase_status.md` template와 lifecycle 문안을 정의한다.
- 공통 policy와 guide에 runtime state file 및 hard-stop validator 사용 규칙을 반영한다.
- validator를 구현하고 bundle/test 경계에 포함시킨다.
- sample artifact와 현재 task workspace를 갱신한다.

## 테스트 계획

- `python3 scripts/check_harness_docs.py`
- `python3 -m unittest tests.test_validate_phase_gate tests.test_generate_downstream_bundle`

## 문서 반영 계획

- 공통 policy와 guide에 `phase_status.md` 및 validator 역할을 반영한다.
- sample task와 현재 task workspace에 `phase_status.md`를 추가한다.
- 관련 `docs/decisions/README.md` 또는 `DEC-###-slug.md` 읽기/수정/생성 필요 여부: 해당 없음
- 새 decision이 필요하면 index 갱신 계획: 해당 없음

## 비범위

- downstream project별 task runner 구현
- CI에서 phase gate를 자동 강제하는 workflow 추가

## 리스크 또는 확인 포인트

- validator가 지나치게 엄격하면 unrelated local changes까지 잡을 수 있으므로 `--paths` preflight 경로가 필요하다.
- phase_status lifecycle을 문서에 충분히 설명하지 않으면 삭제 시점이 다시 흔들릴 수 있다.
