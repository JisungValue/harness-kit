# Python Coding Conventions Template

## 목적

이 문서는 Python 프로젝트 또는 Python 모듈에 적용할 언어별 convention 초안이다.
가능하면 Python의 단순한 표현, 명시적 계약, 읽기 쉬운 모듈 경계를 우선하되, 동적 기능과 편의 문법이 구조를 흐리지 않도록 반복 판단 기준을 남긴다.

## 사용 방법

- 필요한 항목만 `docs/standard/coding_conventions_project.md`에 복사 또는 병합한다.
- 다중 언어 프로젝트면 Python 전용 문서로 분리한 뒤 프로젝트 문서에서 참조해도 된다.
- framework, runtime, packaging, serialization, persistence 기술에 강하게 묶인 규칙은 `[프로젝트 결정 필요]`로 남긴다.

## 코드 스타일과 convention 분리

- import 정렬, 공백, 줄바꿈, line length, quote style, unused import 같은 기계적으로 판별 가능한 규칙은 formatter/linter 또는 CI check로 강제한다.
- 이 문서는 자동 검사로 대체하기 어려운 판단 규칙과 예외 기준을 남긴다.
- tool 설정으로 고정 가능한 스타일 규칙은 여기서 길게 반복하지 않는다.

## 공통 품질 규칙 참조

- 공통 boundary translation, 에러 처리, 테스트 책임, 범위 제한 규칙은 `docs/standard/coding_guidelines_core.md`를 따른다.
- 이 문서는 그 위에 Python에서 반복적으로 결정해야 하는 언어별 선택 기준만 추가한다.

## 적용 전 결정

- 기준 Python 버전을 `3.10+`, `3.11+`, `3.12+` 같은 대표 기준점 또는 그 이후 버전 중 어디로 둘지 먼저 정한다.
- sync 중심인지 async 중심인지, 그리고 두 방식을 어느 경계까지 함께 허용할지 정한다.
- packaging 방식(`src/` layout, 단일 패키지, monorepo package), 실행 진입점, worker/API/CLI 분리 방식은 `[프로젝트 결정 필요]`로 남긴다.
- validation/modeling에서 `dataclass`, `TypedDict`, `Protocol`, 사용자 정의 클래스, 외부 라이브러리 모델 중 무엇을 기본값으로 둘지 정한다.
- serialization, settings, dependency injection, background task 방식은 `[프로젝트 결정 필요]`로 남긴다.

## 런타임과 패키징 검토 예시

- API/worker/CLI가 함께 있는 프로젝트면 import-time 실행, 설정 로딩, 전역 singleton 초기화가 어디까지 허용되는지 먼저 정한다.
- async I/O 중심 프로젝트면 event loop 안에서 blocking 호출을 어떻게 차단할지와 sync adapter 경계를 함께 정한다.
- data processing 또는 batch 중심 프로젝트면 iterator, chunk 처리, 파일/네트워크 stream 사용 기준을 먼저 정한다.
- C extension, PyPy, multiprocessing, uvloop 같은 runtime 특화 최적화는 기본 convention으로 고정하지 말고 `[프로젝트 결정 필요]`로 분리한다.

## 참조 관점

- 아래 항목은 `PEP 8`, `PEP 20`, `PEP 484`, `PEP 544`, `PEP 557` 계열의 실무 관점을 project-facing bootstrap convention으로 재정리한 것이다.
- 문법 기능을 많이 쓰는 것보다, 읽기 쉬운 모듈 경계와 명시적 타입/오류 계약을 유지하는 쪽을 우선한다.

## 타입과 모델링

- 모듈, 파일, 함수, 변수 이름은 `snake_case`, 클래스 이름은 `PascalCase`, 상수는 `UPPER_SNAKE_CASE`를 기본으로 사용한다.
- public 함수와 메서드는 입력과 반환 타입이 드러나는 타입 힌트를 우선한다.
- internal 코드도 의미가 모호하거나 foreign data가 오가는 경계면 타입 힌트를 생략하지 않는다.
- `Any`는 마지막 수단으로만 사용하고, 도입 이유 없이 넓은 `dict[str, Any]` 전파를 기본값으로 두지 않는다.
- key 집합이 정해진 사전형 데이터는 plain `dict`보다 `TypedDict`, `dataclass`, 명시적 값 객체 중 더 계약이 분명한 표현을 우선 검토한다.
- 값 의미가 핵심이면 `dataclass(frozen=True)` 같은 불변 모델을 우선 검토하고, 수명주기와 부수효과가 있는 객체는 일반 클래스로 둔다.
- enum 후보를 문자열 상수 묶음으로 흩어놓지 말고, 닫힌 선택지면 `Enum`을 우선 검토한다.
- 서비스 객체, repository, gateway처럼 상태보다 협력이 핵심인 위치에 data container 스타일 클래스를 남용하지 않는다.
- 식별자, 상태, 외부 포맷 값을 단순 문자열 하나로만 유지하지 말고 더 적절한 값 타입이나 alias, enum 가능성을 먼저 본다.

## 객체 생성과 API 설계

- 매개변수가 셋 이상이거나 boolean flag가 들어가면 keyword-only argument 또는 별도 request/value object를 먼저 검토한다.
- mutable default argument는 사용하지 않고 `None` + 초기화 또는 `default_factory`를 사용한다.
- `__init__`에서 네트워크 I/O, 파일 I/O, 환경 조회, 무거운 계산을 숨기지 않는다.
- resource 수명주기가 있는 객체는 `with` 문과 context manager 사용 가능성을 먼저 검토한다.
- `@property`는 싸고 예측 가능한 상태 조회에만 사용하고, 비용 큰 계산이나 부수효과는 메서드로 드러낸다.
- public API는 `None`, sentinel, 예외를 섞어 같은 실패 의미를 여러 방식으로 표현하지 않도록 프로젝트 기준을 정한다.
- 직접 생성보다 주입이 더 단순하고 테스트 가능성을 높이면 생성자 또는 함수 인자로 의존성을 받는다.

## 함수와 추상화 설계

- 상태가 필요 없는 로직은 클래스로 감싸기보다 함수와 모듈로 유지하는 쪽을 먼저 검토한다.
- decorator는 cross-cutting concern을 분리할 때만 사용하고, 핵심 흐름과 에러 경로를 숨기지 않는다.
- comprehension, generator, walrus operator, structural pattern matching은 읽기 쉬움이 분명할 때만 사용한다.
- nested function과 closure는 지역 캡슐화 이점이 있을 때만 사용하고, 과도한 free variable 캡처로 흐름을 숨기지 않는다.
- `getattr`, `setattr`, `hasattr`, `__dict__`, metaclass, dynamic import 같은 동적 기능은 framework 요구나 대체 불가 사유가 있을 때만 도입한다.
- 재사용 근거 없는 base class, mixin, metaprogramming helper를 조기 도입하지 않는다.
- 모듈이 `utils`, `common`, `helpers` 같은 넓은 이름으로 비대해지기 시작하면 책임을 다시 나눈다.

## 컬렉션과 데이터 처리

- 반복 membership lookup이 있으면 `list` 순회보다 `set` 또는 `dict` index가 더 단순한지 먼저 검토한다.
- 큰 입력을 처리할 때 불필요한 `list(...)`, `tuple(...)`, `dict(...)` materialization이 연속 발생하지 않는지 확인한다.
- 큰 파일, 큰 응답, batch 데이터는 전체 적재보다 iterator, generator, chunk 처리로 충분한지 먼저 본다.
- `sorted`, `groupby`, regex, JSON parse, datetime parse 같은 상대적으로 비싼 연산을 루프 안에서 반복하지 않는다.
- 같은 데이터의 변형본을 여러 번 복사하지 말고, 필요한 필드만 추출하거나 한 번의 순회로 줄일 수 있는지 검토한다.
- 한 줄 comprehension이더라도 조건과 변환이 여러 단계로 겹치면 명시적 loop가 더 읽기 쉬운지 다시 본다.
- 숫자 처리, 시계열, 데이터프레임 같은 특화 연산은 표준 컬렉션보다 프로젝트 표준 라이브러리 사용이 더 명확한지 `[프로젝트 결정 필요]`로 남긴다.

## 예외와 결과 표현

- `except Exception`과 bare `except`는 기본 금지로 두고, 구체 예외만 잡는다.
- 외부 라이브러리나 런타임 예외는 경계에서 프로젝트 의미를 가진 예외나 결과 타입으로 번역한다.
- 예외를 다시 던질 때 원인 보존이 중요하면 `raise ... from ...`를 사용한다.
- `None` 반환, boolean 실패 코드, 예외 발생을 같은 계층에서 혼용하지 않도록 프로젝트 기준을 정한다.
- 예외를 잡고 로그만 남긴 뒤 정상 흐름처럼 계속 진행하지 않는다.
- 같은 실패를 여러 계층에서 중복 로그하지 않고, 최종 경계에서 한 번 기록하는 쪽을 우선 검토한다.
- validation 오류, business rule 위반, 외부 의존성 실패, retry 가능 오류는 구분 가능한 계약으로 남긴다.

## 동시성과 비동기

- `async def`는 실제 비동기 I/O 경계를 표현할 때만 사용하고, 동기 로직을 관성적으로 async로 감싸지 않는다.
- event loop 안에서는 blocking DB/file/HTTP/client 호출을 직접 수행하지 않는다.
- sync API와 async API를 같은 이름/같은 계층에 섞어 두지 말고 경계를 분명히 한다.
- `asyncio.create_task` 같은 fire-and-forget 작업은 수명주기, cancellation, 예외 수집 책임이 있을 때만 사용한다.
- shared mutable state, module-level cache, in-memory singleton은 thread/process/async safety를 설명할 수 있을 때만 도입한다.
- multiprocessing, thread pool, background scheduler는 실제 병목 또는 운영 요구가 있을 때만 도입하고 `[프로젝트 결정 필요]`로 남긴다.

## 동적 기능, 직렬화, 런타임 경계

- `pickle`은 외부 계약 기본값으로 사용하지 않고, 명시적 포맷(JSON, MessagePack, 별도 schema 기반 포맷 등)을 우선 검토한다.
- serialization 라이브러리, validation 모델, settings loader는 하나의 project 기본값을 정하고 무분별하게 혼용하지 않는다.
- runtime reflection, plugin discovery, entry point 로딩, dynamic import는 확장 지점이 실제로 필요한 경우에만 도입한다.
- framework가 요구하는 magic method, descriptor, metaclass, signal hook은 필요 범위만 제한적으로 사용한다.
- import 시점에 registry 등록, 환경 변수 읽기, DB 연결, 네트워크 호출 같은 side effect를 만들지 않는다.

## Import 와 Dependency 사용 관례

- absolute import를 기본으로 사용하고, relative import는 같은 패키지 내부의 짧은 로컬 관계에서만 제한적으로 사용한다.
- 내부 전용 모듈의 deep import를 public API처럼 퍼뜨리지 않는다.
- `from module import *`는 사용하지 않는다.
- 순환 import를 임시 local import로만 덮지 말고, 모듈 책임과 dependency 방향을 다시 확인한다.
- optional dependency가 있으면 호출 경계와 fallback 계약을 프로젝트 문서에 명시한다.
- dependency 추가는 "짧은 코드"보다 유지보수 이점과 표준 라이브러리 대체 가능성을 먼저 비교한다.

## 패키지와 파일 구조

- 패키지 구조는 프로젝트의 구조 문서가 정한 책임 경계를 먼저 드러내고, framework 중심 그룹화만 남지 않게 정한다.
- public export가 필요한 경우에만 `__init__.py`에서 재노출하고, 무거운 로직이나 side effect는 넣지 않는다.
- 파일 하나에는 함께 변경될 이유가 높은 타입과 함수만 둔다.
- `utils.py`, `common.py`, `helpers.py`, `misc.py` 같은 만능 파일이 커지기 시작하면 역할별 모듈로 나눈다.
- boundary translation, domain 판단, 외부 I/O를 한 모듈이나 파일에 함께 몰아넣지 않는다.
- naming만으로도 adapter, service, repository, model, schema, client, command/result 같은 역할이 읽히게 유지한다.

## 테스트 관례 초안

- 테스트 이름은 동작과 기대 결과가 드러나게 작성한다.
- fixture는 재사용 가치가 있는 경우에만 공통화하고, 테스트 입력과 흐름을 숨기지 않게 유지한다.
- parameterized test는 같은 계약을 여러 입력으로 검증할 때만 사용하고, 서로 다른 책임을 한 테스트에 섞지 않는다.
- mock, patch, monkeypatch는 외부 협력 경계에서만 제한적으로 사용하고 내부 구현 세부사항 고정은 피한다.
- 예외 테스트는 예외 타입뿐 아니라 에러 메시지 계약, boundary translation, 원인 보존 여부가 중요한지도 함께 본다.
- async 테스트 도구와 event loop fixture 방식은 `[프로젝트 결정 필요]`로 남기되, sleep 기반 대기보다 종료 조건과 결과를 직접 관찰하는 쪽을 우선한다.

## 자주 생기는 품질 리스크와 금지 패턴

- mutable default argument 사용
- bare `except` 또는 광범위한 `except Exception`
- import-time 환경 조회, 설정 로딩, 네트워크 호출, DB 연결
- `dict[str, Any]`와 dynamic attribute를 핵심 domain 계약 기본값처럼 사용하는 코드
- `utils`, `common`, `helper` 모듈에 unrelated logic를 계속 누적하는 구조
- `Any`, `cast`, monkeypatch, mock을 근거 없이 넓게 사용하는 테스트와 구현
- `asyncio.create_task`를 수명주기 관리 없이 호출하는 코드
- `from x import *`, deep import, 순환 import를 구조 수정 없이 임시 import로만 숨기는 코드

## 확인 필요 항목

- 기준 Python 버전과 target runtime(CPython/PyPy 등)
- formatter와 lint 도구(`ruff`, `black`, `flake8`, `isort` 등) 및 import/format 규칙 자동 강제 범위
- 타입 검사 도구(`mypy`, `pyright` 등)와 strictness 범위
- 테스트 스택(`pytest`, async test 도구, factory/fixture 라이브러리 등)
- async 사용 범위, background task 전략, thread/process 사용 원칙 `[프로젝트 결정 필요]`
- settings, serialization, validation 모델, dependency injection 방식 `[프로젝트 결정 필요]`
