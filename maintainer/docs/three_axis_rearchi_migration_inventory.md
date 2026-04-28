# 3-Axis Migration Inventory

## 목적

- `#125` 하위 이슈들이 같은 이동 기준과 비범위 정책을 공유하도록 1차 migration inventory를 고정한다.
- 이 문서는 실제 파일 이동을 수행하지 않고, 현재 저장소 기준 source path와 목표 canonical path를 정리하는 기준 문서다.

## 확정 정책

### 1차 범위

- downstream 적용 복잡도를 낮추는 데 직접 도움이 되는 문서, 스크립트, bundle 경계 자산을 우선 정리한다.
- 실제 consumer가 읽거나 복사하거나 실행하는 자산은 `downstream/` 또는 `bootstrap/` 아래로 분리한다.
- source repo maintainer만 사용하는 문서와 스크립트는 `maintainer/` 아래로 분리한다.

### 축 의미 경계

- `downstream/`은 downstream 프로젝트에 vendoring되거나 도입 이후 계속 참조되는 장기 운영 자산을 둔다.
- `bootstrap/`은 downstream 프로젝트를 처음 세팅하거나 adoption/readiness 상태를 맞출 때 읽는 가이드, 생성 템플릿, 초기화/검사 스크립트를 둔다.
- 따라서 `docs/project_overlay/*`는 현재 문서 의미를 유지한 채 `bootstrap` 축으로 옮긴다.
  - 이 경로는 `bootstrap/language_conventions/*`처럼 선택적 보조 자산이라는 뜻이 아니라, bootstrap/adoption 시점에 project-local 문서를 생성하는 source-of-truth라는 뜻이다.
  - 즉 `docs/project_overlay/*`의 기존 역할인 "프로젝트 문서 골격과 생성 템플릿"은 유지하고, 3축 구조 안에서만 bootstrap canonical path로 재배치한다.
- `README.md`와 bundle boundary가 현재 `docs/...`와 `bootstrap/...` 병행 구조를 설명하는 이유는 아직 실제 이동 전이기 때문이다. 후속 이슈에서는 이 inventory에 맞춰 설명과 경계를 함께 갱신한다.

### 1차 비범위와 루트 유지

- `docs/task/*`는 1차 비범위다.
  - 이유: source repo 작업 산출물 성격이 강하고 downstream 구조 단순화와 직접 연결되지 않는다.
  - 이번 이슈와 후속 하위 이슈의 task 산출물 위치도 계속 `docs/task/*`를 사용한다.
- `harness.log`는 루트 유지다.
  - 이유: 이번 재배치의 핵심은 downstream 구조 단순화이지 maintainer 변경 로그 위치 조정이 아니다.
- `tests/`는 1차에서 물리 이동하지 않는다.
  - 단, 경로 expectation은 자산 이동 단계에서 바로 수정한다.
- 루트 `README.md`는 최종적으로 저장소 지도 문서로 축소하되, 실제 재작성은 후속 이슈에서 수행한다.

### Wrapper 정책

- 스크립트 이동 단계에서는 짧은 transition wrapper를 허용한다.
- wrapper는 새 canonical path로 포워딩하는 임시 수단이며, source-of-truth가 아니다.
- wrapper를 도입한 하위 이슈는 같은 PR 또는 후속 이슈에서 아래 둘 중 하나를 반드시 남긴다.
  - 제거 시점
  - 제거 조건과 추적 이슈

### 테스트 path expectation 정책

- `tests/` 물리 이동 여부와 별개로, 자산을 옮긴 단계에서 관련 테스트의 경로 expectation을 즉시 수정한다.
- `일단 자산만 이동하고 테스트는 나중`은 허용하지 않는다.

### Dist / Manifest 정책

- bundle boundary 또는 canonical path가 바뀌는 단계에서는 아래를 완료 조건에 포함한다.
  - `dist/harness-kit-project-bundle/` 재생성
  - generated `README.md` 검토
  - `bundle_manifest.json` 검토
  - bundle validation 또는 smoke validation 관련 검증

## Epic #125 Working Rules

- `#125`의 모든 child issue는 실제 파일 이동이나 경로 수정 전에 이 문서를 현재 canonical 기준으로 먼저 확인한다.
- child issue는 자신이 건드리는 자산군이 이 문서의 어떤 축과 어떤 target canonical path에 속하는지 먼저 확인한 뒤 작업을 시작한다.
- child issue에서 실제 저장소 상태가 이 문서와 어긋난다는 점을 발견하면, 경로 이동만 먼저 밀어붙이지 말고 같은 작업에서 이 문서를 함께 갱신하거나 drift를 명시적으로 남긴다.
- task 문서, PR 설명, 대화 요약에 이 문서와 다른 별도 migration source-of-truth를 만들지 않는다.
- child issue는 작업 중 아래 항목을 계속 이 문서 기준으로 확인한다.
  - old path 검색 키워드 적용 여부
  - wrapper 사용 여부와 제거 조건 기록 여부
  - 테스트 path expectation 동시 수정 여부
  - `dist/` 및 `bundle_manifest.json` 재검증 필요 여부
- `#125` 범위에서 새 canonical path나 비범위 정책이 바뀌면, 이후 하위 이슈로 넘기기 전에 먼저 이 문서를 갱신한다.

### Child Issue Checklist

- 작업 시작 전에 해당 자산군의 source path와 target canonical path를 이 문서에서 확인한다.
- 실제 파일 이동 직후 문서 링크, CLI 예시, import/path 상수, workflow, 테스트 expectation을 같은 단계에서 수정한다.
- wrapper를 도입했다면 제거 시점 또는 제거 조건과 추적 이슈를 남긴다.
- bundle boundary나 canonical path가 바뀌는 단계라면 `dist/harness-kit-project-bundle/`, generated `README.md`, `bundle_manifest.json`, 관련 validation/smoke를 같이 점검한다.
- 작업 종료 전에 old path 검색 키워드로 잔존 참조를 검색한다.
- 이 문서와 실제 저장소 상태 사이에 새 차이가 생기면 `harness.log`와 task 기록에 남긴다.

## 현재 저장소 기준 분류

### 1. Maintainer axis

| 현재 경로 | 목표 canonical path | 비고 |
| --- | --- | --- |
| `docs/kit_maintenance/audit_policy.md` | `maintainer/docs/audit_policy.md` | maintainer 전용 감사 기준 |
| `docs/kit_maintenance/drift_response_guide.md` | `maintainer/docs/drift_response_guide.md` | doc guard 실패 대응 |
| `docs/kit_maintenance/release_process.md` | `maintainer/docs/release_process.md` | 릴리스 절차 |
| `docs/kit_maintenance/downstream_bundle_boundary.md` | `maintainer/docs/downstream_bundle_boundary.md` | bundle 경계 정본 |
| `maintainer/docs/downstream_final_layout_contract.md` | `maintainer/docs/downstream_final_layout_contract.md` | downstream final install layout 계약 |
| `docs/kit_maintenance/downstream_bundle_smoke_validation.md` | `maintainer/docs/downstream_bundle_smoke_validation.md` | maintainer smoke 기준 |
| `docs/kit_maintenance/three_axis_rearchi_migration_inventory.md` | `maintainer/docs/three_axis_rearchi_migration_inventory.md` | maintainer migration source-of-truth |
| `maintainer/scripts/check_harness_docs.py` | `maintainer/scripts/check_harness_docs.py` | maintainer 전용 문서 검사 |
| `maintainer/scripts/generate_downstream_bundle.py` | `maintainer/scripts/generate_downstream_bundle.py` | bundle 생성 |
| `maintainer/scripts/validate_downstream_bundle.py` | `maintainer/scripts/validate_downstream_bundle.py` | bundle 검증 |
| `maintainer/scripts/install_downstream_bundle.py` | `maintainer/scripts/install_downstream_bundle.py` | source repo helper |

루트 유지:

- `.github/workflows/harness-doc-guard.yml`
- `README.md`
- `harness.log`

### 2. Bootstrap axis

#### bootstrap/docs entry docs

| 현재 경로 | 목표 canonical path |
| --- | --- |
| `docs/quickstart.md` | `bootstrap/docs/quickstart.md` |
| `docs/how_harness_kit_works.md` | `bootstrap/docs/how_harness_kit_works.md` |
| `docs/version_support.md` | `bootstrap/docs/version_support.md` |

#### bootstrap/docs/project_overlay guides and templates

`docs/project_overlay/*`는 namespace를 유지한 채 `bootstrap/docs/project_overlay/*`로 이동한다.

근거:

- `bootstrap/README.md`가 설명하는 기존 원칙처럼, 이 자산군은 downstream 프로젝트의 장기 운영 문서 자체가 아니라 project-local 문서를 만들고 adoption/readiness를 맞추는 source template와 guide다.
- 따라서 3축 구조에서는 `bootstrap` 축으로 옮기되, `bootstrap/language_conventions/*`와는 달리 optional supplement가 아니라 bootstrap canonical source로 취급한다.

현재 확인된 파일:

- `bootstrap/docs/project_overlay/README.md`
- `bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md`
- `bootstrap/docs/project_overlay/first_success_guide.md`
- `bootstrap/docs/project_overlay/downstream_overlay_diff_review_checklist.md`
- `bootstrap/docs/project_overlay/downstream_harness_upgrade_guide.md`
- `bootstrap/docs/project_overlay/adopt_dry_run.md`
- `bootstrap/docs/project_overlay/adopt_safe_write.md`
- `bootstrap/docs/project_overlay/cross_document_consistency_checker.md`
- `bootstrap/docs/project_overlay/unresolved_decision_validator.md`
- `bootstrap/docs/project_overlay/overlay_completion_checklist.md`
- `bootstrap/docs/project_overlay/harness_upgrade_impact_policy.md`
- `bootstrap/docs/project_overlay/decision_record_template.md`
- `bootstrap/docs/project_overlay/decisions_index_template.md`
- `bootstrap/docs/project_overlay/project_entrypoint_template.md`
- `bootstrap/docs/project_overlay/claude_entrypoint_template.md`
- `bootstrap/docs/project_overlay/agent_entrypoint_template.md`
- `bootstrap/docs/project_overlay/gemini_entrypoint_template.md`
- `bootstrap/docs/project_overlay/implementation_order_template.md`
- `bootstrap/docs/project_overlay/architecture_template.md`
- `bootstrap/docs/project_overlay/quality_gate_profile_template.md`
- `bootstrap/docs/project_overlay/coding_conventions_project_template.md`
- `bootstrap/docs/project_overlay/testing_profile_template.md`
- `bootstrap/docs/project_overlay/harness_doc_guard_workflow_template.yml`
- `bootstrap/docs/project_overlay/commit_rule_template.md`

#### bootstrap/scripts

| 현재 경로 | 목표 canonical path |
| --- | --- |
| `bootstrap/scripts/bootstrap_init.py` | `bootstrap/scripts/bootstrap_init.py` |
| `bootstrap/scripts/check_first_success_docs.py` | `bootstrap/scripts/check_first_success_docs.py` |
| `bootstrap/scripts/validate_overlay_decisions.py` | `bootstrap/scripts/validate_overlay_decisions.py` |
| `bootstrap/scripts/validate_overlay_consistency.py` | `bootstrap/scripts/validate_overlay_consistency.py` |
| `bootstrap/scripts/adopt_common.py` | `bootstrap/scripts/adopt_common.py` |
| `bootstrap/scripts/adopt_dry_run.py` | `bootstrap/scripts/adopt_dry_run.py` |
| `bootstrap/scripts/adopt_safe_write.py` | `bootstrap/scripts/adopt_safe_write.py` |

루트 `scripts/*.py` bootstrap wrapper는 제거되었다.

#### bootstrap/language_conventions

이 경로는 이미 `bootstrap/` 아래에 있으므로 1차에서 물리 이동 대상이 아니다. bootstrap canonical 자산으로 유지한다.

현재 확인된 파일:

- `bootstrap/README.md`
- `bootstrap/language_conventions/README.md`
- `bootstrap/language_conventions/python_coding_conventions_template.md`
- `bootstrap/language_conventions/java_coding_conventions_template.md`
- `bootstrap/language_conventions/kotlin_coding_conventions_template.md`

### 3. Downstream axis

#### downstream/docs core and runtime docs

| 현재 경로 | 목표 canonical path |
| --- | --- |
| `downstream/docs/harness_guide.md` | `downstream/docs/harness_guide.md` |
| `downstream/docs/downstream_harness_flow.md` | `downstream/docs/downstream_harness_flow.md` |
| `downstream/docs/standard/coding_guidelines_core.md` | `downstream/docs/standard/coding_guidelines_core.md` |

#### downstream/docs common policy docs

`downstream/docs/harness/common/*`는 downstream common policy의 canonical path다.

현재 확인된 파일:

- `downstream/docs/harness/common/audit_policy.md`
- `downstream/docs/harness/common/process_policy.md`
- `downstream/docs/harness/common/artifact_policy.md`
- `downstream/docs/harness/common/validation_policy.md`
- `downstream/docs/harness/common/lightweight_task_policy.md`
- `downstream/docs/harness/common/design_quality_policy.md`
- `downstream/docs/harness/common/performance_policy.md`
- `downstream/docs/harness/common/code_hygiene_policy.md`
- `downstream/docs/harness/common/testing_policy.md`
- `downstream/docs/harness/common/test_double_policy.md`

#### downstream/docs phase docs

`downstream/docs/phase_*/*`는 downstream phase docs의 canonical path다.

현재 확인된 파일:

- `downstream/docs/phase_1_requirement_and_planning/implementation.md`
- `downstream/docs/phase_1_requirement_and_planning/audit.md`
- `downstream/docs/phase_2_tdd_implementation/implementation.md`
- `downstream/docs/phase_2_tdd_implementation/audit.md`
- `downstream/docs/phase_3_integration/implementation.md`
- `downstream/docs/phase_3_integration/audit.md`
- `downstream/docs/phase_4_validation/implementation.md`
- `downstream/docs/phase_4_validation/audit.md`
- `downstream/docs/phase_5_documentation/implementation.md`
- `downstream/docs/phase_5_documentation/audit.md`

#### downstream/docs task templates

`downstream/docs/templates/task/*`는 downstream task template의 canonical path다.

현재 확인된 파일:

- `downstream/docs/templates/task/phase_status.md`
- `downstream/docs/templates/task/implementation_notes.md`
- `downstream/docs/templates/task/validation_report.md`
- `downstream/docs/templates/task/plan.md`
- `downstream/docs/templates/task/issue.md`
- `downstream/docs/templates/task/requirements.md`

#### downstream/docs examples

`downstream/docs/examples/**/*`는 downstream example docs의 canonical path다.

현재 저장소 기준 전체 범위는 아래 4개 subtree 전부다.

- `downstream/docs/examples/sample-task/*`
- `downstream/docs/examples/sample-lightweight-task/*`
- `downstream/docs/examples/bootstrap-first-success/*`
- `downstream/docs/examples/project-decisions/*`

현재 확인된 파일 전체 목록:

- `downstream/docs/examples/sample-task/phase_status.md`
- `downstream/docs/examples/sample-task/validation_report.md`
- `downstream/docs/examples/sample-task/implementation_notes.md`
- `downstream/docs/examples/sample-task/plan.md`
- `downstream/docs/examples/sample-task/issue.md`
- `downstream/docs/examples/sample-task/requirements.md`
- `downstream/docs/examples/sample-task/coding_conventions_project_example.md`
- `downstream/docs/examples/sample-lightweight-task/phase_status.md`
- `downstream/docs/examples/sample-lightweight-task/validation_report.md`
- `downstream/docs/examples/sample-lightweight-task/implementation_notes.md`
- `downstream/docs/examples/sample-lightweight-task/plan.md`
- `downstream/docs/examples/sample-lightweight-task/issue.md`
- `downstream/docs/examples/sample-lightweight-task/requirements.md`
- `downstream/docs/examples/bootstrap-first-success/validation_report.md`
- `downstream/docs/examples/bootstrap-first-success/overlay_completion_validation_report.md`
- `downstream/docs/examples/project-decisions/DEC-001-authorization-validation-location.md`

#### downstream/scripts

| 현재 경로 | 목표 canonical path |
| --- | --- |
| `downstream/scripts/validate_phase_gate.py` | `downstream/scripts/validate_phase_gate.py` |

루트 `scripts/validate_phase_gate.py` wrapper는 제거되었다.

### 4. 루트 유지 또는 후속 결정

| 현재 경로 | 1차 정책 |
| --- | --- |
| `docs/task/*` | 루트 유지, 1차 비범위 |
| `harness.log` | 루트 유지 |
| `tests/*` | 물리 이동은 보류, expectation은 각 단계에서 즉시 수정 |
| `.github/workflows/harness-doc-guard.yml` | 루트 유지 |
| `README.md` | 루트 유지, 최종적으로 저장소 지도 문서로 재작성 |

## 하위 이슈별 참조 기준

- `#134`, `#135`: maintainer docs 이동, boundary consumer, harness-doc-guard
- `#136`, `#141`, `#143`: bootstrap entry docs와 `project_overlay` guides/templates 이동
- `#144`, `#138`: bootstrap scripts 이동과 import/path 상수 갱신
- `#142`, `#140`, `#137`, `#145`: downstream docs, common policy, phase docs, task templates, examples 이동
- `#131`: downstream runtime script 이동
- `#139`: bundle boundary, generated bundle surface, manifest, dist 정리
- `#146`: install flow, root README, tests/CI 물리 정리, wrapper 제거 판단

## Old Path Search Keywords

후속 이슈에서는 아래 old path 문자열이 남아 있는지 단계마다 검색한다.

- `docs/kit_maintenance/audit_policy.md`
- `docs/kit_maintenance/drift_response_guide.md`
- `docs/kit_maintenance/release_process.md`
- `docs/kit_maintenance/downstream_bundle_boundary.md`
- `docs/kit_maintenance/downstream_bundle_smoke_validation.md`
- `docs/kit_maintenance/three_axis_rearchi_migration_inventory.md`
- `docs/project_overlay/`
- `docs/quickstart.md`
- `docs/how_harness_kit_works.md`
- `docs/version_support.md`
- `docs/harness_guide.md`
- `docs/downstream_harness_flow.md`
- `docs/harness/common/`
- `docs/standard/coding_guidelines_core.md`
- `docs/phase_1_requirement_and_planning/`
- `docs/phase_2_tdd_implementation/`
- `docs/phase_3_integration/`
- `docs/phase_4_validation/`
- `docs/phase_5_documentation/`
- `docs/templates/task/`
- `docs/examples/`
- `scripts/bootstrap_init.py`
- `scripts/check_first_success_docs.py`
- `scripts/validate_overlay_decisions.py`
- `scripts/validate_overlay_consistency.py`
- `scripts/adopt_common.py`
- `scripts/adopt_dry_run.py`
- `scripts/adopt_safe_write.py`
- `scripts/validate_phase_gate.py`
- `scripts/check_harness_docs.py`
- `scripts/generate_downstream_bundle.py`
- `scripts/validate_downstream_bundle.py`
- `scripts/install_downstream_bundle.py`

## 메모

- 이 문서는 `#126` 시점의 기준선이다.
- 실제 이동 단계에서 새 파일이 추가되거나 source path가 달라지면, 해당 하위 이슈에서 inventory drift를 함께 정리한다.
