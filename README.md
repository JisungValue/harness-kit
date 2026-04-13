# Harness Kit

여러 프로젝트에서 공통으로 재사용할 수 있는 Harness 기본 패키지다.

## 목적

- 프로젝트마다 Harness 절차와 공통 규칙을 처음부터 다시 작성하지 않도록 한다.
- 공통 Phase, 공통 정책, 공통 산출물 템플릿, 공통 예시를 한 곳에서 관리한다.
- 프로젝트별 문서는 공통 규칙 위에 얇은 overlay만 추가하도록 한다.
- 한 번 생성되는 코드의 품질을 높이고, 이후 변경에서도 유지보수성과 지속 가능성을 계속 유지할 수 있는 프로젝트 코드를 만들도록 돕는다.

## 시작 문서

- 처음 시작: `docs/quickstart.md`
- 전체 동작 설명: `docs/how_harness_kit_works.md`
- 새 프로젝트 first success: `docs/project_overlay/first_success_guide.md`
- 로컬 진단과 dry-run: `docs/project_overlay/local_diagnostics_and_dry_run.md`
- 기존 프로젝트 read-only adopt: `docs/project_overlay/adopt_dry_run.md`
- 기존 프로젝트 upgrade impact 분류: `docs/project_overlay/harness_upgrade_impact_policy.md`

## 디렉터리 구조

- `docs/harness_guide.md` - reusable core guide
  - kit의 공통 진입점이다.
- `docs/harness/common/`
  - process, artifact, audit, testing, validation, code hygiene, design quality, performance, lightweight 정책을 둔다.
- `docs/phase_*`
  - 각 Phase의 구현 기준과 감사 기준을 둔다.
- `docs/standard/coding_guidelines_core.md`
  - 여러 프로젝트에서 공통으로 재사용할 수 있는 코드 품질 규칙을 둔다.
- `docs/templates/task/`
  - 새 task를 시작할 때 복사해서 쓸 기본 산출물 템플릿을 둔다.
- `docs/examples/`
  - 기대 산출물 밀도를 보여 주는 예시 task들을 둔다.
- `bootstrap/`
  - 프로젝트 스캐폴딩 또는 수동 복사에 쓰는 bootstrap 자산을 둔다.
- `scripts/bootstrap_init.py`
  - 새 프로젝트 또는 거의 빈 디렉터리에 최소 project overlay 문서 세트와 runtime instruction entrypoint 파일을 deterministic하게 생성하는 init CLI다. 현재 MVP는 관리 대상 파일 경로만 검사하고 생성한다.
- `scripts/validate_overlay_decisions.py`
  - project overlay 문서의 unresolved placeholder를 `first-success` 또는 `phase2` readiness 기준으로 검사하는 validator다.
- `scripts/validate_overlay_consistency.py`
  - project overlay 문서 간 참조, runtime instruction entrypoint 연결, 책임 경계 불일치를 검사하는 cross-document consistency checker다.
- `scripts/adopt_dry_run.py`
  - 기존 프로젝트의 현재 overlay 상태를 bootstrap baseline과 비교해 missing, unchanged, differing, conflict candidate를 read-only로 분류하는 adopt dry-run이다.
- `scripts/adopt_safe_write.py`
  - 기존 프로젝트에 대해 `adopt_dry_run.py`와 같은 판정 규칙을 사용해 missing file create, unchanged refresh, explicit path force overwrite만 허용하는 제한적 safe write/update 도구다.
- `scripts/generate_downstream_bundle.py`
  - downstream 배포 경계 기준으로 project-facing 자산만 모아 `dist/harness-kit-project-bundle/` directory artifact와 `bundle_manifest.json`을 생성하는 maintainer용 bundle generation command다.
- `scripts/validate_downstream_bundle.py`
  - generated downstream bundle이 boundary 문서, manifest, 실제 copied file 내용과 일치하는지 검사하는 maintainer용 bundle validation command다.
- `docs/project_overlay/`
  - 프로젝트별로 추가 작성해야 하는 문서와 템플릿을 둔다.
- `docs/project_overlay/first_success_guide.md`
  - 새 프로젝트 또는 거의 빈 프로젝트에서 최소 문서 세트와 첫 성공 상태를 빠르게 재현하는 가이드다.
- `docs/project_overlay/local_diagnostics_and_dry_run.md`
  - init, validator, adopt dry-run을 로컬에서 어떤 순서로 실행하고 출력을 어떻게 해석할지 정리한 진단 가이드다.
- `docs/project_overlay/harness_upgrade_impact_policy.md`
  - downstream bundle 변경을 consumer 관점의 impact category로 분류해 adoption timing, manual intervention 필요성, breaking 가능성을 판단하는 정책 문서다.
- `docs/quickstart.md`
  - 0.1.0 사용자 관점에서 greenfield/brownfield 시작 절차를 한 번에 보여 주는 상위 입문 문서다.
- `docs/how_harness_kit_works.md`
  - core, overlay, bootstrap, validation, adopt dry-run이 어떤 역할로 나뉘는지 설명하는 개념 문서다.
- `docs/kit_maintenance/audit_policy.md`
  - harness-kit core 수정 시 maintainer가 따르는 전용 감사 기준이다.
- `docs/kit_maintenance/drift_response_guide.md`
  - Harness Doc Guard CI 실패 시 maintainer 대응 순서를 정의한다.
- `docs/kit_maintenance/release_process.md`
  - maintainer가 release gate 점검, release note 작성, tag, GitHub Release 생성을 어떤 순서로 수행할지 정의한다.
- `docs/kit_maintenance/downstream_bundle_smoke_validation.md`
  - generated bundle을 vendored dependency처럼 써서 greenfield/brownfield 기본 경로가 실제로 동작하는지 점검하는 maintainer용 smoke validation 기준이다.
- `docs/kit_maintenance/downstream_bundle_boundary.md`
  - maintainer가 downstream bundle에 포함할 자산과 제외할 자산의 경계를 정의한다.
- `scripts/check_harness_docs.py`
  - core/overlay 경로 정합성과 `harness.log` 기록 규칙을 자동 검사한다.
- `.github/workflows/harness-doc-guard.yml`
  - 문서 정합성 검사를 PR/merge 전에 자동 실행한다.
- `harness.log`
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
  - 주 문서: `docs/harness_guide.md`, `docs/harness/common/*`, `docs/phase_*`
  - `docs/project_overlay/*`는 downstream 프로젝트 문서를 시작할 때 복사하거나 참조하는 template/guide다.
- harness-kit maintainer용 문서
  - 목적: `harness-kit` core 규칙, template, example, 문서 구조 자체를 수정할 때의 감사와 기록
  - 주 문서: `docs/kit_maintenance/audit_policy.md`, `docs/kit_maintenance/drift_response_guide.md`, `docs/kit_maintenance/release_process.md`, `docs/kit_maintenance/downstream_bundle_smoke_validation.md`, `harness.log`

이 경계와 별도로, downstream에 실제로 배포할 자산은 저장소 전체가 아니라 project-facing 문서/스크립트/예시/bootstrapping 자산 중심의 부분집합으로 본다. downstream bundle 경계의 정본은 `docs/kit_maintenance/downstream_bundle_boundary.md`를 따른다.

개별 서비스 프로젝트의 task 수행자는 maintainer 문서를 기본 운영 규칙으로 사용하지 않는다.
`docs/kit_maintenance/*`는 downstream 프로젝트가 가져가야 하는 최소 프로젝트 문서 세트에 포함되지 않는다.
maintainer 문서는 `harness-kit` core 의미 변경이 있을 때만 적용한다.

- 프로젝트 task를 수행하면 사용 프로젝트용 문서를 따른다.
- `harness-kit` core를 수정하면 maintainer용 문서를 따른다.

## 권장 도입 순서

1. `harness-kit`를 새 프로젝트로 가져온다.
2. 새 프로젝트 first success 경로는 `docs/project_overlay/first_success_guide.md`를 먼저 본다.
3. 로컬 진단 순서와 dry-run 해석은 `docs/project_overlay/local_diagnostics_and_dry_run.md`를 함께 본다.
4. init CLI 또는 `docs/project_overlay/` 수동 복사로 최소 문서 세트를 만든다.
5. 생성된 `docs/project_entrypoint.md`, `docs/decisions/README.md`, `docs/standard/coding_conventions_project.md`를 읽고 현재 프로젝트에서 먼저 확정해야 할 구조/정책/예외 결정이 있는지 확인한다.
6. `vendor/harness-kit/`가 아닌 경로에 kit를 둘 예정이면 bootstrap 시점부터 `--vendor-path <actual-path>`를 사용해 generated vendored reference를 바로 현지화한다. 그 옵션 없이 생성했다면 이후 `docs/project_entrypoint.md`와 `docs/standard/coding_conventions_project.md`의 경로를 실제 배치 경로에 맞게 수동 현지화한다.
7. 아래 예시는 `vendor/harness-kit/`를 기준으로 한다. 다른 경로를 쓰면 실행 명령의 `vendor/harness-kit/` 부분도 같은 실제 경로로 함께 바꿔야 한다.
8. `python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness first-success`로 unresolved decision readiness를 확인한다.
9. `python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .`로 문서 간 교차 정합성과 runtime instruction entrypoint 연결을 확인한다.
10. local validator가 통과하면 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 프로젝트 `.github/workflows/` 아래 workflow 파일로 복사하고 `@<pin-tag-or-sha>`를 실제 릴리스 태그 또는 고정 SHA로 바꿔 future-session guardrail을 고정한다.
11. `vendor/harness-kit/docs/templates/task/`를 프로젝트 작업 경로로 복사해 첫 task를 시작한다.
12. 실제 task 몇 개를 돌린 뒤 project overlay와 decisions index를 함께 보강한다.

기존 프로젝트나 부분 도입 상태를 먼저 읽어야 하면 `docs/project_overlay/adopt_dry_run.md`의 read-only adopt 흐름부터 시작한다.

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

- 이 저장소 source repo를 읽는 중이라면 먼저 `docs/project_overlay/first_success_guide.md`, `docs/quickstart.md`, `docs/how_harness_kit_works.md`를 본다.
- source repo에는 root `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`가 아직 없고, 이 파일들은 downstream 프로젝트를 bootstrap한 뒤에 생긴다.
- 아래 순서는 downstream 프로젝트를 bootstrap한 뒤 생성되는 문서 기준이다.

- runtime 시작점: `AGENTS.md`
- project-local 문서 entrypoint: `docs/project_entrypoint.md`
- project decision index: `docs/decisions/README.md`
- reusable core guide: `vendor/harness-kit/docs/harness_guide.md`
- project-specific supporting docs: `docs/standard/*`

## Kit 유지보수 기록 규칙

- maintainer 감사 기준의 정본은 `docs/kit_maintenance/audit_policy.md`를 따른다.
- maintainer 감사는 `docs/kit_maintenance/audit_policy.md`의 Strict Mode 체크포인트를 기준으로 수행한다.
- maintainer가 GitHub issue를 해결하기 위해 `harness-kit` core를 수정할 때는 issue마다 전용 브랜치를 따로 잡아 진행하고, 이름은 `{issue_num}_{title}` 형식을 사용한다.
- `harness-kit` core에 의미 있는 변경이 있으면 같은 변경에서 루트 `harness.log`를 반드시 함께 갱신한다.
- `harness.log` 항목마다 `변경`과 `이유`를 모두 적는다. 둘 중 하나라도 빠지면 기록으로 인정하지 않는다.
- core 의미 변경 항목은 `변경`, `이유`, `audit`, `audit-summary`를 같은 항목에 함께 남긴다.
- 기록 대상은 공통 규칙, phase 기준, audit 기준, 템플릿, 예시, core 문서 구조처럼 여러 프로젝트에 영향을 줄 수 있는 변경이다.
- 단순 오탈자, 링크 수정, 비의미적 포맷 정리만 예외로 둘 수 있다. 애매하면 기록한다.
- 변경 후에는 구현 주체와 분리된 subagent audit를 반드시 수행한다.
- audit는 `changed-parts`와 `whole-harness`를 모두 수행한다. 전자는 바뀐 부분과 인접 영향을 보고, 후자는 전체 흐름과 core 일관성을 본다.
- `audit-summary` 필수 규칙은 2026-04-03 이후 신규 항목부터 적용한다.
- changed-parts / whole-harness audit에는 이번 변경이 필수 재참조 문서 수, 중복 규칙, 문서 길이를 불필요하게 늘려 하네스 수행 중 오동작이나 누락 위험을 키우지 않는지도 포함한다.
- maintainer agent는 변경과 audit 요약을 같은 작업에서 `harness.log`에 기록한다.

## 운영 원칙

- 공통 Core는 가능한 한 안정적으로 유지한다.
- 프로젝트별 차이는 overlay에 두고 core를 쉽게 포크하지 않는다.
- 새 규칙이 여러 프로젝트에서 반복되면 core로 승격한다.
- 특정 프로젝트에만 필요한 규칙은 overlay에 남긴다.
