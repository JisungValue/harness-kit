# Adopt Safe Write

이 문서는 `adopt_dry_run.py` 결과를 바탕으로, 기존 프로젝트에 대해 제한된 범위에서만 bootstrap 기준 파일을 쓰는 방법을 설명한다.

## 목적

- 기존 프로젝트에 대해 repo 전체가 아니라 downstream bundle 경계 안의 overlay 대상만 제한적으로 갱신한다.
- `missing files`, `existing but unchanged targets`, `differing files`, `conflict candidates`를 같은 판정 규칙으로 읽고 write 동작에 연결한다.
- user-modified 파일을 자동 merge하지 않고, 명시적으로 허용한 범위만 쓴다.

## 실행 명령

프로젝트 루트에서 아래처럼 실행한다.

```bash
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python
```

필요하면 아래 옵션을 추가한다.

```bash
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python --update-unchanged
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python --force-overwrite docs/entrypoint.md
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python --migrate-legacy-entrypoint
```

## 기본 규칙

- `missing files`
  - 기본 동작에서 자동 생성한다.
- `existing but unchanged targets`
  - 기본 동작에서는 그대로 둔다.
  - `--update-unchanged`를 주면 현재 bootstrap 기준 내용으로 다시 쓴다.
- `differing files`
  - 기본 동작에서는 수동 검토 대상으로 남긴다.
  - 정말 overwrite가 필요한 특정 경로만 `--force-overwrite`로 명시한다.
- `conflict candidates`
  - 기본 동작에서는 쓰지 않는다.
  - path shape 충돌이 아닌 regular file conflict만 `--force-overwrite`로 덮어쓸 수 있다.
  - 디렉터리 충돌, 부모 경로 shape 충돌은 먼저 수동으로 바로잡아야 한다.
- `legacy entrypoint migration candidates`
  - 기본 동작에서는 새 canonical 파일을 그냥 create하지 않는다.
  - `--migrate-legacy-entrypoint`를 주면 legacy `docs/harness_guide.md`를 `docs/entrypoint.md`로 rename하고, 안전한 경우 필요한 runtime entrypoint follow-up도 함께 적용한다.

## 현재 지원 범위

- safe create: 지원한다.
- unchanged target refresh: 지원한다.
- explicit path force overwrite: 지원한다.
- legacy project entrypoint rename migration: 제한적으로 지원한다.
- user-modified 파일 automatic merge: 지원하지 않는다.
- semantic diff 기반 selective update: 지원하지 않는다.

## 출력 해석

- `created files`
  - 이번 실행에서 새로 쓴 missing target 수다.
- `refreshed unchanged targets`
  - `--update-unchanged`로 다시 쓴 exact-match target 수다.
- `forced overwrites`
  - 사용자가 명시적으로 지정해 덮어쓴 경로 수다.
- `migrated legacy entrypoints`
  - legacy `docs/harness_guide.md`를 새 canonical `docs/entrypoint.md`로 옮긴 수다.
- `created runtime entrypoints for migration`
  - legacy entrypoint migration과 함께 새 canonical 흐름에 맞게 생성한 runtime entrypoint 수다.
- `refreshed runtime entrypoints for migration`
  - legacy `AGENTS.md`를 새 canonical runtime contract에 맞게 다시 쓴 수다.
- `remaining differing files`
  - 여전히 수동 검토가 필요한 파일 수다.
- `remaining conflict candidates`
  - path shape 문제 또는 unrelated 문서 가능성 때문에 수동 판단이 먼저 필요한 파일 수다.

## 권장 순서

1. 먼저 `adopt_dry_run.py`를 실행한다.
2. `legacy entrypoint migration candidates`가 보이면 `docs/harness_guide.md -> docs/entrypoint.md` rename migration이 필요한 상태로 읽는다.
3. legacy local path만 남아 있고 runtime entrypoint가 안전하게 따라올 수 있으면 `--migrate-legacy-entrypoint`를 먼저 검토한다.
4. legacy migration candidate가 없고 `missing files`가 주로 문제라면 `adopt_safe_write.py`를 기본 옵션으로 실행한다.
5. exact-match target만 다시 쓰고 싶으면 `--update-unchanged`를 추가한다.
6. `differing files`나 `conflict candidates`를 자동으로 전체 overwrite하지 않는다.
7. 정말 필요한 특정 경로만 `--force-overwrite`로 하나씩 명시한다.
8. write 전후로 partial adoption 상태가 structurally safe한지 보려면 `validate_overlay_consistency.py --mode incremental`을 먼저 쓴다.
9. 최소 문서 세트가 충분히 맞춰진 뒤에는 `validate_overlay_decisions.py`, `validate_overlay_consistency.py` full mode로 상태를 다시 확인한다.

## 주의점

- `--force-overwrite`는 explicit overwrite다. merge가 아니다.
- `--migrate-legacy-entrypoint`는 rename migration이지 semantic merge가 아니다.
- canonical `docs/entrypoint.md`가 이미 존재하거나, `AGENTS.md`가 legacy path를 가리키는 custom 문서로 크게 diverge한 경우는 수동 검토가 먼저다.
- 현재 판정 기준은 선택한 `--language` bootstrap baseline을 기준으로 한다.
- old bundle과 new bundle 사이의 semantic migration은 자동 판단하지 않는다.
