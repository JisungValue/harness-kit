# Architecture

## 목적

이 문서는 프로젝트의 실제 레이어 구조와 의존성 방향을 정의한다.

## 구현 순서 문서와의 관계

- `docs/project/standards/implementation_order.md`는 이 문서의 레이어 구조와 의존성 방향을 기준으로 작성한다.
- 이 문서는 구조와 경계를 정의하고, 프로젝트 기본 레이어 진행 순서는 `implementation_order.md`에서 확정한다.
- 특정 TASK에서 어떤 API나 기능부터 구현할지는 `implementation_order.md`가 아니라 `plan.md`에서 정한다.

## 레이어 또는 모듈 구조

- 프로젝트가 실제로 사용하는 레이어 또는 모듈 명칭
- 각 레이어 또는 모듈의 책임
- 경계 번역 책임을 수행하는 위치

프로젝트에 맞는 실제 명칭과 패키지 구조를 위 항목에 맞춰 정리한다.

## 추측 금지와 근거 수준

greenfield 프로젝트에서는 실제 레이어, 모듈, 패키지, 클래스명이 아직 없을 수 있다. 이 문서는 추측성 설계 초안이 아니라 근거가 있는 project standard이므로, 아래 세 범주를 구분해서 작성한다.

- 확정된 프로젝트 구조: repo에 이미 존재하거나, framework convention, 사용자 승인, `docs/project/decisions/*`, project architecture를 소유하는 기술 설계 문서로 근거가 확인된 구조
- 의도한 레이어/책임: 코드가 아직 없어도 설명할 수 있는 책임, 의존성 방향, 경계 번역 위치
- 미확정 구조 결정: 아직 근거가 부족해 open decision 또는 decision candidate로 남겨야 하는 이름, 경로, 모듈 경계

기획서만 보고 구체 클래스명/파일명/패키지명/모듈명을 추측하지 않는다. feature requirement, endpoint 목록, user story, screen 목록, product planning 문서만 보고 `UserController`, `AuthService`, `UserRepository`, `OrderUseCase` 같은 클래스명이나 `src/main/.../controller/UserController.kt` 같은 파일/패키지 경로를 확정 구조처럼 쓰지 않는다.

구체 이름이나 경로는 아래 근거 중 하나 이상이 있을 때만 쓴다.

- 해당 이름이나 경로가 이미 repo에 존재한다.
- 프로젝트가 이미 선택하고 문서화한 framework convention을 따른다.
- 사용자가 해당 이름/경로/구조 결정을 명시적으로 승인했다.
- `docs/project/decisions/*`에 해당 결정이 기록되어 있다.
- 기능 요구사항 문서가 아니라 project architecture를 소유하는 기술 설계 문서에서 온 값이다.

근거가 아직 없으면 아래처럼 미확정 상태를 드러낸다.

- `레이어/책임: [프로젝트 결정 필요]`
- `패키지/경로: [프로젝트 결정 필요; 기획서만 보고 추론하지 않음]`
- `확정 근거: [기존 코드 / 사용자 승인 / framework convention / decision record]`

코드가 없어도 의도한 책임 수준은 쓸 수 있지만, 구체 이름은 근거가 생길 때까지 미확정으로 둔다.

## 의존성 원칙

- 안쪽 레이어는 바깥 레이어를 직접 알지 않는다.
- 외부 모델, 저장 구조, transport 구조는 경계에서 번역한다.
- 실제 조립과 환경 설정은 bootstrap 또는 이에 준하는 레이어에 둔다.
