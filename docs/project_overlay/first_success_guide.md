# First Success Guide

빈 프로젝트 또는 거의 빈 프로젝트에서 `harness-kit`를 처음 붙일 때, 가장 먼저 재현해야 하는 성공 상태를 정리한 가이드다.

## 문서 역할

- 이 문서는 greenfield first-success 상세판이다.
- canonical 시작 경로를 먼저 고르려면 `docs/quickstart.md`를 보고, 실패 원인과 출력 해석은 `docs/project_overlay/local_diagnostics_and_dry_run.md`를 본다.
- downstream 구조와 Phase 흐름 전체는 `docs/downstream_harness_flow.md`를 본다.
- 새 서브에이전트가 가장 먼저 여는 onboarding 문서는 아니고, `docs/quickstart.md`에서 greenfield 경로를 고른 뒤에 읽는 문서다.

## 시작 전 준비물

- 프로젝트 루트가 준비되어 있어야 한다.
- `harness-kit`가 프로젝트 안에서 참조 가능한 경로에 있어야 한다.
- 아래 예시는 `vendor/harness-kit/`에 vendored 되어 있다고 가정한다.
- Python, Java, Kotlin 중 이번 프로젝트의 주 언어를 하나 먼저 정한다.
- bootstrap과 validator 예시는 모두 Python 3 runtime으로 실행한다.
- `vendor/harness-kit/`가 아닌 다른 경로를 쓴다면 init CLI에서 같은 경로를 `--vendor-path`로 함께 준다.
- 현재 MVP는 생성 대상 문서 경로만 검사하므로, first success를 빠르게 재현하려면 빈 디렉터리 또는 거의 빈 디렉터리에서 시작하는 편이 안전하다.

## 목표 성공 상태

first success의 최소 기준은 아래 둘이다.

- 프로젝트에 최소 문서 세트가 빠짐없이 생긴다.
- runtime launcher entrypoint 세트(`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`)가 함께 생긴다.
- 로컬 `docs/project_entrypoint.md`가 공통 kit 문서와 프로젝트 전용 문서를 함께 가리킨다.
- 로컬 `docs/decisions/README.md`가 프로젝트 결정 문서 진입점으로 함께 생긴다.

## Confidence Path

greenfield first success는 아래 신호를 순서대로 쌓는 경로로 본다.

1. bootstrap output
   - `bootstrap_init.py`가 최소 문서 세트와 runtime entrypoint 세트를 생성한다.
   - non-default vendoring이면 `--vendor-path`를 받은 generated reference가 즉시 현지화된다.
2. minimum docs present
   - `check_first_success_docs.py`가 최소 문서 세트 존재 여부를 가장 얕게 확인한다.
3. ready for the next session
   - `validate_overlay_decisions.py --readiness first-success`가 canonical field와 허용 가능한 unresolved marker 경계를 확인한다.
   - `validate_overlay_consistency.py`가 runtime traversal contract, decisions index link, vendored guide/bootstrap reference가 실제로 이어지는지 확인한다.
4. future-session guardrail installed
   - `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 프로젝트 `.github/workflows/` 아래 workflow 파일로 복사하고 `@<pin-tag-or-sha>`를 실제 릴리스 태그 또는 고정 SHA로 바꿔 future PR에서도 같은 검사를 고정한다.

위 4단계가 되면 새 세션이 최소 문서 세트, runtime traversal, decisions entrypoint, early CI guardrail을 같은 계약으로 따라갈 수 있다.

아직 수동 확인이 남는 항목:

- `architecture.md`, `implementation_order.md`, `coding_conventions_project.md`의 프로젝트별 실제 결정 내용
- `quality_gate_profile.md`, `testing_profile.md`, `commit_rule.md`의 팀/프로젝트 정책 확정
- workflow template의 ref pin을 실제 릴리스 태그 또는 고정 SHA로 바꾸는 작업

## 최소 문서 세트

- `docs/project_entrypoint.md`
- `docs/decisions/README.md`
- `docs/standard/architecture.md`
- `docs/standard/implementation_order.md`
- `docs/standard/coding_conventions_project.md`
- `docs/standard/quality_gate_profile.md`
- `docs/standard/testing_profile.md`
- `docs/standard/commit_rule.md`

## Runtime Instruction Entrypoint 세트

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`

## 최소 도입 순서

1. 프로젝트 루트에 `harness-kit`를 vendoring 하거나 참조 가능한 경로로 둔다.
2. 이번 프로젝트의 주 언어를 하나 정한다.
3. init CLI 또는 수동 복사로 최소 문서 세트를 만든다.
4. `vendor/harness-kit/`가 아닌 경로에 kit를 뒀다면 init CLI에 `--vendor-path <actual-path>`를 함께 준다. 이미 default 경로로 생성했다면 이후 수동 현지화가 필요하다.
5. `docs/project_entrypoint.md`와 `docs/decisions/README.md`를 먼저 읽고, 현재 프로젝트에서 바로 확정할 중요한 결정이 있는지 확인한다.
6. 아래 첫 검증 명령으로 최소 문서 세트 존재 여부와 next-session readiness를 확인한다.
7. local validator가 통과하면 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 프로젝트 `.github/workflows/` 아래 workflow 파일로 복사하고 `@<pin-tag-or-sha>`를 실제 릴리스 태그 또는 고정 SHA로 바꾼다.
8. 그다음 프로젝트 결정이 필요한 항목을 `architecture.md`, `implementation_order.md`, `coding_conventions_project.md`부터 채운다.

## 가장 빠른 경로: init CLI

프로젝트 루트에서 아래처럼 실행한다.

이 명령은 `harness-kit` source repo가 아니라 downstream 프로젝트 루트에서 실행한다.

```bash
python3 vendor/harness-kit/scripts/bootstrap_init.py . --language python
```

언어만 바꾸면 Java/Kotlin도 같은 방식으로 시작할 수 있다.

```bash
python3 vendor/harness-kit/scripts/bootstrap_init.py . --language java
python3 vendor/harness-kit/scripts/bootstrap_init.py . --language kotlin
```

non-default vendoring이면 같은 시점에 vendored 경로도 같이 고정한다.

```bash
python3 third_party/harness-kit/scripts/bootstrap_init.py . --language python --vendor-path third_party/harness-kit
```

### 기대 결과

- 명령이 성공하면 `Created harness bootstrap docs in ...`가 출력된다.
- 출력에는 생성된 파일 경로와 source template 경로가 함께 나온다.
- 생성 결과는 항상 같은 최소 문서 세트로 수렴한다.

예시 출력:

```text
Created harness bootstrap docs in /path/to/project
- AGENTS.md <- docs/project_overlay/agent_entrypoint_template.md
- CLAUDE.md <- docs/project_overlay/claude_entrypoint_template.md
- GEMINI.md <- docs/project_overlay/gemini_entrypoint_template.md
- docs/project_entrypoint.md <- docs/project_overlay/project_entrypoint_template.md
- docs/decisions/README.md <- docs/project_overlay/decisions_index_template.md
- docs/standard/architecture.md <- docs/project_overlay/architecture_template.md
- docs/standard/implementation_order.md <- docs/project_overlay/implementation_order_template.md
- docs/standard/coding_conventions_project.md <- docs/project_overlay/coding_conventions_project_template.md
- docs/standard/quality_gate_profile.md <- docs/project_overlay/quality_gate_profile_template.md
- docs/standard/testing_profile.md <- docs/project_overlay/testing_profile_template.md
- docs/standard/commit_rule.md <- docs/project_overlay/commit_rule_template.md
```

## 수동 경로

init CLI를 쓰지 않아도 된다. 수동 경로의 목표도 같은 최소 문서 세트를 재현하는 것이다.

1. `vendor/harness-kit/docs/project_overlay/`의 template를 프로젝트 경로로 복사한다.
2. 아래 매핑대로 배치한다.

```text
vendor/harness-kit/docs/project_overlay/agent_entrypoint_template.md -> AGENTS.md
vendor/harness-kit/docs/project_overlay/claude_entrypoint_template.md -> CLAUDE.md
vendor/harness-kit/docs/project_overlay/gemini_entrypoint_template.md -> GEMINI.md
vendor/harness-kit/docs/project_overlay/project_entrypoint_template.md -> docs/project_entrypoint.md
vendor/harness-kit/docs/project_overlay/decisions_index_template.md -> docs/decisions/README.md
vendor/harness-kit/docs/project_overlay/architecture_template.md -> docs/standard/architecture.md
vendor/harness-kit/docs/project_overlay/implementation_order_template.md -> docs/standard/implementation_order.md
vendor/harness-kit/docs/project_overlay/coding_conventions_project_template.md -> docs/standard/coding_conventions_project.md
vendor/harness-kit/docs/project_overlay/quality_gate_profile_template.md -> docs/standard/quality_gate_profile.md
vendor/harness-kit/docs/project_overlay/testing_profile_template.md -> docs/standard/testing_profile.md
vendor/harness-kit/docs/project_overlay/commit_rule_template.md -> docs/standard/commit_rule.md
```

3. 선택한 언어의 bootstrap convention을 `vendor/harness-kit/bootstrap/language_conventions/`에서 골라 `docs/standard/coding_conventions_project.md`에 병합한다.
4. `docs/project_entrypoint.md` 안의 vendored 경로가 실제 배치 경로와 맞는지 확인한다.

## 자동 경로와 수동 경로의 관계

- init CLI는 `docs/project_overlay/*` template를 source of truth로 사용하는 얇은 copier다.
- 수동 경로는 CLI가 하는 일을 사람이 직접 수행하는 fallback이다.
- 따라서 자동 경로와 수동 경로는 같은 최소 문서 세트와 같은 문서 책임 경계로 수렴해야 한다.
- CLI가 있어도 수동 기준 경로는 유지한다. 이후 CLI 동작이 바뀌어도 비교 기준은 template와 최소 문서 세트다.

## 첫 검증 명령과 기대 결과

CLI 경로든 수동 경로든, 아래 명령으로 최소 문서 세트가 실제로 생겼는지 먼저 확인한다.

아래 명령도 downstream 프로젝트 루트에서 실행한다.

```bash
python3 vendor/harness-kit/scripts/check_first_success_docs.py .
```

기대 결과:

- 성공이면 `first success docs are present`가 출력된다.
- 실패면 빠진 문서 경로가 bullet 목록으로 출력된다.

이 명령은 문서 존재 여부만 확인하는 가장 얕은 체크다.
runtime instruction entrypoint 연결과 unresolved placeholder readiness까지 보려면 아래 validator를 이어서 실행한다. `bootstrap_init.py`를 non-default vendoring으로 실행할 때 `--vendor-path`를 함께 줬다면 별도 현지화 없이 바로 다음 validator로 넘어갈 수 있다. 수동 복사 경로나 default 경로로 먼저 생성한 뒤 위치를 바꾼 경우에는 validator보다 먼저 `docs/project_entrypoint.md`와 `docs/standard/coding_conventions_project.md`의 vendored 경로를 실제 배치 경로로 맞춘다.

```bash
python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness first-success
python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .
```

local validator가 통과하면 아래 workflow template를 복사해 future-session CI guardrail을 붙인다.

```text
vendor/harness-kit/docs/project_overlay/harness_doc_guard_workflow_template.yml -> project .github/workflows/ 아래 harness doc guard workflow 파일
```

non-default vendoring이면 source 경로의 `vendor/harness-kit/` 부분만 실제 경로로 바꾸고, workflow 안의 `@<pin-tag-or-sha>`를 릴리스 태그 또는 고정 SHA로 치환한다.

first success를 확인한 뒤 첫 task를 시작하기 전에는 `docs/downstream_harness_flow.md`를 한 번 읽고 Phase 1~5, approval gate, 재수행 규칙을 먼저 이해한다.

## 첫 검증 포인트

아래 항목이 보이면 first success로 본다.

- `docs/project_entrypoint.md`가 존재한다.
- `docs/decisions/README.md`가 존재한다.
- `docs/project_entrypoint.md` 제목이 project-local entrypoint 역할을 드러낸다.
- `AGENTS.md`가 `docs/project_entrypoint.md`를 우선 읽을 문서로 가리킨다.
- `docs/project_entrypoint.md`가 `docs/decisions/README.md`를 프로젝트 결정 문서 entrypoint로 연결한다.
- `AGENTS.md`가 linked document를 순서대로 모두 읽고 적용하라고 명시한다.
- `docs/project_entrypoint.md`가 `공통 규칙`, `프로젝트 전용 규칙` 문서를 함께 읽고 적용하라고 명시한다.
- `CLAUDE.md`, `GEMINI.md`가 `AGENTS.md`를 공통 진입점으로 가리킨다.
- `docs/project_entrypoint.md` 안에 공통 규칙으로 `vendor/harness-kit/docs/harness_guide.md` 또는 프로젝트가 실제로 사용하는 vendored kit 경로가 적혀 있다.
- `docs/project_entrypoint.md` 안에 `docs/standard/*` project 문서 경로가 함께 연결되어 있다.
- `docs/standard/coding_conventions_project.md` 안에 현재 선택한 언어와 bootstrap 기준 문서가 적혀 있다.
- `docs/standard/quality_gate_profile.md`, `testing_profile.md`, `commit_rule.md`가 비어 있지 않다.
- `docs/standard/quality_gate_profile.md`와 `commit_rule.md`에는 아직 팀 또는 프로젝트가 채워야 하는 결정 자리가 남아 있다.

## 성공 상태 예시

예를 들어 Python 프로젝트면 아래 정도가 보이면 된다.

```text
AGENTS.md
CLAUDE.md
GEMINI.md
docs/
  project_entrypoint.md
  decisions/
    README.md
  standard/
    architecture.md
    implementation_order.md
    coding_conventions_project.md
    quality_gate_profile.md
    testing_profile.md
    commit_rule.md
```

그리고 `docs/standard/coding_conventions_project.md`에는 최소한 아래 정보가 보여야 한다.

- 현재 프로젝트의 활성 언어/런타임
- bootstrap 출처 또는 기준 언어 문서
- 현재 프로젝트에서 우선 적용하는 핵심 규칙 범주

## 흔한 실패 원인

- 대상 경로에 이미 `docs/project_entrypoint.md`나 `docs/standard/*` 파일이 있어 init CLI가 fail-fast로 중단됨
- `vendor/harness-kit/`가 아닌 다른 위치에 kit를 뒀는데 generated vendored 경로를 그대로 둠
- 실제 프로젝트 언어와 다른 `--language`를 선택해 잘못된 bootstrap 기준이 기록됨
- 언어 bootstrap 문서를 복사만 하고 프로젝트에 쓰지 않는 규칙을 그대로 남김

## 빠른 점검 포인트

- init CLI 실패 시: 충돌한 파일을 정리하거나, 정말 overwrite가 맞는 경우에만 `--force`를 쓴다.
- 문서는 생겼는데 경로가 이상하면: `docs/project_entrypoint.md`와 `docs/standard/coding_conventions_project.md`의 vendored 경로를 먼저 확인한다.
- non-default vendoring인데 매번 수동 수정이 생기면: bootstrap 단계부터 `--vendor-path <actual-path>`를 같이 줬는지 먼저 확인한다.
- non-default vendored 경로라면: localize가 끝나기 전에는 consistency validator green을 기대하지 않는다.
- local validator는 통과했는데 이후 PR에서 drift가 다시 생기면: `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 복사했고 `@<pin-tag-or-sha>`를 실제 ref로 바꿨는지 확인한다.
- consistency checker가 entrypoint 관련으로 실패하면: `AGENTS.md -> docs/project_entrypoint.md`, `CLAUDE.md`/`GEMINI.md` -> `AGENTS.md` 연결을 먼저 확인한다.
- agent가 첫 문서만 읽고 멈추는 것 같으면: `AGENTS.md`와 `docs/project_entrypoint.md`의 실행 계약 문구가 남아 있는지 먼저 확인한다.
- 문서는 맞는데 무엇부터 채워야 할지 막히면: `architecture.md`, `implementation_order.md`, `coding_conventions_project.md` 순으로 프로젝트 결정을 채운다.
- 품질 게이트와 테스트 기준이 섞여 보이면: 실행 명령은 `quality_gate_profile.md`, 테스트 범위와 환경은 `testing_profile.md`에 둔다.

## 참고 검증 자산

- 실제 end-to-end smoke validation 예시는 `docs/examples/bootstrap-first-success/validation_report.md`를 본다.
- init, validator, adopt dry-run의 로컬 진단 순서는 `docs/project_overlay/local_diagnostics_and_dry_run.md`를 본다.
- 사람이 읽는 overlay 완료 기준은 `docs/project_overlay/overlay_completion_checklist.md`를 본다.
- overlay 완료 상태 sample validation 예시는 `docs/examples/bootstrap-first-success/overlay_completion_validation_report.md`를 본다.
- first success 이후 unresolved placeholder를 점검하려면 `docs/project_overlay/unresolved_decision_validator.md`를 본다.
- 문서 간 교차 정합성을 점검하려면 `docs/project_overlay/cross_document_consistency_checker.md`를 본다.
