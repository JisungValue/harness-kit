# Testing Profile

## 목적

이 문서는 프로젝트에서 실제로 사용하는 테스트 실행 방법과 세부 기준을 정의한다.

## 최소 포함 항목

- 단위 테스트 실행 명령
- 통합 테스트 실행 명령
- coverage 확인 방법
- 외부 의존성 또는 테스트 컨테이너 필요 여부
- 로컬 개발 환경에서 주의할 점

## 권장 추가 항목

- 구현체 단위 통합 테스트 대상
- 외부 의존성 기동 방식
- 테스트 데이터 초기화 방식
- sandbox, container, local service 중 어떤 방식을 쓰는지

## 구현체 단위 통합 테스트 대상 예시

- storage adapter 구현체: 실제 저장/조회 연산, 레코드 또는 문서 매핑, 저장소별 경계 책임
- HTTP client adapter 구현체: 실제 응답 포맷, DTO 매핑, 에러 번역
- gateway 구현체: 외부 요청/응답 계약, timeout, retry 경계

## 외부 의존성 기동 방식 예시

- test container 기반
- docker compose 기반
- 로컬 sandbox 서비스 기반
- 프로젝트 공용 개발 DB 또는 mock server 기반
