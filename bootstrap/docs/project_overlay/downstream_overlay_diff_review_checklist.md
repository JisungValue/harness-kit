# Downstream Overlay Diff Review Checklist

이 문서는 downstream 프로젝트가 새 `harness-kit` bundle과 현재 project-local overlay 사이의 diff를 사람 기준으로 검토할 때 확인할 항목을 정리한다.

## 목적

- repo 전체가 아니라 downstream bundle 경계 안의 overlay 관련 자산만 기준으로 review하게 한다.
- `harness_upgrade_impact_policy.md`의 category 판단을 실제 diff review 질문으로 연결한다.
- 자동 merge가 없는 상태에서도 어떤 차이를 먼저 보고, 어떤 차이는 수동 개입 신호로 볼지 일관되게 유지한다.

## 언제 보는가

- `downstream_harness_upgrade_guide.md`의 영향도 분류 결과가 `C3` 또는 `C4`일 때
- `adopt_dry_run.py` 결과에서 `differing files`나 `conflict candidates`가 핵심 문서에 걸렸을 때
- safe write 전에 실제 문서 차이를 사람이 읽고 반영 순서를 정해야 할 때

## 먼저 고정할 입력

review를 시작하기 전에 아래를 먼저 고정한다.

- 현재 프로젝트가 따르는 `harness-kit` 기준 tag, commit, bundle
- 새로 반영하려는 tag, commit, bundle
- downstream bundle 경계 안에서 실제로 비교할 경로 목록
- 이번 update의 impact category 초안

이 네 가지가 불명확하면 diff review를 진행하지 말고 먼저 provenance와 bundle boundary부터 정리한다.

여기서 bundle boundary는 현재 프로젝트가 실제로 소비하는 project-facing 문서, overlay template, bootstrap 자산, shipped script, shipped example 문서만 뜻한다. maintainer release/audit 문서, maintainer change log, test-only 자산, maintainer workflow 같은 자산은 diff review 기본 대상에서 제외한다.

## 기본 review 순서

1. bundle 경계 안의 변경만 비교 대상으로 남긴다.
2. 새 문서 추가인지, 기존 필수 문서 변경인지, validator 또는 phase 규칙 변경인지 먼저 나눈다.
3. 필수 문서 세트와 entrypoint chain 관련 변경을 먼저 읽는다.
4. 그다음 project decision, phase gate, quality/testing responsibility 이동을 본다.
5. 마지막에 bootstrap template, safe write, dry-run 도구 출력과 연결되는 follow-up을 정리한다.

## Checklist

### 1. 필수 문서 세트 변화

- 새 bundle이 downstream 필수 문서 세트를 늘리거나 줄였는가?
- 현재 프로젝트에 없는 새 필수 문서가 생겼는가?
- 기존 필수 문서가 권장 문서로 내려갔거나, 반대로 권장 문서가 필수로 올라갔는가?
- 문서 경로 rename, canonical path 변경, legacy migration이 필요한가?

### 2. Runtime / Entrypoint 체인 변화

- `AGENTS.md -> docs/entrypoint.md -> docs/process/harness_guide.md -> docs/project/standards/*` 체인이 바뀌었는가?
- 새 필수 재참조 문서가 추가됐는가?
- 현재 프로젝트의 runtime entrypoint가 새 traversal contract를 그대로 만족하는가?
- legacy local entrypoint를 계속 둘 수 있는가, 아니면 migration이 필요한가?

### 3. 프로젝트 결정 필요 항목 변화

- `docs/project/decisions/README.md`에서 새로 읽어야 하는 decision 종류가 생겼는가?
- 기존에는 project-local 결정이 필요 없던 항목이 새 bundle에서 team decision을 요구하는가?
- 반대로 이제 core rule로 승격돼 project-local decision 부담이 줄어든 항목이 있는가?

### 4. Phase Gate 변화

- phase 순서 자체가 바뀌었는가?
- 사용자 승인 게이트 위치나 재수행 규칙이 더 엄격해졌는가?
- 이전 Phase로 되돌아가야 하는 조건이 바뀌었는가?
- 현재 프로젝트 task template, 운영 메모, 진행 기준과 충돌하는가?

### 5. Validator / Quality / Testing 책임 이동

- `validate_overlay_decisions.py`의 readiness 기대치가 바뀌었는가?
- `validate_overlay_consistency.py`가 새로 요구하는 경로, 참조, traversal contract가 생겼는가?
- `quality_gate_profile.md` 또는 `testing_profile.md`가 새 bundle 기준에서 더 많은 책임을 요구하는가?
- 기존 프로젝트가 새 validator 기준을 그대로 두고는 통과하지 못할 가능성이 있는가?

### 6. Bootstrap / Template 영향

- bootstrap template 변경이 `docs/project/standards/coding_conventions_project.md` 같은 localized 문서에 영향을 주는가?
- 새 baseline wording이 아니라 실제 팀 규칙 변경이 필요한가?
- missing create로 해결되는 additive change인가, 아니면 localized 기존 문서 수동 병합이 필요한가?

### 7. Dry-Run / Safe Write 연결

- 이번 변경은 `missing files` create로 충분한가?
- `existing but unchanged targets` refresh만으로 충분한가?
- `differing files`가 핵심 문서라서 safe write보다 수동 review가 먼저인가?
- `conflict candidates`가 path shape 문제인지, unrelated local rewrite인지 구분됐는가?
- `--force-overwrite`가 정말 필요한가, 아니면 별도 migration task가 맞는가?

### 8. 수동 개입이 필요한 신호

아래 중 하나면 review 결과를 `manual intervention required`로 남긴다.

- 필수 문서 구조가 바뀌었다.
- phase gate 또는 validator 기준이 강화됐다.
- localized `docs/project/standards/*`, `docs/entrypoint.md`, `AGENTS.md`가 새 baseline과 실질 충돌한다.
- breaking 가능성이 있는 `C4` 수준으로 판단된다.
- safe write로 덮어쓰면 project-local rule이 사라질 수 있다.

## Review 결과 정리 방식

review가 끝나면 최소한 아래를 정리한다.

- 이번 diff의 impact category 확정값
- safe write로 반영 가능한 파일 목록
- 수동 검토 또는 별도 migration이 필요한 파일 목록
- validator 재검증에 꼭 포함할 명령
- 남은 리스크와 follow-up task

task workspace를 함께 운영하면 이 판단을 `implementation_notes.md`, `validation_report.md`에 남긴다.

## 현재 범위 밖

- 프로젝트 맞춤 변경의 정답 자동 판정
- semantic merge 규칙
- maintainer release note 작성 절차
- framework별 migration cookbook

## 함께 볼 문서

- `bootstrap/docs/project_overlay/downstream_harness_upgrade_guide.md`
- `bootstrap/docs/project_overlay/harness_upgrade_impact_policy.md`
- `bootstrap/docs/project_overlay/adopt_dry_run.md`
- `bootstrap/docs/project_overlay/adopt_safe_write.md`
