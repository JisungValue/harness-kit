# Kotlin Coding Conventions Template

## 목적

이 문서는 Kotlin 프로젝트 또는 Kotlin 모듈에 적용할 언어별 convention 초안이다.
가능하면 `Effective Kotlin` 성격의 실무 원칙을 따르되, Kotlin의 null-safety, 불변성, 표현력, structured concurrency 장점을 기본값으로 활용한다.

## 사용 방법

- 필요한 항목만 `docs/standard/coding_conventions_project.md`에 복사 또는 병합한다.
- 다중 언어 프로젝트면 Kotlin 전용 문서로 분리한 뒤 프로젝트 문서에서 참조해도 된다.
- framework, runtime, build tool, serialization, persistence 기술에 강하게 묶인 규칙은 `[프로젝트 결정 필요]`로 남긴다.

## 코드 스타일과 convention 분리

- import 위치/정렬, 공백, 줄바꿈, brace 위치, line length, unused import 같은 기계적으로 판별 가능한 규칙은 formatter/linter/build 또는 CI check로 강제한다.
- 이 문서는 자동 검사로 대체하기 어려운 판단 규칙과 예외 기준을 남긴다.
- tool 설정으로 고정 가능한 스타일 규칙은 여기서 길게 반복하지 않는다.

## 공통 품질 규칙 참조

- 공통 boundary translation, 에러 처리, 테스트 책임, 범위 제한 규칙은 `docs/standard/coding_guidelines_core.md`를 따른다.
- 이 문서는 그 위에 Kotlin에서 반복적으로 결정해야 하는 언어별 선택 기준만 추가한다.

## 적용 전 결정

- 기준 Kotlin 버전과 주 타깃 런타임(JVM, Android, Multiplatform 등)을 먼저 정한다.
- K2 compiler, explicit API mode, context receivers 같은 옵션성 기능은 `[프로젝트 결정 필요]`로 남긴다.
- Java interop 비중, coroutine 사용 범위, serialization 방식, reflection 허용 범위를 함께 정한다.

## 런타임과 언어 기능 검토 예시

- JVM 중심 프로젝트면 platform type 정리, Java interop, annotation/serialization 전략을 먼저 정한다.
- Android 또는 UI 환경이면 lifecycle과 cancellation 경계, state holder 패턴, dispatcher 사용 기준을 함께 정한다.
- Multiplatform 프로젝트면 공통 모듈 추출과 `expect/actual` 경계를 실제 중복 감소가 있을 때만 도입한다.
- coroutine, `Flow`, value class, compiler option은 기본 강제가 아니라 프로젝트 맥락에 맞는 선택 기준으로 남긴다.

## 참조 관점

- 아래 항목은 `Effective Kotlin`의 좋은 코드/코드 설계/효율성 분류와 `Kotlin in Action`의 언어 기능, interop, coroutine/flow 주제를 project-facing bootstrap convention으로 재정리한 것이다.
- 책 내용을 그대로 복제하지 않고, project-facing bootstrap 자산에서 바로 복사하거나 현지화할 수 있는 Kotlin-specific 선택 기준만 남긴다.

## 타입과 모델링

- 기본 선택지는 `var`보다 `val`이다.
- null 가능성은 타입으로 우선 표현하고, `!!`는 마지막 수단으로만 사용한다.
- platform type은 Java 경계에서 최대한 빨리 nullable/non-null 계약으로 정규화한다.
- nullable collection과 collection of nullable element를 혼동하지 않도록 타입 의미를 분명히 한다.
- 결과가 없을 가능성이 있으면 nullable, `Result`, sealed result, 빈 컬렉션 중 하나로 프로젝트 기준을 통일한다.
- 값 중심 모델은 `data class`를 우선 검토하되, 식별성/수명주기/프록시가 핵심이면 일반 클래스를 유지한다.
- primitive wrapper가 도메인 의미와 검증을 명확히 하면 `@JvmInline value class`를 검토한다.
- 닫힌 상태 집합과 결과 모델은 `sealed interface` 또는 `sealed class`를 우선 검토한다.
- global state가 아닌 명시적 싱글턴 의미가 있을 때만 `object` 또는 `data object`를 사용한다.
- enum은 값 목록과 닫힌 선택지를 표현할 때 사용하고, 더 복잡한 상태 전이는 sealed hierarchy가 더 나은지 검토한다.

## 객체 생성과 API 설계

- secondary constructor보다 factory function이나 primary constructor + named optional args가 더 단순한지 먼저 검토한다.
- 복잡한 객체 생성은 DSL이나 builder 스타일이 실제로 읽기 쉬울 때만 도입한다.
- 의존성은 직접 생성보다 주입을 우선 검토한다.
- Boolean flag 인자가 의미를 숨기면 named argument, 별도 함수, 명시적 타입으로 분리한다.
- 기본값과 named argument로 읽기 쉬워질 수 있으면 overload보다 우선 검토한다.
- 타입 추론이 계약을 흐리면 명시적 타입 선언을 추가한다.
- 프로퍼티는 상태를 표현하고, 비용 큰 연산이나 부수효과는 함수로 드러낸다.
- `Unit?` 반환이나 nullable side-effect API는 기본 선택지로 두지 않는다.

## 함수와 추상화 설계

- 각각의 함수는 가능한 한 하나의 추상화 수준으로 유지한다.
- 반복되는 알고리즘과 knowledge는 중복하지 않는다.
- 재사용 가치가 높은 알고리즘은 제네릭으로 일반화할 수 있는지 검토한다.
- 타입 매개변수 이름은 표준 관례를 따르되, 바깥 타입 매개변수와 shadowing되지 않게 유지한다.
- variance(`out`, `in`)는 producer/consumer 의미가 분명할 때만 선언한다.
- top-level function은 특정 타입의 부수속물이 아니라 모듈 공용 동작일 때만 사용한다.
- extension function은 자연스러운 vocabulary 확장일 때만 사용하고, import 없이는 발견하기 어려운 핵심 로직을 숨기지 않는다.
- member extension은 발견성과 dispatch 이해를 어렵게 하면 피한다.
- interface, adapter, facade 같은 추상화는 외부 변경으로부터 코드를 실제로 보호할 때만 도입한다.
- 가시성은 가능한 최소로 유지한다.
- 중요한 계약, failure mode, thread-safety, nullability는 문서와 타입으로 정의한다.

## 컬렉션과 데이터 처리

- 작은 컬렉션 처리나 한 번의 순회가 더 읽기 쉬우면 collection 연산보다 명시 loop를 선택한다.
- `List`/`Set`/`Map`의 read-only view와 truly immutable collection을 혼동하지 않도록 프로젝트 기준을 분명히 한다.
- `Sequence`는 처리 단계가 둘 이상이고 laziness 이득이 실제로 있을 때만 사용한다.
- `asSequence()`를 습관적으로 붙이지 않고, 실제 비용 감소와 가독성 이점을 비교한다.
- `Flow`는 비동기 스트림, backpressure, cancellation 모델이 필요한 경우에만 사용하고 단순 일회성 값 전달에 남용하지 않는다.
- 요소들을 key 기반으로 반복 조회하면 `Map`으로 재구성할 수 있는지 검토한다.
- 단순 `groupBy`보다 `groupingBy`가 메모리/연산 측면에서 더 적합한지 검토한다.
- `map/filter/groupBy/associate` 체인이 커질수록 연산 횟수를 줄일 수 있는지 다시 확인한다.
- 성능이 중요한 경로는 원시형 배열이나 primitive specialization을 검토한다.
- mutation이 실제로 더 단순하고 빠르면 mutable collection을 제한적으로 사용한다.
- 목적에 맞는 컬렉션 타입(`List`, `Set`, `Map`, `ArrayDeque`, `LinkedHashMap` 등)을 명시적으로 선택한다.

## 예외와 결과 표현

- precondition 위반은 `require`, 상태 위반은 `check`, 도달 불가 분기는 `error`처럼 의도가 드러나는 표준 함수를 우선 사용한다.
- 모든 실패를 `Result`로 감싸기보다 nullable, sealed result, exception 중 호출자가 가장 명확히 이해할 수 있는 계약을 선택한다.
- broad `runCatching`으로 큰 블록 전체를 감싸 핵심 제어 흐름을 숨기지 않는다.
- `CancellationException`을 일반 실패처럼 삼키지 않고 coroutine cancellation 의미를 보존한다.
- 사용자 정의 오류보다 표준 오류 타입과 표준 precondition 도구를 우선 검토한다.
- 테스트 가능성과 계약 재현성은 언어 기능 선택의 일부로 본다.

## 동시성과 비동기

- shared mutable state보다 immutability, confinement, message passing으로 임계 영역 자체를 줄일 수 있는지 먼저 검토한다.
- coroutine은 structured concurrency 안에서 사용하고 `GlobalScope`는 기본 선택지로 쓰지 않는다.
- `suspend` 함수는 실제 비동기/취소 가능 경계를 표현할 때만 사용한다.
- dispatcher 선택은 호출자 책임인지 내부 구현 책임인지 프로젝트 기준을 정한다.
- blocking I/O와 CPU-bound 작업은 서로 다른 dispatcher 전략이 필요한지 분리해 검토한다.
- `launch`와 `async`는 fire-and-forget인지 결과 수집인지 의도를 분명히 나눠 사용한다.
- `Flow`는 cold/hot/shared/state 구분이 실제 모델에 도움이 될 때만 사용한다.
- `buffer`, `conflate`, `debounce`, `flowOn`, `catch`, `retry` 같은 연산자는 의미와 취소 모델이 더 명확해질 때만 사용한다.
- correctness를 sleep, timing, scheduler 우연성에 기대지 않는다.

## Interop, Reflection, Serialization

- Java API는 platform type을 그대로 전파하지 말고 Kotlin 경계에서 계약을 명시화한다.
- Kotlin public API를 Java에서도 쓸 계획이면 named/default parameter 의존, top-level 선언, companion API 노출 방식을 함께 검토한다.
- primitive/nullability/checked exception 차이 때문에 Java와 Kotlin 양쪽 호출자가 다르게 오해하지 않게 계약을 문서화한다.
- annotation은 명명 패턴보다 선언적 메타데이터가 실제로 더 안전할 때 사용한다.
- reflection은 꼭 필요할 때만 도입하고, 명시적 계약이나 code generation으로 대체 가능한지 먼저 검토한다.
- serialization 방식은 `kotlinx.serialization`, Jackson 등 프로젝트 표준을 정하고 혼용을 최소화한다.
- compiler plugin, annotation processor, reflection 기반 magic은 핵심 흐름을 숨기지 않는 범위에서만 허용한다.
- Lombok, Jackson, JPA proxy 같은 Java 생태계 도구와의 interop 제약은 `[프로젝트 결정 필요]`로 남긴다.

## Import 와 Dependency 사용 관례

- tool이 강제하는 import 순서와 format 규칙을 우선 따른다.
- typealias는 긴 타입을 줄이기보다 도메인 의미가 더 선명해질 때만 사용한다.
- operator overload, infix function, 구조 분해, 위임 프로퍼티는 문법적 편의보다 의미가 더 선명해질 때만 사용한다.
- delegated property는 lazy initialization, observable state, backing store 추상화처럼 명확한 목적이 있을 때만 사용한다.
- `lazy` 초기화는 비용, thread-safety 모드, 수명주기와 맞는지 확인한다.
- DSL은 프로젝트 전체 readability를 실제로 높일 때만 도입하고 숨은 부수효과를 만들지 않는다.

## 패키지와 파일 구조

- 패키지 구조는 프로젝트의 구조 문서가 정한 책임 경계를 먼저 드러내고, framework 중심 그룹화만 남지 않게 정한다.
- public 타입 이름은 역할 중심 명사로 두고, 구현 상세가 드러나는 `Impl`, `Util`, `Helper` 남용은 피한다.
- 하나의 파일에는 함께 변경될 이유가 높은 선언만 둔다. 붙어 다니지 않는 extension, top-level constant, helper를 관성적으로 한 파일에 몰아넣지 않는다.
- `data class`, `sealed hierarchy`, `value class`는 파일 배치만으로도 관계가 읽히게 유지한다.

## 테스트 관례 초안

- 테스트 이름은 동작과 기대 결과를 읽기 쉬운 문장으로 작성한다.
- coroutine 테스트는 실제 비동기 경계를 드러내는 경우에만 사용하고 임의 sleep 기반 검증은 피한다.
- `runTest`, test dispatcher, virtual time, Turbine 사용 여부를 프로젝트 기준으로 정한다.
- `data class`, `sealed hierarchy`, `value class` 선택은 값 비교, exhaustiveness, serialization/interop 관점에서 테스트로 확인한다.
- mock은 외부 협력 경계에서만 제한적으로 사용하고, 상태 검증과 값 비교로 충분한 경우 우선 단순하게 유지한다.
- framework 통합 테스트는 실제 연결 책임이 있는 위치에만 사용하고, 단위 테스트로 충분한 책임까지 과도하게 끌어오지 않는다.

## 자주 생기는 품질 리스크와 금지 패턴

- `!!` 남용
- 여러 scope function을 겹쳐 receiver와 부수효과가 흐려지는 코드
- `data class`를 mutable entity처럼 사용하는 설계
- 모든 반환값을 nullable 또는 `Result`로 통일해 오히려 의미가 흐려지는 계약
- 작은 데이터 처리에도 습관적으로 `Sequence`, `Flow`를 붙여 디버깅 난도를 높이는 코드
- coroutine 안에서 blocking 호출을 숨기는 코드
- platform type을 그대로 내부 레이어로 퍼뜨리는 interop 코드
- reflection, annotation magic, compiler plugin 의존으로 핵심 흐름을 숨기는 구조

## 확인 필요 항목

- 기준 Kotlin 버전과 target runtime(JVM/Android/MPP)
- formatter와 lint 도구(`ktlint`, `detekt`, `spotless` 등) 및 import/format 규칙 자동 강제 범위
- coroutine 테스트 도구(`kotlinx-coroutines-test`, `Turbine` 등)와 dispatcher 정책
- Java interop, nullability annotation, transaction 사용 원칙
- serialization 방식(`kotlinx.serialization`, Jackson 등) `[프로젝트 결정 필요]`
- explicit API mode, context receivers, compiler plugin, reflection 사용 여부 `[프로젝트 결정 필요]`
