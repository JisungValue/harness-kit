# Agent Runtime Entry Point

이 파일은 agent runtime이 공통으로 먼저 읽는 instruction entrypoint다.

## 우선 읽을 문서

- `docs/project_entrypoint.md`

## 유지 원칙

- 프로젝트 규칙 추가 또는 수정은 `docs/project_entrypoint.md`와 연결된 `docs/standard/*` 문서에서 관리한다.
- agent별 adapter file은 이 파일만 다시 가리키고 규칙 본문을 중복 복사하지 않는다.
