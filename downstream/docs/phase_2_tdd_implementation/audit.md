# Phase 2 Audit

## 목적

구현이 TDD 원칙과 승인된 범위를 지키며 진행되었는지 검토한다.

## 재참조 문서

### 필수 재참조

- `docs/process/common/audit_policy.md`
- `docs/process/common/testing_policy.md`
- `docs/process/common/test_double_policy.md`
- `docs/process/common/code_hygiene_policy.md`
- `docs/process/common/design_quality_policy.md`
- `docs/process/common/performance_policy.md`
- `docs/process/common/coding_guidelines_policy.md`
- 프로젝트 `docs/project/standards/architecture.md`
- 프로젝트 `docs/project/standards/implementation_order.md`
- 프로젝트 `docs/project/standards/coding_conventions_project.md`
- 프로젝트 `docs/project/standards/quality_gate_profile.md`

### 조건부 참조

- 없음

## Phase 체크리스트

아래 체크리스트는 감사 시작 전에 빠르게 훑는 진입용 요약이다.
세부 판정은 `감사 항목`과 `승인 불가 기준`을 따른다.

- TDD 순서가 유지되었는가
- 최소 구현 원칙과 범위 통제가 지켜졌는가
- 테스트 더블 선택이 검증 책임과 맞는가
- 선택한 레이어 명칭, 순서, 세분화가 프로젝트 `docs/project/standards/implementation_order.md`와 정합한가
- 프로젝트 문서가 없거나 모호한 상태에서 임의 순서로 진행하지 않았는가
- 프로젝트 `docs/project/standards/coding_conventions_project.md`에 정의한 convention과 충돌하지 않는가
- 현재 변경과 직접 관련 있는 언어별 convention 항목이 `coding_conventions_project.md`에 식별 가능하게 정리돼 있는가
- 현재 변경과 직접 관련 있는 언어별 금지 패턴을 실제로 위반하지 않았는가
- 프로젝트 `docs/project/standards/quality_gate_profile.md`가 현재 Phase 2까지 적용하도록 정의한 품질 게이트와 모순되거나 생략된 검증이 있는가
- 현재 변경과 직접 관련 있는 import/unused/dead code/debug 흔적이 남아 있지 않은가
- stale 상태의 레이어 감사 또는 Phase 2 전체 감사 결과를 재사용하지 않는가
- 현재 변경이 책임 분리, 추상화 수준, 응집도, 경계 분리를 악화시키지 않았는가
- 현재 변경이 시간복잡도, 메모리 사용, 중간 컬렉션, 반복 호출, 과도한 I/O를 불필요하게 악화시키지 않았는가
- 불필요한 리팩터링이나 선제 추상화가 섞이지 않았는가
- 실패 경로와 핵심 예외가 검토되었는가
- 경계 번역, 민감정보 보호, 외부 에러 차단 규칙이 지켜졌는가
- 성능 이슈나 최적화 주장이 있다면 근거와 검증 계획이 식별 가능한가

## 프로젝트 구현 순서 준수 감사

- 레이어 명칭, 구현 순서, 세분화 기준의 1차 기준은 프로젝트 `docs/project/standards/implementation_order.md`다.
- 감사자는 Phase 2 진행 순서가 프로젝트 문서와 일치하는지 먼저 확인한다.
- Core harness는 `안쪽 책임 -> 바깥쪽 책임`과 `테스트 작성 -> 구현 -> 감사` 절차 준수 여부를 확인하며, 프로젝트 상세 순서 자체를 대체하지 않는다.
- 특정 API나 기능을 이번 TASK에서 어떤 순서로 구현할지는 `plan.md`가 담당하고, 감사자는 그 task 순서가 `implementation_order.md`의 프로젝트 기본 레이어 기준과 충돌하지 않는지 본다.
- 프로젝트 문서가 없거나 현재 TASK 기준으로 모호하면, 구현 진행 정당성은 승인 가능으로 판정하지 않는다.
- 승인된 입력 또는 특정 레이어 산출물이 바뀌면 해당 레이어 이후의 감사 결과와 Phase 2 전체 감사는 stale 로 본다.
- 감사자는 최신 테스트/구현 상태를 기준으로만 승인 가능 여부를 판정한다.

## 감사 항목

- 각 선택 레이어가 `테스트 작성 -> 구현 -> 감사` 순서로 진행되었는가
- 재수행이 있었다면 가장 이른 영향 레이어부터 동일 순서가 다시 적용되었는가
- 선택한 레이어 명칭, 순서, 세분화 기준이 프로젝트 `docs/project/standards/implementation_order.md`와 충돌하지 않는가
- `implementation_order.md`가 task별 API backlog처럼 오염되지 않았는가
- API/기능 단위 실제 작업 순서가 `plan.md`에 있고, 그 계획이 프로젝트 기본 레이어 순서와 충돌하지 않는가
- 프로젝트 문서가 없거나 현재 TASK 기준으로 모호한 상태에서 임의 순서를 적용하지 않았는가
- 프로젝트 `docs/project/standards/coding_conventions_project.md`가 정의한 language/framework convention과 구현이 충돌하지 않는가
- 현재 변경과 직접 관련 있는 언어별 규칙 범주가 `coding_conventions_project.md` 또는 그가 참조하는 언어 문서에서 식별 가능한가
- 현재 변경에 직접 영향을 주는 언어별 항목이 아직 `[프로젝트 결정 필요]` 상태로 남아 있지 않은가
- 현재 변경이 프로젝트 convention 문서의 주요 금지 패턴을 사실상 새 기본값으로 만들지 않는가
- 프로젝트 `docs/project/standards/quality_gate_profile.md`가 현재 Phase 2까지 적용하도록 정의한 formatter/linter/type checker/test 게이트가 누락되었거나 생략 사유 없이 빠지지 않았는가
- 현재 변경과 직접 관련 있는 import/unused/dead code/debug 흔적이 남아 있지 않은가
- 현재 변경이 긴 함수, 긴 인수 목록, 메시지 체인, 기능 편애, 거대한 클래스 같은 구조 악취를 더 심하게 만들지 않았는가
- 추측성 일반화, 재사용 근거 없는 추상화, 범위 밖 재설계가 포함되지 않았는가
- 성능 민감 경로이거나 성능 이슈 또는 최적화 주장이 있으면 대상 경로, 근거, 검토 항목, 검증 방법 또는 후속 검증 계획이 `implementation_notes.md`에 식별 가능하게 남아 있는가
- design quality와 performance 충돌 시 `performance_policy.md` 기준의 대안, 추천안, 근거, 검증 계획, trade-off가 `implementation_notes.md`에 식별 가능하게 남아 있는가
- 테스트를 통과시키는 최소 구현이 반영되었는가
- `mock`, `stub`, `fake`가 현재 단위 테스트 책임에 맞게 선택되었는가
- 승인되지 않은 범위 확장이 없는가
- 현재 TASK와 직접 관련 없는 기존 중복 제거, 구조 정리, 선제 추상화를 함께 넣지 않았는가
- 실패 경로와 예외 케이스가 점검되었는가
- 원시 외부 에러가 core로 직접 유입되지 않는가
- 로그와 에러 메시지가 민감정보를 직접 노출하지 않는가
- 경계 바로 앞 레이어가 번역 책임을 수행하는가
- 테스트가 구현 세부사항보다 동작과 계약을 검증하는가
- 새 계약이나 구조 결정이 있으면 문서 반영 필요성이 식별되었는가

## 언어별 convention 감사 체크리스트

- 현재 프로젝트가 실제로 사용하는 언어/런타임이 `coding_conventions_project.md`에 명시되어 있는가
- bootstrap 템플릿을 복사했다면 현재 프로젝트에 적용하지 않는 언어/런타임 규칙이 정리되지 않은 채 남아 있지 않은가
- 언어별 상세 규칙을 별도 문서로 뺐다면 `coding_conventions_project.md`가 정확한 경로를 참조하는가
- 현재 변경과 직접 관련 있는 규칙 범주(naming, modeling, error handling, concurrency, collections, testing, interop 등)가 식별 가능하게 정리돼 있는가
- 현재 변경에 영향을 주는 항목이 아직 `[프로젝트 결정 필요]` 상태면, 그 상태를 암묵적 예외처럼 사용하지 않았는가
- 현재 변경이 프로젝트가 금지한 언어별 패턴을 새 기본값처럼 도입하지 않는가
- stale 상태의 레이어 감사 결과나 이전 승인 상태를 최신 구현 대신 근거로 사용하지 않는가

## Code Hygiene 감사 체크리스트

- 사용하지 않는 import가 남아 있지 않은가
- dead code, 더 이상 호출되지 않는 helper, 의미 없는 fallback 분기가 현재 변경 결과에 남아 있지 않은가
- 임시 debug print/log, 주석 처리된 코드, 의미 없는 실험 흔적이 제거되었는가
- framework/generator/serialization 같은 예외가 실제 필요 이상으로 넓게 적용되지 않았는가
- hygiene를 명분으로 현재 TASK와 무관한 대규모 코드 청소가 함께 반영되지 않았는가

## Design Quality 감사 체크리스트

- 이름이 역할과 의도를 분명히 드러내는가
- 함수가 한 가지 일과 한 단계 추상화 수준을 유지하는가
- 긴 매개변수 목록, 플래그 인수, 숨은 부수효과를 새 기본값으로 도입하지 않았는가
- 책임 분리가 유지되고, domain/application/infrastructure 경계가 섞이지 않는가
- 중복 처리 방식이 현재 TASK에서 가장 단순한 선택인지 설명 가능한가
- 추측성 일반화, 불필요한 wrapper/facade/interface/helper가 추가되지 않았는가
- 메시지 체인, 기능 편애, 뒤엉킨 변경, 산탄총 수술 징후가 더 심해지지 않았는가
- design quality와 performance 충돌이 있다면 근거 없는 최적화 대신 `performance_policy.md` 기준의 대안과 trade-off가 식별 가능한가
- 위 판단이 애매하면 `docs/process/common/design_quality_policy.md`의 함수 분리 판정 질문, 추상화 도입 판정 질문, 중복 처리 결정 규칙, 빠른 판정 체크리스트로 다시 좁혀 보았는가
- design quality trade-off 기록이 있다면 `implementation_notes.md`가 canonical source로 사용됐는가

## Performance 감사 체크리스트

- 현재 변경에서 핵심 입력 규모와 비용 증가 축을 설명할 수 있는가
- 큰 컬렉션, 대량 배치, 큰 파일, 스트림, 전체 조회 경로에서 중첩 탐색이나 반복 정렬 같은 불필요한 비용 증가가 없는가
- 같은 요청이나 배치 안에서 반복 호출, 중복 계산, 외부 I/O 루프를 새 기본값으로 만들지 않았는가
- 중간 컬렉션, 큰 객체 복사, 전체 materialization이 현재 요구사항 대비 과도하지 않은가
- 성능 이슈나 최적화 주장이 있다면 측정값, 운영 증상, 입력 규모, query 수, timeout, 메모리 사용량 중 하나 이상의 근거가 있는가
- 정확한 측정이 어렵다면 대상 경로, 우려 이유, 후속 검증 계획, 미실행 사유, 잔여 리스크가 대신 남아 있는가
- 설계 품질과 성능 충돌 시 더 작은 국소 변경으로 해결 가능한지 먼저 검토했는가
- 위 판단이 애매하면 `docs/process/common/performance_policy.md`의 성능 검토 트리거 규칙, 시간복잡도 판정 질문, 메모리 판정 질문, 반복 호출 판정 질문, 빠른 판정 체크리스트로 다시 좁혀 보았는가

## 승인 불가 기준

- 테스트 없이 구현이 먼저 들어감
- 과도한 선제 구현이 포함됨
- stale 상태의 레이어 감사 또는 Phase 2 전체 감사 결과를 그대로 승인 근거로 사용함
- 테스트 더블이 구현 내부 협력을 과도하게 고정하거나 현재 책임과 맞지 않게 선택됨
- 선택한 레이어 명칭, 순서, 세분화가 프로젝트 `docs/project/standards/implementation_order.md`와 충돌함
- 프로젝트 문서가 없거나 모호한 상태에서 기준 확정 없이 구현을 진행함
- 승인되지 않은 범위 확장이 있음
- 현재 변경과 직접 관련 없는 기존 중복 제거 또는 구조 정리가 함께 반영됨
- 성능 민감 변경 또는 성능 최적화 주장이 있는데 근거, 검증 계획, 미실행 사유 없이 추측성 최적화를 반영함
- 외부 포맷이나 원시 에러가 core로 직접 유입됨
- 로그 또는 에러 메시지에 민감정보가 직접 포함됨
- 테스트가 핵심 동작과 계약을 설명하지 못함
