# Harness Kit

여러 프로젝트에서 공통으로 재사용할 수 있는 Harness 기본 패키지다.

## 목적

- 프로젝트마다 Harness 절차와 공통 규칙을 처음부터 다시 작성하지 않도록 한다.
- 공통 Phase, 공통 정책, 공통 산출물 템플릿, 공통 예시를 한 곳에서 관리한다.
- 프로젝트별 문서는 공통 규칙 위에 얇은 overlay만 추가하도록 한다.

## 디렉터리 구조

- `docs/harness_guide.md`
  - kit의 공통 진입점이다.
- `docs/harness/common/`
  - process, artifact, audit, testing, validation, lightweight 정책을 둔다.
- `docs/phase_*`
  - 각 Phase의 구현 기준과 감사 기준을 둔다.
- `docs/standard/coding_guidelines_core.md`
  - 여러 프로젝트에서 공통으로 재사용할 수 있는 코드 품질 규칙을 둔다.
- `docs/templates/task/`
  - 새 task를 시작할 때 복사해서 쓸 기본 산출물 템플릿을 둔다.
- `docs/examples/sample-task/`
  - 기대 산출물 밀도를 보여 주는 예시 task를 둔다.
- `docs/project_overlay/`
  - 프로젝트별로 추가 작성해야 하는 문서와 템플릿을 둔다.
- `harness.log`
  - harness-kit core의 의미 있는 변경과 감사 결과를 남긴다.

## 무엇이 Core 인가

다음 항목은 공통 Core로 관리한다.

- Phase 운영 순서와 감사 반복 규칙
- task workspace 구조와 산출물 최소 템플릿
- 감사 입력물 기준과 결과 형식
- 검증 기록 형식
- 경량 태스크 예외 운영 원칙
- 코드 품질, 리팩터링 범위 제한, 에러 처리, 로깅, 경계 번역, 리뷰 체크리스트

## 무엇이 Project Overlay 인가

다음 항목은 프로젝트마다 별도로 유지한다.

- 프로젝트 아키텍처 문서
- 프레임워크 또는 런타임 특화 규칙
- 인프라 또는 클라우드 특화 규칙
- DTO postfix, 네이밍 세부 규칙처럼 프로젝트 결정이 필요한 규칙
- 테스트 실행 명령, 실제 coverage 기준, 로컬 개발 규칙

## 권장 도입 순서

1. `harness-kit`를 새 프로젝트로 가져온다.
2. 프로젝트 로컬 `docs/harness_guide.md`를 얇은 index 문서로 만든다.
3. `docs/project_overlay/`의 템플릿을 기준으로 프로젝트 전용 문서를 작성한다.
4. `docs/templates/task/`를 복사해 첫 task를 시작한다.
5. 실제 task 몇 개를 돌린 뒤 project overlay만 보강한다.

## 최소 프로젝트 문서 세트

- `docs/harness_guide.md`
- `docs/standard/architecture.md`
- `docs/standard/coding_guidelines_project.md`
- `docs/standard/testing_profile.md`

## Kit 유지보수 기록 규칙

- `harness-kit` core에 의미 있는 변경이 있으면 같은 변경에서 루트 `harness.log`를 반드시 함께 갱신한다.
- `harness.log` 항목마다 `변경`과 `이유`를 모두 적는다. 둘 중 하나라도 빠지면 기록으로 인정하지 않는다.
- 기록 대상은 공통 규칙, phase 기준, audit 기준, 템플릿, 예시, core 문서 구조처럼 여러 프로젝트에 영향을 줄 수 있는 변경이다.
- 단순 오탈자, 링크 수정, 비의미적 포맷 정리만 예외로 둘 수 있다. 애매하면 기록한다.
- 변경 후에는 구현 주체와 분리된 subagent audit를 반드시 수행한다.
- audit는 `changed-parts`와 `whole-harness`를 구분한다. 전자는 바뀐 부분과 인접 영향을 보고, 후자는 전체 흐름과 core 일관성을 본다.
- maintainer agent는 변경과 audit 요약을 같은 작업에서 `harness.log`에 기록한다.

## 운영 원칙

- 공통 Core는 가능한 한 안정적으로 유지한다.
- 프로젝트별 차이는 overlay에 두고 core를 쉽게 포크하지 않는다.
- 새 규칙이 여러 프로젝트에서 반복되면 core로 승격한다.
- 특정 프로젝트에만 필요한 규칙은 overlay에 남긴다.
