# Kotlin Coding Conventions Template

## 목적

이 문서는 Kotlin 프로젝트 또는 Kotlin 모듈에 적용할 언어별 convention 초안이다.

## 사용 방법

- 필요한 항목만 `docs/standard/coding_conventions_project.md`에 복사 또는 병합한다.
- 다중 언어 프로젝트면 Kotlin 전용 문서로 분리한 뒤 프로젝트 문서에서 참조해도 된다.

## 기본 규칙

- null 가능성은 타입 시스템으로 우선 표현하고, `!!`는 마지막 수단으로만 사용한다.
- scope function(`let`, `run`, `apply`, `also`, `with`)은 의도가 더 분명해질 때만 사용한다.
- data class, sealed class, extension function은 언어 장점을 살리는 범위에서 쓰되 책임을 숨기지 않게 유지한다.
- 경계 계층에서 외부 모델을 domain 또는 application 관점 타입으로 번역한다.
- coroutine 사용 시 dispatcher 전환, cancellation, blocking 호출 경계를 문서로 분명히 한다.

## 테스트 관례 초안

- 테스트 이름은 동작과 기대 결과를 읽기 쉬운 문장으로 작성한다.
- coroutine 테스트는 실제 비동기 경계를 드러내는 경우에만 사용하고 임의 sleep 기반 검증은 피한다.
- mock은 외부 협력 경계에서만 제한적으로 사용하고, data class 비교와 상태 검증으로 충분한 경우 우선 단순하게 유지한다.

## 확인 필요 항목

- formatter와 lint 도구(`ktlint`, `detekt`, `spotless` 등)
- coroutine 테스트 도구와 dispatcher 정책
- Java interop, nullability annotation, transaction 사용 원칙
