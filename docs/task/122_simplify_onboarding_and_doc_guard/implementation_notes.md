# Implementation Notes

## 진행 로그

- quickstart를 canonical 시작 문서로 더 분명히 세우고, first-success/local diagnostics는 상세 reference로 내리는 방향으로 범위를 확정했다.
- 구현: `README.md`, `docs/quickstart.md`, `docs/project_overlay/README.md`, `docs/project_overlay/first_success_guide.md`, `docs/project_overlay/local_diagnostics_and_dry_run.md`에서 온보딩 중복을 줄이고 role wording을 정리했다.
- 구현: `scripts/check_harness_docs.py`에서 example sample validation과 phrase-level 결합 검사를 줄이고 구조/경로 중심 검사를 남겼다.

## 경량 검토 기록

- 해당 없음

## 구현 중 결정 사항

- repo-local 근거: `README.md`, `docs/quickstart.md`, `docs/project_overlay/README.md`, `docs/project_overlay/first_success_guide.md`, `docs/project_overlay/local_diagnostics_and_dry_run.md`, `scripts/check_harness_docs.py`
- repo에 없어 문서화/승인 대상으로 넘긴 결정: 없음

## 위임된 책임

- 없음

## 사용자 승인 필요 항목

- 없음

## 후속 태스크 후보

- README와 `docs/how_harness_kit_works.md`의 시작 경로 설명도 더 강하게 quickstart 중심으로 압축할 수 있다.
