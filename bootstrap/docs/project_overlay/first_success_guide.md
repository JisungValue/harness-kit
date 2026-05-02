# First Success Guide

빈 프로젝트 또는 거의 빈 프로젝트에서 `harness-kit`를 처음 붙일 때, 가장 먼저 재현해야 하는 성공 상태를 정리한 가이드다.

## 문서 역할

- 이 문서는 greenfield first-success 상세판이다.
- canonical 시작 경로는 항상 `bootstrap/docs/quickstart.md`를 먼저 본다.
- 이 문서는 quickstart의 greenfield 경로를 더 자세히 풀어 쓴 reference다.
- 실패 원인과 출력 해석은 `bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md`를 본다.
- 설치된 downstream Phase 흐름 전체는 final runtime path인 `docs/process/harness_guide.md`와 common policy 문서를 본다.
- 새 서브에이전트가 가장 먼저 여는 onboarding 문서는 아니고, `bootstrap/docs/quickstart.md`에서 greenfield 경로를 고른 뒤에 읽는 문서다.

## 시작 전 준비물

- 프로젝트 루트가 준비되어 있어야 한다.
- source repo shortcut을 실행할 수 있거나, release bundle 또는 vendored checkout 같은 install-time 입력이 있어야 한다. source repo shortcut의 실제 maintainer command는 repo root `README.md`의 "Source Repo Shortcut"만 본다.
- install-time 입력이 `vendor/harness-kit/` 같은 프로젝트 안 경로에 있더라도 final runtime surface에는 남기지 않는다.
- Python, Java, Kotlin 중 이번 프로젝트의 주 언어를 하나 먼저 정한다.
- install helper, bootstrap helper, validator 예시는 모두 Python 3 runtime으로 실행한다.
- legacy cleanup 또는 manual bootstrap 입력이 `vendor/harness-kit/`가 아닌 다른 경로라면 install/bootstrap 시점에 같은 경로를 `--vendor-path`로 함께 준다.
- 현재 MVP는 생성 대상 문서 경로만 검사하므로, first success를 빠르게 재현하려면 빈 디렉터리 또는 거의 빈 디렉터리에서 시작하는 편이 안전하다.

## 목표 성공 상태

first success의 최소 기준은 아래 둘이다.

- 프로젝트에 최소 문서 세트가 빠짐없이 생긴다.
- runtime launcher entrypoint 세트(`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`)가 함께 생긴다.
- 로컬 `docs/entrypoint.md`가 공통 kit 문서와 프로젝트 전용 문서를 함께 가리킨다.
- 로컬 `docs/project/decisions/README.md`가 프로젝트 결정 문서 진입점으로 함께 생긴다.

## Confidence Path

greenfield first success는 아래 신호를 순서대로 쌓는 경로로 본다.

1. bootstrap output
   - install flow가 install-time bundle의 `bootstrap_init.py`로 최소 문서 세트와 runtime entrypoint 세트를 생성한다.
   - non-default install-time 입력이면 `--vendor-path`를 받은 language convention bootstrap reference가 즉시 현지화된다.
2. minimum docs present
   - install flow가 `check_first_success_docs.py`를 install-completion helper로 실행해 최소 문서 세트 존재 여부를 가장 얕게 확인한다.
3. ready for the next session
   - root `scripts/validate_overlay_decisions.py --readiness first-success`가 canonical field와 허용 가능한 unresolved marker 경계를 확인한다.
   - root `scripts/validate_overlay_consistency.py`가 runtime traversal contract, decisions index link, process guide/bootstrap reference가 실제로 이어지는지 확인한다.
4. future-session guardrail installed
   - source repo 또는 delivery bundle의 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 프로젝트 `.github/workflows/` 아래 workflow 파일로 복사하고 `@<pin-tag-or-sha>`를 실제 릴리스 태그 또는 고정 SHA로 바꿔 future PR에서도 같은 검사를 고정한다.

위 4단계가 되면 새 세션이 최소 문서 세트, runtime traversal, decisions entrypoint, early CI guardrail을 같은 계약으로 따라갈 수 있다.

아직 수동 확인이 남는 항목:

- `architecture.md`, `implementation_order.md`, `coding_conventions_project.md`의 프로젝트별 실제 결정 내용
- `quality_gate_profile.md`, `testing_profile.md`, `commit_rule.md`의 팀/프로젝트 정책 확정
- workflow template의 ref pin을 실제 릴리스 태그 또는 고정 SHA로 바꾸는 작업

## 최소 문서 세트

- `docs/entrypoint.md`
- `docs/project/decisions/README.md`
- `docs/project/standards/architecture.md`
- `docs/project/standards/implementation_order.md`
- `docs/project/standards/coding_conventions_project.md`
- `docs/project/standards/quality_gate_profile.md`
- `docs/project/standards/testing_profile.md`
- `docs/project/standards/commit_rule.md`

## Runtime Instruction Entrypoint 세트

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`

## 최소 도입 순서

1. source repo shortcut 또는 release bundle 같은 install-time 입력을 준비한다.
2. 이번 프로젝트의 주 언어를 하나 정한다.
3. install flow 또는 manual bootstrap으로 최소 문서 세트를 만든다.
4. install-time 입력 또는 legacy cleanup 경로가 `vendor/harness-kit/`가 아니라면 install/bootstrap CLI에 `--vendor-path <actual-path>`를 함께 준다. 이미 default 경로로 생성했다면 이후 수동 현지화가 필요하다.
5. `docs/entrypoint.md`와 `docs/project/decisions/README.md`를 먼저 읽고, 현재 프로젝트에서 바로 확정할 중요한 결정이 있는지 확인한다.
6. install-completion helper가 통과한 뒤, 아래 첫 runtime 검증 명령으로 next-session readiness를 확인한다.
7. local validator가 통과하면 source repo 또는 delivery bundle의 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 프로젝트 `.github/workflows/` 아래 workflow 파일로 복사하고 `@<pin-tag-or-sha>`를 실제 릴리스 태그 또는 고정 SHA로 바꾼다.
8. 그다음 프로젝트 결정이 필요한 항목을 `architecture.md`, `implementation_order.md`, `coding_conventions_project.md`부터 채운다.
9. 이때 `implementation_order.md`에는 프로젝트 기본 레이어 순서만 적고, 특정 기획서 기준의 API 구현 우선순위나 task-specific 작업 순서는 `plan.md`에 남긴다.
10. project standard를 보강할 때는 repo-local evidence를 먼저 확인하고, 기획서만 보고 architecture나 class/file/package 구조를 invent하지 않는다. 미확정 구조는 `[프로젝트 결정 필요]` placeholder로 남기며, 구체 구조가 필요하면 사용자 승인 또는 decision candidate로 올린다.

## 가장 빠른 경로: greenfield install flow

source repo shortcut 또는 release install flow로 시작한다. 이 flow는 canonical downstream bundle을 임시 install-time 입력으로 사용한 뒤, 최종 프로젝트에는 root-local `docs/*`와 `scripts/*` runtime surface만 남긴다.

언어는 `python`, `java`, `kotlin` 중 하나를 고른다. non-default install-time 또는 legacy vendored 경로를 정리해야 하면 같은 시점에 `--vendor-path <actual-path>`로 경로도 같이 고정한다.

### 기대 결과

- 명령이 성공하면 `Install flow completed for ...`가 출력된다.
- 출력에는 canonical bundle 생성, install-time helper 실행, post-install cleanup 완료 신호가 함께 나온다.
- 생성 결과는 항상 같은 최소 문서 세트로 수렴한다.
- final runtime surface에는 `vendor/harness-kit/`, `docs/project_overlay/`, `scripts/bootstrap_init.py`, `scripts/check_first_success_docs.py`가 남지 않는다.

예시 출력:

```text
Generated canonical downstream bundle in /path/to/source/dist/harness-kit-project-bundle
Created harness bootstrap docs in /path/to/project
- AGENTS.md <- bootstrap/docs/project_overlay/agent_entrypoint_template.md
- CLAUDE.md <- bootstrap/docs/project_overlay/claude_entrypoint_template.md
- GEMINI.md <- bootstrap/docs/project_overlay/gemini_entrypoint_template.md
- docs/entrypoint.md <- bootstrap/docs/project_overlay/project_entrypoint_template.md
- docs/project/decisions/README.md <- bootstrap/docs/project_overlay/decisions_index_template.md
- docs/project/standards/architecture.md <- bootstrap/docs/project_overlay/architecture_template.md
- docs/project/standards/implementation_order.md <- bootstrap/docs/project_overlay/implementation_order_template.md
- docs/project/standards/coding_conventions_project.md <- bootstrap/docs/project_overlay/coding_conventions_project_template.md
- docs/project/standards/quality_gate_profile.md <- bootstrap/docs/project_overlay/quality_gate_profile_template.md
- docs/project/standards/testing_profile.md <- bootstrap/docs/project_overlay/testing_profile_template.md
- docs/project/standards/commit_rule.md <- bootstrap/docs/project_overlay/commit_rule_template.md
first success docs are present
Install-time bundle inputs removed from final runtime surface
Install flow completed for /path/to/project
```

release bundle이나 vendored checkout에서 `scripts/bootstrap_init.py`를 직접 실행하는 방식은 manual install-time path다. 이 경로를 쓰더라도 완료 뒤 canonical runtime command는 아래 root `scripts/*` validator다.

## 수동 경로

install helper를 쓰지 않아도 된다. 수동 경로의 목표도 같은 최소 문서 세트와 같은 no-vendor final runtime surface를 재현하는 것이다.

1. source repo 또는 delivery bundle의 `docs/project_overlay/` template를 프로젝트 경로로 복사한다.
2. 아래 매핑대로 배치한다.

```text
docs/project_overlay/agent_entrypoint_template.md -> AGENTS.md
docs/project_overlay/claude_entrypoint_template.md -> CLAUDE.md
docs/project_overlay/gemini_entrypoint_template.md -> GEMINI.md
docs/project_overlay/project_entrypoint_template.md -> docs/entrypoint.md
docs/project_overlay/decisions_index_template.md -> docs/project/decisions/README.md
docs/project_overlay/architecture_template.md -> docs/project/standards/architecture.md
docs/project_overlay/implementation_order_template.md -> docs/project/standards/implementation_order.md
docs/project_overlay/coding_conventions_project_template.md -> docs/project/standards/coding_conventions_project.md
docs/project_overlay/quality_gate_profile_template.md -> docs/project/standards/quality_gate_profile.md
docs/project_overlay/testing_profile_template.md -> docs/project/standards/testing_profile.md
docs/project_overlay/commit_rule_template.md -> docs/project/standards/commit_rule.md
```

3. 선택한 언어의 bootstrap convention을 install-time 입력의 `bootstrap/language_conventions/`에서 골라 `docs/project/standards/coding_conventions_project.md`에 병합한다.
4. `docs/entrypoint.md` 안의 공통 규칙이 `docs/process/harness_guide.md`를 가리키는지 확인한다.
5. runtime validator source를 root `scripts/validate_overlay_decisions.py`, `scripts/validate_overlay_consistency.py`, `scripts/validate_phase_gate.py`로 materialize 한다.
6. install-time 입력 경로와 `docs/project_overlay/`, `scripts/bootstrap_init.py`, `scripts/check_first_success_docs.py` 같은 helper residue를 final runtime surface에 남기지 않는다.

## 자동 경로와 수동 경로의 관계

- install flow는 `bootstrap/docs/project_overlay/*` template를 source of truth로 사용하는 얇은 bootstrap step을 포함한다.
- 수동 경로는 CLI가 하는 일을 사람이 직접 수행하는 fallback이다.
- 따라서 자동 경로와 수동 경로는 같은 최소 문서 세트와 같은 문서 책임 경계로 수렴해야 한다.
- CLI가 있어도 수동 기준 경로는 유지한다. 이후 CLI 동작이 바뀌어도 비교 기준은 template와 최소 문서 세트다.

## 첫 검증 명령과 기대 결과

greenfield install flow는 install-time helper인 `check_first_success_docs.py`를 실행해 최소 문서 세트가 실제로 생겼는지 먼저 확인한다. 이 helper는 final runtime surface에 남기지 않으므로, 설치 완료 뒤 downstream 프로젝트 루트에서는 root-local runtime validator를 실행한다.

기대 결과:

- 성공이면 `first success docs are present`가 출력된다.
- 실패면 빠진 문서 경로가 bullet 목록으로 출력된다.

이 helper는 문서 존재 여부만 확인하는 가장 얕은 체크다.
runtime instruction entrypoint 연결과 unresolved placeholder readiness까지 보려면 아래 validator를 이어서 실행한다. install/bootstrap을 non-default 입력 경로로 실행할 때 `--vendor-path`를 함께 줬다면 language convention bootstrap reference는 별도 현지화 없이 바로 다음 validator로 넘어갈 수 있다. 수동 복사 경로나 default 경로로 먼저 생성한 뒤 위치를 바꾼 경우에는 validator보다 먼저 `docs/project/standards/coding_conventions_project.md`의 bootstrap reference를 실제 입력 경로 또는 install-time-only note에 맞춘다.

```bash
python3 scripts/validate_overlay_decisions.py . --readiness first-success
python3 scripts/validate_overlay_consistency.py .
```

local validator가 통과하면 source repo 또는 delivery bundle에서 아래 workflow template를 복사해 future-session CI guardrail을 붙인다.

```text
docs/project_overlay/harness_doc_guard_workflow_template.yml -> project .github/workflows/ 아래 harness doc guard workflow 파일
```

non-default install-time 입력이면 source 경로의 `vendor/harness-kit/` 부분을 실제 경로로 바꾸고, workflow 안의 `@<pin-tag-or-sha>`를 릴리스 태그 또는 고정 SHA로 치환한다. 이 workflow template는 final runtime docs tree에 남는 canonical process 문서가 아니다.

first success를 확인한 뒤 첫 task를 시작하기 전에는 설치된 프로젝트의 `docs/entrypoint.md`와 `docs/process/harness_guide.md`를 읽고 Phase 1~5, approval gate, 재수행 규칙을 먼저 이해한다.

## 첫 검증 포인트

아래 항목이 보이면 first success로 본다.

- `docs/entrypoint.md`가 존재한다.
- `docs/project/decisions/README.md`가 존재한다.
- `docs/entrypoint.md` 제목이 project-local entrypoint 역할을 드러낸다.
- `AGENTS.md`가 `docs/entrypoint.md`를 우선 읽을 문서로 가리킨다.
- `docs/entrypoint.md`가 `docs/project/decisions/README.md`를 프로젝트 결정 문서 entrypoint로 연결한다.
- `AGENTS.md`가 linked document를 순서대로 모두 읽고 적용하라고 명시한다.
- `docs/entrypoint.md`가 `공통 규칙`, `프로젝트 전용 규칙` 문서를 함께 읽고 적용하라고 명시한다.
- `CLAUDE.md`, `GEMINI.md`가 `AGENTS.md`를 공통 진입점으로 가리킨다.
- `docs/entrypoint.md` 안에 공통 규칙으로 `docs/process/harness_guide.md`가 적혀 있다.
- `docs/entrypoint.md` 안에 `docs/project/standards/*` project 문서 경로가 함께 연결되어 있다.
- `docs/project/standards/coding_conventions_project.md` 안에 현재 선택한 언어와 bootstrap 기준 문서가 적혀 있다.
- `docs/project/standards/quality_gate_profile.md`, `testing_profile.md`, `commit_rule.md`가 비어 있지 않다.
- `docs/project/standards/quality_gate_profile.md`와 `commit_rule.md`에는 아직 팀 또는 프로젝트가 채워야 하는 결정 자리가 남아 있다.

## 성공 상태 예시

예를 들어 Python 프로젝트면 아래 정도가 보이면 된다.

```text
AGENTS.md
CLAUDE.md
GEMINI.md
docs/
  entrypoint.md
  project/
    decisions/
      README.md
    standards/
      architecture.md
      implementation_order.md
      coding_conventions_project.md
      quality_gate_profile.md
      testing_profile.md
      commit_rule.md
  process/
    harness_guide.md
```

그리고 `docs/project/standards/coding_conventions_project.md`에는 최소한 아래 정보가 보여야 한다.

- 현재 프로젝트의 활성 언어/런타임
- bootstrap 출처 또는 기준 언어 문서
- 현재 프로젝트에서 우선 적용하는 핵심 규칙 범주

## 흔한 실패 원인

- 대상 경로에 이미 `docs/entrypoint.md`나 `docs/project/standards/*` 파일이 있어 init CLI가 fail-fast로 중단됨
- `vendor/harness-kit/`가 아닌 다른 install-time 입력을 썼는데 generated bootstrap reference를 그대로 둠
- 실제 프로젝트 언어와 다른 `--language`를 선택해 잘못된 bootstrap 기준이 기록됨
- 언어 bootstrap 문서를 복사만 하고 프로젝트에 쓰지 않는 규칙을 그대로 남김

## 빠른 점검 포인트

- init CLI 실패 시: 충돌한 파일을 정리하거나, 정말 overwrite가 맞는 경우에만 `--force`를 쓴다.
- 문서는 생겼는데 경로가 이상하면: `docs/entrypoint.md`의 process guide/process flow 경로와 `docs/project/standards/coding_conventions_project.md`의 bootstrap reference를 먼저 확인한다.
- non-default install-time 입력인데 매번 수동 수정이 생기면: install/bootstrap 단계부터 `--vendor-path <actual-path>`를 같이 줬는지 먼저 확인한다.
- non-default install-time 입력 경로라면: localize가 끝나기 전에는 consistency validator green을 기대하지 않는다.
- local validator는 통과했는데 이후 PR에서 drift가 다시 생기면: source repo 또는 delivery bundle의 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 복사했고 `@<pin-tag-or-sha>`를 실제 ref로 바꿨는지 확인한다.
- consistency checker가 entrypoint 관련으로 실패하면: `AGENTS.md -> docs/entrypoint.md`, `CLAUDE.md`/`GEMINI.md` -> `AGENTS.md` 연결을 먼저 확인한다.
- agent가 첫 문서만 읽고 멈추는 것 같으면: `AGENTS.md`와 `docs/entrypoint.md`의 실행 계약 문구가 남아 있는지 먼저 확인한다.
- 문서는 맞는데 무엇부터 채워야 할지 막히면: `architecture.md`, `implementation_order.md`, `coding_conventions_project.md` 순으로 프로젝트 결정을 채운다.
- 품질 게이트와 테스트 기준이 섞여 보이면: 실행 명령은 `quality_gate_profile.md`, 테스트 범위와 환경은 `testing_profile.md`에 둔다.

## 참고 검증 자산

- 실제 end-to-end smoke validation 예시는 maintainer smoke/reference 자료가 필요할 때만 `downstream/docs/examples/bootstrap-first-success/validation_report.md`를 본다. 이 예시는 final runtime surface에 복사하지 않는다.
- init, validator, adopt dry-run의 로컬 진단 순서는 `bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md`를 본다.
- 사람이 읽는 overlay 완료 기준은 `bootstrap/docs/project_overlay/overlay_completion_checklist.md`를 본다.
- overlay 완료 상태 sample validation 예시는 maintainer smoke/reference 자료가 필요할 때만 `downstream/docs/examples/bootstrap-first-success/overlay_completion_validation_report.md`를 본다. 이 예시는 final runtime surface에 복사하지 않는다.
- first success 이후 unresolved placeholder를 점검하려면 `bootstrap/docs/project_overlay/unresolved_decision_validator.md`를 본다.
- 문서 간 교차 정합성을 점검하려면 `bootstrap/docs/project_overlay/cross_document_consistency_checker.md`를 본다.
