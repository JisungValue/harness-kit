# Downstream Bundle Boundary

이 문서는 `harness-kit` 저장소 안의 자산 중 무엇이 downstream 배포 대상이고, 무엇이 maintainer 전용 자산인지 구분하는 기준을 정의한다.

Epic #153의 no-vendor greenfield final install 결과와 asset taxonomy는 [`maintainer/docs/downstream_final_layout_contract.md`](downstream_final_layout_contract.md)를 따른다. 이 문서의 현재 bundle 구조 섹션은 source repo에서 만든 delivery artifact 기준이며, final installed runtime layout 자체는 별도 계약 문서가 정본이다.

Epic #166의 final runtime docs surface 경량화도 같은 구분을 따른다. generated delivery bundle은 reference-only 자산을 포함할 수 있지만, final install은 `maintainer/docs/downstream_final_layout_contract.md`의 runtime minimum과 examples taxonomy만 target project에 남겨야 한다.

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

- `downstream/docs/harness_guide.md`
- `downstream/docs/harness/common/**/*.md`
- `downstream/docs/phase_*/*.md`
- `downstream/docs/harness/common/coding_guidelines_policy.md`
- `bootstrap/docs/project_overlay/**/*.md`
- `bootstrap/docs/project_overlay/harness_doc_guard_workflow_template.yml`
- `downstream/docs/templates/task/**/*.md`
- `bootstrap/docs/quickstart.md`
- `bootstrap/docs/how_harness_kit_works.md`
- `bootstrap/docs/version_support.md`
- `bootstrap/**/*`
- `bootstrap/scripts/bootstrap_init.py`
- `bootstrap/scripts/check_first_success_docs.py`
- `bootstrap/scripts/validate_overlay_decisions.py`
- `bootstrap/scripts/validate_overlay_consistency.py`
- `downstream/scripts/validate_phase_gate.py`
- `bootstrap/scripts/adopt_common.py`
- `bootstrap/scripts/adopt_dry_run.py`
- `bootstrap/scripts/adopt_safe_write.py`

repo 루트 `README.md`는 저장소 진입 문서로서 maintainer 안내도 함께 담고 있으므로, 현재 기준에서는 downstream bundle에 그대로 포함하지 않는다.

### 2) Downstream 선택 자산

핵심 실행에는 필수는 아니지만, 온보딩·예시·검증 이해를 돕는 자산이다.

- `downstream/docs/examples/**/*.md`

기본 배포에서는 포함하는 편을 우선으로 본다. 단, 이후 bundle size나 유지 비용 때문에 분리가 필요해지면 이 문서에서 별도 판단 근거를 추가한 뒤 조정한다.

### 3) Maintainer 전용 자산

`harness-kit` core 자체를 유지보수하거나 릴리스할 때만 필요한 자산이다. downstream bundle에는 포함하지 않는다.

- `maintainer/docs/*`
- `harness.log`
- `maintainer/scripts/check_harness_docs.py`
- `maintainer/scripts/install_downstream_bundle.py`
- `maintainer/scripts/generate_downstream_bundle.py`
- `maintainer/scripts/validate_downstream_bundle.py`
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

source repo canonical path는 `downstream/docs/*`, `downstream/scripts/*`, `bootstrap/docs/*`, `bootstrap/docs/project_overlay/*`, `bootstrap/scripts/*`이지만, generated bundle에서는 runtime/process docs는 `docs/process/*` 아래로, overlay 자산은 `docs/project_overlay/*` 아래로, runtime validator와 bootstrap/adoption 스크립트는 `scripts/*` 아래로 materialize 한다.

```text
README.md
bundle_manifest.json
bootstrap/
docs/
  process/
    harness_guide.md
    common/
      coding_guidelines_policy.md
    phases/
      phase_*/
    templates/task/
    examples/
  how_harness_kit_works.md
  project_overlay/
    *.md
    harness_doc_guard_workflow_template.yml
  quickstart.md
  version_support.md
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

`docs/entrypoint.md`와 `docs/project/decisions/README.md`는 bundle 안에 직접 들어가는 파일이 아니라, downstream 프로젝트에서 각각 `docs/project_overlay/project_entrypoint_template.md`, `docs/project_overlay/decisions_index_template.md`를 bootstrap 또는 수동 복사해 생성하는 consumer-local 파일이다. 반면 source repo 기준 `bootstrap/docs/project_overlay/*` guide/template/workflow는 generated bundle 안에서 `docs/project_overlay/*`로 materialize 되고, `docs/project_overlay/harness_doc_guard_workflow_template.yml`은 first-success 이후 consumer project가 `.github/workflows/harness-doc-guard.yml`로 복사해 future-session CI guardrail을 고정하는 shipped asset이다.

## Final Install 과 Delivery Bundle 의 차이

이 문서의 include 목록은 generated delivery bundle을 만든다. final install helper는 이 bundle을 입력으로 사용할 수 있지만, target project에 남기는 파일은 더 좁다.

- coding guideline policy는 source repo `downstream/docs/harness/common/coding_guidelines_policy.md`, generated/final `docs/process/common/coding_guidelines_policy.md`가 canonical path다.
- final install은 `docs/process/standard/`와 `coding_guidelines_core.md`를 남기지 않는다.
- final install examples는 `maintainer/docs/downstream_final_layout_contract.md`의 Final Runtime Minimum Examples만 기본으로 남긴다.
- generated delivery bundle에 reference-only examples가 남더라도, final install smoke는 그 파일들이 target project runtime tree에 남지 않는지 별도로 검증해야 한다.
- `bootstrap-first-success/*` validation reports는 maintainer smoke/reference 성격이며 final runtime dependency가 아니다.
- brownfield/upgrade 자동 migration은 이 boundary 문서와 Epic #166의 기본 범위가 아니다.

## Bundle Generation Command

- canonical generation command: `python3 maintainer/scripts/generate_downstream_bundle.py`
- canonical validation command: `python3 maintainer/scripts/validate_downstream_bundle.py`
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
- consumer-facing change classification policy는 source repo 기준 `bootstrap/docs/project_overlay/harness_upgrade_impact_policy.md`에 두고, generated bundle에서는 `docs/project_overlay/harness_upgrade_impact_policy.md`로 materialize 하는 편을 우선한다.
- Epic #153의 runtime-only final install 작업은 delivery bundle 경계와 final installed runtime surface를 구분해야 한다. final installed path, install-time only lifecycle, root `scripts/*` command surface는 `maintainer/docs/downstream_final_layout_contract.md`를 먼저 확인한다.
