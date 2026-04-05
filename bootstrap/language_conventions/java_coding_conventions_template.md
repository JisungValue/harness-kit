# Java Coding Conventions Template

## 목적

이 문서는 Java 프로젝트 또는 Java 모듈에 적용할 언어별 convention 초안이다.

## 사용 방법

- 필요한 항목만 `docs/standard/coding_conventions_project.md`에 복사 또는 병합한다.
- 다중 언어 프로젝트면 Java 전용 문서로 분리한 뒤 프로젝트 문서에서 참조해도 된다.

## 기본 규칙

- 패키지 이름은 소문자 기준으로 유지하고, 역할이 드러나는 패키지 경계를 우선한다.
- 공개 API의 null 허용 여부는 시그니처와 계약에서 분명히 드러낸다.
- 도메인 규칙과 프레임워크 어노테이션 의존 코드는 분리한다.
- 경계 계층에서는 외부 DTO, persistence model, transport model을 domain 또는 application 관점 타입으로 번역한다.
- checked/unchecked 예외 사용 원칙을 프로젝트 문서에서 정하고, raw infrastructure 예외를 core로 직접 흘리지 않는다.

## 테스트 관례 초안

- 테스트 이름은 시나리오와 기대 결과를 드러내게 작성한다.
- 테스트 더블은 협력 경계 검증에만 사용하고 내부 호출 순서 고정은 최소화한다.
- Spring 같은 프레임워크 통합 테스트는 실제 연결 책임이 있는 위치에만 사용하고, 단위 테스트로 충분한 책임까지 과도하게 끌어오지 않는다.

## 확인 필요 항목

- formatter와 lint 도구(`spotless`, `checkstyle`, `errorprone` 등)
- 테스트 스택(`JUnit`, `AssertJ`, `Mockito` 등)
- nullability, transaction, annotation 사용 원칙
