# Testing Profile

## 목적

이 문서는 프로젝트에서 실제로 사용하는 테스트 전략, 환경 준비, coverage 기준, 통합 테스트 세부 기준을 정의한다.

## 책임 경계

- 테스트 실행 명령 자체와 formatter/linter/type checker/test 게이트 강제 여부는 `quality_gate_profile.md`에서 정의한다.
- 이 문서는 테스트를 어떤 환경과 범위로 수행할지 설명하는 문서다.

## 최소 포함 항목

- coverage 확인 방법
- 외부 의존성 또는 테스트 컨테이너 필요 여부
- 로컬 개발 환경에서 주의할 점
- 통합 테스트 대상 또는 범위

## quality_gate_profile에 두는 항목

- `test` 실행 명령
- test 게이트의 필수 여부
- 언제 test를 반드시 돌려야 하는지
- 테스트 실패 시 커밋/승인 불가 기준

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
