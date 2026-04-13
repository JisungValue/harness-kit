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
python3 vendor/harness-kit/scripts/check_first_success_docs.py .
python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness first-success
python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .
```

bootstrap 직후에는 `docs/project_entrypoint.md`와 `docs/decisions/README.md`를 먼저 읽고, 현재 작업에서 바로 중요하게 다뤄야 할 구조/정책/예외 결정이 있는지 확인한다.

`vendor/harness-kit/`가 아닌 다른 경로에 kit를 뒀다면, bootstrap 시점부터 `--vendor-path <actual-path>`를 같이 주는 쪽을 우선한다. 그렇게 생성하지 않았다면 `validate_overlay_consistency.py` 전에 `docs/project_entrypoint.md`와 `docs/standard/coding_conventions_project.md`의 vendored 경로를 먼저 실제 배치 경로로 맞춘다.

local validator가 통과하면 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 프로젝트 `.github/workflows/` 아래 workflow 파일로 복사하고 `@<pin-tag-or-sha>`를 실제 릴리스 태그 또는 고정 SHA로 바꿔 future-session guardrail을 붙인다.

### 2. 기존 프로젝트 또는 부분 도입 상태

```bash
python3 vendor/harness-kit/scripts/adopt_dry_run.py . --language python
```

그 다음 `legacy entrypoint migration candidates`, `missing files`, `conflict candidates`를 먼저 읽고, 최소 overlay 문서 세트가 어느 정도 맞춰졌을 때만 아래 validator로 넘어간다.

legacy `docs/harness_guide.md`가 남아 있으면 먼저 rename migration을 검토한다.

```bash
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python --migrate-legacy-entrypoint
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
- `--vendor-path`: generated `docs/project_entrypoint.md`, `docs/standard/coding_conventions_project.md` 안의 vendored reference를 실제 배치 경로로 맞춘다.

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

### check_first_success_docs.py

- 역할: 최소 문서 세트가 생겼는지만 가장 얕게 확인한다.
- write 여부: read-only
- 실행 전제: Python 3 runtime이 필요하다.
- 이 단계만으로는 next-session readiness나 future-session CI guardrail까지 보장하지 않는다.

성공 신호:

- `first success docs are present`

실패 신호:

- `first-success docs are missing:`
  - 출력된 bullet 목록의 문서를 먼저 채워야 한다.

### validate_overlay_decisions.py

- 역할: unresolved placeholder와 readiness 상태를 본다.
- write 여부: read-only

성공 신호:

- `overlay decision validation passed for readiness 'first-success'`
- `overlay decision validation passed for readiness 'phase2'`

실패 신호:

- `overlay decision validation failed for readiness '...'`
- `Missing required overlay docs:`
- `Resolve these required canonical fields first:`
- `Then resolve these blocking unresolved markers:`

해석:

- `first-success` 통과는 최소 시작 상태가 맞는지 보는 것이다.
- `phase2` 통과는 더 많은 placeholder가 정리되어야 한다.
- `Still allowed after the blocking items above are fixed:`가 함께 나오면, 현재 readiness에서 허용되는 미결정이 참고용으로 남아 있다는 뜻이다.
- `required-field`는 먼저 해결해야 하는 canonical 항목이며, 같은 줄의 placeholder가 allowed여도 중복으로 참고 목록에 다시 나오지 않는다.
- non-default vendoring이면 bootstrap 때 `--vendor-path`를 사용했는지 먼저 확인하면 unnecessary path drift를 줄일 수 있다.

### validate_overlay_consistency.py

- 역할: 문서 간 참조와 책임 경계가 맞는지 본다.
- 추가로 runtime instruction entrypoint가 같은 공통 진입점으로 수렴하는지도 본다.
- write 여부: read-only

성공 신호:

- `overlay consistency validation passed.`

실패 신호:

- `overlay consistency validation failed.`
- 이어서 어떤 문서의 어떤 계약이 깨졌는지 bullet로 출력된다.

해석:

- unresolved decision이 아니라, 문서 세트의 구조적 연결이 맞는지 보는 단계다.
- 예: `AGENTS.md`가 `docs/project_entrypoint.md`로 연결되는지, `implementation_order.md`가 `architecture.md`를 기준으로 연결하는지, quality gate와 testing profile이 서로 역할을 나누는지.
- non-default vendored path라면 common guide 경로나 bootstrap 기준 문서 경로가 실제로 존재하는지도 함께 본다.
- decisions index가 있으면 project entrypoint와 연결되는지, index에 적힌 decision file이 실제로 존재하는지도 함께 본다.
- 이 단계가 통과하면 local first-success confidence는 갖췄다고 보고, 이후에는 workflow template로 CI guardrail을 붙인다.

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
- `legacy entrypoint migration candidates`
  - 예전 project-local `docs/harness_guide.md`가 남아 있어 `docs/project_entrypoint.md`로 rename migration이 먼저 필요한 대상
  - 기본 safe create보다 `--migrate-legacy-entrypoint` 또는 수동 rename 검토가 우선이다

### adopt_safe_write.py

- 역할: `adopt_dry_run.py`와 같은 분류를 기준으로 제한적 write를 수행한다.
- write 여부: write 한다.
- 기본 동작: `missing files`만 생성한다.
- `--update-unchanged`: exact-match target을 현재 bootstrap 기준으로 다시 쓴다.
- `--force-overwrite`: 명시한 특정 경로만 overwrite한다.
- `--migrate-legacy-entrypoint`: legacy `docs/harness_guide.md`를 새 canonical `docs/project_entrypoint.md`로 rename하고 안전한 runtime entrypoint follow-up을 적용한다.
- merge/semantic update: 하지 않는다.

성공 신호:

- `adopt safe write for ...`
- `created files`, `refreshed unchanged targets`, `forced overwrites`

실패 신호:

- `adopt safe write failed.`
- `invalid force-overwrite target:`
- `force-overwrite blocked by target path shape conflict:`
- `legacy entrypoint migration blocked:`

## fail-fast 와 dry-run 해석 규칙

- fail-fast는 write 전에 멈춘다는 뜻이다.
- dry-run은 분류와 보고만 하고 파일은 바꾸지 않는다는 뜻이다.
- 현재 `0.1.0`에서 adopt는 read-only dry-run과 제한적 safe write까지만 있다.
- 현재 `0.1.0`에서 일반 merge-based update는 없다.
- 따라서 `adopt_dry_run.py` 결과를 보고 바로 전체 merge/write가 일어난다고 기대하면 안 된다.

## 흔한 로컬 진단 순서

### 새 프로젝트인데 init가 안 된다

1. 대상 경로에 이미 `docs/project_entrypoint.md`나 `docs/standard/*`가 있는지 본다.
2. 부모 경로 중 파일이 있는지 본다.
3. non-default vendoring이면 `--vendor-path <actual-path>`를 같이 줬는지 본다.
4. overwrite가 정말 필요한 경우에만 `--force`를 쓴다.

### 문서는 생겼는데 validator가 실패한다

1. `coding_conventions_project.md`의 언어/ bootstrap 기준 문서가 채워졌는지 본다.
2. `quality_gate_profile.md`, `commit_rule.md`의 placeholder가 현재 readiness에서 허용되는 범위인지 본다.
3. `phase2` 실패면 `first-success`부터 통과하는지 먼저 본다.
4. local validator는 통과했는데 이후 세션에서 drift가 반복되면 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 복사했고 `@<pin-tag-or-sha>`를 실제 ref로 바꿨는지 본다.

### decision validator는 통과하는데 consistency checker가 실패한다

1. `AGENTS.md`가 `docs/project_entrypoint.md`를 가리키고, `CLAUDE.md`/`GEMINI.md`가 `AGENTS.md`를 다시 가리키는지 본다.
2. `implementation_order.md`가 `architecture.md`를 기준 문서로 연결하는지 본다.
3. `quality_gate_profile.md`와 `testing_profile.md`가 서로 책임 경계를 참조하는지 본다.

### 기존 프로젝트인데 무엇부터 해야 할지 모르겠다

1. `adopt_dry_run.py`부터 실행한다.
2. `legacy entrypoint migration candidates`가 있으면 `docs/harness_guide.md -> docs/project_entrypoint.md` migration부터 검토한다.
3. `missing files`와 `conflict candidates`를 먼저 구분한다.
4. `missing files`가 주 문제면 `adopt_safe_write.py`로 제한적 생성부터 수행한다.
5. baseline과 큰 차이가 없는 경우에만 이후 validator로 넘어간다.

## 관련 문서

- 새 프로젝트 first success: `docs/project_overlay/first_success_guide.md`
- 기존 프로젝트 read-only 비교: `docs/project_overlay/adopt_dry_run.md`
- 기존 프로젝트 제한적 write: `docs/project_overlay/adopt_safe_write.md`
- unresolved placeholder readiness: `docs/project_overlay/unresolved_decision_validator.md`
- cross-document consistency: `docs/project_overlay/cross_document_consistency_checker.md`
- 사람이 읽는 overlay 완료 판정: `docs/project_overlay/overlay_completion_checklist.md`
