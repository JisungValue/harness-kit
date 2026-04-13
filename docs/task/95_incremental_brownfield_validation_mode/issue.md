# Issue

## 배경

- 현재 brownfield/in-progress adoption에서는 `adopt_dry_run.py`와 `adopt_safe_write.py`가 일부 도움을 주지만, validator는 최소 overlay 세트가 꽤 갖춰져야 useful signal을 준다.
- strict 감사 결과상 현재 흐름은 substantial manual cleanup 이후에야 green/red 판정을 주기 때문에, 이미 진행 중인 프로젝트가 harness를 단계적으로 도입할 때 자동화 신호가 약하다.
- 특히 구조는 맞아 가지만 아직 문서 세트가 덜 갖춰진 intermediate state를 validator가 다루지 못한다.

## 요청사항

- partial adoption 상태를 위한 validation/readiness 모드를 설계한다.
- missing docs, linked entrypoints, decisions index, legacy/stale leftovers 등 intermediate state를 어떤 수준으로 classify할지 정의한다.
- project-facing docs에서 언제 incremental mode를 쓰고 언제 full consistency mode로 올라갈지 설명한다.
- downstream smoke 또는 sample validation으로 intermediate state 시나리오를 검증한다.
- default full validator와 incremental mode의 역할 경계를 정리한다.

## 비범위

- 모든 partial state를 green으로 완화하는 것
- semantic merge/update automation 전체 추가
- fully custom doc ecosystems를 자동으로 valid state로 인정하는 것

## 승인 또는 제약 조건

- full consistency validator의 엄격한 계약은 유지하고, incremental mode는 부분 도입 상태의 안전한 intermediate signal만 제공해야 한다.
- adopt dry-run과 역할이 겹치더라도, write classification이 아니라 구조적 intermediate readiness를 보여 주는 선에서 최소 구현을 우선한다.
