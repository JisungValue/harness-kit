# Adopt Dry-Run

이 문서는 이미 일부 harness가 적용된 프로젝트에서 현재 상태를 읽고 bootstrap 기준과의 차이를 write 없이 비교하는 방법을 설명한다.

## 목적

- 기존 프로젝트에 새 문서를 무조건 복사하지 않고, 현재 상태를 먼저 읽는다.
- bootstrap 기준 대비 어떤 파일이 없는지, 그대로인지, 달라졌는지, 수동 판단이 필요한지 나눈다.
- force overwrite와 의미적으로 분리된 read-only adopt 흐름을 제공한다.

## 실행 명령

프로젝트 루트에서 아래처럼 실행한다.

```bash
python3 vendor/harness-kit/scripts/adopt_dry_run.py . --language python
```

언어 baseline은 현재 프로젝트가 비교하고 싶은 bootstrap 기준과 맞춰 선택한다.

## 출력 분류

- `missing files`
  - 현재 프로젝트에 없는 bootstrap 대상 파일이다.
  - bootstrap 기준으로 안전하게 생성 가능한 후보로 본다.
- `existing but unchanged targets`
  - 현재 파일이 bootstrap 기준과 완전히 같은 상태다.
  - adopt 관점에서는 추가 조치가 거의 필요 없다.
- `differing files`
  - 현재 파일이 bootstrap 기준과 다르지만, 최소한 같은 primary heading을 유지한다.
  - 보통은 프로젝트 현지화 결과이므로 수동 검토 대상이다.
- `conflict candidates`
  - 현재 파일이 unrelated 문서이거나, target path가 파일이 아니거나, bootstrap 기준과의 shape 충돌이 크다.
  - overwrite보다 수동 판단이 먼저 필요한 대상으로 본다.
- `legacy entrypoint migration candidates`
  - 예전 project-local 경로 `docs/harness_guide.md`가 남아 있어, 새 canonical 경로 `docs/entrypoint.md`로 rename migration이 먼저 필요한 상태다.
  - 기본 safe create보다 `adopt_safe_write.py --migrate-legacy-entrypoint` 또는 수동 rename 검토가 우선이다.

## 예시 해석

- `docs/entrypoint.md`가 process guide path만 다르면 보통 `differing files`로 나온다.
- legacy `docs/harness_guide.md`만 있고 `docs/entrypoint.md`가 아직 없으면 보통 `legacy entrypoint migration candidates`로 나온다.
- `docs/project/standards/commit_rule.md`가 다른 제목의 unrelated 문서로 바뀌어 있으면 `conflict candidates`로 나온다.
- `docs/project/standards/testing_profile.md`가 없으면 `missing files`로 나온다.

## 현재 범위

- write는 하지 않는다.
- 자동 merge는 하지 않는다.
- framework별 의미 비교는 하지 않는다.
- baseline 비교는 선택한 `--language`의 bootstrap 결과를 기준으로 한다.

## 다음 단계

- `legacy entrypoint migration candidates`가 있으면 먼저 rename migration부터 검토한다.
- `missing files`는 legacy migration candidate가 없을 때 우선적으로 확인해 안전하게 추가 가능한 범위를 판단한다.
- partial adoption 상태가 structurally safe한지 먼저 보려면 `python3 scripts/validate_overlay_consistency.py . --mode incremental`을 함께 실행한다.
- incremental mode는 missing docs/runtime entrypoints를 follow-up으로 보여 주고, legacy leftover나 broken traversal chain 같은 unsafe state는 계속 fail 한다.
- 자동 복사가 괜찮은 `missing files`는 `bootstrap/docs/project_overlay/adopt_safe_write.md`의 제한적 safe write 경로로 생성할 수 있다.
- `differing files`와 `conflict candidates`는 수동 검토 대상으로 남긴다.
- 최소 문서 세트가 더 맞춰지면 `validate_overlay_decisions.py`, `validate_overlay_consistency.py` full mode로 올라가 현재 프로젝트 overlay 상태를 더 구체적으로 점검한다.
- init / validator / adopt dry-run을 어떤 순서로 로컬에서 먼저 돌릴지는 `bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md`를 본다.
