# Plan

## 변경 대상 파일 또는 모듈

- `README.md`
- `docs/quickstart.md`
- `docs/project_overlay/README.md`
- `docs/project_overlay/first_success_guide.md`
- `docs/project_overlay/local_diagnostics_and_dry_run.md`
- `scripts/check_harness_docs.py`

## 레이어별 작업 계획

- quickstart를 canonical 시작 문서로 더 분명히 고정한다.
- overlay/README와 세부 가이드에서 quickstart 우선, detailed reference 후순위 구조를 분명히 한다.
- doc guard에서 example sample validation과 phrase-level 강결합 검사를 줄인다.
- examples는 advanced/reference 위치라는 설명을 보강한다.

## 테스트 계획

- `python3 scripts/check_harness_docs.py`

## 문서 반영 계획

- onboarding 역할 분리를 `README.md`, `quickstart.md`, overlay 문서에 반영한다.
- 관련 `docs/decisions/README.md` 또는 `DEC-###-slug.md` 읽기/수정/생성 필요 여부: 해당 없음
- 새 decision이 필요하면 index 갱신 계획: 해당 없음

## 비범위

- validator semantics 변경
- bundle boundary 재분류

## 리스크 또는 확인 포인트

- doc guard를 과도하게 완화하면 실제 구조 drift까지 놓칠 수 있으므로 구조/경로 중심 검사는 유지한다.
- quickstart를 canonical로 세우되 세부 문서의 유용한 참고 정보는 잃지 않게 해야 한다.
