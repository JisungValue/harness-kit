# Bootstrap Assets

이 디렉터리는 실제 프로젝트를 시작할 때 수동 복사하거나 스캐폴딩 입력으로 사용할 bootstrap 자산을 둔다.

## 원칙

- `bootstrap/`은 maintainer 전용 문서가 아니다.
- 여기 있는 파일은 downstream 프로젝트로 복사될 수 있는 project-facing 시작 자산이다.
- `bootstrap/`은 프로젝트 문서 골격 자체를 대체하지 않고, `docs/project_overlay/` 템플릿 안에 언어별 세부 내용을 채워 넣을 때만 사용한다.
- 복사 후에는 프로젝트 저장소에서 팀 규칙에 맞게 수정한다.
- bootstrap 자산의 정본은 이 저장소에 유지한다.
- 새 프로젝트 first success 경로는 `bootstrap/docs/project_overlay/first_success_guide.md`를 기준으로 본다.

## 현재 자산

- `bootstrap/language_conventions/`
  - 언어별 coding convention 초안을 둔다.
  - 필요한 언어만 골라 `docs/standard/coding_conventions_project.md`에 병합하거나 별도 언어 문서로 복사해 사용한다.

## Init CLI

- source repo canonical CLI는 `bootstrap/scripts/bootstrap_init.py`, `bootstrap/scripts/check_first_success_docs.py`, `bootstrap/scripts/validate_overlay_decisions.py`, `bootstrap/scripts/validate_overlay_consistency.py`이며 모두 Python 3 runtime으로 실행한다.
- `bootstrap/scripts/bootstrap_init.py`는 `bootstrap/docs/project_overlay/*` 템플릿을 source of truth로 삼고, generated bundle에서는 같은 자산을 `docs/project_overlay/*`와 `scripts/*`로 materialize 한 뒤 새 프로젝트 또는 거의 빈 대상 디렉터리에 최소 project overlay 문서 세트를 그대로 복사해 생성한다.
- 최소 입력은 target path와 `--language`이고, `--force`는 선택적 overwrite 플래그다.
- 기본 동작은 기존 생성 대상 파일이 하나라도 있으면 fail-fast다.
- `--force`는 overwrite 의미로만 사용하며 merge는 하지 않는다.
- 대상 경로 자체가 디렉터리가 아니거나, 생성 경로의 부모가 파일인 경우에는 부분 생성 없이 즉시 실패한다.
- 현재 MVP는 관리 대상 문서 경로만 검사한다. 즉, unrelated 파일이 있는 비어 있지 않은 저장소라도 생성 대상 경로와 충돌하지 않으면 진행한다.
- 생성되는 기본 문서 경로는 아래와 같다.
  - `docs/project_entrypoint.md`
  - `docs/decisions/README.md`
  - `docs/standard/architecture.md`
  - `docs/standard/implementation_order.md`
  - `docs/standard/coding_conventions_project.md`
  - `docs/standard/quality_gate_profile.md`
  - `docs/standard/testing_profile.md`
  - `docs/standard/commit_rule.md`
- 선택 언어 convention은 프로젝트 문서 안에 `vendor/harness-kit/bootstrap/language_conventions/...` 참조를 기본값으로 기록한다.
- 로컬 `docs/project_entrypoint.md`도 기본적으로 `vendor/harness-kit/docs/harness_guide.md`를 참조하는 초안을 생성한다.
- 따라서 init 결과를 사용하는 프로젝트는 vendored harness-kit 경로를 실제 배치 경로에 맞게 현지화해야 한다.

## First-Success Existence Check

- `bootstrap/scripts/check_first_success_docs.py`는 source repo canonical helper command다. generated bundle에서는 `scripts/check_first_success_docs.py`로 materialize 된다.
- bootstrap 직후 이 명령을 먼저 실행하고, 그다음 decision/consistency validator로 넘어간다.

## 사용 예시

```bash
python3 bootstrap/scripts/bootstrap_init.py ../sample-project --language python
python3 bootstrap/scripts/bootstrap_init.py ../sample-project --language kotlin --force
```
