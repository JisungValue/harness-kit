# Downstream Bundle Boundary

이 문서는 `harness-kit` 저장소 안의 자산 중 무엇이 downstream 배포 대상이고, 무엇이 maintainer 전용 자산인지 구분하는 기준을 정의한다.

## 목적

- 이미 작성된 프로젝트에 `harness-kit`를 적용할 때, 소비자가 실제로 받는 배포 단위를 먼저 명확히 한다.
- safe write/update, upgrade impact, diff review가 모두 같은 배포 경계를 기준으로 동작하게 한다.
- maintainer 전용 운영 자산이 downstream 배포물에 섞이지 않게 한다.

## 핵심 원칙

- 저장소 전체가 곧 downstream 배포물은 아니다.
- downstream bundle은 저장소 안 source-of-truth 자산에서 파생되는 배포용 부분집합이다.
- maintainer 전용 감사, 릴리스, 기록 자산은 저장소 안에 유지하되 downstream bundle에는 포함하지 않는다.
- downstream bundle 경계는 repo-local 문서 기준으로 관리하며, 릴리스 직전 임의 판단으로 바꾸지 않는다.
- bundle 생성은 section 1, 2의 include path를 기본 후보 집합으로 삼고, section 3 maintainer-only path가 겹치면 exclusion을 우선 적용한다.

## 자산 분류

### 1) Downstream 필수 자산

downstream 프로젝트가 `harness-kit`를 시작하거나 적용하고 검증하는 데 직접 필요한 자산이다.

- `docs/harness_guide.md`
- `docs/harness/common/**/*.md`
- `docs/phase_*/*.md`
- `docs/standard/coding_guidelines_core.md`
- `docs/project_overlay/**/*.md`
- `docs/project_overlay/harness_doc_guard_workflow_template.yml`
- `docs/templates/task/**/*.md`
- `docs/quickstart.md`
- `docs/downstream_harness_flow.md`
- `docs/how_harness_kit_works.md`
- `docs/version_support.md`
- `bootstrap/**/*`
- `scripts/bootstrap_init.py`
- `scripts/check_first_success_docs.py`
- `scripts/validate_overlay_decisions.py`
- `scripts/validate_overlay_consistency.py`
- `scripts/validate_phase_gate.py`
- `scripts/adopt_common.py`
- `scripts/adopt_dry_run.py`
- `scripts/adopt_safe_write.py`

repo 루트 `README.md`는 저장소 진입 문서로서 maintainer 안내도 함께 담고 있으므로, 현재 기준에서는 downstream bundle에 그대로 포함하지 않는다.

### 2) Downstream 선택 자산

핵심 실행에는 필수는 아니지만, 온보딩·예시·검증 이해를 돕는 자산이다.

- `docs/examples/**/*.md`

기본 배포에서는 포함하는 편을 우선으로 본다. 단, 이후 bundle size나 유지 비용 때문에 분리가 필요해지면 이 문서에서 별도 판단 근거를 추가한 뒤 조정한다.

### 3) Maintainer 전용 자산

`harness-kit` core 자체를 유지보수하거나 릴리스할 때만 필요한 자산이다. downstream bundle에는 포함하지 않는다.

- `docs/kit_maintenance/*`
- `harness.log`
- `scripts/check_harness_docs.py`
- `scripts/install_downstream_bundle.py`
- `scripts/generate_downstream_bundle.py`
- `scripts/validate_downstream_bundle.py`
- `.github/workflows/harness-doc-guard.yml`
- `tests/*`
- `.git*`

기타 저장소 메타데이터도 downstream bundle에는 포함하지 않는다.

### 4) Release Metadata / Generated Artifact

배포 시점에 생성되는 산출물이다. source-of-truth 문서 자체가 아니라, 위 분류를 바탕으로 만들어지는 결과물이다.

- `dist/harness-kit-project-bundle/`
- `dist/harness-kit-project-bundle/README.md`
- `dist/harness-kit-project-bundle/bundle_manifest.json`
- 필요 시 위 디렉터리에서 파생한 release zip/tarball

## 현재 저장소 기준 기대 bundle 구조

현재 downstream 배포물은 아래 구조를 기본으로 한다.

```text
README.md
bundle_manifest.json
bootstrap/
docs/
  harness_guide.md
  harness/
  downstream_harness_flow.md
  how_harness_kit_works.md
  phase_*/
  project_overlay/
    harness_doc_guard_workflow_template.yml
  quickstart.md
  standard/coding_guidelines_core.md
  templates/task/
  version_support.md
  examples/
scripts/
  adopt_common.py
  adopt_dry_run.py
  adopt_safe_write.py
  bootstrap_init.py
  check_first_success_docs.py
  validate_phase_gate.py
  validate_overlay_consistency.py
  validate_overlay_decisions.py
```

`docs/project_entrypoint.md`와 `docs/decisions/README.md`는 bundle 안에 직접 들어가는 파일이 아니라, downstream 프로젝트에서 각각 `docs/project_overlay/project_entrypoint_template.md`, `docs/project_overlay/decisions_index_template.md`를 bootstrap 또는 수동 복사해 생성하는 consumer-local 파일이다. 반면 `docs/project_overlay/harness_doc_guard_workflow_template.yml`은 first-success 이후 consumer project가 `.github/workflows/harness-doc-guard.yml`로 복사해 future-session CI guardrail을 고정하는 shipped asset이다.

## Bundle Generation Command

- canonical generation command: `python3 scripts/generate_downstream_bundle.py`
- canonical validation command: `python3 scripts/validate_downstream_bundle.py`
- canonical smoke validation command: `python3 -m unittest tests.test_downstream_bundle_smoke`
- 기본 출력 경로: `dist/harness-kit-project-bundle/`
- canonical artifact format은 directory다.
- `README.md`는 bundle entry artifact로 생성한다.
- `bundle_manifest.json`은 copied source file 목록과 checksum을 기록한다.
- validation은 boundary 문서의 include pattern, 실제 copied file 내용, generated `README.md`, `bundle_manifest.json`이 서로 일치하는지 검사해야 한다.
- validation은 include pattern뿐 아니라 maintainer-only exclusion pattern과 실제 bundle contents의 충돌도 함께 잡아야 한다.
- smoke validation은 canonical `dist/harness-kit-project-bundle/`를 임시 consumer project에 vendored 한 뒤, bundle 안의 project-facing script만 실행해 greenfield/brownfield 기본 경로가 유지되는지 확인해야 한다.
- zip/tarball이 필요하면 이 directory artifact에서 파생 생성한다. source-of-truth는 압축본이 아니라 위 디렉터리 구조와 manifest다.

## 분류 판단 규칙

- downstream 프로젝트가 바로 읽거나 복사하거나 실행해야 하는 자산이면 downstream bundle 후보로 본다.
- `harness-kit` maintainer만 릴리스, 감사, 드리프트 대응, 저장소 자체 검증에 사용하는 자산이면 maintainer 전용으로 본다.
- 같은 자산이 downstream 사용과 maintainer 운영을 동시에 만족해야 한다면, 먼저 downstream 역할을 기준으로 두고 maintainer 전용 절차는 별도 문서에 둔다.
- 경계가 애매한 자산은 "프로젝트 소비자가 이 자산 없이도 bundle을 정상 사용 가능한가"를 먼저 질문한다.

## 후속 이슈와의 연결

- bundle generation은 이 문서의 include path와 maintainer-only exclusion 우선순위를 그대로 사용해야 한다.
- bundle validation은 이 문서의 분류와 기대 구조를 검사 기준으로 사용해야 한다.
- safe write/update, change classification, upgrade guide, diff review는 repo 전체가 아니라 downstream bundle 경계를 기준으로 판단해야 한다.
- consumer-facing change classification policy는 `docs/project_overlay/harness_upgrade_impact_policy.md`처럼 downstream bundle에 포함되는 경로에 두는 편을 우선한다.
