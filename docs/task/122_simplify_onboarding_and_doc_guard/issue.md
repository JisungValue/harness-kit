# Issue

## 배경

- 현재 harness-kit는 runtime contract 자체보다 onboarding 문서층, example 노출, maintainer용 doc guard 결합도가 무겁게 느껴진다.
- 특히 quickstart 외에도 first success, local diagnostics, README가 같은 시작 흐름을 반복하고, doc guard가 예시 문서와 표현 문구까지 강하게 결합해 유지 비용을 높인다.

## 요청사항

- `bootstrap/docs/quickstart.md`를 canonical 시작 문서로 더 분명히 고정한다.
- `README.md`, `docs/project_overlay/README.md`, `first_success_guide.md`, `local_diagnostics_and_dry_run.md`의 온보딩 중복을 완화한다.
- `scripts/check_harness_docs.py`에서 example/phrase-level 결합을 줄이고 구조 중심 검증으로 완화한다.
- examples는 기본 소비 경로보다 reference/advanced 위치로 조정한다.

## 비범위

- phase runtime contract 또는 self-healing/stale invalidation 규칙 삭제
- 핵심 validator 제거
- downstream bundle 경계 재설계

## 승인 또는 제약 조건

- quickstart를 기본 진입점으로 두되, 상세 reference 문서는 유지한다.
- 경량화는 구조 유지와 운영 부담 완화에 집중하고, 기존 핵심 runtime contract는 약화하지 않는다.
