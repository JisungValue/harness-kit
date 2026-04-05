# Python Coding Conventions Template

## 목적

이 문서는 Python 프로젝트 또는 Python 모듈에 적용할 언어별 convention 초안이다.

## 사용 방법

- 필요한 항목만 `docs/standard/coding_conventions_project.md`에 복사 또는 병합한다.
- 다중 언어 프로젝트면 Python 전용 문서로 분리한 뒤 프로젝트 문서에서 참조해도 된다.

## 기본 규칙

- 모듈과 파일 이름은 `snake_case`를 기본으로 사용한다.
- 공개 함수와 메서드는 입력과 반환 타입을 드러내는 타입 힌트를 우선한다.
- 경계 계층에서 받은 외부 데이터는 그대로 전파하지 말고 프로젝트 표준 타입으로 번역한다.
- 예외는 경계에서 번역하고, core에는 Python 런타임이나 외부 라이브러리 예외를 그대로 흘리지 않는다.
- comprehension, generator, decorator는 읽기 난도를 높이지 않는 범위에서만 사용한다.

## 테스트 관례 초안

- 테스트 이름은 동작과 기대 결과가 드러나게 작성한다.
- fixture는 재사용 가치가 있는 경우에만 공통화하고, 테스트 흐름을 숨기지 않게 유지한다.
- mock은 외부 협력 경계에 가깝게 두고 내부 구현 세부사항 고정은 피한다.

## 확인 필요 항목

- formatter와 linter 조합(`ruff`, `black`, `flake8` 등)
- 타입 검사 도구(`mypy`, `pyright` 등)
- async 사용 범위와 테스트 방식
