# Harness Kit

여러 프로젝트에서 공통으로 재사용할 수 있는 Harness 기본 패키지다.

## 목적

- 프로젝트마다 Harness 절차와 공통 규칙을 처음부터 다시 작성하지 않도록 한다.
- 공통 Phase, 공통 정책, 공통 산출물 템플릿, 공통 예시를 한 곳에서 관리한다.
- 프로젝트별 문서는 공통 규칙 위에 얇은 overlay만 추가하도록 한다.
- 한 번 생성되는 코드의 품질을 높이고, 이후 변경에서도 유지보수성과 지속 가능성을 계속 유지할 수 있는 프로젝트 코드를 만들도록 돕는다.

## 이 README가 설명하는 대상

- 이 README는 먼저 `harness-kit`가 어떤 패키지인지, 어떤 자산을 담고 있는지, 어디서 시작해야 하는지 설명한다.
- downstream 프로젝트에서 bootstrap 또는 brownfield adoption으로 하네스를 도입하는 흐름과, 도입 후 task가 어떤 Phase로 진행되는지는 [`docs/downstream_harness_flow.md`](docs/downstream_harness_flow.md)에서 따로 정리한다.
- 즉, 상단은 kit 자체 설명, 뒤쪽은 downstream 사용 흐름 설명으로 읽으면 된다.

## 핵심 용어

- `source repo`
  - 지금 보고 있는 `harness-kit` 저장소 자체다.
- `downstream project`
  - `harness-kit`를 vendoring하거나 bootstrap한 실제 사용 프로젝트다.
- `vendored core`
  - downstream 프로젝트 안에 들어온 `vendor/harness-kit/docs/harness_guide.md` 같은 공통 규칙 문서다.
- `runtime launcher entrypoint`
  - agent runtime이 맨 먼저 여는 `AGENTS.md`다.
- `documentation/policy entrypoint`
  - runtime launcher가 진입한 뒤 실제 문서 규칙을 묶어 주는 `docs/project_entrypoint.md`다.

기본 예시는 `source repo`를 downstream 프로젝트 안의 `vendor/harness-kit/`로 vendoring하는 경로를 기준으로 설명한다.

## Source Repo 와 Downstream 관계

| source repo file | downstream generated or vendored file | runtime role |
| --- | --- | --- |
| [`docs/project_overlay/agent_entrypoint_template.md`](docs/project_overlay/agent_entrypoint_template.md) | `AGENTS.md` | runtime launcher entrypoint |
| [`docs/project_overlay/project_entrypoint_template.md`](docs/project_overlay/project_entrypoint_template.md) | `docs/project_entrypoint.md` | documentation/policy entrypoint |
| [`docs/project_overlay/decisions_index_template.md`](docs/project_overlay/decisions_index_template.md) | `docs/decisions/README.md` | project decision index |
| [`docs/harness_guide.md`](docs/harness_guide.md) | `vendor/harness-kit/docs/harness_guide.md` | vendored core guide |
| [`docs/project_overlay/architecture_template.md`](docs/project_overlay/architecture_template.md) | `docs/standard/architecture.md` | project-local supporting doc |

- source repo의 template/guide는 downstream에서 그대로 쓰이거나, bootstrap 결과물로 생성되거나, vendored copy로 들어간다.
- downstream 사용자는 source repo의 template를 직접 실행하는 것이 아니라, downstream 프로젝트 안에 생긴 `AGENTS.md`, `docs/project_entrypoint.md`, `docs/standard/*`, `docs/decisions/README.md`, `vendor/harness-kit/docs/harness_guide.md`를 따라간다.

## 시작 문서

- Start here: [`docs/quickstart.md`](docs/quickstart.md)
- 이 저장소의 `README.md`는 source repo 안내 문서다. 실제 bootstrap, adopt, validate 명령은 `harness-kit` source repo가 아니라 downstream 프로젝트 루트에서 실행한다.

### Source Repo Shortcut

- source repo에서 downstream 프로젝트로 첫 설치를 바로 시작하려면 `scripts/install_downstream_bundle.py`를 쓸 수 있다.
- 이 helper는 canonical bundle 재생성, target 프로젝트 vendoring, vendored `bootstrap_init.py` 실행을 한 번에 묶는다.
- 기본 vendored 경로는 `vendor/harness-kit`이고, 다른 경로를 쓰려면 `--vendor-path third_party/harness-kit`처럼 project-root relative path를 준다.
- vendored path는 downstream `docs/` 트리 밖에 두는 것을 전제로 하며, 이미 vendored bundle이 있으면 `--force-vendor`, bootstrap 결과물이 이미 있으면 `--force-bootstrap`을 사용한다.

```bash
python3 scripts/install_downstream_bundle.py /path/to/downstream-project --language java
python3 scripts/install_downstream_bundle.py /path/to/downstream-project --language java --vendor-path third_party/harness-kit
```

### 새 프로젝트 시작

- 현재 지원 범위: [`docs/version_support.md`](docs/version_support.md)
- canonical 시작 문서: [`docs/quickstart.md`](docs/quickstart.md)
- greenfield 상세 reference: [`docs/project_overlay/first_success_guide.md`](docs/project_overlay/first_success_guide.md)
- diagnostics reference: [`docs/project_overlay/local_diagnostics_and_dry_run.md`](docs/project_overlay/local_diagnostics_and_dry_run.md)

### 기존 프로젝트에 도입

- 아직 `docs/project_entrypoint.md`나 vendored harness 기준 문서가 없거나, legacy `docs/harness_guide.md` 상태라면 이 경로부터 시작한다.
- read-only 현재 상태 파악: [`docs/project_overlay/adopt_dry_run.md`](docs/project_overlay/adopt_dry_run.md)
- diagnostics reference: [`docs/project_overlay/local_diagnostics_and_dry_run.md`](docs/project_overlay/local_diagnostics_and_dry_run.md)

### 이미 도입된 프로젝트 업그레이드

- 이미 `docs/project_entrypoint.md`와 vendored harness가 있고, 새 bundle 버전만 반영하려면 이 경로부터 시작한다.
- upgrade 전체 흐름: [`docs/project_overlay/downstream_harness_upgrade_guide.md`](docs/project_overlay/downstream_harness_upgrade_guide.md)
- diff review checklist: [`docs/project_overlay/downstream_overlay_diff_review_checklist.md`](docs/project_overlay/downstream_overlay_diff_review_checklist.md)
- impact 분류: [`docs/project_overlay/harness_upgrade_impact_policy.md`](docs/project_overlay/harness_upgrade_impact_policy.md)

### 개념 이해

- 현재 버전/지원 범위: [`docs/version_support.md`](docs/version_support.md)
- 전체 개념 설명: [`docs/how_harness_kit_works.md`](docs/how_harness_kit_works.md)
- downstream 도입/운영 흐름: [`docs/downstream_harness_flow.md`](docs/downstream_harness_flow.md)

## 디렉터리 구조

- [`docs/harness_guide.md`](docs/harness_guide.md) - reusable core guide
  - kit의 공통 진입점이다.
- `docs/harness/common/`
  - process, artifact, audit, testing, validation, code hygiene, design quality, performance, lightweight 정책을 둔다.
- `docs/phase_*`
  - 각 Phase의 구현 기준과 감사 기준을 둔다.
- [`docs/standard/coding_guidelines_core.md`](docs/standard/coding_guidelines_core.md)
  - 여러 프로젝트에서 공통으로 재사용할 수 있는 코드 품질 규칙을 둔다.
- `docs/templates/task/`
  - 새 task를 시작할 때 복사해서 쓸 기본 산출물 템플릿을 둔다.
- `docs/examples/`
  - 기본 시작 경로가 아니라 필요할 때 보는 advanced/reference 예시 task들을 둔다.
- `bootstrap/`
  - 프로젝트 스캐폴딩 또는 수동 복사에 쓰는 bootstrap 자산을 둔다.
- [`scripts/bootstrap_init.py`](scripts/bootstrap_init.py)
  - 새 프로젝트 또는 거의 빈 디렉터리에 최소 project overlay 문서 세트와 runtime instruction entrypoint 파일을 deterministic하게 생성하는 init CLI다. 현재 MVP는 관리 대상 파일 경로만 검사하고 생성한다.
- [`scripts/validate_overlay_decisions.py`](scripts/validate_overlay_decisions.py)
  - project overlay 문서의 unresolved placeholder를 `first-success` 또는 `phase2` readiness 기준으로 검사하는 validator다.
- [`scripts/validate_overlay_consistency.py`](scripts/validate_overlay_consistency.py)
  - project overlay 문서 간 참조, runtime instruction entrypoint 연결, 책임 경계 불일치를 검사하는 cross-document consistency checker다. `--mode incremental`은 brownfield partial adoption의 safe gap과 blocker를 구분하는 intermediate mode다.
- [`scripts/adopt_dry_run.py`](scripts/adopt_dry_run.py)
  - 기존 프로젝트의 현재 overlay 상태를 bootstrap baseline과 비교해 missing, unchanged, differing, conflict candidate를 read-only로 분류하는 adopt dry-run이다.
- [`scripts/adopt_safe_write.py`](scripts/adopt_safe_write.py)
  - 기존 프로젝트에 대해 `adopt_dry_run.py`와 같은 판정 규칙을 사용해 missing file create, unchanged refresh, explicit path force overwrite만 허용하는 제한적 safe write/update 도구다.
- [`scripts/generate_downstream_bundle.py`](scripts/generate_downstream_bundle.py)
  - downstream 배포 경계 기준으로 project-facing 자산만 모아 `dist/harness-kit-project-bundle/` directory artifact와 `bundle_manifest.json`을 생성하는 maintainer용 bundle generation command다.
- [`scripts/validate_downstream_bundle.py`](scripts/validate_downstream_bundle.py)
  - generated downstream bundle이 boundary 문서, manifest, 실제 copied file 내용과 일치하는지 검사하는 maintainer용 bundle validation command다.
- `docs/project_overlay/`
  - 프로젝트별로 추가 작성해야 하는 문서와 템플릿을 둔다.
- [`docs/project_overlay/first_success_guide.md`](docs/project_overlay/first_success_guide.md)
  - 새 프로젝트 또는 거의 빈 프로젝트에서 최소 문서 세트와 첫 성공 상태를 빠르게 재현하는 가이드다.
- [`docs/project_overlay/local_diagnostics_and_dry_run.md`](docs/project_overlay/local_diagnostics_and_dry_run.md)
  - init, validator, adopt dry-run을 로컬에서 어떤 순서로 실행하고 출력을 어떻게 해석할지 정리한 진단 가이드다.
- [`docs/project_overlay/harness_upgrade_impact_policy.md`](docs/project_overlay/harness_upgrade_impact_policy.md)
  - downstream bundle 변경을 consumer 관점의 impact category로 분류해 adoption timing, manual intervention 필요성, breaking 가능성을 판단하는 정책 문서다.
- [`docs/project_overlay/downstream_harness_upgrade_guide.md`](docs/project_overlay/downstream_harness_upgrade_guide.md)
  - downstream 프로젝트가 새 bundle 변경을 어떤 순서와 기준으로 검토하고 반영할지 설명하는 consumer-facing upgrade guide다.
- [`docs/project_overlay/downstream_overlay_diff_review_checklist.md`](docs/project_overlay/downstream_overlay_diff_review_checklist.md)
  - downstream 프로젝트가 bundle upgrade diff를 사람 기준으로 검토할 때 확인할 항목을 정리한 checklist다.
- [`docs/quickstart.md`](docs/quickstart.md)
  - 현재 지원 범위 기준으로 greenfield/brownfield 시작 절차를 한 번에 보여 주는 상위 입문 문서다.
- [`docs/version_support.md`](docs/version_support.md)
  - 현재 최신 릴리스와 지원 범위를 한 곳에서 관리하는 canonical 문서다.
- [`docs/how_harness_kit_works.md`](docs/how_harness_kit_works.md)
  - core, overlay, bootstrap, validation, adopt dry-run이 어떤 역할로 나뉘는지 설명하는 개념 문서다.
- [`maintainer/docs/audit_policy.md`](maintainer/docs/audit_policy.md)
  - harness-kit core 수정 시 maintainer가 따르는 전용 감사 기준이다.
- [`maintainer/docs/drift_response_guide.md`](maintainer/docs/drift_response_guide.md)
  - Harness Doc Guard CI 실패 시 maintainer 대응 순서를 정의한다.
- [`maintainer/docs/release_process.md`](maintainer/docs/release_process.md)
  - maintainer가 release gate 점검, release note 작성, tag, GitHub Release 생성을 어떤 순서로 수행할지 정의한다.
- [`maintainer/docs/downstream_bundle_smoke_validation.md`](maintainer/docs/downstream_bundle_smoke_validation.md)
  - generated bundle을 vendored dependency처럼 써서 greenfield/brownfield 기본 경로가 실제로 동작하는지 점검하는 maintainer용 smoke validation 기준이다.
- [`maintainer/docs/downstream_bundle_boundary.md`](maintainer/docs/downstream_bundle_boundary.md)
  - maintainer가 downstream bundle에 포함할 자산과 제외할 자산의 경계를 정의한다.
- [`scripts/check_harness_docs.py`](scripts/check_harness_docs.py)
  - core/overlay 경로 정합성과 `harness.log` 기록 규칙을 자동 검사한다.
- [`.github/workflows/harness-doc-guard.yml`](.github/workflows/harness-doc-guard.yml)
  - 문서 정합성 검사를 PR/merge 전에 자동 실행한다.
- [`harness.log`](harness.log)
  - harness-kit core의 의미 있는 변경과 감사 결과를 남긴다.

## 무엇이 Core 인가

다음 항목은 공통 Core로 관리한다.

- Phase 운영 순서와 감사 반복 규칙
- task workspace 구조와 산출물 최소 템플릿
- 감사 입력물 기준과 결과 형식
- 검증 기록 형식
- 경량 태스크 예외 운영 원칙
- 코드 품질, 리팩터링 범위 제한, 설계 품질, 성능 검토, 에러 처리, 로깅, 경계 번역, 리뷰 체크리스트

## 무엇이 Project Overlay 인가

다음 항목은 프로젝트마다 별도로 유지한다.

- 프로젝트 아키텍처 문서
- 프레임워크 또는 런타임 특화 규칙
- 인프라 또는 클라우드 특화 규칙
- DTO postfix, 네이밍 세부 규칙처럼 프로젝트 결정이 필요한 규칙
- 테스트 전략, 실제 coverage 기준, 통합 테스트 범위, 로컬 개발 규칙
- formatter, linter, type checker, test 같은 품질 게이트 실행 명령과 실패 기준

## 문서 적용 경계

이 저장소의 문서는 다음 두 범위로 나뉜다.

- 사용 프로젝트용 문서
  - 목적: `harness-kit`를 가져다 쓰는 프로젝트의 task 수행, phase 진행, project overlay 작성
  - 주 문서: [`docs/harness_guide.md`](docs/harness_guide.md), `docs/harness/common/*`, `docs/phase_*`
  - `docs/project_overlay/*`는 downstream 프로젝트 문서를 시작할 때 복사하거나 참조하는 template/guide다.
- harness-kit maintainer용 문서
  - 목적: `harness-kit` core 규칙, template, example, 문서 구조 자체를 수정할 때의 감사와 기록
  - 주 문서: [`maintainer/docs/audit_policy.md`](maintainer/docs/audit_policy.md), [`maintainer/docs/drift_response_guide.md`](maintainer/docs/drift_response_guide.md), [`maintainer/docs/release_process.md`](maintainer/docs/release_process.md), [`maintainer/docs/downstream_bundle_smoke_validation.md`](maintainer/docs/downstream_bundle_smoke_validation.md), [`harness.log`](harness.log)

이 경계와 별도로, downstream에 실제로 배포할 자산은 저장소 전체가 아니라 project-facing 문서/스크립트/예시/bootstrapping 자산 중심의 부분집합으로 본다. downstream bundle 경계의 정본은 [`maintainer/docs/downstream_bundle_boundary.md`](maintainer/docs/downstream_bundle_boundary.md)를 따른다.

개별 서비스 프로젝트의 task 수행자는 maintainer 문서를 기본 운영 규칙으로 사용하지 않는다.
`maintainer/docs/*`는 downstream 프로젝트가 가져가야 하는 최소 프로젝트 문서 세트에 포함되지 않는다.
maintainer 문서는 `harness-kit` core 의미 변경이 있을 때만 적용한다.

- 프로젝트 task를 수행하면 사용 프로젝트용 문서를 따른다.
- `harness-kit` core를 수정하면 maintainer용 문서를 따른다.

## 권장 도입 순서

1. 먼저 [`docs/quickstart.md`](docs/quickstart.md)부터 읽는다.
2. `harness-kit`를 새 프로젝트로 가져온다.
3. 새 프로젝트면 `quickstart`의 greenfield 경로를, 기존 프로젝트 첫 도입이면 brownfield 경로를, 이미 도입된 프로젝트 업그레이드면 upgrade 경로를 먼저 따른다.
4. 상세 설명이 더 필요할 때만 greenfield는 [`docs/project_overlay/first_success_guide.md`](docs/project_overlay/first_success_guide.md)를, 기존 프로젝트 진단은 [`docs/project_overlay/local_diagnostics_and_dry_run.md`](docs/project_overlay/local_diagnostics_and_dry_run.md)를 reference로 본다.
5. init CLI 또는 `docs/project_overlay/` 수동 복사로 최소 문서 세트를 만든다.
6. 생성된 `docs/project_entrypoint.md`, `docs/decisions/README.md`, `docs/standard/coding_conventions_project.md`를 읽고 현재 프로젝트에서 먼저 확정해야 할 구조/정책/예외 결정이 있는지 확인한다.
7. `vendor/harness-kit/`가 아닌 경로에 kit를 둘 예정이면 bootstrap 시점부터 `--vendor-path <actual-path>`를 사용해 generated vendored reference를 바로 현지화한다. 그 옵션 없이 생성했다면 이후 `docs/project_entrypoint.md`와 `docs/standard/coding_conventions_project.md`의 경로를 실제 배치 경로에 맞게 수동 현지화한다.
8. 아래 예시는 `vendor/harness-kit/`를 기준으로 한다. 다른 경로를 쓰면 실행 명령의 `vendor/harness-kit/` 부분도 같은 실제 경로로 함께 바꿔야 한다.
9. `python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness first-success`로 unresolved decision readiness를 확인한다.
10. `python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .`로 문서 간 교차 정합성과 runtime instruction entrypoint 연결을 확인한다.
11. local validator가 통과하면 [`docs/project_overlay/harness_doc_guard_workflow_template.yml`](docs/project_overlay/harness_doc_guard_workflow_template.yml)을 프로젝트 `.github/workflows/` 아래 workflow 파일로 복사하고 `@<pin-tag-or-sha>`를 실제 릴리스 태그 또는 고정 SHA로 바꿔 future-session guardrail을 고정한다.
12. 첫 task를 시작하기 전에 [`docs/downstream_harness_flow.md`](docs/downstream_harness_flow.md)를 한 번 읽고 Phase 1~5, approval gate, 재수행 규칙을 먼저 이해한다.
13. `vendor/harness-kit/docs/templates/task/`를 프로젝트 작업 경로로 복사해 첫 task를 시작한다.
14. 실제 task 몇 개를 돌린 뒤 project overlay와 decisions index를 함께 보강한다.

기존 프로젝트나 부분 도입 상태를 먼저 읽어야 하면 [`docs/project_overlay/adopt_dry_run.md`](docs/project_overlay/adopt_dry_run.md)의 read-only adopt 흐름부터 시작한다.

## 최소 프로젝트 문서 세트

- `docs/project_entrypoint.md`
- `docs/decisions/README.md`
- `docs/standard/architecture.md`
- `docs/standard/implementation_order.md`
- `docs/standard/coding_conventions_project.md`
- `docs/standard/quality_gate_profile.md`
- `docs/standard/testing_profile.md`
- `docs/standard/commit_rule.md`

## Runtime Instruction Entrypoint 세트

- `AGENTS.md` - canonical runtime entrypoint
- `CLAUDE.md` - Claude adapter entrypoint
- `GEMINI.md` - Gemini adapter entrypoint

## 권장 읽기 순서

- 이 저장소 source repo를 읽는 중이라면 먼저 [`docs/quickstart.md`](docs/quickstart.md)를 본다.
- 그다음 greenfield면 [`docs/project_overlay/first_success_guide.md`](docs/project_overlay/first_success_guide.md), brownfield first adoption이면 [`docs/project_overlay/adopt_dry_run.md`](docs/project_overlay/adopt_dry_run.md), 이미 도입된 downstream upgrade면 [`docs/project_overlay/downstream_harness_upgrade_guide.md`](docs/project_overlay/downstream_harness_upgrade_guide.md)를 본다.
- 적용이 끝나면 첫 task 전에 [`docs/downstream_harness_flow.md`](docs/downstream_harness_flow.md)를 읽어 Phase 운영 규칙으로 넘어간다.
- source repo에는 root `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`가 아직 없고, 이 파일들은 downstream 프로젝트를 bootstrap한 뒤에 생긴다.
- 아래 순서는 downstream 프로젝트를 bootstrap한 뒤 생성되는 문서 기준이다.

- runtime launcher entrypoint: `AGENTS.md`
- documentation/policy entrypoint: `docs/project_entrypoint.md`
- project decision index: `docs/decisions/README.md`
- reusable core guide: `vendor/harness-kit/docs/harness_guide.md`
- project-specific supporting docs: `docs/standard/*`

## Kit 유지보수 기록 규칙

- maintainer 감사 기준의 정본은 [`maintainer/docs/audit_policy.md`](maintainer/docs/audit_policy.md)를 따른다.
- maintainer 감사는 [`maintainer/docs/audit_policy.md`](maintainer/docs/audit_policy.md)의 Strict Mode 체크포인트를 기준으로 수행한다.
- maintainer가 GitHub issue를 해결하기 위해 `harness-kit` core를 수정할 때는 issue마다 전용 브랜치를 따로 잡아 진행하고, 이름은 `{issue_num}_{title}` 형식을 사용한다.
- `harness-kit` core에 의미 있는 변경이 있으면 같은 변경에서 루트 [`harness.log`](harness.log)를 반드시 함께 갱신한다.
- [`harness.log`](harness.log) 항목마다 `변경`과 `이유`를 모두 적는다. 둘 중 하나라도 빠지면 기록으로 인정하지 않는다.
- core 의미 변경 항목은 `변경`, `이유`, `audit`, `audit-summary`를 같은 항목에 함께 남긴다.
- 기록 대상은 공통 규칙, phase 기준, audit 기준, 템플릿, 예시, core 문서 구조처럼 여러 프로젝트에 영향을 줄 수 있는 변경이다.
- 단순 오탈자, 링크 수정, 비의미적 포맷 정리만 예외로 둘 수 있다. 애매하면 기록한다.
- 변경 후에는 구현 주체와 분리된 subagent audit를 반드시 수행한다.
- audit는 `changed-parts`와 `whole-harness`를 모두 수행한다. 전자는 바뀐 부분과 인접 영향을 보고, 후자는 전체 흐름과 core 일관성을 본다.
- `audit-summary` 필수 규칙은 2026-04-03 이후 신규 항목부터 적용한다.
- changed-parts / whole-harness audit에는 이번 변경이 필수 재참조 문서 수, 중복 규칙, 문서 길이를 불필요하게 늘려 하네스 수행 중 오동작이나 누락 위험을 키우지 않는지도 포함한다.
- maintainer agent는 변경과 audit 요약을 같은 작업에서 `harness.log`에 기록한다.

## 운영 원칙

- 작업 기준은 현재 repo 안의 `README`, `docs/*`, `docs/decisions/*`, `scripts/*`, `config` 같은 repo-local 근거를 source-of-truth로 우선한다.
- 기억, 외부 대화, 다른 프로젝트 관행, 다른 저장소의 비슷한 규칙은 참고할 수 있어도 현재 repo 근거보다 우선하지 않는다.
- 필요한 결정이나 근거가 repo 안에 없으면 추측으로 메우지 않는다.
- repo에 없는 결정은 project overlay, `docs/decisions/`, `implementation_notes.md`, `validation_report.md` 같은 task workspace 기록으로 넘기고 필요하면 사용자 승인 대상으로 올린다.
- 공통 Core는 가능한 한 안정적으로 유지한다.
- 프로젝트별 차이는 overlay에 두고 core를 쉽게 포크하지 않는다.
- 새 규칙이 여러 프로젝트에서 반복되면 core로 승격한다.
- 특정 프로젝트에만 필요한 규칙은 overlay에 남긴다.
