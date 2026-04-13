# Downstream Bundle Smoke Validation

## 목적

이 문서는 canonical `dist/harness-kit-project-bundle/`만으로 새 프로젝트 bootstrap 경로, localized vendoring 경로, future-session CI onboarding 자산, 기존 프로젝트 adopt dry-run 경로가 실제로 동작하는지 확인하는 maintainer용 smoke validation 기준이다.

## 검증 대상

- `scripts/generate_downstream_bundle.py`
- canonical `dist/harness-kit-project-bundle/`
- generated bundle 안의 `scripts/bootstrap_init.py`
- generated bundle 안의 `scripts/check_first_success_docs.py`
- generated bundle 안의 `docs/project_overlay/harness_doc_guard_workflow_template.yml`
- generated bundle 안의 `scripts/adopt_dry_run.py`
- generated bundle 안의 `scripts/adopt_safe_write.py`
- generated bundle 안의 `scripts/validate_overlay_decisions.py`
- generated bundle 안의 `scripts/validate_overlay_consistency.py`
- `tests/test_downstream_bundle_smoke.py`

## 검증 시나리오

### 시나리오 1. greenfield vendored bundle bootstrap

- 입력 조건:
- 빈 임시 consumer project
- canonical `dist/harness-kit-project-bundle/`를 `vendor/harness-kit/`로 복사
- 언어 선택: `python`, `java`, `kotlin`
- 실행 명령:

```bash
python3 /tmp/python-project/vendor/harness-kit/scripts/bootstrap_init.py /tmp/python-project --language python
python3 /tmp/python-project/vendor/harness-kit/scripts/check_first_success_docs.py /tmp/python-project
python3 /tmp/python-project/vendor/harness-kit/scripts/validate_overlay_decisions.py /tmp/python-project --readiness first-success
python3 /tmp/python-project/vendor/harness-kit/scripts/validate_overlay_consistency.py /tmp/python-project

python3 /tmp/java-project/vendor/harness-kit/scripts/bootstrap_init.py /tmp/java-project --language java
python3 /tmp/java-project/vendor/harness-kit/scripts/check_first_success_docs.py /tmp/java-project
python3 /tmp/java-project/vendor/harness-kit/scripts/validate_overlay_decisions.py /tmp/java-project --readiness first-success
python3 /tmp/java-project/vendor/harness-kit/scripts/validate_overlay_consistency.py /tmp/java-project

python3 /tmp/kotlin-project/vendor/harness-kit/scripts/bootstrap_init.py /tmp/kotlin-project --language kotlin
python3 /tmp/kotlin-project/vendor/harness-kit/scripts/check_first_success_docs.py /tmp/kotlin-project
python3 /tmp/kotlin-project/vendor/harness-kit/scripts/validate_overlay_decisions.py /tmp/kotlin-project --readiness first-success
python3 /tmp/kotlin-project/vendor/harness-kit/scripts/validate_overlay_consistency.py /tmp/kotlin-project

python3 /tmp/localized-project/third_party/harness-kit/scripts/bootstrap_init.py /tmp/localized-project --language python --vendor-path third_party/harness-kit
python3 /tmp/localized-project/third_party/harness-kit/scripts/check_first_success_docs.py /tmp/localized-project
python3 /tmp/localized-project/third_party/harness-kit/scripts/validate_overlay_decisions.py /tmp/localized-project --readiness first-success
python3 /tmp/localized-project/third_party/harness-kit/scripts/validate_overlay_consistency.py /tmp/localized-project
```

- 기대 결과:
  - 각 언어별 fresh consumer project에서 canonical bundle의 project-facing script만으로 최소 문서 세트 생성과 first-success validator 실행이 끝난다.
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`도 함께 생성되고 `AGENTS.md -> docs/project_entrypoint.md` 연결이 성립한다.
  - `docs/decisions/README.md`도 함께 생성된다.
  - `docs/project_entrypoint.md`와 `coding_conventions_project.md`는 vendored bundle 경로를 그대로 참조한다.
  - `coding_conventions_project.md`는 각 언어에 맞는 bootstrap convention template 경로를 가리킨다.
  - localized vendoring 시나리오는 `--vendor-path third_party/harness-kit`만으로 manual path edit 없이 consistency validator까지 통과한다.
  - generated bundle 안에 `docs/project_overlay/harness_doc_guard_workflow_template.yml`이 존재하고, consumer project는 이를 `.github/workflows/harness-doc-guard.yml`로 복사한 뒤 `@<pin-tag-or-sha>`를 실제 ref로 치환해 future-session guardrail을 붙일 수 있다.
  - bundle 안에 maintainer 전용 문서나 maintainer용 bundle script가 없어도 greenfield 경로가 막히지 않는다.

### 시나리오 2. brownfield partial repo adopt dry-run

- 입력 조건:
  - canonical `dist/harness-kit-project-bundle/`를 `vendor/harness-kit/`로 복사한 임시 consumer project
  - 기존 프로젝트 쪽에는 `docs/project_entrypoint.md`만 있고, 나머지 최소 문서 세트와 decisions index는 없음
  - 기존 `docs/project_entrypoint.md`는 heading은 유지하지만 vendored guide 경로를 다른 위치로 현지화한 상태
- 실행 명령:

```bash
python3 vendor/harness-kit/scripts/adopt_dry_run.py . --language python
```

- 기대 결과:
  - dry-run이 write 없이 `missing files`, `differing files`, `conflict candidates`를 출력한다.
  - 위 조건에서는 `docs/project_entrypoint.md`가 `differing files`로 분류되고, 나머지 최소 문서 세트, decisions index, runtime entrypoint 세트는 `missing files`로 남는다.
  - maintainer 전용 자산 없이도 brownfield inspection 경로가 동작한다.

### 시나리오 3. brownfield missing-file safe write

- 입력 조건:
  - canonical `dist/harness-kit-project-bundle/`를 `vendor/harness-kit/`로 복사한 임시 consumer project
  - 기존 프로젝트 쪽에는 localized `docs/project_entrypoint.md`만 있고, 나머지 최소 문서 세트와 decisions index는 없음
- 실행 명령:

```bash
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python
```

- 기대 결과:
  - `missing files`는 생성되고 localized `docs/project_entrypoint.md`는 기본 동작에서 그대로 남는다.
  - 실행 후 first-success 문서 존재 확인과 overlay decision validator가 통과한다.
  - maintainer 전용 자산 없이도 brownfield create-only safe write 경로가 동작한다.

### 시나리오 4. legacy entrypoint migration

- 입력 조건:
  - canonical `dist/harness-kit-project-bundle/`를 `vendor/harness-kit/`로 복사한 임시 consumer project
  - 기존 프로젝트 쪽에는 legacy `docs/harness_guide.md`만 있고 `AGENTS.md`도 legacy 경로를 가리킨다.
- 실행 명령:

```bash
python3 vendor/harness-kit/scripts/adopt_dry_run.py . --language python
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python --migrate-legacy-entrypoint
python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .
```

- 기대 결과:
  - dry-run이 `legacy entrypoint migration candidates`를 보고한다.
  - safe write가 legacy entrypoint를 canonical `docs/project_entrypoint.md`로 rename migration 한다.
  - migration 후 consistency validator가 통과한다.

## 실행 명령

```bash
python3 -m unittest tests.test_downstream_bundle_smoke
```

## 현재 기준 기대 결과

- canonical `dist/harness-kit-project-bundle/`만으로 greenfield `python`/`java`/`kotlin` bootstrap, localized vendoring bootstrap, first-success validator, brownfield adopt dry-run, brownfield create-only safe write, legacy entrypoint migration의 최소 흐름이 재현된다.
- generated bundle은 consumer-facing workflow template까지 포함해 local first-success 뒤의 future-session CI onboarding 경로도 끊기지 않는다.
- smoke test는 maintainer 전용 자산 누락 때문에 consumer 경로가 깨지는 문제를 release 전에 조기에 드러낸다.

## 잔여 리스크

- smoke test는 bundle usability를 보는 경량 검증이다. explicit overwrite 정책의 세부 upgrade 판단, impact classification, diff review는 후속 이슈에서 더 추가된다.
- brownfield 경로는 여전히 read-only inspection 중심이며 자동 merge나 semantic update는 지원하지 않는다.
