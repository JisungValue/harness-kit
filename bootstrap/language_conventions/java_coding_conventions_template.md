# Java Coding Conventions Template

## 목적

이 문서는 Java 프로젝트 또는 Java 모듈에 적용할 언어별 convention 초안이다.
가능하면 `Effective Java`의 실무 원칙을 따르되, 프로젝트가 선택한 JDK 버전에서 기본 제공하는 현대 Java 기능을 우선 활용한다.

## 사용 방법

- 필요한 항목만 `docs/project/standards/coding_conventions_project.md`에 복사 또는 병합한다.
- 다중 언어 프로젝트면 Java 전용 문서로 분리한 뒤 프로젝트 문서에서 참조해도 된다.
- framework, runtime, build tool, persistence 기술에 강하게 묶인 규칙은 `[프로젝트 결정 필요]`로 남긴다.

## 코드 스타일과 convention 분리

- import 위치/정렬, 공백, 줄바꿈, brace 위치, line length, unused import 같은 기계적으로 판별 가능한 규칙은 formatter/linter/build 또는 CI check로 강제한다.
- 이 문서는 자동 검사로 대체하기 어려운 판단 규칙과 예외 기준을 남긴다.
- tool 설정으로 고정 가능한 스타일 규칙은 여기서 길게 반복하지 않는다.

## 공통 품질 규칙 참조

- 공통 boundary translation, 에러 처리, 테스트 책임, 범위 제한 규칙은 `docs/process/common/coding_guidelines_policy.md`를 따른다.
- 이 문서는 그 위에 Java에서 반복적으로 결정해야 하는 언어별 선택 기준만 추가한다.

## 적용 전 결정

- 기준 JDK 버전을 `17+`, `21+`, `24+` 같은 대표 기준점 또는 그 이후 GA 버전 중 어디로 둘지 먼저 정한다.
- 하위 호환성 때문에 쓰지 못하는 기능과, 적극적으로 사용할 기능을 함께 문서화한다.
- preview 또는 incubator 기능은 기본값으로 강제하지 말고 `[프로젝트 결정 필요]`로 분리한다.

## 버전별 검토 예시

- 아래 항목은 대표 기준점 예시다. 프로젝트가 더 최신 GA 버전을 사용하면 같은 방식으로 새 표준 기능 채택 여부를 검토한다.

### Java 17+

- 불변 carrier, command/result, response projection처럼 값 중심 타입은 `record`를 우선 검토한다.
- 유한한 계층 구조는 `sealed class` 또는 `sealed interface`로 닫힌 모델을 표현한다.
- 여러 줄 문자열이 가독성을 높이면 text block을 사용하되, 들여쓰기와 escape 규칙을 테스트로 확인한다.
- `switch` 문이 값을 계산하는 책임이면 switch expression을 우선 검토한다.

### Java 21+

- blocking I/O 중심 동시성은 platform thread 풀 확장, 기존 executor 조정, virtual thread 중 어떤 방식이 더 단순하고 안전한지 비교 검토한다.
- 분기 조건이 타입과 구조를 함께 읽어야 하면 record pattern과 pattern matching for switch를 우선 검토한다.
- 순서가 중요한 컬렉션 API는 ad-hoc helper보다 sequenced collection 계열 표준 API를 우선 검토한다.
- virtual thread 도입 여부와 thread-local, transaction, MDC, 외부 라이브러리 호환성은 `[프로젝트 결정 필요]`로 남긴다.

### Java 24+

- 긴 stream 파이프라인이 읽기 어려우면 먼저 loop 또는 collector로 더 단순하게 표현할 수 있는지 검토한다.
- 그다음에도 상태 있는 파이프라인이 남고 gatherer가 더 읽기 쉬울 때만 stream gatherer 적용 가능성을 검토한다.
- 24+에서 표준화된 기능으로 대체 가능한 보조 유틸리티나 관성적 패턴이 있으면 새 라이브러리 추가보다 JDK 표준 기능을 우선 검토한다.
- preview 기능은 도입 이유, 롤백 가능성, 대체안이 없으면 기본 convention으로 채택하지 않는다.

## 참조 관점

- 아래 항목은 `Effective Java`의 장별 주제를 project-facing bootstrap convention으로 재정리한 것이다.
- 책의 모든 항목을 그대로 복제하지 않고, project-facing bootstrap 자산에서 바로 복사하거나 현지화할 수 있는 Java-specific 선택 기준만 남긴다.

## 타입과 모델링

- 값 의미가 있는 타입은 mutable POJO보다 `record` 또는 명시적 값 객체를 우선 검토한다.
- `equals`를 재정의하면 `hashCode`도 함께 맞추고, hash 기반 컬렉션 사용 시 테스트로 확인한다.
- 자연 순서가 있는 값 타입은 `Comparable` 구현을 검토하되 `equals`와 충돌하지 않게 유지한다.
- 값 의미가 있는 타입은 `toString` 재정의를 검토하되 민감정보는 직접 노출하지 않는다.
- enum 외부 계약에는 ordinal을 사용하지 않고, 필요한 값은 명시 필드로 둔다.
- 상태 집합 연산은 bit field보다 `EnumSet`을, enum key 기반 매핑은 배열 인덱싱보다 `EnumMap`을 우선 검토한다.
- API가 구체 구현보다 추상 계약에 의존하게 `List`, `Set`, `Map` 같은 인터페이스 타입을 우선 노출한다.
- 식별자, 복합 키, 상태를 단순 문자열 하나에 몰아넣지 말고 더 적절한 타입을 검토한다.
- `Optional`은 반환 타입에서만 우선 사용하고, 엔티티 필드, DTO 필드, 직렬화 모델 필드의 기본 표현으로 삼지 않는다.
- `Optional<List<T>>`, `Optional<Set<T>>`, `Optional<T[]>`, `Optional<Stream<T>>`보다 빈 결과를 반환한다.
- `Optional.get()`을 기본 흐름 제어로 사용하지 않고, `orElseThrow`, `map`, `flatMap`, `ifPresent` 같은 의도를 드러내는 연산을 우선한다.
- `isPresent()` 후 `get()`으로 다시 꺼내는 패턴은 분기 책임이 분명하지 않으면 피한다.

## 객체 생성과 API 설계

- 생성자 오버로드가 의미를 숨기면 named static factory를 우선 검토한다.
- 선택 인자가 많아지는 타입은 telescoping constructor보다 builder 또는 별도 request/value type을 우선 검토한다.
- 싱글턴은 진짜로 하나의 인스턴스만 허용해야 할 때만 사용하고, 직렬화/리플렉션 안정성까지 필요하면 enum 기반 구현을 우선 검토한다.
- 인스턴스화할 이유가 없는 utility 클래스는 private 생성자로 막는다.
- 자원을 직접 만들기보다 의존 객체 주입으로 교체 가능성과 테스트 가능성을 유지한다.
- 반복 생성 비용이 큰 formatter, regex pattern, immutable helper는 재사용 가능성을 먼저 검토한다.
- listener, cache, thread-local, static registry에 넣은 참조는 수명주기와 해제 책임을 함께 문서화한다.
- finalizer와 cleaner는 기본 자원 정리 수단으로 사용하지 않는다.
- `AutoCloseable` 자원은 `try-finally`보다 `try-with-resources`를 기본으로 사용한다.
- public API는 boxed primitive, `null`, sentinel value를 섞어 애매한 계약을 만들지 않는다.
- 컬렉션 내부 상태를 그대로 노출하지 않고, 방어적 복사 또는 불변 뷰 필요 여부를 계약으로 명시한다.
- public/protected 메서드는 매개변수 유효성 검사를 빠뜨리지 않는다.
- mutable 입력과 내부 상태 노출이 계약을 깨뜨릴 수 있으면 방어적 복사를 검토한다.
- 컬렉션이나 배열 결과가 비어 있을 수 있으면 `null` 대신 빈 값을 반환한다.

## 함수와 추상화 설계

- 클래스와 멤버의 접근 권한은 가능한 최소로 유지한다.
- public 클래스는 mutable public 필드 대신 접근자와 명시적 메서드 계약을 사용한다.
- 상속보다 합성을 우선하고, 상속은 진짜 is-a 관계와 override 계약을 유지할 수 있을 때만 사용한다.
- 상속을 열어 두는 클래스는 protected hook, 호출 순서, 상태 불변식까지 문서화하고, 그렇지 않으면 상속을 막는다.
- public 확장 지점은 추상 클래스보다 인터페이스를 우선 검토한다.
- 인터페이스는 타입을 표현하는 용도로 쓰고, 상수 묶음 역할은 지양한다.
- 태그 값으로 분기하는 클래스보다 sealed hierarchy 또는 명시적 타입 계층을 우선 검토한다.
- 바깥 인스턴스가 필요 없는 멤버 클래스는 static nested class를 우선 사용한다.
- raw type은 사용하지 않는다.
- 비검사 경고는 무시하지 말고 제거하거나, 정말 필요한 경우 가장 좁은 범위에서만 근거와 함께 억제한다.
- 타입 관계가 반복되는 도우미는 제네릭 타입 또는 제네릭 메서드로 일반화할 수 있는지 검토한다.
- producer/consumer 성격이 분명한 API는 bounded wildcard로 유연성을 높일 수 있는지 검토한다.
- 제네릭과 가변인수를 함께 쓸 때는 힙 오염 가능성을 확인하고, 안전성이 명확할 때만 제한적으로 사용한다.
- 타입 안전 이종 컨테이너 패턴은 ad-hoc `Map<String, Object>`보다 계약이 더 분명해질 때만 사용한다.
- reflection보다는 인터페이스와 명시적 계약을 우선 사용한다.

## 컬렉션과 데이터 처리

- 한 번의 명시적 loop가 더 읽기 쉬우면 stream보다 loop를 선택한다.
- stream 파이프라인은 mapping/filtering/aggregation 책임이 한눈에 읽히는 길이까지만 허용한다.
- stream 안에는 부작용 없는 함수를 유지하고, 상태 변경을 숨기지 않는다.
- 재사용 가능한 결과를 반환할 때는 `Stream`보다 `Collection` 반환이 더 나은지 먼저 검토한다.
- `parallelStream()`은 기본값으로 사용하지 않고, workload 특성과 검증 근거가 있을 때만 도입한다.
- 정렬, grouping, deduplication처럼 표준 collector로 충분한 경우 직접 상태 누적 코드를 반복하지 않는다.
- 문자열 누적은 반복 `+`보다 `StringBuilder`, `StringJoiner`, collector가 더 명확한지 비교한다.
- stream, lambda, boxing이 hot path에서 반복되면 loop, primitive specialization, 중간 객체 제거가 더 단순한지 먼저 검토한다.
- `map().filter().collect()` 연쇄가 큰 중간 컬렉션을 여러 번 만들면 한 번의 순회로 줄일 수 있는지 확인한다.
- `Stream<Integer>`처럼 boxing 비용이 반복되는 경로는 `IntStream`, `LongStream`, `DoubleStream` 적용 가능성을 검토한다.
- 정확한 수치 계산이 필요하면 `float`/`double` 대신 프로젝트 표준 수치 타입을 명시한다.
- hot path와 null 허용 비교에서는 boxed primitive보다 primitive를 우선 검토한다.
- 최적화는 측정 근거와 병목 정보가 있을 때만 도입한다.

## 예외와 결과 표현

- 예외는 진짜 예외 상황에만 사용하고 정상 흐름 제어 수단으로 남용하지 않는다.
- 복구 가능한 상황은 checked exception, 프로그래밍 오류는 runtime exception이 더 맞는지 구분한다.
- 꼭 필요하지 않은 checked exception은 추가하지 않는다.
- ad-hoc 예외보다 표준 예외 타입으로 충분한지 먼저 검토한다.
- 공개 API는 던질 수 있는 예외와 조건을 문서화한다.
- 실패 후 객체 상태가 부분적으로 깨지지 않도록 failure atomicity를 검토한다.
- 예외를 무시하지 않고, 정말 삼켜야 하면 이유와 보완을 남긴다.
- `InterruptedException`을 삼키지 않고 interrupt 의미를 보존한다.

## 동시성과 비동기

- 공유 mutable 상태는 동기화하거나, 더 먼저 공유 자체를 제거할 수 있는지 검토한다.
- 과도한 동기화와 lock 내부 외부 호출을 피한다.
- raw thread 생성보다 executor, task, concurrency utility를 우선 검토한다.
- `wait`/`notify`보다 `java.util.concurrent` 유틸리티를 우선 검토한다.
- thread-safety 수준을 프로젝트 문서나 타입 계약에 명시한다.
- 지연 초기화는 동시성 비용과 초기화 비용을 비교해 신중히 사용한다.
- correctness를 sleep, timing, scheduler 우연성에 기대지 않는다.

## Interop, Reflection, Serialization

- native method는 꼭 필요할 때만 사용하고, 대체 불가 사유를 남긴다.
- reflection, bytecode 조작, annotation processor, agent 기반 접근은 필요성과 대체 불가 사유가 있을 때만 도입한다.
- 외부 경계 계약은 Java native serialization보다 명시적 포맷(JSON, Protobuf, 별도 mapper)을 우선 검토한다.
- `Serializable` 구현은 장기 호환성과 공격 표면을 고려해 신중히 결정한다.
- 직렬화가 꼭 필요하면 기본 직렬화 형태가 아니라 커스텀 직렬화 형태가 더 안전한지 검토한다.
- `readObject`는 방어적으로 작성하고 불변식 복원을 확인한다.
- 인스턴스 수 통제가 중요한 singleton은 `readResolve`보다 enum singleton이 더 맞는지 우선 검토한다.
- 복잡한 직렬화 대상은 serialization proxy 패턴이 더 안전한지 검토한다.

## Import 와 Dependency 사용 관례

- static import는 assertion, math, enum constant처럼 반복 사용으로 오히려 의미가 선명해질 때만 제한적으로 사용한다.
- 표준 JDK 기능으로 충분한 경우 작은 편의 라이브러리 추가보다 JDK 표준 API를 우선 검토한다.
- Lombok 같은 코드 생성 도구 사용 여부와 허용 범위는 `[프로젝트 결정 필요]`로 남긴다.

## 패키지와 파일 구조

- 패키지 구조는 프로젝트의 구조 문서가 정한 책임 경계를 먼저 드러내고, framework 중심 그룹화만 남지 않게 정한다.
- public 타입 이름은 역할 중심 명사로 두고, 구현 상세가 드러나는 `Impl`, `Util`, `Helper` 남용은 피한다.
- 하나의 파일에는 함께 변경될 이유가 높은 타입만 둔다. 붙어 다니지 않는 보조 타입을 관성적으로 중첩시키지 않는다.
- 톱레벨 타입은 가능한 한 파일당 하나로 유지한다.
- record, enum, sealed hierarchy는 파일 배치만으로도 닫힌 모델 관계가 읽히게 유지한다.

## 테스트 관례 초안

- 테스트 이름은 시나리오와 기대 결과를 드러내게 작성한다.
- 프레임워크 통합 테스트는 실제 연결 책임이 있는 위치에만 사용하고, 단위 테스트로 충분한 책임까지 과도하게 끌어오지 않는다.
- `record`, enum, sealed hierarchy 같은 모델링 선택은 값 비교, 분기 exhaustiveness, 직렬화/역직렬화 관점에서 테스트로 확인한다.
- virtual thread, 비동기 실행, timeout 관련 테스트는 sleep 기반 대기보다 종료 조건과 결과를 직접 관찰하는 방식으로 작성한다.
- 예외 테스트는 checked/runtime 선택과 공개 계약 문서가 실제 동작과 맞는지 확인한다.

## 자주 생기는 품질 리스크와 금지 패턴

- setter 위주의 광범위한 mutable entity/DTO 남용
- `null`과 `Optional`을 혼용해 부재 의미가 흔들리는 API
- `Util`, `Common`, `Manager`처럼 책임이 넓은 만능 클래스 확장
- `catch (Exception)` 또는 광범위한 예외 삼키기
- stream, lambda, method reference를 과도하게 중첩해 디버깅과 읽기 난도를 높이는 코드
- `parallelStream()`, custom thread pool, virtual thread를 근거 없이 혼용하는 동시성 코드
- reflection 또는 annotation 마법으로 핵심 비즈니스 흐름을 숨기는 구조

## 확인 필요 항목

- 기준 JDK 버전(`17+`, `21+`, `24+` 같은 대표 기준점 또는 이후 GA 버전)과 사용 가능 기능 범위
- preview 기능 허용 여부와 승인 절차
- formatter와 lint 도구(`spotless`, `checkstyle`, `errorprone` 등) 및 import/format 규칙 자동 강제 범위
- 테스트 스택(`JUnit`, `AssertJ`, `Mockito`, `Testcontainers` 등)
- nullability, transaction, annotation 사용 원칙
- virtual thread, module system, AOT/Native Image 대응 여부 `[프로젝트 결정 필요]`
