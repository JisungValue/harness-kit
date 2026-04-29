# Downstream Harness Upgrade Guide

이 문서는 downstream 프로젝트가 새 `harness-kit` bundle 변경을 어떤 순서와 기준으로 검토하고 반영할지 설명한다.

## 목적

- repo 전체가 아니라 downstream bundle 경계 안의 변경만 기준으로 upgrade 작업을 수행하게 한다.
- `adopt_dry_run.py`, `adopt_safe_write.py`, validator, impact policy를 한 upgrade 흐름으로 연결한다.
- 자동 merge가 없는 상태에서도 소비자 프로젝트가 안전하게 update 작업 단위를 만들 수 있게 한다.

## 언제 보는가

- vendored `harness-kit`를 새 tag 또는 새 commit으로 올리려 할 때
- release bundle tarball, zip, directory artifact를 받아 현재 프로젝트에 반영하려 할 때
- 지금 프로젝트 overlay가 새 bundle과 얼마나 다른지 먼저 읽고 싶을 때

## 핵심 원칙

- upgrade 기준은 저장소 전체가 아니라 downstream bundle 경계다.
- 먼저 read-only diff를 보고, 그다음 impact를 분류하고, 마지막에 제한적 write를 검토한다.
- `differing files`와 `conflict candidates`는 기본적으로 수동 검토 대상이다.
- breaking 가능성이 있는 update는 별도 upgrade 작업 단위로 분리한다.

## 1. 현재 참조 기준 확인

먼저 지금 프로젝트가 어떤 `harness-kit` 기준을 따라가고 있는지 확인한다.

- vendored copy를 쓰면 현재 `vendor/harness-kit/` 또는 팀이 정한 실제 vendored 경로의 tag, commit, branch를 확인한다.
- harness doc guard workflow를 복사해 썼다면, 그 workflow 안에 적힌 `@<pin-tag-or-sha>`가 현재 고정 기준이다.
- release bundle을 수동 복사해 쓰는 프로젝트라면, 마지막 upgrade 작업 기록이나 해당 복사본이 들어온 commit을 현재 기준으로 본다.
- 현재 기준을 정확히 복원할 수 없으면 provenance가 불명확한 상태로 보고 conservative하게 review-required update로 다룬다.

## 2. 새 기준 입력 확인

현재 프로젝트가 어떤 방식으로 `harness-kit`를 받아오는지에 따라 먼저 보는 입력이 다르다.

- source repo vendored copy를 tag 또는 commit 기준으로 올리는 경우
  - 새 source tree 안에서 downstream bundle 경계에 포함되는 문서, template, script 경로만 비교 대상으로 남긴다.
  - 이 경우 generated `README.md`, `bundle_manifest.json`은 없을 수 있으므로 source repo tree를 canonical input으로 본다.
- release bundle tarball, zip, directory artifact를 받아 반영하는 경우
  - release note 또는 배포 안내
  - bundle entry `README.md`
  - `bundle_manifest.json`
  - downstream bundle에 실제 포함되는 경로 범위

이 단계에서는 maintainer 전용 문서, 테스트, release script까지 같이 비교하지 않는다. 기본 비교 대상은 현재 프로젝트가 실제로 소비하는 project-facing 문서, overlay template, bootstrap 자산, shipped script, shipped example 문서만 남기고, maintainer release/audit 문서, maintainer change log, test-only 자산, maintainer workflow 같은 자산은 제외한다.

## 3. 영향도 먼저 분류

반영 전에 `bootstrap/docs/project_overlay/harness_upgrade_impact_policy.md`로 이번 변경을 먼저 분류한다.

- `C0`: 설명 보강 위주면 다음 sync 때 반영해도 된다.
- `C1`: 새 권장 문서나 참고 경로 추가면 다음 정리 시점 반영 후보로 둔다.
- `C2`: additive baseline update면 제한적 safe write 후보로 본다.
- `C3`: phase 규칙, validator, 필수 문서 구조 변화면 사람 중심 review가 필요하다.
- `C4`: overlay contract 자체가 크게 바뀌면 별도 migration 작업으로 분리한다.

분류가 애매하면 더 높은 category로 본다.

## 4. Read-Only 비교부터 실행

현재 프로젝트 루트에서 먼저 dry-run을 실행한다.

아래 명령은 `vendor/harness-kit/` 기준 예시다. 다른 vendored 경로를 쓰면 그 부분을 같은 실제 경로로 바꿔 실행한다.

```bash
python3 vendor/harness-kit/scripts/adopt_dry_run.py . --language python
python3 scripts/validate_overlay_consistency.py . --mode incremental
```

출력은 아래처럼 읽는다.

- `missing files`: 새 baseline에서 안전하게 만들 수 있는 후보
- `existing but unchanged targets`: 현재 baseline과 같은 상태
- `differing files`: 프로젝트 현지화 결과일 가능성이 큰 수동 검토 대상
- `conflict candidates`: overwrite보다 수동 판단이 먼저 필요한 대상
- `legacy entrypoint migration candidates`: old local entrypoint를 새 canonical 경로로 옮겨야 하는 상태

## 5. 반영 전략 선택

### C0 또는 C1

- 당장 upgrade 작업으로 묶지 않아도 된다.
- 다음 bundle sync 또는 문서 정리 시점에 반영 후보로 기록한다.

### C2

- `missing files` 위주면 `adopt_safe_write.py` 기본 동작을 먼저 검토한다.
- exact-match target refresh만 필요하면 `--update-unchanged`를 좁게 사용한다.
- 특정 regular file overwrite가 꼭 필요할 때만 `--force-overwrite <path>`를 명시한다.

### C3 또는 C4

- 별도 upgrade task를 만든다.
- 먼저 수동 review로 반영 순서를 정한다.
- `bootstrap/docs/project_overlay/downstream_overlay_diff_review_checklist.md`를 함께 보며 diff 검토 결과를 남긴다.
- safe write는 보조 수단으로만 쓰고, validator 재검증을 함께 계획한다.

## 6. 수동 개입이 필요한 경우

아래 중 하나면 자동 반영보다 수동 개입이 먼저다.

- `differing files`가 핵심 문서에 걸려 있다.
- `conflict candidates`가 나온다.
- 필수 문서 세트, phase gate, validator 기준이 바뀌었다.
- localized `docs/entrypoint.md`, `docs/project/standards/*`, `AGENTS.md`가 현재 팀 규칙과 강하게 결합돼 있다.
- 새 bundle이 기존 overlay를 그대로 두고는 validator를 통과시키지 못한다.

이 경우에는 파일을 한 번에 전면 overwrite하지 말고, 문서별로 현재 local rule과 새 baseline을 비교해 반영한다.

## 7. 반영 후 검증

반영이 끝나면 최소한 아래를 다시 확인한다.

아래 명령도 `vendor/harness-kit/` 기준 예시다. 다른 vendored 경로를 쓰면 같은 실제 경로로 바꾼다.

```bash
python3 scripts/validate_overlay_decisions.py . --readiness first-success
python3 scripts/validate_overlay_consistency.py .
```

phase2 readiness까지 끌어올려야 하는 프로젝트면 해당 readiness 기준으로도 다시 확인한다.

## 8. 작업 결과 기록

upgrade 작업을 끝내면 아래를 남긴다.

- 어떤 tag, commit, bundle 기준으로 올렸는지
- impact category를 어떻게 판단했는지
- 어떤 파일을 safe write로 반영했고 어떤 파일을 수동 검토했는지
- validator 결과와 남은 follow-up이 무엇인지

현재 프로젝트가 task workspace를 함께 운영하면 이 사실을 `implementation_notes.md`, `validation_report.md`에 남겨 다음 세션에서도 같은 기준으로 이어가게 한다.

## 현재 범위 밖

- automatic merge 기반 update
- framework별 semantic migration 자동화
- repo 전체 diff를 upgrade 기준으로 삼는 흐름
- maintainer release 절차 자체 설명

## 함께 볼 문서

- `bootstrap/docs/project_overlay/downstream_overlay_diff_review_checklist.md`
- `bootstrap/docs/project_overlay/harness_upgrade_impact_policy.md`
- `bootstrap/docs/project_overlay/adopt_dry_run.md`
- `bootstrap/docs/project_overlay/adopt_safe_write.md`
- `bootstrap/docs/project_overlay/local_diagnostics_and_dry_run.md`
