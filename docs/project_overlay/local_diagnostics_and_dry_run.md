# Local Diagnostics And Dry-Run

이 문서는 `harness-kit` bootstrap 관련 문제를 CI 전에 로컬에서 먼저 좁히는 방법을 정리한다.

## 목적

- init, validator, adopt dry-run을 어떤 순서로 먼저 돌려야 하는지 한 곳에서 본다.
- 각 명령의 출력이 무엇을 뜻하는지 빠르게 해석한다.
- fail-fast와 write/dry-run 의미를 혼동하지 않게 한다.

## 먼저 구분할 것

- 새 프로젝트 또는 거의 빈 프로젝트면 `first success` 경로를 따른다.
- 기존 프로젝트나 부분 도입 상태면 `adopt dry-run`부터 시작한다.
- 현재 `0.1.0` 범위에서 기존 프로젝트 비교는 `adopt_dry_run.py`, 제한적 brownfield write는 `adopt_safe_write.py`가 담당한다.
- `bootstrap_init.py --force`는 merge가 아니라 overwrite다.

## 권장 로컬 진단 순서

### 1. 새 프로젝트 first success

```bash
python3 vendor/harness-kit/scripts/bootstrap_init.py . --language python
python3 -c "from pathlib import Path; paths = ['docs/harness_guide.md', 'docs/standard/architecture.md', 'docs/standard/implementation_order.md', 'docs/standard/coding_conventions_project.md', 'docs/standard/quality_gate_profile.md', 'docs/standard/testing_profile.md', 'docs/standard/commit_rule.md']; missing = [p for p in paths if not Path(p).exists()]; print('first success docs are present') if not missing else (_ for _ in ()).throw(SystemExit('missing: ' + ', '.join(missing)))"
python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness first-success
python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .
```

### 2. 기존 프로젝트 또는 부분 도입 상태

```bash
python3 vendor/harness-kit/scripts/adopt_dry_run.py . --language python
```

그 다음 `missing files`와 `conflict candidates`가 크지 않고, 최소 overlay 문서 세트가 어느 정도 맞춰졌을 때만 아래 validator로 넘어간다.

필요하면 `missing files`를 먼저 안전하게 생성한다.

```bash
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python
```

```bash
python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness first-success
python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .
```

## 명령별 의미

### bootstrap_init.py

- 역할: 최소 overlay 문서 세트를 실제로 생성한다.
- write 여부: write 한다.
- 기본 동작: fail-fast
- `--force`: overwrite만 수행한다. merge하지 않는다.

성공 신호:

- `Created harness bootstrap docs in ...`
- 생성된 문서 경로와 source template 경로가 함께 출력된다.

자주 보는 실패:

- `bootstrap init failed: target files already exist.`
  - 생성 대상 파일이 이미 있다.
  - overwrite가 정말 맞는 경우에만 `--force`를 쓴다.
- `bootstrap init failed: target path is not writable as a bootstrap tree.`
  - target path 자체가 디렉터리가 아니거나, 부모 경로 중 하나가 파일이다.
  - 먼저 경로 shape를 바로잡아야 한다.

### first success 존재 확인 one-liner

- 역할: 최소 문서 세트가 생겼는지만 가장 얕게 확인한다.
- write 여부: read-only

성공 신호:

- `first success docs are present`

실패 신호:

- `missing: ...`
  - 빠진 문서 경로를 먼저 채워야 한다.

### validate_overlay_decisions.py

- 역할: unresolved placeholder와 readiness 상태를 본다.
- write 여부: read-only

성공 신호:

- `overlay decision validation passed for readiness 'first-success'`
- `overlay decision validation passed for readiness 'phase2'`

실패 신호:

- `overlay decision validation failed for readiness '...'`
- `Missing required overlay docs:`
- `Blocking unresolved markers:`

해석:

- `first-success` 통과는 최소 시작 상태가 맞는지 보는 것이다.
- `phase2` 통과는 더 많은 placeholder가 정리되어야 한다.
- `Allowed unresolved markers`가 함께 나오면, 현재 readiness에서 허용되는 미결정이 남아 있다는 뜻이다.

### validate_overlay_consistency.py

- 역할: 문서 간 참조와 책임 경계가 맞는지 본다.
- write 여부: read-only

성공 신호:

- `overlay consistency validation passed.`

실패 신호:

- `overlay consistency validation failed.`
- 이어서 어떤 문서의 어떤 계약이 깨졌는지 bullet로 출력된다.

해석:

- unresolved decision이 아니라, 문서 세트의 구조적 연결이 맞는지 보는 단계다.
- 예: `implementation_order.md`가 `architecture.md`를 기준으로 연결하는지, quality gate와 testing profile이 서로 역할을 나누는지.

### adopt_dry_run.py

- 역할: 기존 프로젝트의 현재 상태를 bootstrap baseline과 비교한다.
- write 여부: read-only
- merge/overwrite: 하지 않는다.

출력 분류:

- `missing files`
  - 현재 없는 대상 문서
  - bootstrap preflight 기준으로 safe-to-create 후보
- `existing but unchanged targets`
  - bootstrap baseline과 완전히 같은 대상
- `differing files`
  - baseline과 다르지만 최소한 같은 primary heading을 유지하는 대상
  - 보통 프로젝트 현지화 결과라 수동 검토 대상으로 본다
- `conflict candidates`
  - target path shape가 잘못됐거나, unrelated 문서일 가능성이 높은 대상
  - overwrite보다 수동 판단이 먼저 필요하다

### adopt_safe_write.py

- 역할: `adopt_dry_run.py`와 같은 분류를 기준으로 제한적 write를 수행한다.
- write 여부: write 한다.
- 기본 동작: `missing files`만 생성한다.
- `--update-unchanged`: exact-match target을 현재 bootstrap 기준으로 다시 쓴다.
- `--force-overwrite`: 명시한 특정 경로만 overwrite한다.
- merge/semantic update: 하지 않는다.

성공 신호:

- `adopt safe write for ...`
- `created files`, `refreshed unchanged targets`, `forced overwrites`

실패 신호:

- `adopt safe write failed.`
- `invalid force-overwrite target:`
- `force-overwrite blocked by target path shape conflict:`

## fail-fast 와 dry-run 해석 규칙

- fail-fast는 write 전에 멈춘다는 뜻이다.
- dry-run은 분류와 보고만 하고 파일은 바꾸지 않는다는 뜻이다.
- 현재 `0.1.0`에서 adopt는 read-only dry-run과 제한적 safe write까지만 있다.
- 현재 `0.1.0`에서 일반 merge-based update는 없다.
- 따라서 `adopt_dry_run.py` 결과를 보고 바로 전체 merge/write가 일어난다고 기대하면 안 된다.

## 흔한 로컬 진단 순서

### 새 프로젝트인데 init가 안 된다

1. 대상 경로에 이미 `docs/harness_guide.md`나 `docs/standard/*`가 있는지 본다.
2. 부모 경로 중 파일이 있는지 본다.
3. overwrite가 정말 필요한 경우에만 `--force`를 쓴다.

### 문서는 생겼는데 validator가 실패한다

1. `coding_conventions_project.md`의 언어/ bootstrap 기준 문서가 채워졌는지 본다.
2. `quality_gate_profile.md`, `commit_rule.md`의 placeholder가 현재 readiness에서 허용되는 범위인지 본다.
3. `phase2` 실패면 `first-success`부터 통과하는지 먼저 본다.

### decision validator는 통과하는데 consistency checker가 실패한다

1. `docs/harness_guide.md`가 필수 `docs/standard/*`를 모두 참조하는지 본다.
2. `implementation_order.md`가 `architecture.md`를 기준 문서로 연결하는지 본다.
3. `quality_gate_profile.md`와 `testing_profile.md`가 서로 책임 경계를 참조하는지 본다.

### 기존 프로젝트인데 무엇부터 해야 할지 모르겠다

1. `adopt_dry_run.py`부터 실행한다.
2. `missing files`와 `conflict candidates`를 먼저 구분한다.
3. `missing files`가 주 문제면 `adopt_safe_write.py`로 제한적 생성부터 수행한다.
4. baseline과 큰 차이가 없는 경우에만 이후 validator로 넘어간다.

## 관련 문서

- 새 프로젝트 first success: `docs/project_overlay/first_success_guide.md`
- 기존 프로젝트 read-only 비교: `docs/project_overlay/adopt_dry_run.md`
- 기존 프로젝트 제한적 write: `docs/project_overlay/adopt_safe_write.md`
- unresolved placeholder readiness: `docs/project_overlay/unresolved_decision_validator.md`
- cross-document consistency: `docs/project_overlay/cross_document_consistency_checker.md`
- 사람이 읽는 overlay 완료 판정: `docs/project_overlay/overlay_completion_checklist.md`
