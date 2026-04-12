# Validation Report

## 목적

이 문서는 새 프로젝트 first success 경로가 실제로 재현 가능한지 end-to-end로 확인한 예시 검증 자산이다.

## 검증 대상

- `scripts/bootstrap_init.py`
- `docs/project_overlay/first_success_guide.md`
- `docs/project_overlay/*` template

## 검증 시나리오

### 시나리오 1. init CLI 경로

- 입력 조건:
  - 빈 임시 프로젝트 디렉터리
  - 언어 선택: `python`
- 실행 명령:

```bash
python3 scripts/bootstrap_init.py /tmp/bootstrap-cli-project --language python
python3 -c "from pathlib import Path; paths = ['docs/harness_guide.md', 'docs/standard/architecture.md', 'docs/standard/implementation_order.md', 'docs/standard/coding_conventions_project.md', 'docs/standard/quality_gate_profile.md', 'docs/standard/testing_profile.md', 'docs/standard/commit_rule.md']; missing = [p for p in paths if not Path(p).exists()]; print('first success docs are present') if not missing else (_ for _ in ()).throw(SystemExit('missing: ' + ', '.join(missing)))"
```

- 기대 결과:
  - `scripts/bootstrap_init.py`가 최소 문서 세트를 생성한다.
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`가 함께 생성된다.
  - 첫 검증 명령이 `first success docs are present`를 출력한다.
  - `docs/harness_guide.md`가 vendored kit guide 경로를 가리키고, `AGENTS.md`가 그 문서로 수렴하며, `coding_conventions_project.md`가 선택 언어와 bootstrap 기준 문서를 함께 보여준다.

### 시나리오 2. 수동 복사 경로

- 입력 조건:
  - 빈 임시 프로젝트 디렉터리
  - `docs/project_overlay/*` template를 수동 복사
- 수동 복사 매핑:

```text
docs/project_overlay/agent_entrypoint_template.md -> AGENTS.md
docs/project_overlay/claude_entrypoint_template.md -> CLAUDE.md
docs/project_overlay/gemini_entrypoint_template.md -> GEMINI.md
docs/project_overlay/project_harness_guide_template.md -> docs/harness_guide.md
docs/project_overlay/architecture_template.md -> docs/standard/architecture.md
docs/project_overlay/implementation_order_template.md -> docs/standard/implementation_order.md
docs/project_overlay/coding_conventions_project_template.md -> docs/standard/coding_conventions_project.md
docs/project_overlay/quality_gate_profile_template.md -> docs/standard/quality_gate_profile.md
docs/project_overlay/testing_profile_template.md -> docs/standard/testing_profile.md
docs/project_overlay/commit_rule_template.md -> docs/standard/commit_rule.md
```

- 기대 결과:
  - 수동 경로도 init CLI와 같은 최소 문서 세트로 수렴한다.
  - 첫 검증 명령이 동일하게 성공한다.
  - 수동 경로에서도 non-default vendored path와 언어 bootstrap 기준 문서가 함께 확인된다.

## 확인한 최소 문서 세트

- `docs/harness_guide.md`
- `docs/standard/architecture.md`
- `docs/standard/implementation_order.md`
- `docs/standard/coding_conventions_project.md`
- `docs/standard/quality_gate_profile.md`
- `docs/standard/testing_profile.md`
- `docs/standard/commit_rule.md`

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
  harness_guide.md
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
  - 대조한 입력물: `scripts/bootstrap_init.py`, `docs/project_overlay/first_success_guide.md`
  - 실행 방법 또는 확인 방식: `python3 -m unittest tests.test_bootstrap_e2e`의 CLI 시나리오 실행
  - 결과: init CLI가 최소 문서 세트와 runtime instruction entrypoint 세트를 만들고 첫 검증 명령이 성공했으며, `docs/harness_guide.md`의 vendored guide 경로, `AGENTS.md -> docs/harness_guide.md`, `CLAUDE.md`/`GEMINI.md` -> `AGENTS.md` 연결, `coding_conventions_project.md`의 언어/bootstrap 기준 문서도 함께 확인됐다
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: generated 문서의 vendored 경로 현지화는 소비자 프로젝트에서 추가로 확인해야 한다

- 검증 항목: 수동 복사 경로가 같은 최소 문서 세트로 수렴하는지 확인
  - 대조한 입력물: `docs/project_overlay/*`, `docs/project_overlay/first_success_guide.md`
  - 실행 방법 또는 확인 방식: `python3 -m unittest tests.test_bootstrap_e2e`의 수동 복사 시나리오에서 template 복사 후 non-default vendored path를 `docs/harness_guide.md`에 반영하고, `bootstrap/language_conventions/python_coding_conventions_template.md` 발췌 내용을 `coding_conventions_project.md`에 수동 병합해 검증
  - 결과: 수동 경로도 최소 문서 세트와 runtime instruction entrypoint 세트, 첫 검증 명령 결과, vendored path 현지화, entrypoint 연결, 선택 언어와 bootstrap 기준 문서, 핵심 규칙 범주 식별 신호가 함께 확인됐다
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 실제 프로젝트 언어에 맞는 convention 현지화는 여전히 수동 결정이 필요하다

- 검증 항목: first success 가이드의 검증 명령과 expected success 상태 일치 여부 확인
  - 대조한 입력물: `docs/project_overlay/first_success_guide.md`, `tests/test_bootstrap_e2e.py`
  - 실행 방법 또는 확인 방식: 가이드의 검증 명령을 테스트 상수와 동일한 내용으로 실행하고, 같은 테스트에서 vendored guide 경로, `AGENTS.md -> docs/harness_guide.md`, `CLAUDE.md`/`GEMINI.md` -> `AGENTS.md`, `docs/standard/*` project 문서 링크, 선택 언어, bootstrap 기준 문서, 핵심 규칙 범주, profile 문서 비어 있지 않음, quality gate/commit rule의 미해결 decision marker 존재를 함께 확인
  - 결과: 가이드의 첫 검증 명령과 실제 smoke test가 같은 성공 신호를 사용하고, 가이드가 말하는 핵심 first-success content signal과 runtime entrypoint 연결도 smoke test 범위 안에 포함됐다
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 현재 검증 명령 자체는 파일 존재 여부 중심이고, 추가 content signal 확인은 테스트 레이어에서 보강한다

## 실행 명령

```bash
python3 -m unittest tests.test_bootstrap_e2e
```

## 결과 요약

- 새 프로젝트 first success 경로는 init CLI와 수동 복사 양쪽 모두에서 재현 가능하다.
- 최소 문서 세트, runtime instruction entrypoint 세트, 첫 검증 명령은 실제 smoke test로 뒷받침된다.

## 남은 리스크

- vendored `harness-kit` 경로 현지화는 아직 소비자 프로젝트의 수동 확인 대상이다.
- 현재 end-to-end 검증은 greenfield 기준이다. brownfield adopt 검증은 별도 이슈 범위다.
- smoke test는 first-success 수준까지만 본다. 프로젝트별 세부 결정 완결성은 이후 overlay validator 범위에서 더 확인해야 한다.
