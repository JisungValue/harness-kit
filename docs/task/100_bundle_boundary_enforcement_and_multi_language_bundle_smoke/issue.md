# Issue

## 배경

- strict audit에서 downstream bundle boundary 문서, generator 실제 동작, bundle smoke coverage 사이에 drift가 남아 있다.
- `maintainer/docs/downstream_bundle_boundary.md`는 maintainer-only exclusion을 강한 경계 규칙처럼 설명하지만 `scripts/generate_downstream_bundle.py`는 include pattern만으로 bundle 파일을 계산한다.
- downstream bundle smoke는 현재 Python flow만 확인하고 있어, project-facing docs가 지원한다고 설명하는 Java/Kotlin bootstrap surface와 tested surface가 어긋난다.
- `maintainer/docs/downstream_bundle_smoke_validation.md`도 실제 smoke가 다루는 helper/migration/support surface를 충분히 설명하지 못할 수 있다.

## 요청사항

- bundle boundary 문서와 generator/validator의 include-exclude 책임 경계를 더 정확히 맞춘다.
- section 3 maintainer-only exclusion을 실제 generator 동작에도 반영할지, 아니면 문서를 현재 동작에 맞게 낮출지 결정해 정렬한다.
- downstream bundle smoke coverage를 Java/Kotlin greenfield bootstrap surface까지 확장하거나, 그렇지 않다면 support boundary를 더 좁게 명시한다.
- maintainer smoke validation 문서가 current shipped migration/helper/support 범위를 빠뜨리지 않게 보강한다.
- 같은 drift가 다시 나면 doc guard와 테스트가 다시 잡도록 재발 방지 장치를 추가한다.

## 비범위

- 모든 언어의 full e2e integration test 추가
- archive packaging 전체 재설계
- brownfield semantic merge/update 자동화

## 승인 또는 제약 조건

- 현재 release:must-have blocker를 줄이는 방향으로, 문서만 바꾸는 봉합보다 실제 동작과 검증을 맞추는 최소 수정이 우선이다.
- project-facing Java/Kotlin 지원 표현을 유지하려면 bundle smoke가 그 claim과 맞는 신호를 제공해야 한다.
