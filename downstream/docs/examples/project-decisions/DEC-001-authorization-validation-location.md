# DEC-001-authorization-validation-location

- Status: Accepted
- Type: Policy
- Date: 2026-04-13
- Related Docs:
  - docs/project/standards/architecture.md
  - docs/project/standards/coding_conventions_project.md
- When To Update:
  - 인증 진입 지점이 filter/interceptor/controller 중 다른 위치로 바뀔 때
  - 인증 실패 응답 규칙이 바뀔 때
  - principal 주입 방식이 바뀔 때

## Context

현재 프로젝트는 HTTP 요청에서 `Authorization` 헤더를 사용한다.
여러 controller와 use case가 인증된 사용자 정보를 전제로 동작하므로,
인증 검증 책임이 여러 계층에 흩어지면 다음 세션마다 구현 품질이 달라질 수 있다.

## Decision

`Authorization` 헤더의 존재 여부, 형식 검증, 토큰 검증은 HTTP 진입 계층의 auth filter에서 담당한다.

controller는 이미 검증된 principal 또는 auth context만 받는다.
service/use case는 헤더 원문을 직접 읽거나 검증하지 않는다.

## Rationale

인증 검증 책임을 filter에 고정하면 모든 요청 경로에서 같은 기준을 적용할 수 있고,
controller/service가 인증 세부사항에 오염되지 않는다.
다음 harness 세션도 같은 책임 경계를 재사용할 수 있다.

## Consequences

- controller와 service는 `Authorization` 헤더를 직접 파싱하지 않는다.
- 인증 실패는 business exception이 아니라 auth boundary failure로 처리한다.
- 인증 방식이 바뀌면 filter와 auth context 계약을 먼저 수정해야 한다.

## Related Docs

- docs/project/standards/architecture.md
- docs/project/standards/coding_conventions_project.md

## When To Update

- filter가 아닌 다른 계층이 인증 책임을 맡게 될 때
- principal/context 전달 방식이 바뀔 때
- 인증 실패 응답 정책이 바뀔 때
