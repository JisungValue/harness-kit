# First Success Guide

빈 프로젝트 또는 거의 빈 프로젝트에서 `harness-kit`를 처음 붙일 때, 가장 먼저 재현해야 하는 성공 상태를 정리한 가이드다.

## 시작 전 준비물

- 프로젝트 루트가 준비되어 있어야 한다.
- `harness-kit`가 프로젝트 안에서 참조 가능한 경로에 있어야 한다.
- 아래 예시는 `vendor/harness-kit/`에 vendored 되어 있다고 가정한다.
- Python, Java, Kotlin 중 이번 프로젝트의 주 언어를 하나 먼저 정한다.
- 현재 MVP는 생성 대상 문서 경로만 검사하므로, first success를 빠르게 재현하려면 빈 디렉터리 또는 거의 빈 디렉터리에서 시작하는 편이 안전하다.

## 목표 성공 상태

first success의 최소 기준은 아래 둘이다.

- 프로젝트에 최소 문서 세트가 빠짐없이 생긴다.
- runtime instruction entrypoint 세트(`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`)가 함께 생긴다.
- 로컬 `docs/project_entrypoint.md`가 공통 kit 문서와 프로젝트 전용 문서를 함께 가리킨다.

## 최소 문서 세트

- `docs/project_entrypoint.md`
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
4. `docs/project_entrypoint.md`와 `docs/standard/coding_conventions_project.md` 안의 vendored 경로를 실제 배치 경로와 맞춘다.
5. 아래 첫 검증 명령으로 최소 문서 세트 존재 여부를 확인한다.
6. 그다음 프로젝트 결정이 필요한 항목을 `architecture.md`, `implementation_order.md`, `coding_conventions_project.md`부터 채운다.

## 가장 빠른 경로: init CLI

프로젝트 루트에서 아래처럼 실행한다.

```bash
python3 vendor/harness-kit/scripts/bootstrap_init.py . --language python
```

언어만 바꾸면 Java/Kotlin도 같은 방식으로 시작할 수 있다.

```bash
python3 vendor/harness-kit/scripts/bootstrap_init.py . --language java
python3 vendor/harness-kit/scripts/bootstrap_init.py . --language kotlin
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

```bash
python3 -c "from pathlib import Path; paths = ['docs/project_entrypoint.md', 'docs/standard/architecture.md', 'docs/standard/implementation_order.md', 'docs/standard/coding_conventions_project.md', 'docs/standard/quality_gate_profile.md', 'docs/standard/testing_profile.md', 'docs/standard/commit_rule.md']; missing = [p for p in paths if not Path(p).exists()]; print('first success docs are present') if not missing else (_ for _ in ()).throw(SystemExit('missing: ' + ', '.join(missing)))"
```

기대 결과:

- 성공이면 `first success docs are present`가 출력된다.
- 실패면 빠진 문서 경로가 `missing: ...` 형식으로 출력된다.

이 명령은 문서 존재 여부만 확인하는 가장 얕은 체크다.
runtime instruction entrypoint 연결과 unresolved placeholder readiness까지 보려면 아래 validator를 이어서 실행한다.

```bash
python3 vendor/harness-kit/scripts/validate_overlay_decisions.py . --readiness first-success
python3 vendor/harness-kit/scripts/validate_overlay_consistency.py .
```

## 첫 검증 포인트

아래 항목이 보이면 first success로 본다.

- `docs/project_entrypoint.md`가 존재한다.
- `docs/project_entrypoint.md` 제목이 project-local entrypoint 역할을 드러낸다.
- `AGENTS.md`가 `docs/project_entrypoint.md`를 우선 읽을 문서로 가리킨다.
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
- consistency checker가 entrypoint 관련으로 실패하면: `AGENTS.md -> docs/project_entrypoint.md`, `CLAUDE.md`/`GEMINI.md` -> `AGENTS.md` 연결을 먼저 확인한다.
- 문서는 맞는데 무엇부터 채워야 할지 막히면: `architecture.md`, `implementation_order.md`, `coding_conventions_project.md` 순으로 프로젝트 결정을 채운다.
- 품질 게이트와 테스트 기준이 섞여 보이면: 실행 명령은 `quality_gate_profile.md`, 테스트 범위와 환경은 `testing_profile.md`에 둔다.

## 참고 검증 자산

- 실제 end-to-end smoke validation 예시는 `docs/examples/bootstrap-first-success/validation_report.md`를 본다.
- init, validator, adopt dry-run의 로컬 진단 순서는 `docs/project_overlay/local_diagnostics_and_dry_run.md`를 본다.
- 사람이 읽는 overlay 완료 기준은 `docs/project_overlay/overlay_completion_checklist.md`를 본다.
- overlay 완료 상태 sample validation 예시는 `docs/examples/bootstrap-first-success/overlay_completion_validation_report.md`를 본다.
- first success 이후 unresolved placeholder를 점검하려면 `docs/project_overlay/unresolved_decision_validator.md`를 본다.
- 문서 간 교차 정합성을 점검하려면 `docs/project_overlay/cross_document_consistency_checker.md`를 본다.
