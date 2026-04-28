# Code Hygiene Policy

## 목적

이 문서는 구현 결과가 불필요한 잔여 코드, 죽은 코드, 임시 디버깅 흔적 없이 기본 청결성을 유지하는지 판단하는 공통 기준을 정의한다.

## 언제 다시 읽는가

- Phase 2 구현 시작 전에 다시 확인한다.
- 구현 중 import 정리, dead code 제거, 임시 디버깅 흔적 정리가 애매할 때 다시 참조한다.
- Phase 2 감사 직전에 최소 청결성 기준을 다시 확인할 때 참조한다.

## 기본 원칙

- 현재 변경 결과는 현재 TASK와 직접 관련 있는 코드만 남기고, 의미 없는 잔여물은 제거한다.
- hygiene는 보기 좋은 정리가 아니라 변경 후 코드가 혼동 없이 읽히고 유지보수 가능한 상태인지 확인하는 기준이다.
- 자동화 가능한 hygiene는 project `docs/project/standards/quality_gate_profile.md`에서 연결할 수 있지만, 도구가 못 잡는 잔여 코드는 여전히 구현자와 감사자가 직접 확인한다.

## import 규칙

- 사용하지 않는 import는 남기지 않는다.
- 언어나 도구가 특별히 요구하지 않으면 import는 파일 상단에 둔다.
- fully qualified name과 import 방식을 불필요하게 혼용하지 않는다.
- import 추가/삭제는 현재 변경 결과가 실제로 사용하는 symbol 기준으로 정리한다.

## dead code 규칙

- 더 이상 호출되지 않는 private 함수, helper, 상수, 분기, fallback 코드는 현재 변경과 직접 연결돼 있다면 함께 제거한다.
- 현재 수정으로 의미를 잃은 TODO stub, 임시 우회 분기, 과거 호환용 흔적을 그대로 남기지 않는다.
- "나중에 쓸 수도 있음" 수준의 보관 코드는 기본 허용하지 않는다.

## 임시 디버깅 흔적 규칙

- 임시 `print`, `console.log`, 디버깅용 logger, 테스트용 우회 플래그는 최종 결과에 남기지 않는다.
- 주석 처리된 코드 블록, 의미 없는 실험 코드, 임시 메모는 제거한다.
- 로그는 디버깅 흔적이 아니라 실제 운영 목적이 있을 때만 남긴다.

## 사용되지 않는 선언 규칙

- 현재 변경 범위에서 실제로 쓰이지 않는 지역 변수, private field, helper 함수, 임시 상수는 제거한다.
- public API 호환성, framework reflection, serialization, generated contract 때문에 남겨야 하는 unused 형태는 예외로 둘 수 있다.
- 예외는 설명 가능해야 하며, 단순 관성 때문에 유지하지 않는다.

## 범위 제한 규칙

- 현재 TASK와 무관한 대규모 코드 청소는 별도 태스크로 분리한다.
- hygiene를 명분으로 광범위한 구조 정리, 네이밍 통일, 파일 이동, 선제 추상화를 함께 넣지 않는다.
- 현재 변경과 직접 맞닿은 잔여물만 함께 정리하고, 범위가 커지면 `implementation_notes.md`에 후속 후보로 남긴다.

## quality gate 연결 원칙

- import 정리, dead code, unused symbol, debug 흔적 제거처럼 자동화 가능한 항목은 project `docs/project/standards/quality_gate_profile.md`에서 linter 또는 hygiene check로 연결할 수 있다.
- 이 문서는 어떤 도구를 쓰라고 강제하지 않는다.
- 도구가 없거나 도구가 못 잡는 hygiene는 Phase 2 구현과 감사에서 수동으로 확인한다.

## Phase 2에서 확인해야 할 것

- 현재 변경과 직접 관련 있는 import/unused/dead code/debug 흔적이 남아 있지 않은가.
- 현재 변경과 무관한 대규모 청소를 함께 넣지 않았는가.
- framework나 generated contract 예외를 이유 없이 넓게 적용하지 않았는가.

## 승인 불가 예시

- 사용하지 않는 import를 그대로 남김
- 더 이상 호출되지 않는 helper와 fallback 분기를 변경 후에도 그대로 둠
- 임시 debug print/log를 제거하지 않음
- dead code 청소를 명분으로 현재 TASK와 무관한 대규모 정리를 함께 반영함
