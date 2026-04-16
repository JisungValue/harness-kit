# Requirements

## 기능 요구사항

- `docs/quickstart.md`는 downstream 사용자가 가장 먼저 보는 canonical 시작 문서로 읽혀야 한다.
- `README.md`와 `docs/project_overlay/README.md`는 quickstart를 먼저 가리키고, 세부 온보딩 문서는 reference 역할이 더 분명해야 한다.
- `docs/project_overlay/first_success_guide.md`와 `docs/project_overlay/local_diagnostics_and_dry_run.md`는 quickstart의 상세 reference로 읽히도록 표현을 정리해야 한다.
- `scripts/check_harness_docs.py`는 example 문서의 세부 표현과 sample validation 내용을 강하게 결합하지 않고, 구조/경로/핵심 섹션 위주로 검사해야 한다.
- examples는 유지하되 기본 소비 경로보다 advanced/reference 위치로 설명해야 한다.

## 비기능 요구사항 또는 품질 요구사항

- 경량화는 기존 핵심 validator와 runtime contract를 약화하지 않는 최소 변경이어야 한다.
- quickstart와 세부 문서 사이 역할 분리가 한눈에 읽혀야 한다.
- doc guard는 불필요한 표현 drift에는 덜 민감하고, 구조 drift에는 여전히 민감해야 한다.

## 입력/출력

- 입력:
  - `README.md`
  - `docs/quickstart.md`
  - `docs/project_overlay/README.md`
  - `docs/project_overlay/first_success_guide.md`
  - `docs/project_overlay/local_diagnostics_and_dry_run.md`
  - `scripts/check_harness_docs.py`
- 출력:
  - 경량화된 onboarding 문서 설명층
  - example/phrase-level 결합이 완화된 doc guard

## 제약사항

- existing quickstart/adoption/upgrade 경로는 유지한다.
- example 문서를 삭제하지 않고 기본 진입점에서의 노출만 줄인다.

## 예외 상황

- 세부 reference 문서가 필요 없는 사용자는 quickstart만으로 시작할 수 있어야 한다.
- maintainer smoke validation 문서와 examples는 남기되 guard의 강결합 대상으로 취급하지 않는다.

## 성공 기준

- quickstart가 유일한 기본 시작 문서로 읽힌다.
- 세부 문서는 reference 성격이 더 분명해진다.
- doc guard가 example/문구 결합보다 구조 중심으로 동작한다.
- 관련 검증이 통과한다.
