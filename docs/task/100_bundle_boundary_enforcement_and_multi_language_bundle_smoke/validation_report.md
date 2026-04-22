# Validation Report

## 실행한 검증

- 검증 항목: bundle boundary include/exclude semantics 정합성 확인
  - 대조한 입력물: `maintainer/docs/downstream_bundle_boundary.md`, `scripts/generate_downstream_bundle.py`, `scripts/validate_downstream_bundle.py`
  - 실행 방법 또는 확인 방식: boundary 문서의 include path와 maintainer-only exclusion 우선 규칙이 generator, manifest, validator에 같은 의미로 반영됐는지 코드와 focused test를 함께 검토
  - 결과: generator가 include 후보에 exclusion 우선순위를 적용하고, manifest/validator가 `excluded_patterns`까지 같은 계약으로 검증하도록 정렬됐다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 향후 더 복잡한 exclusion glob이 추가되면 `Path.match()` 해석이 기대와 같은지 다시 확인이 필요하다.

- 검증 항목: downstream bundle generation/validation focused test
  - 대조한 입력물: `tests/test_generate_downstream_bundle.py`, `tests/test_validate_downstream_bundle.py`
  - 실행 방법 또는 확인 방식: `python3 -m unittest tests.test_generate_downstream_bundle tests.test_validate_downstream_bundle`
  - 결과: bundle manifest의 `excluded_patterns`, exclusion precedence, generated README/manifest drift, boundary 밖 path 유입 검증을 포함한 focused test가 통과했다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 없음

- 검증 항목: multi-language downstream bundle smoke
  - 대조한 입력물: `maintainer/docs/downstream_bundle_smoke_validation.md`, `tests/test_downstream_bundle_smoke.py`, `scripts/bootstrap_init.py`
  - 실행 방법 또는 확인 방식: `python3 -m unittest tests.test_downstream_bundle_smoke`
  - 결과: canonical bundle 기준 greenfield `python`/`java`/`kotlin` bootstrap + first-success/overlay validation, brownfield dry-run, create-only safe write, legacy entrypoint migration 시나리오가 통과했다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: Java/Kotlin smoke는 여전히 Python runtime 위에서 bundle script를 실행하는 수준이므로, 언어별 깊은 ecosystem integration까지 보장하지는 않는다.

- 검증 항목: maintainer doc guard 및 canonical bundle validation
  - 대조한 입력물: `scripts/check_harness_docs.py`, `maintainer/docs/downstream_bundle_smoke_validation.md`, generated `dist/harness-kit-project-bundle/`
  - 실행 방법 또는 확인 방식: `python3 scripts/check_harness_docs.py`, `python3 scripts/generate_downstream_bundle.py --force`, `python3 scripts/validate_downstream_bundle.py`
  - 결과: doc guard가 multi-language smoke/legacy migration 설명을 포함한 current contract를 통과했고, canonical generated bundle validation도 통과했다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 없음

- 검증 항목: changed-parts / whole-harness subagent audit
  - 대조한 입력물: 변경 파일 전체, task workspace 산출물, focused test 결과
  - 실행 방법 또는 확인 방식: 분리된 subagent changed-parts audit 1회, whole-harness audit 2회 수행
  - 결과: changed-parts는 바로 `APPROVE`였고, whole-harness는 처음에 지원 언어 source-of-truth 분산을 지적해 `NEEDS_CHANGES`가 나왔다. smoke test/doc guard가 `bootstrap_init.py`의 `LANGUAGE_BOOTSTRAP_PATHS`를 직접 참조하도록 보강한 뒤 재감사에서 `APPROVE`가 나왔다.
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: maintainer 문서의 명령 예시는 여전히 사람이 갱신해야 하지만, 현재는 doc guard와 smoke test가 핵심 누락을 다시 잡는 구조다.

## 실행하지 못한 검증

- Java/Kotlin consumer project의 framework-specific build tool 또는 runtime ecosystem integration까지 포함한 deeper end-to-end 검증은 미실행

## 결과 요약

- downstream bundle boundary 문서, generator/validator semantics, multi-language greenfield smoke coverage, maintainer smoke 문서가 같은 계약으로 정렬됐다.

## Phase 5에서 반영할 related decisions/

- 해당 없음. 이번 작업은 downstream project-local decision record가 아니라 `harness-kit` core bundle boundary와 maintainer validation 흐름 정합화 범위다.

## 남은 리스크

- support claim과 smoke coverage 정렬은 개선됐지만, Java/Kotlin 경로는 여전히 bootstrap/validator 수준 confidence에 머문다.

## 후속 조치 필요 사항

- 필요하면 후속 이슈에서 Java/Kotlin 관련 deeper integration signal 또는 broader greenfield confidence path를 별도로 강화한다.
