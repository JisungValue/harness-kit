# Downstream Bundle Smoke Validation

## 목적

이 문서는 canonical `dist/harness-kit-project-bundle/`만으로 새 프로젝트 bootstrap 경로와 기존 프로젝트 adopt dry-run 경로가 실제로 동작하는지 확인하는 maintainer용 smoke validation 기준이다.

## 검증 대상

- `scripts/generate_downstream_bundle.py`
- canonical `dist/harness-kit-project-bundle/`
- generated bundle 안의 `scripts/bootstrap_init.py`
- generated bundle 안의 `scripts/adopt_dry_run.py`
- generated bundle 안의 `scripts/validate_overlay_decisions.py`
- generated bundle 안의 `scripts/validate_overlay_consistency.py`
- `tests/test_downstream_bundle_smoke.py`

## 검증 시나리오

### 시나리오 1. greenfield vendored bundle bootstrap

- 입력 조건:
  - 빈 임시 consumer project
  - canonical `dist/harness-kit-project-bundle/`를 `vendor/harness-kit/`로 복사
  - 언어 선택: `python`
- 실행 명령:

```bash
python3 vendor/harness-kit/scripts/bootstrap_init.py . --language python
python3 -c "from pathlib import Path; paths = ['docs/harness_guide.md', 'docs/standard/architecture.md', 'docs/standard/implementation_order.md', 'docs/standard/coding_conventions_project.md', 'docs/standard/quality_gate_profile.md', 'docs/standard/testing_profile.md', 'docs/standard/commit_rule.md']; missing = [p for p in paths if not Path(p).exists()]; print('first success docs are present') if not missing else (_ for _ in ()).throw(SystemExit('missing: ' + ', '.join(missing)))"
python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness first-success
python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .
```

- 기대 결과:
  - canonical bundle의 project-facing script만으로 최소 문서 세트 생성과 first-success validator 실행이 끝난다.
  - `docs/harness_guide.md`와 `coding_conventions_project.md`는 vendored bundle 경로를 그대로 참조한다.
  - bundle 안에 maintainer 전용 문서나 maintainer용 bundle script가 없어도 greenfield 경로가 막히지 않는다.

### 시나리오 2. brownfield partial repo adopt dry-run

- 입력 조건:
  - canonical `dist/harness-kit-project-bundle/`를 `vendor/harness-kit/`로 복사한 임시 consumer project
  - 기존 프로젝트 쪽에는 `docs/harness_guide.md`만 있고, 나머지 최소 문서 세트는 없음
  - 기존 `docs/harness_guide.md`는 heading은 유지하지만 vendored guide 경로를 다른 위치로 현지화한 상태
- 실행 명령:

```bash
python3 vendor/harness-kit/scripts/adopt_dry_run.py . --language python
```

- 기대 결과:
  - dry-run이 write 없이 `missing files`, `differing files`, `conflict candidates`를 출력한다.
  - 위 조건에서는 `docs/harness_guide.md`가 `differing files`로 분류되고, 나머지 최소 문서 세트는 `missing files`로 남는다.
  - maintainer 전용 자산 없이도 brownfield inspection 경로가 동작한다.

## 실행 명령

```bash
python3 -m unittest tests.test_downstream_bundle_smoke
```

## 현재 기준 기대 결과

- canonical `dist/harness-kit-project-bundle/`만으로 greenfield bootstrap, first-success validator, brownfield adopt dry-run의 최소 흐름이 재현된다.
- smoke test는 maintainer 전용 자산 누락 때문에 consumer 경로가 깨지는 문제를 release 전에 조기에 드러낸다.

## 잔여 리스크

- smoke test는 bundle usability를 보는 경량 검증이다. safe write/update, upgrade impact classification, diff review는 후속 이슈에서 더 추가된다.
- brownfield 경로는 여전히 read-only inspection 중심이며 자동 merge나 semantic update는 지원하지 않는다.
