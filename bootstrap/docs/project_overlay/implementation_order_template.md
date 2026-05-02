# Implementation Order

## 목적

이 문서는 Phase 2에서 이 프로젝트가 레이어를 어떤 순서와 단위로 구현하는지 정의한다.

- 이 문서는 프로젝트 기본 구현 순서를 정의하는 문서다.
- 특정 기능, user story, API endpoint를 이번 TASK에서 어떤 순서로 구현할지는 여기보다 `plan.md`에 남긴다.
- 즉, `implementation_order.md`는 `domain -> application -> adapter` 같은 프로젝트 기본 흐름을 다루고, `POST /signup -> POST /login` 같은 task-specific 순서는 다루지 않는다.

## 기본 원칙

- 레이어 순서와 세분화 기준은 `docs/project/standards/architecture.md`의 실제 구조와 의존성 방향을 기준으로 정한다.
- 필요한 레이어만 선택해 진행한다.
- 선택한 레이어는 의존성 안쪽부터 바깥쪽 순서로 진행한다.
- 각 선택 레이어는 `테스트 작성 -> 구현 -> 감사` 순서를 따른다.

## 프로젝트 권장 순서

- 이 프로젝트의 실제 레이어 순서를 명시한다.
- 레이어가 일부 없거나 통합되어 있으면 그 이유를 함께 남긴다.
- endpoint, screen, user story 같은 기능 backlog 순서를 그대로 옮기지 않는다.
- 기능 구현 순서는 이번 TASK의 `plan.md`가 이 문서를 참고해 별도로 정한다.

## 구현 단위 추측 금지

이 문서는 class/file 단위 구현 순서가 아니라 layer/boundary 단위 기본 구현 순서를 정의한다. endpoint, screen, user story, 기능 backlog 순서를 canonical 구현 순서로 옮기지 않는다.

- 아직 존재하지 않거나 승인되지 않은 클래스/파일을 구현 단위로 나열하지 않는다.
- 기획서만 보고 `UserController`, `AuthService`, `UserRepository`, `OrderUseCase` 같은 class-level 구현 단위를 만들지 않는다.
- repo에 없는 파일 경로나 패키지 경로를 project standard의 canonical 구현 단위처럼 쓰지 않는다.
- 특정 task의 feature/API 구현 순서는 task `plan.md`에 남긴다.
- 구현 중 실제로 확인된 구체 이름이나 구조는 근거와 함께 `implementation_notes.md`, task `plan.md`, 또는 필요한 경우 `docs/project/decisions/*`에 남긴다.

구조가 미확정이면 abstract layer/responsibility level로만 순서를 남기고, 미확정 항목은 명시적으로 표시한다.

- 허용 예: `domain responsibility -> application boundary -> adapter boundary`
- 허용 예: `경계 번역 책임: [프로젝트 결정 필요]`
- 금지 예: `UserController -> AuthService -> UserRepository`
- 금지 예: `POST /signup -> POST /login`를 프로젝트 표준 구현 순서로 기록

## 레이어 세분화 기준

- 필요하면 레이어를 하위 단위로 나눠 진행한다.
- 예: `adapter`를 `outbound`, `persistence`, `external client` 같은 경계별 단위로 세분화
- 세분화 순서는 의존성 변화가 작은 단위부터 정의한다.

## 기록 규칙

- 이번 TASK에서 선택한 레이어 순서와 세분화 근거를 `implementation_notes.md`에 남긴다.
- 이번 TASK에서 어떤 API 또는 기능부터 구현할지는 `plan.md`에 남긴다.
- 공통 규칙과 다른 예외 적용이 필요하면 근거와 승인 여부를 함께 남긴다.
