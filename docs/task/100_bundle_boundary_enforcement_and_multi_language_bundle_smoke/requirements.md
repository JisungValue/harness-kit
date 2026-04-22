# Requirements

## 기능 요구사항

- downstream bundle을 계산하는 generator와 validator는 boundary 문서가 정의한 include/exclude 책임 경계와 모순되지 않아야 한다.
- maintainer-only path가 include path와 겹치는 상황이 생겨도 downstream bundle에는 포함되지 않도록 우선순위를 명시적으로 처리해야 한다.
- downstream bundle smoke는 canonical bundle만으로 greenfield bootstrap surface를 `python`, `java`, `kotlin` 언어 프로필에서 재현 가능한지 확인해야 한다.
- downstream bundle smoke 관련 maintainer 문서는 실제 smoke가 다루는 helper, validator, migration 시나리오와 언어 범위를 설명해야 한다.
- doc guard 또는 focused test는 boundary 문서와 generator 동작, 그리고 project-facing support claim과 smoke coverage 사이의 핵심 drift를 다시 감지할 수 있어야 한다.

## 비기능 요구사항 또는 품질 요구사항

- bundle manifest와 generated README는 deterministic하게 유지돼야 한다.
- 기존 Python greenfield/brownfield bundle smoke 흐름은 회귀 없이 유지돼야 한다.
- 변경은 현재 shipped surface를 크게 재설계하지 않고, release blocker를 줄이는 최소 수정이어야 한다.

## 입력/출력

- 입력:
  - `maintainer/docs/downstream_bundle_boundary.md`
  - `maintainer/docs/downstream_bundle_smoke_validation.md`
  - `scripts/generate_downstream_bundle.py`
  - `scripts/validate_downstream_bundle.py`
  - `scripts/check_harness_docs.py`
  - `tests/test_downstream_bundle_smoke.py`
  - 관련 bundle validation/generation 테스트
- 출력:
  - 정렬된 boundary/generator/smoke maintainer 문서
  - Java/Kotlin greenfield bundle smoke coverage 또는 support boundary 축소 근거
  - drift 재발 방지용 focused test/doc guard 보강

## 제약사항

- downstream bundle은 maintainer-only 자산을 여전히 포함하면 안 된다.
- Java/Kotlin coverage는 bootstrap CLI와 first-success/overlay validator surface 검증 수준이면 충분하며 full language-specific e2e까지 확장하지 않는다.
- downstream 프로젝트 로컬에서 생성되는 `docs/project_entrypoint.md`, `docs/decisions/README.md`는 bundle 직접 포함 대상이 아니라 bootstrap/generated surface라는 현재 계약을 유지한다.

## 예외 상황

- Java/Kotlin smoke를 추가했을 때 bundle consumer path나 coding convention template reference가 언어별로 다르면 언어별 expectation을 별도로 검증해야 한다.
- boundary 문서의 exclusion rule을 실제 enforcement로 끌어올리면 synthetic overlap 상황을 별도 테스트로 고정해야 한다.
- 문서 설명과 테스트 범위를 모두 바꾸지 않고 한쪽만 바꾸면 다시 support claim drift가 생긴다.

## 성공 기준

- boundary 문서 설명과 generator/validator 동작이 include/exclude 책임 경계에서 더 이상 모순되지 않는다.
- downstream bundle smoke가 Java/Kotlin greenfield bootstrap surface까지 확인하거나, project-facing docs가 그보다 좁은 support boundary로 명시적으로 조정된다.
- `maintainer/docs/downstream_bundle_smoke_validation.md`가 실제 tested helper/migration/support surface를 설명한다.
- focused test와 doc guard가 새 계약을 고정하고 관련 검증이 통과한다.
