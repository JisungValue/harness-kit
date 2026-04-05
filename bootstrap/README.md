# Bootstrap Assets

이 디렉터리는 실제 프로젝트를 시작할 때 수동 복사하거나 스캐폴딩 입력으로 사용할 bootstrap 자산을 둔다.

## 원칙

- `bootstrap/`은 maintainer 전용 문서가 아니다.
- 여기 있는 파일은 downstream 프로젝트로 복사될 수 있는 project-facing 시작 자산이다.
- `bootstrap/`은 프로젝트 문서 골격 자체를 대체하지 않고, `docs/project_overlay/` 문서 안에 언어별 세부 내용을 채워 넣을 때만 사용한다.
- 복사 후에는 프로젝트 저장소에서 팀 규칙에 맞게 수정한다.
- bootstrap 자산의 정본은 이 저장소에 유지한다.

## 현재 자산

- `bootstrap/language_conventions/`
  - 언어별 coding convention 초안을 둔다.
  - 필요한 언어만 골라 `docs/standard/coding_conventions_project.md`에 병합하거나 별도 언어 문서로 복사해 사용한다.
