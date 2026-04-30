# Validation Report

## 목적

이 문서는 새 프로젝트 first success 경로가 실제로 재현 가능한지 end-to-end로 확인한 예시 검증 자산이다.

## 검증 대상

- `bootstrap/scripts/bootstrap_init.py`
- `bootstrap/docs/project_overlay/first_success_guide.md`
- `bootstrap/docs/project_overlay/*` template

## 검증 시나리오

### 시나리오 1. init CLI 기본 vendoring 경로

- 입력 조건:
  - 빈 임시 프로젝트 디렉터리
  - 언어 선택: `python`
- 실행 명령:

```bash
python3 bootstrap/scripts/bootstrap_init.py /tmp/bootstrap-cli-project --language python
python3 bootstrap/scripts/check_first_success_docs.py /tmp/bootstrap-cli-project
```

- 기대 결과:
- `bootstrap/scripts/bootstrap_init.py`가 최소 문서 세트를 생성한다.
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`가 함께 생성된다.
  - first-success helper command가 `first success docs are present`를 출력한다.
  - `docs/entrypoint.md`가 vendored kit guide 경로를 가리키고, `AGENTS.md`가 그 문서로 수렴하며, `coding_conventions_project.md`가 선택 언어와 bootstrap 기준 문서를 함께 보여준다.

### 시나리오 2. init CLI non-default vendoring 경로

- 입력 조건:
  - 빈 임시 프로젝트 디렉터리
  - 실제 vendored 경로: `third_party/harness-kit`
  - 언어 선택: `python`
- 실행 명령:

```bash
python3 bootstrap/scripts/bootstrap_init.py /tmp/bootstrap-cli-localized-project --language python --vendor-path third_party/harness-kit
python3 bootstrap/scripts/check_first_success_docs.py /tmp/bootstrap-cli-localized-project
python3 bootstrap/scripts/validate_overlay_consistency.py /tmp/bootstrap-cli-localized-project
```

- 기대 결과:
  - `docs/entrypoint.md`와 `coding_conventions_project.md`가 처음부터 `third_party/harness-kit/...` 경로를 가리킨다.
  - 별도 수동 현지화 없이도 first-success helper와 consistency validator가 같은 vendored 경로를 기준으로 통과한다.

### 시나리오 3. 수동 복사 경로

- 입력 조건:
  - 빈 임시 프로젝트 디렉터리
  - `bootstrap/docs/project_overlay/*` template를 기준으로 수동 복사
- 수동 복사 매핑:

```text
bootstrap/docs/project_overlay/agent_entrypoint_template.md -> AGENTS.md
bootstrap/docs/project_overlay/claude_entrypoint_template.md -> CLAUDE.md
bootstrap/docs/project_overlay/gemini_entrypoint_template.md -> GEMINI.md
bootstrap/docs/project_overlay/project_entrypoint_template.md -> docs/entrypoint.md
bootstrap/docs/project_overlay/decisions_index_template.md -> docs/project/decisions/README.md
bootstrap/docs/project_overlay/architecture_template.md -> docs/project/standards/architecture.md
bootstrap/docs/project_overlay/implementation_order_template.md -> docs/project/standards/implementation_order.md
bootstrap/docs/project_overlay/coding_conventions_project_template.md -> docs/project/standards/coding_conventions_project.md
bootstrap/docs/project_overlay/quality_gate_profile_template.md -> docs/project/standards/quality_gate_profile.md
bootstrap/docs/project_overlay/testing_profile_template.md -> docs/project/standards/testing_profile.md
bootstrap/docs/project_overlay/commit_rule_template.md -> docs/project/standards/commit_rule.md
```

- 기대 결과:
  - 수동 경로도 init CLI와 같은 최소 문서 세트로 수렴한다.
  - 첫 검증 명령이 동일하게 성공한다.
  - 수동 경로에서도 non-default vendored path와 언어 bootstrap 기준 문서가 함께 확인된다.

## 확인한 최소 문서 세트

- `docs/entrypoint.md`
- `docs/project/decisions/README.md`
- `docs/project/standards/architecture.md`
- `docs/project/standards/implementation_order.md`
- `docs/project/standards/coding_conventions_project.md`
- `docs/project/standards/quality_gate_profile.md`
- `docs/project/standards/testing_profile.md`
- `docs/project/standards/commit_rule.md`

## 확인한 runtime instruction entrypoint 세트

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`

## 성공 상태 예시

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

## 실행한 검증

- 검증 항목: init CLI 경로가 first success 문서 세트를 생성하는지 확인
- 대조한 입력물: `bootstrap/scripts/bootstrap_init.py`, `bootstrap/docs/project_overlay/first_success_guide.md`
  - 실행 방법 또는 확인 방식: default vendoring bootstrap smoke 시나리오에서 init CLI와 first-success helper를 순서대로 실행
  - 결과: init CLI가 최소 문서 세트, decisions index, runtime instruction entrypoint 세트를 만들고 첫 검증 명령이 성공했으며, `docs/entrypoint.md`의 vendored guide 경로, `docs/project/decisions/README.md`의 numbering/index 규칙, `AGENTS.md -> docs/entrypoint.md`, `CLAUDE.md`/`GEMINI.md` -> `AGENTS.md` 연결, `coding_conventions_project.md`의 언어/bootstrap 기준 문서도 함께 확인됐다
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: generated 문서의 vendored 경로 현지화는 소비자 프로젝트에서 추가로 확인해야 한다

- 검증 항목: init CLI가 non-default vendoring 경로를 bootstrap 시점에 바로 현지화하는지 확인
- 대조한 입력물: `bootstrap/scripts/bootstrap_init.py`, `bootstrap/docs/project_overlay/first_success_guide.md`
  - 실행 방법 또는 확인 방식: localized vendoring bootstrap smoke 시나리오에서 `--vendor-path third_party/harness-kit`와 local validator를 함께 실행
  - 결과: `--vendor-path third_party/harness-kit`로 생성한 `docs/entrypoint.md`, `coding_conventions_project.md`가 같은 vendored 경로를 가리켰고, first-success helper와 consistency validator도 추가 수동 수정 없이 통과했다
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: vendored 경로를 bootstrap 이후에 다시 옮기면 path update는 별도 수동 작업이 필요하다

- 검증 항목: 수동 복사 경로가 같은 최소 문서 세트로 수렴하는지 확인
- 대조한 입력물: `bootstrap/docs/project_overlay/*`, `bootstrap/docs/project_overlay/first_success_guide.md`
  - 실행 방법 또는 확인 방식: 수동 복사 시나리오에서 template 복사 후 non-default vendored path를 `docs/entrypoint.md`에 반영하고, `bootstrap/language_conventions/python_coding_conventions_template.md` 발췌 내용을 `coding_conventions_project.md`에 수동 병합해 검증
  - 결과: 수동 경로도 최소 문서 세트와 runtime instruction entrypoint 세트, 첫 검증 명령 결과, vendored path 현지화, entrypoint 연결, 선택 언어와 bootstrap 기준 문서, 핵심 규칙 범주 식별 신호가 함께 확인됐다
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 실제 프로젝트 언어에 맞는 convention 현지화는 여전히 수동 결정이 필요하다

- 검증 항목: first success 가이드의 검증 명령과 expected success 상태 일치 여부 확인
- 대조한 입력물: `bootstrap/docs/project_overlay/first_success_guide.md`, `bootstrap/scripts/check_first_success_docs.py`
  - 실행 방법 또는 확인 방식: 가이드의 검증 명령을 실제 bootstrap 결과에 그대로 실행하고, 같은 smoke 시나리오에서 vendored guide 경로, `AGENTS.md -> docs/entrypoint.md`, `CLAUDE.md`/`GEMINI.md` -> `AGENTS.md`, `docs/process/common/coding_guidelines_policy.md` project 문서 링크, 선택 언어, bootstrap 기준 문서, 핵심 규칙 범주, profile 문서 비어 있지 않음, quality gate/commit rule의 미해결 decision marker 존재를 함께 확인
  - 결과: 가이드의 첫 검증 명령과 실제 smoke 시나리오가 같은 성공 신호를 사용하고, 가이드가 말하는 핵심 first-success content signal과 runtime entrypoint 연결도 smoke 범위 안에 포함됐다
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 현재 검증 명령 자체는 파일 존재 여부 중심이고, 추가 content signal 확인은 별도 smoke 검증에서 보강한다

## 실행 명령

```bash
python3 bootstrap/scripts/bootstrap_init.py /tmp/bootstrap-cli-project --language python
python3 bootstrap/scripts/check_first_success_docs.py /tmp/bootstrap-cli-project
python3 bootstrap/scripts/bootstrap_init.py /tmp/bootstrap-cli-localized-project --language python --vendor-path third_party/harness-kit
python3 bootstrap/scripts/check_first_success_docs.py /tmp/bootstrap-cli-localized-project
python3 bootstrap/scripts/validate_overlay_consistency.py /tmp/bootstrap-cli-localized-project
```

## 해석 메모

- init CLI를 쓰는 경우에는 bootstrap 시점의 `--vendor-path`가 가장 먼저 시도할 현지화 경로다.
- `python3`는 bootstrap CLI, first-success helper, validator를 실행하는 prerequisite runtime이다.
- local validator가 통과하면 `docs/project_overlay/harness_doc_guard_workflow_template.yml`을 프로젝트 `.github/workflows/` 아래 workflow 파일로 복사하고 `@<pin-tag-or-sha>`를 실제 릴리스 태그 또는 고정 SHA로 바꿔 future-session guardrail을 붙인다.

## 결과 요약

- 새 프로젝트 first success 경로는 init CLI와 수동 복사 양쪽 모두에서 재현 가능하다.
- 최소 문서 세트, decisions index, runtime instruction entrypoint 세트, 첫 검증 명령은 실제 smoke test로 뒷받침된다.
- non-default vendoring도 `--vendor-path`를 쓰면 bootstrap 시점부터 같은 confidence path로 시작할 수 있다.

## 남은 리스크

- vendored `harness-kit` 경로를 bootstrap 이후에 다시 옮기면 path update는 여전히 소비자 프로젝트의 수동 확인 대상이다.
- 현재 end-to-end 검증은 greenfield 기준이다. brownfield adopt 검증은 별도 이슈 범위다.
- smoke test는 first-success 수준까지만 본다. 프로젝트별 세부 결정 완결성은 이후 overlay validator 범위에서 더 확인해야 한다.
