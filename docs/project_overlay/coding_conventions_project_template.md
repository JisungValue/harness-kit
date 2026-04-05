# Coding Conventions Project

## 목적

이 문서는 공통 `coding_guidelines_core.md` 위에 프로젝트 전용 coding convention만 추가한다.

## 시작 방법

- 언어별 convention 초안이 필요하면 `bootstrap/language_conventions/`에서 해당 언어 템플릿을 골라 이 문서에 병합한다.
- 단일 언어 프로젝트면 필요한 항목만 이 문서에 직접 복사해 시작한다.
- 다중 언어 프로젝트면 공통 규칙은 이 문서에 두고, 언어별 상세 규칙은 별도 문서로 분리한 뒤 여기서 참조해도 된다.

## 여기에 둘 내용 예시

- 프레임워크 특화 관례
- DTO postfix 또는 suffix 규칙
- 트랜잭션 경계 규칙
- 프로젝트 전용 에러 타입 규칙
- 프로젝트 전용 로깅 필드 규칙

## 금지

- core에 이미 있는 규칙을 중복해서 다시 쓰지 않는다.
- 여러 프로젝트에 공통인 규칙을 project 전용 규칙처럼 두지 않는다.
