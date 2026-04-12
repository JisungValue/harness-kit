# Drift Response Guide

`Harness Doc Guard` CI가 실패했을 때 maintainer가 우선 확인할 순서를 정의한다.

## 1) 경로 정합성 실패

- 우선 비교 문서
  - `README.md`의 `최소 프로젝트 문서 세트`
  - `docs/project_overlay/README.md`의 `필수 문서`
  - `docs/project_overlay/project_entrypoint_template.md`
- 기준
  - 세 문서의 `docs/standard/*` 문서 목록은 동일해야 한다.
  - `docs/harness_guide.md` core guide에 구식 경로(`프로젝트 testing_profile.md`)가 있으면 수정한다.

## 2) harness.log 필드 실패

- 2026-04-03 이후 신규 항목은 `변경`, `이유`, `audit`, `audit-summary`를 모두 포함해야 한다.
- `audit`는 `changed-parts + whole-harness`를 모두 기록해야 한다.
- `audit-summary`는 계획형이 아니라 완료형 판정과 근거를 남긴다.

## 3) 수정 우선순위

- 먼저 기준 문서(`README.md`, `docs/kit_maintenance/audit_policy.md`)를 확인한다.
- 다음으로 파생 문서(`docs/project_overlay/README.md`, 템플릿, `harness.log`)를 기준에 맞춘다.
- 마지막으로 CI를 재실행해 재현 가능하게 통과 여부를 확인한다.
