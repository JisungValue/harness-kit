# Quickstart

`harness-kit`를 처음 쓰는 사람이 현재 지원 범위 안에서 가장 빨리 시작하는 방법을 정리한 문서다.

## 문서 역할

- 이 문서는 canonical happy path를 고르는 빠른 시작 문서다.
- greenfield 상세 설명이 더 필요할 때만 `bootstrap/docs/project_overlay/first_success_guide.md`를, 실패 원인과 출력 해석이 필요할 때만 `bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md`를 본다.
- downstream 구조와 Phase 흐름 전체 설명은 `downstream/docs/downstream_harness_flow.md`를 본다.
- 현재 지원 범위와 최신 릴리스는 `bootstrap/docs/version_support.md`를 기준으로 본다.
- 새 서브에이전트와 새 사용자는 이 문서를 첫 문서로 본다. 다른 onboarding 문서는 이 문서에서 경로를 고른 뒤 필요할 때만 이어서 읽는다.

## 누구를 위한 문서인가

- 새 프로젝트를 시작하려는 팀
- 기존 프로젝트에 `harness-kit`를 부분 도입하려는 팀
- 여러 세부 문서를 오가기 전에 전체 흐름을 먼저 알고 싶은 사용자

## 현재 바로 할 수 있는 것

- 새 프로젝트에 최소 overlay 문서 세트를 생성한다.
- first success 상태를 로컬에서 확인한다.
- future-session consistency를 doc-guard CI로 조기에 고정한다.
- overlay 문서의 unresolved decision을 점검한다.
- overlay 문서 간 교차 정합성을 점검한다.
- 기존 프로젝트 상태를 read-only dry-run으로 읽고 baseline과 비교한다.
- 기존 프로젝트에서 missing file create와 explicit path overwrite 중심의 제한적 safe write/update를 수행한다.

## 현재 아직 안 되는 것

- 기존 프로젝트에 대한 자동 merge
- user-modified existing file에 대한 automatic merge/update
- framework별 semantic diff
- interactive TUI

## 빠른 시작 경로

### 새 프로젝트

1. source repo shortcut이나 release install flow로 greenfield final layout을 만든다. source repo shortcut의 실제 maintainer command는 repo root `README.md`의 "Source Repo Shortcut"만 본다.
2. release bundle 또는 vendored checkout을 직접 쓰는 경우, 그 경로는 install-time 입력으로만 취급한다. 아래 legacy 예시의 기준 경로는 `vendor/harness-kit/`이고, 다른 경로를 쓰면 문서 안의 vendored path와 예시 명령의 `vendor/harness-kit/` 부분을 모두 같은 실제 경로로 바꿔서 실행한다.

- install helper, `bootstrap_init.py`, validator 예시는 모두 Python 3 runtime이 필요하다.
- 현재 bootstrap CLI는 `python`, `java`, `kotlin` language profile을 지원하지만, 실행 자체는 Python 3로 한다.
- non-default install-time 또는 legacy vendored 입력을 정리해야 하면 install/bootstrap 시점부터 `--vendor-path <actual-path>`를 함께 줘 generated reference와 cleanup target을 바로 현지화한다.
- 설치가 끝난 downstream 프로젝트에는 `vendor/harness-kit/`, `docs/project_overlay/`, `scripts/bootstrap_init.py`, `scripts/check_first_success_docs.py`가 final runtime surface로 남지 않는다.

release bundle이나 vendored checkout에서 bootstrap helper를 직접 실행하는 legacy/manual 경로는 install-time 입력 경로에서만 실행한다. 이 명령은 final runtime command surface가 아니며, 완료 뒤에는 root `scripts/*` validator만 사용한다.

```bash
python3 vendor/harness-kit/scripts/bootstrap_init.py . --language python
```

3. 설치 직후 `docs/entrypoint.md`와 `docs/project/decisions/README.md`를 먼저 읽고, 현재 프로젝트에서 구조/정책/예외/책임 위치 중 바로 확정해야 할 결정이 있는지 확인한다.

4. install-time 입력을 `vendor/harness-kit/` 이외의 경로에 두었다면, install/bootstrap 때 `--vendor-path`를 이미 준 경우 language convention bootstrap reference는 바로 맞는다. 그 옵션 없이 생성했다면 validator를 돌리기 전에 아래 파일의 bootstrap reference를 실제 입력 경로 또는 install-time-only note에 맞게 먼저 현지화한다.

- `docs/project/standards/coding_conventions_project.md`

5. install flow는 install-time helper인 `check_first_success_docs.py`로 최소 문서 세트 존재 여부를 확인한 뒤 helper를 final runtime surface에 남기지 않는다. 설치가 끝난 뒤에는 아래 root-local runtime validator를 실행한다.

```bash
python3 scripts/validate_overlay_decisions.py . --readiness first-success
python3 scripts/validate_overlay_consistency.py .
```

6. local validator가 통과하면 source repo 또는 delivery bundle의 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 프로젝트 `.github/workflows/` 아래 workflow 파일로 복사하고 workflow 안의 `@<pin-tag-or-sha>`를 실제 릴리스 태그 또는 고정 SHA로 바꾼다. 이 template는 install-time 자산이고, final runtime docs tree의 일부로 남기지 않는다.

7. 첫 task를 시작하기 전에 `docs/process/downstream_harness_flow.md`를 한 번 읽고 Phase 1~5, approval gate, 재수행 규칙을 먼저 이해한다.
8. `docs/process/templates/task/`를 프로젝트 작업 경로로 복사해 첫 task를 시작한다.
9. task를 시작하면 `phase_status.md`에 현재 gate와 허용 write-set을 먼저 적고, 필요할 때 아래 validator로 hard-stop 위반을 점검한다.
10. 이때 `docs/project/standards/implementation_order.md`는 프로젝트 기본 레이어 순서 문서로 유지하고, 이번 task에서 어떤 API/기능부터 구현할지는 `plan.md`에 적는다.
11. `validate_phase_gate.py`를 인자 없이 실행하면 기본적으로 현재 task workspace와 `phase_status.md`의 허용/잠금 패턴에 걸리는 dirty path만 검사한다. repo 전체 dirty path까지 함께 보려면 `--git-scope repo`를 명시한다.

```bash
python3 scripts/validate_phase_gate.py docs/task/<task_id> --paths docs/task/<task_id>/issue.md docs/task/<task_id>/phase_status.md
```

상세 설명이 더 필요하면 아래 reference로 이어서 읽는다.

- greenfield 상세판: `bootstrap/docs/project_overlay/first_success_guide.md`
- 로컬 진단/출력 해석: `bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md`

### 기존 프로젝트 첫 도입

- 아직 `docs/entrypoint.md`가 없거나, legacy `docs/harness_guide.md`만 남아 있거나, 최소 overlay 문서 세트가 아직 맞춰지지 않았다면 이 경로를 따른다.

1. `bootstrap/docs/project_overlay/adopt_dry_run.md`를 본다.
2. 아래 명령을 실행한다.

- 아래 명령도 downstream 프로젝트 루트에서 실행한다.

```bash
python3 vendor/harness-kit/scripts/adopt_dry_run.py . --language python
```

3. 결과를 아래처럼 읽는다.
    - `missing files`: 안전하게 생성 가능한 후보
    - `existing but unchanged targets`: baseline과 동일
    - `differing files`: 수동 검토 대상
    - `conflict candidates`: 수동 판단 우선 대상
    - `legacy entrypoint migration candidates`: 예전 `docs/harness_guide.md`를 새 canonical `docs/entrypoint.md`로 옮겨야 하는 상태
4. `legacy entrypoint migration candidates`가 보이면 아래 rename migration부터 먼저 검토한다.

```bash
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python --migrate-legacy-entrypoint
```

5. legacy migration candidate가 없고 `missing files`를 먼저 안전하게 반영하려면 아래 명령을 실행한다.

```bash
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python
```

6. exact-match target만 다시 쓰거나 특정 경로만 명시적으로 덮어쓰려면 아래처럼 범위를 좁힌다.

```bash
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python --update-unchanged
python3 vendor/harness-kit/scripts/adopt_safe_write.py . --language python --force-overwrite docs/entrypoint.md
```

7. `differing files`와 `conflict candidates`는 기본적으로 수동 비교 대상으로 남긴다.
8. partial adoption 상태가 structurally safe한지 먼저 보려면 아래 incremental validator를 실행한다.
9. 최소 문서 세트가 어느 정도 맞춰진 뒤에만 full validator로 넘어간다.
10. 첫 task를 시작하기 전에 `docs/process/downstream_harness_flow.md`를 한 번 읽고 Phase 1~5, approval gate, 재수행 규칙을 먼저 이해한다.

```bash
python3 scripts/validate_overlay_consistency.py . --mode incremental
python3 scripts/validate_overlay_decisions.py . --readiness first-success
python3 scripts/validate_overlay_consistency.py .
```

출력 해석과 로컬 진단 순서가 더 필요하면 `bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md`를 reference로 본다.

### 이미 도입된 downstream 업그레이드

- 이미 `docs/entrypoint.md`와 process guide 기준 문서가 있고, 새 bundle 버전만 반영하려면 adoption이 아니라 upgrade 경로를 따른다.
- 이 경우에는 `bootstrap/docs/project_overlay/downstream_harness_upgrade_guide.md`를 먼저 보고, 영향도를 분류하려면 `bootstrap/docs/project_overlay/harness_upgrade_impact_policy.md`를, 사람 기준 diff review 항목이 필요하면 `bootstrap/docs/project_overlay/downstream_overlay_diff_review_checklist.md`를 함께 본다.

## 핵심 도구 역할

- `bootstrap_init.py`
  - 새 프로젝트용 문서 세트를 실제로 생성한다.
- `check_first_success_docs.py`
  - install-time completion helper다. greenfield final install 완료 뒤에는 root `scripts/*` runtime surface에 남지 않는다.
- `docs/project_overlay/harness_doc_guard_workflow_template.yml`
  - first-success local validator가 통과한 뒤 future-session consistency를 CI에 고정하는 workflow template다.
  - 복사 후 `@<pin-tag-or-sha>`를 실제 릴리스 태그 또는 고정 SHA로 바꿔 사용한다.
- `validate_overlay_decisions.py`
  - unresolved placeholder와 readiness 상태를 보고, 먼저 고쳐야 하는 canonical field를 우선순위와 함께 보여 준다.
- `validate_overlay_consistency.py`
  - 문서 간 참조, decisions index 연결, runtime instruction entrypoint 연결, traversal contract, 책임 경계를 본다.
  - `--mode incremental`은 partial adoption 상태의 safe gap과 blocker를 먼저 분리한다.
- `validate_phase_gate.py`
  - task workspace의 `phase_status.md`와 현재 candidate path 또는 git 변경분을 기준으로 hard-stop gate와 write-set 위반을 검사한다.
- `adopt_dry_run.py`
  - 기존 프로젝트 상태를 read-only로 분류한다.
- `adopt_safe_write.py`
  - 기존 프로젝트에서 missing file create, unchanged refresh, explicit path force overwrite만 허용하는 제한적 write 도구다.

## first-success 와 phase2 차이

- `first-success`
  - 최소 문서 세트가 갖춰졌고, 초기 시작 상태가 성립하는지 본다.
  - 일부 placeholder는 아직 허용된다.
- `phase2`
  - 실제 구현/감사에 들어가기 전 더 많은 프로젝트 결정을 채웠는지 본다.
  - `first-success`보다 훨씬 엄격하다.

## 흔한 실패 원인

- init 대상 경로에 이미 생성 대상 문서가 있어 fail-fast가 발생함
- install-time 또는 legacy vendored path를 실제 프로젝트 경로에 맞게 현지화하지 않음
- non-default install-time 입력인데 bootstrap 때 `--vendor-path`를 주지 않아 unnecessary 수동 현지화가 생김
- non-default install-time 입력 경로인데 현지화 전에 consistency validator부터 실행해 false confidence 또는 즉시 실패를 만듦
- agent가 `AGENTS.md`만 읽고 `docs/entrypoint.md`, core guide, `docs/project/standards/*`까지 따라가지 않음
- 중요한 정책/예외/책임 위치 변경인데 `docs/project/decisions/README.md`와 관련 decision 문서를 같이 안 봄
- `--language`를 실제 프로젝트와 다르게 선택함
- local validator 이후 source repo 또는 delivery bundle의 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 복사하지 않거나 `@<pin-tag-or-sha>`를 그대로 둬 future-session guardrail이 고정되지 않음
- 기존 프로젝트에서 `adopt_dry_run.py` 결과를 보지 않고 validator를 너무 일찍 실행함
- 기존 프로젝트에서 legacy `docs/harness_guide.md`를 그냥 두고 `docs/entrypoint.md`만 새로 생성해 반쪽 migration 상태가 됨
- `validate_overlay_decisions.py`와 `validate_overlay_consistency.py`의 역할 차이를 혼동함

## 다음에 읽을 문서

- 전체 동작 설명: `bootstrap/docs/how_harness_kit_works.md`
- greenfield 상세 reference: `bootstrap/docs/project_overlay/first_success_guide.md`
- diagnostics reference: `bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md`
- 기존 프로젝트 dry-run: `bootstrap/docs/project_overlay/adopt_dry_run.md`
- 기존 프로젝트 bundle upgrade 절차: `bootstrap/docs/project_overlay/downstream_harness_upgrade_guide.md`
- 기존 프로젝트 diff review checklist: `bootstrap/docs/project_overlay/downstream_overlay_diff_review_checklist.md`
- 기존 프로젝트 upgrade impact 분류: `bootstrap/docs/project_overlay/harness_upgrade_impact_policy.md`
