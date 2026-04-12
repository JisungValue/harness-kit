# Quickstart

`harness-kit`를 처음 쓰는 사람이 `0.1.0` 범위 안에서 가장 빨리 시작하는 방법을 정리한 문서다.

## 누구를 위한 문서인가

- 새 프로젝트를 시작하려는 팀
- 기존 프로젝트에 `harness-kit`를 부분 도입하려는 팀
- 여러 세부 문서를 오가기 전에 전체 흐름을 먼저 알고 싶은 사용자

## 0.1.0에서 바로 할 수 있는 것

- 새 프로젝트에 최소 overlay 문서 세트를 생성한다.
- first success 상태를 로컬에서 확인한다.
- overlay 문서의 unresolved decision을 점검한다.
- overlay 문서 간 교차 정합성을 점검한다.
- 기존 프로젝트 상태를 read-only dry-run으로 읽고 baseline과 비교한다.
- 기존 프로젝트에서 missing file create와 explicit path overwrite 중심의 제한적 safe write/update를 수행한다.

## 0.1.0에서 아직 안 되는 것

- 기존 프로젝트에 대한 자동 merge
- user-modified existing file에 대한 automatic merge/update
- framework별 semantic diff
- interactive TUI

## 빠른 시작 경로

### 새 프로젝트

1. `harness-kit`를 프로젝트 안의 vendored 경로로 둔다.
   - 아래 예시는 `vendor/harness-kit/`를 기준으로 한다.
   - 다른 경로를 쓰면 예시 명령의 `vendor/harness-kit/` 부분을 실제 경로로 바꿔서 실행한다.
2. `docs/project_overlay/first_success_guide.md`를 본다.
3. `docs/project_overlay/local_diagnostics_and_dry_run.md`를 같이 본다.
4. 아래 명령을 실행한다.

```bash
python3 vendor/harness-kit/scripts/bootstrap_init.py . --language python
python3 -c "from pathlib import Path; paths = ['docs/project_entrypoint.md', 'docs/standard/architecture.md', 'docs/standard/implementation_order.md', 'docs/standard/coding_conventions_project.md', 'docs/standard/quality_gate_profile.md', 'docs/standard/testing_profile.md', 'docs/standard/commit_rule.md']; missing = [p for p in paths if not Path(p).exists()]; print('first success docs are present') if not missing else (_ for _ in ()).throw(SystemExit('missing: ' + ', '.join(missing)))"
python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness first-success
python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .
```

5. `docs/project_entrypoint.md`와 `docs/standard/coding_conventions_project.md`의 vendored 경로를 실제 배치 경로에 맞게 현지화한다.
6. `vendor/harness-kit/docs/templates/task/`를 프로젝트 작업 경로로 복사해 첫 task를 시작한다.

### 기존 프로젝트 또는 부분 도입 상태

1. `docs/project_overlay/adopt_dry_run.md`를 본다.
2. `docs/project_overlay/local_diagnostics_and_dry_run.md`를 같이 본다.
3. 아래 명령을 실행한다.

```bash
python3 vendor/harness-kit/scripts/adopt_dry_run.py . --language python
```

4. 결과를 아래처럼 읽는다.
    - `missing files`: 안전하게 생성 가능한 후보
    - `existing but unchanged targets`: baseline과 동일
    - `differing files`: 수동 검토 대상
    - `conflict candidates`: 수동 판단 우선 대상
    - `legacy entrypoint migration candidates`: 예전 `docs/harness_guide.md`를 새 canonical `docs/project_entrypoint.md`로 옮겨야 하는 상태
5. `legacy entrypoint migration candidates`가 보이면 아래 rename migration부터 먼저 검토한다.

```bash
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python --migrate-legacy-entrypoint
```

6. legacy migration candidate가 없고 `missing files`를 먼저 안전하게 반영하려면 아래 명령을 실행한다.

```bash
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python
```

7. exact-match target만 다시 쓰거나 특정 경로만 명시적으로 덮어쓰려면 아래처럼 범위를 좁힌다.

```bash
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python --update-unchanged
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python --force-overwrite docs/project_entrypoint.md
```

8. `differing files`와 `conflict candidates`는 기본적으로 수동 비교 대상으로 남긴다.
9. 최소 문서 세트가 어느 정도 맞춰진 뒤에만 아래 validator로 넘어간다.
10. 새 bundle 버전을 반영할 때 영향도를 먼저 분류하려면 `docs/project_overlay/harness_upgrade_impact_policy.md`를 함께 본다.

```bash
python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness first-success
python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .
```

## 핵심 도구 역할

- `bootstrap_init.py`
  - 새 프로젝트용 문서 세트를 실제로 생성한다.
- `validate_overlay_decisions.py`
  - unresolved placeholder와 readiness 상태를 본다.
- `validate_overlay_consistency.py`
  - 문서 간 참조, runtime instruction entrypoint 연결, 책임 경계를 본다.
- `adopt_dry_run.py`
  - 기존 프로젝트 상태를 read-only로 분류한다.
- `adopt_safe_write.py`
  - 기존 프로젝트에서 missing file create, unchanged refresh, explicit path force overwrite만 허용하는 제한적 write 도구다.

## first-success 와 phase2 차이

- `first-success`
  - 최소 문서 세트가 갖춰졌고, 초기 시작 상태가 성립하는지 본다.
  - 일부 placeholder는 아직 허용된다.
- `phase2`
  - 실제 구현/감사에 들어가기 전 더 많은 프로젝트 결정을 채웠는지 본다.
  - `first-success`보다 훨씬 엄격하다.

## 흔한 실패 원인

- init 대상 경로에 이미 생성 대상 문서가 있어 fail-fast가 발생함
- vendored path를 실제 프로젝트 경로에 맞게 현지화하지 않음
- `--language`를 실제 프로젝트와 다르게 선택함
- 기존 프로젝트에서 `adopt_dry_run.py` 결과를 보지 않고 validator를 너무 일찍 실행함
- 기존 프로젝트에서 legacy `docs/harness_guide.md`를 그냥 두고 `docs/project_entrypoint.md`만 새로 생성해 반쪽 migration 상태가 됨
- `validate_overlay_decisions.py`와 `validate_overlay_consistency.py`의 역할 차이를 혼동함

## 다음에 읽을 문서

- 전체 동작 설명: `docs/how_harness_kit_works.md`
- 새 프로젝트 시작: `docs/project_overlay/first_success_guide.md`
- 로컬 진단: `docs/project_overlay/local_diagnostics_and_dry_run.md`
- 기존 프로젝트 dry-run: `docs/project_overlay/adopt_dry_run.md`
- 기존 프로젝트 upgrade impact 분류: `docs/project_overlay/harness_upgrade_impact_policy.md`
