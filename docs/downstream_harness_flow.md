# Downstream Harness Flow

이 문서는 `harness-kit`를 bootstrap하거나 vendoring한 뒤, downstream 프로젝트 안에서 하네스가 어떤 순서와 규칙으로 동작하는지 설명한다.

## 언제 읽는가

- `harness-kit`를 새 프로젝트에 bootstrap하려 할 때
- 기존 프로젝트에 brownfield adoption을 적용하려 할 때
- downstream 프로젝트에서 task가 어떤 Phase 순서와 게이트로 진행되는지 한눈에 이해하고 싶을 때

## 하네스 도입 흐름

```mermaid
flowchart TD
    A[downstream project 시작] --> B{새 프로젝트인가?}
    B -->|Yes| C[bootstrap_init.py]
    B -->|No| D[adopt_dry_run.py]

    C --> E[first-success validator]
    D --> F[impact 분류 C0-C4]
    F --> G{safe write로 충분한가?}
    G -->|Yes| H[adopt_safe_write.py]
    G -->|No| I[manual diff review]
    H --> J[validator 재검증]
    I --> J
    E --> K[task 시작]
    J --> K

    K --> L[Phase 1]
    L --> M[Phase 2]
    M --> N[Phase 3]
    N --> O[Phase 4]
    O --> P[Phase 5]
```

- 이 흐름은 downstream 프로젝트에서 하네스를 새로 bootstrap하거나, 기존 프로젝트에 brownfield adoption을 적용할 때의 도입 흐름이다.
- greenfield는 bootstrap으로 최소 문서 세트를 만들고 validator를 통과한 뒤 task를 시작한다.
- brownfield는 먼저 현재 상태를 읽고, impact 분류와 safe write 또는 manual review를 거친 뒤 validator를 다시 통과하고 task를 시작한다.
- 실제 task 운영 흐름은 아래 `Phase 전체 흐름`과 `Phase별 진행 흐름`이 설명한다.

## Bootstrap 이후 Downstream 상태

- 이 저장소는 bootstrap 전 source repo이고, 실제로 동작하는 하네스는 downstream 프로젝트 안에서 맞물린다.
- bootstrap 또는 vendoring이 끝나면 downstream 프로젝트 안에서 `AGENTS.md`, `docs/project_entrypoint.md`, `docs/standard/*`, `docs/decisions/README.md`, `vendor/harness-kit/docs/harness_guide.md`를 함께 읽는 구조가 된다.
- 자세한 bootstrap/adoption 절차는 `docs/quickstart.md`, `docs/project_overlay/first_success_guide.md`, `docs/project_overlay/adopt_dry_run.md`를 기준으로 본다.

## 프로젝트 진입점은 무엇을 하나

```mermaid
flowchart TD
    A[AGENTS.md] --> B[docs/project_entrypoint.md]
    B --> C[공통 규칙<br/>vendor/harness-kit/docs/harness_guide.md]
    B --> D[프로젝트 전용 규칙<br/>docs/standard/*]
    B --> E[프로젝트 결정<br/>docs/decisions/README.md]
```

- downstream에서 실제 진입점 역할을 하는 문서는 `docs/project_entrypoint.md`다.
- 이 문서가 vendored core guide와 프로젝트 전용 문서를 함께 묶어서, 지금 프로젝트에서 무엇을 읽고 어떤 규칙으로 움직여야 하는지 정해 준다.
- 중요한 정책, 예외, 책임 배치 결정이 있으면 `docs/decisions/README.md`와 개별 decision 문서까지 함께 읽는다.

## Phase 전체 흐름

```mermaid
flowchart LR
    A[Phase 1<br/>Requirement And Planning] --> B[Phase 2<br/>TDD Implementation]
    B --> C[Phase 3<br/>Integration]
    C --> D[Phase 4<br/>Validation]
    D --> E[Phase 5<br/>Documentation]
```

- 기본 순서는 `1 -> 2 -> 3 -> 4 -> 5`다.
- 각 Phase는 `implementation -> audit -> 사용자 승인 -> 다음 Phase` 순서를 따른다.
- validation에서 더 이른 산출물과 모순이 발견되면 원인 Phase까지 되돌아가고, 그렇지 않으면 영향이 걸린 가장 이른 Phase부터만 다시 수행한다.

## Phase별 진행 흐름

### Phase 1. Requirement And Planning

```mermaid
flowchart LR
    A[issue.md] --> B[requirements.md]
    B --> C[requirements 감사]
    C --> D[plan.md]
    D --> E[plan 감사]
    E --> F[issue 대비 plan 누락 감사]
    F --> G[user approval]
```

- 입력은 `issue.md`다.
- 출력은 `requirements.md`, `plan.md`다.
- 실제 권장 순서는 `issue.md` 분석 -> `requirements.md` 작성 -> requirements 감사 -> `plan.md` 작성 -> plan 감사 -> issue 대비 plan 누락 감사다.
- 즉, 내부 감사 세 가지를 한 번에 몰아서 하는 것이 아니라, 각 산출물이 닫히는 시점마다 순서대로 수행한다.
- 세 내부 감사가 모두 승인 가능 상태가 된 뒤에만 사용자 승인으로 간다.

### Phase 2. TDD Implementation

```mermaid
flowchart LR
    A[requirements.md + plan.md] --> B[선택 레이어 순서 결정]
    B --> C[현재 레이어 선택]
    C --> D[테스트 작성]
    D --> E[구현]
    E --> F[현재 레이어 감사]
    F --> G{남은 선택 레이어가 있는가?}
    G -->|Yes| C
    G -->|No| H[Phase 2 전체 감사]
    H --> I[user approval]
```

- 프로젝트별 실제 레이어 순서와 세분화 기준은 `docs/standard/implementation_order.md`가 정한다.
- Phase 2는 기능 전체를 한 번에 구현하는 것이 아니라, 현재 task에 필요한 레이어만 선택해 순서대로 진행한다.
- 각 선택 레이어는 `테스트 작성 -> 구현 -> 현재 레이어 감사` 순서를 따른다.
- 한 레이어 감사가 끝나면 다음 선택 레이어로 넘어가 같은 TDD 루프를 반복한다.
- 모든 선택 레이어가 끝난 뒤에야 `Phase 2 전체 감사`를 수행하고, 그 결과가 승인 가능 상태여야 사용자 승인 게이트로 간다.

### Phase 3. Integration

```mermaid
flowchart LR
    A[Phase 2 결과물] --> B[연결 책임 식별]
    B --> C[통합 검증]
    C --> D[happy path / failure path 확인]
    D --> E[감사]
    E --> F[user approval]
```

- 단위 테스트로 다루기 어려운 연결 책임, 조립 책임, 핵심 happy path와 failure path를 검증한다.
- 전체 앱 end-to-end만이 아니라 구현체 단위 통합 테스트도 포함될 수 있다.

### Phase 4. Validation

```mermaid
flowchart LR
    A[전체 구현 결과] --> B[자동 검증]
    B --> C[수동 검증]
    C --> D[validation_report.md]
    D --> E{earlier artifact contradiction?}
    E -->|Yes| F[원인 Phase부터 재수행]
    E -->|No| G[감사]
    F --> G
    G --> H[user approval]
```

- `validation_report.md`가 핵심 출력이다.
- `validation_report.md`만 보완하면 기본적으로 Phase 4부터 다시 수행하지만, 더 이른 산출물과 모순되면 원인 Phase까지 되돌아간다.

### Phase 5. Documentation

```mermaid
flowchart LR
    A[구현 + 검증 결과] --> B[관련 문서 반영]
    B --> C[related decisions 반영]
    C --> D[작업 로그 정리]
    D --> E[감사]
    E --> F[user approval]
```

- 구조적 결정, 사용법 변경, related decision을 실제 문서에 반영한다.
- 작업 로그는 이후 세션에서도 결과와 판단 근거를 복원할 수 있게 남긴다.
