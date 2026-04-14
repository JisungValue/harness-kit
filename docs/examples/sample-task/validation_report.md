# Validation Report

## 실행한 검증

- 검증 항목: 공통 guide 참조 구조 확인
  - 대조한 입력물: `docs/project_entrypoint.md`, `docs/project_overlay/README.md`
  - 실행 방법 또는 확인 방식: 문서 경로와 역할을 수동 검토
  - 결과: 공통 guide와 project overlay 문서가 분리되어 있음
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 없음

- 검증 항목: overlay 최소 문서 세트 확인
  - 대조한 입력물: `README.md`, `docs/project_overlay/README.md`, `docs/project_overlay/project_entrypoint_template.md`
  - 실행 방법 또는 확인 방식: `docs/project_entrypoint.md`, `docs/standard/architecture.md`, `docs/standard/implementation_order.md`, `docs/standard/coding_conventions_project.md`, `docs/standard/quality_gate_profile.md`, `docs/standard/testing_profile.md`, `docs/standard/commit_rule.md` 존재 여부 확인
  - 결과: 최소 세트 정의 완료
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 프로젝트별 세부 내용은 별도 작성 필요

- 검증 항목: quality gate 실행 여부 기록 확인
  - 대조한 입력물: `docs/standard/quality_gate_profile.md`, `validation_report.md`
  - 실행 방법 또는 확인 방식: `docs/standard/quality_gate_profile.md` 기준으로 어떤 자동 검증을 실행했는지 또는 왜 미실행인지 기록했는지 수동 검토
  - 결과: sample task는 문서 구조 예시라 실제 formatter/linter/type checker/test 명령은 미실행
  - 실패 또는 미실행 사유: project-specific quality gate 명령이 아직 없는 예시 task이기 때문
  - 판정: 정합
  - 잔여 리스크: 실제 프로젝트에서는 quality gate 실행 결과를 더 구체적으로 남겨야 한다

- 검증 항목: code hygiene 확인 기준 존재 여부
  - 대조한 입력물: `docs/harness/common/code_hygiene_policy.md`, `docs/standard/quality_gate_profile.md`, `validation_report.md`
  - 실행 방법 또는 확인 방식: import, dead code, debug 흔적을 자동 게이트 또는 수동 검토 중 어떤 방식으로 확인하는지 기록 구조가 있는지 수동 검토
  - 결과: sample task는 문서 구조 예시라 실제 hygiene gate는 미실행이지만, policy와 quality gate 위치는 식별 가능하다
  - 실패 또는 미실행 사유: project-specific hygiene command가 아직 없는 예시 task이기 때문
  - 판정: 정합
  - 잔여 리스크: 실제 프로젝트에서는 hygiene를 자동 게이트로 볼지 수동 검토로 둘지 더 구체적으로 적어야 한다

- 검증 항목: design quality 판단 기준 존재 여부
  - 대조한 입력물: `docs/harness/common/design_quality_policy.md`, `docs/standard/quality_gate_profile.md`, `validation_report.md`
  - 실행 방법 또는 확인 방식: 책임 분리, 추상화 수준, 구조 악취, design-performance trade-off를 어떤 방식으로 확인하는지 기록 구조가 있는지 수동 검토
  - 결과: policy, quality gate 연결 지점, `implementation_notes.md` canonical source가 모두 식별 가능하고 sample task에도 실제 trade-off 기록 예시가 있다
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 실제 프로젝트에서는 어떤 설계 품질 항목을 수동 감사로 보고 어떤 항목을 architecture rule로 볼지 더 구체적으로 적어야 한다

- 검증 항목: performance 판단 기준 존재 여부
  - 대조한 입력물: `docs/harness/common/performance_policy.md`, `docs/standard/quality_gate_profile.md`, `docs/examples/sample-task/implementation_notes.md`
  - 실행 방법 또는 확인 방식: 시간복잡도, 메모리, 중간 컬렉션, 반복 호출, 성능 근거와 검증 계획을 어떤 구조로 남기는지 수동 검토
  - 결과: `performance_policy.md`에 yes/no 판정 질문, 기록 형식, quality gate 연결 원칙이 있고 sample task에도 대상 경로, 입력 규모, 근거, 검증 계획이 포함된 성능 검토 기록 예시가 있다
  - 실패 또는 미실행 사유: sample task는 문서 구조 예시라 `implementation_notes.md`에 적은 10건/50,000건 데이터셋 비교와 peak memory 확인은 실제 실행하지 않았다
  - 판정: 정합
  - 잔여 리스크: 실제 프로젝트에서는 샘플보다 더 실제 데이터 규모와 운영 지표에 가까운 근거가 필요할 수 있다

- 검증 항목: performance 검증 계획의 Phase 4 반영 여부
  - 대조한 입력물: `docs/examples/sample-task/implementation_notes.md`, `docs/harness/common/validation_policy.md`, `validation_report.md`
  - 실행 방법 또는 확인 방식: `implementation_notes.md`의 성능 검토 기록에서 대상 경로, 근거, 검증 계획을 읽고 `validation_report.md`가 실행 결과 또는 미실행 사유, 잔여 리스크를 함께 남기는지 수동 검토
  - 결과: 대상 경로는 대량 사용자 export 배치 함수이고, 근거는 중간 컬렉션 3회 생성과 payload 복사이며, 검증 계획은 샘플/대량 데이터셋 비교와 peak memory 확인으로 요약할 수 있다
  - 실패 또는 미실행 사유: sample task는 문서 예시라 실제 대량 데이터셋 생성과 profiler 실행은 수행하지 않았다
  - 판정: 정합
  - 잔여 리스크: 실제 프로젝트에서는 같은 형식으로 실제 실행 결과 또는 정확한 미실행 사유를 더 구체적으로 남겨야 한다

- 검증 항목: design quality trade-off 기록 예시 존재 여부
  - 대조한 입력물: `docs/examples/sample-task/implementation_notes.md`, `docs/harness/common/design_quality_policy.md`, `docs/harness/common/performance_policy.md`
  - 실행 방법 또는 확인 방식: `implementation_notes.md`에 함수 분리 판정 질문, 대안/추천안/근거/검증 계획/trade-off 기록 형식이 남아 있고 `validation_report.md`가 이를 요약하는지 수동 검토
  - 결과: sample task에 design quality 판단, 독립 performance 검토, design-performance 충돌 예시를 `implementation_notes.md`에 남기고, validation 단계가 그 canonical source를 다시 확인하는 흐름을 추가했다
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 실제 프로젝트에서는 sample보다 더 실제 코드와 가까운 trade-off 근거가 필요할 수 있다

- 검증 항목: language-specific convention 확인 기준 존재 여부
  - 대조한 입력물: `docs/examples/sample-task/coding_conventions_project_example.md`, `plan.md`
  - 실행 방법 또는 확인 방식: 현재 작업과 직접 관련 있는 언어별 규칙 범주, 금지 패턴, 미해결 금지 항목이 식별 가능한지 수동 검토
  - 결과: sample task 예시에 활성 언어/런타임, 관련 규칙 범주, 주요 금지 패턴, 현재 Phase 2에서 미해결로 둘 수 없는 항목을 함께 기록했다
  - 실패 또는 미실행 사유: 없음
  - 판정: 정합
  - 잔여 리스크: 실제 프로젝트에서는 sample 예시보다 현재 코드베이스에 더 밀착된 규칙 범주를 적어야 한다

## 실행하지 못한 검증

- 실제 새 프로젝트에 kit를 가져와 end-to-end로 적용하는 검증은 미실행

## 결과 요약

- 새 프로젝트가 core와 overlay를 분리해 시작할 수 있는 최소 구조가 준비되었다.
- 이번 판단의 repo-local 근거: `README.md`, `docs/project_overlay/README.md`, `docs/harness/common/*`, sample task 문서를 교차 기준으로 사용했다.
- repo에 없어 후속 문서화/승인 대상으로 남긴 결정: 실제 프로젝트 품질 게이트 명령, 실제 architecture 세부 결정, 실제 language-specific convention은 도입 프로젝트 overlay에서 확정해야 한다.

## Phase 5에서 반영할 related decisions/

- 해당 없음. 이번 sample task는 구조 설명 문서 예시를 만드는 작업이라 project-local decision record까지 확정하지 않는다.

## 남은 리스크

- 실제 프로젝트 적용 시 overlay 문서가 과소 작성될 수 있다.

## 후속 조치 필요 사항

- 첫 도입 프로젝트에서 overlay 작성 예시를 추가한다.
