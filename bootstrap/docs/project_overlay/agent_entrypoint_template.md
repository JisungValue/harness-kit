# Agent Runtime Entry Point

이 파일은 agent runtime이 공통으로 먼저 읽는 instruction entrypoint다.

## 우선 읽을 문서

- `docs/entrypoint.md`

## 실행 계약

- 이 파일에 연결된 문서는 순서대로 모두 읽고 적용한 뒤에만 다음 작업으로 넘어간다.
- `docs/entrypoint.md`를 열었으면 그 문서의 `공통 규칙`, `프로젝트 전용 규칙`에 연결된 문서까지 끝까지 이어서 읽고 적용한다.
- 링크만 확인하고 중간 문서에서 멈추지 않는다.

## 유지 원칙

- 프로젝트 규칙 추가 또는 수정은 `docs/entrypoint.md`와 연결된 `docs/project/standards/*` 문서에서 관리한다.
- agent별 adapter file은 이 파일만 다시 가리키고 규칙 본문을 중복 복사하지 않는다.
