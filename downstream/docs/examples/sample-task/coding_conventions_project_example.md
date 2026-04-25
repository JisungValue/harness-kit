# Coding Conventions Project Example

## 활성 언어와 런타임

- 언어: Kotlin
- 런타임: JVM 21
- bootstrap 기준: `bootstrap/language_conventions/kotlin_coding_conventions_template.md`

## 현재 작업과 직접 관련 있는 규칙 범주

- null-safety와 platform type 정규화
- coroutine cancellation 보존
- collection/sequence/flow 선택 기준
- 테스트에서 `runTest`를 기본으로 사용할 기준

## 주요 금지 패턴

- `!!` 남용
- broad `runCatching`으로 핵심 제어 흐름 숨기기
- coroutine 안에서 blocking 호출 숨기기
- 현재 작업과 무관한 language rule까지 형식적으로 모두 검사한 척 기록하기

## 현재 Phase 2에서 미해결로 둘 수 없는 항목

- nullability와 Java interop 기준
- `Flow`를 실제 비동기 스트림이 아닌 단순 일회성 값 전달에 써도 되는지 여부
- coroutine boundary에서 `CancellationException`을 어떤 결과 타입으로 노출할지 여부
