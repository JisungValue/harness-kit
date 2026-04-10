# Harness Upgrade Impact Policy

이 문서는 downstream 프로젝트가 새 `harness-kit` bundle 변경을 반영하기 전에, 그 변경이 어느 정도의 영향도를 가지는지 소비자 관점에서 분류하는 기준을 정의한다.

## 목적

- 모든 harness 변경을 같은 수준의 update로 보지 않게 한다.
- repo 전체가 아니라 downstream bundle 경계 안의 자산만 기준으로 impact를 판단한다.
- 어떤 변경을 바로 반영해도 되는지, 어떤 변경은 수동 검토가 필요한지, 어떤 변경은 breaking 가능성이 큰지 구분한다.

## 분류 범위

- 분류 대상은 현재 downstream bundle에 실제로 포함되는 문서, template, bootstrap 자산, project-facing script 변경만이다.
- maintainer 전용 문서, 테스트, release 스크립트, maintainer 기록만 바뀐 경우는 downstream upgrade impact 분류 대상이 아니다.
- 같은 커밋에 maintainer 자산과 bundle 자산이 함께 바뀌면, downstream impact는 bundle 자산 변경만 따로 본다.

## 먼저 확인할 질문

1. 이 변경이 downstream bundle에 포함되는 문서, template, bootstrap 자산, project-facing script를 실제로 바꾸는가?
2. 기존 프로젝트 overlay 문서가 바뀌지 않아도 계속 유효한가?
3. validator, phase gate, required doc set, bootstrap 결과가 더 엄격해지는가?
4. safe write로 처리 가능한 additive change인가, 아니면 사람이 diff를 읽고 결정을 내려야 하는가?

## Impact Category

### C0. Clarification Only

- 의미:
  - 설명, 예시, wording만 개선되고 downstream 필수 문서 세트나 validator 판정은 바뀌지 않는다.
- 대표 변경:
  - 문서 설명 개선 수준
- downstream 영향:
  - 기존 overlay를 다시 쓰지 않아도 된다.
- 권장 반영 시점:
  - 다음 bundle sync 때 반영해도 된다.
- manual intervention:
  - 보통 불필요하다.
- breaking 가능성:
  - 사실상 없음.

### C1. Additive Recommendation

- 의미:
  - 새 권장 문서나 참고 경로가 추가되지만, 현재 필수 문서 세트와 validator 성공 조건은 유지된다.
- 대표 변경:
  - 새 권장 문서 추가
- downstream 영향:
  - 당장 프로젝트를 깨뜨리지는 않지만, 다음 정리 시점에 반영하는 편이 좋다.
- 권장 반영 시점:
  - 다음 harness update나 문서 정리 시점
- manual intervention:
  - 보통 낮다. 필요하면 safe create 또는 수동 복사로 충분하다.
- breaking 가능성:
  - 낮다.

### C2. Additive Baseline Update

- 의미:
  - bootstrap template, overlay template, safe write 대상으로 쓰이는 baseline이 확장되지만, 기존 구조를 바로 invalid로 만들지는 않는다.
- 대표 변경:
  - bootstrap template 변경
  - 새 safe-create 대상 문서 추가
- downstream 영향:
  - missing file create나 exact-match refresh 중심으로 따라갈 수 있다.
- 권장 반영 시점:
  - 다음 bundle update 때 비교적 빠르게 반영
- manual intervention:
  - localized file이 있으면 부분 수동 검토가 필요할 수 있다.
- breaking 가능성:
  - 낮음에서 중간.

### C3. Review-Required Policy Shift

- 의미:
  - 필수 문서 구조, phase 규칙, validator 기준이 바뀌어 사람이 diff와 현재 overlay 상태를 읽고 반영 순서를 판단해야 한다.
- 대표 변경:
  - 필수 문서 구조 변경
  - phase 규칙 변경
  - validator 강화
  - bootstrap template 변경 중 기존 localized 문서 검토가 필수인 경우
- downstream 영향:
  - 기존 프로젝트가 즉시 깨질 수도, validator가 새로 실패할 수도 있다.
  - safe write만으로 끝내지 말고 diff review와 validator 재검증이 필요하다.
- 권장 반영 시점:
  - task 도중이 아니라 별도 upgrade 작업 단위로 수행
- manual intervention:
  - 필요하다.
- breaking 가능성:
  - 중간에서 높음.

### C4. Breaking Overlay Contract

- 의미:
  - 기존 overlay를 대규모로 다시 써야 하거나, 현재 project-local 구조가 새 bundle 기준과 직접 충돌한다.
- 대표 변경:
  - 필수 문서 구조 변경 중 기존 문서 재배치가 필요한 경우
  - phase gate 의미 변경으로 기존 진행 기준이 더 이상 유효하지 않은 경우
  - validator 강화로 기존 프로젝트가 기본적으로 manual migration 없이는 통과할 수 없는 경우
- downstream 영향:
  - 단순 safe write로는 해결되지 않는다.
  - 프로젝트 문서 재구성, 수동 migration 계획, 단계적 validator 확인이 필요하다.
- 권장 반영 시점:
  - 별도 upgrade 작업과 명시적 승인 이후
- manual intervention:
  - 필수다.
- breaking 가능성:
  - 높다.

## 변경 유형별 기본 분류 기준

| 변경 유형 | 기본 category | 더 높은 category로 올려야 하는 조건 |
| --- | --- | --- |
| 문서 설명 개선 수준 | C0 | 기존 validator 기준, required doc set, bootstrap 결과까지 바뀌면 C3 이상 |
| 새 권장 문서 추가 | C1 | 그 문서가 validator나 필수 참조로 승격되면 C3 이상 |
| 필수 문서 구조 변경 | C3 | 기존 문서 재배치/재작성 없이는 따라갈 수 없으면 C4 |
| phase 규칙 변경 | C3 | 기존 진행 기준이 사실상 무효가 되면 C4 |
| validator 강화 | C3 | 기존 프로젝트가 manual migration 없이는 기본 실패하면 C4 |
| bootstrap template 변경 | C2 | localized 기존 문서를 광범위하게 다시 봐야 하면 C3 |

## 반영 판단 규칙

- C0:
  - 일반 문서 동기화로 본다.
- C1:
  - 바로 반영하지 않아도 되지만, 다음 bundle sync 때 반영 후보로 기록한다.
- C2:
  - `adopt_dry_run.py`와 `adopt_safe_write.py` 범위 안에서 우선 검토한다.
- C3:
  - `adopt_dry_run.py` 결과, impact policy, validator 재검증을 함께 본다.
  - safe write는 보조 수단일 뿐 최종 판단 수단이 아니다.
- C4:
  - 별도 upgrade 작업으로 분리하고, project-local overlay migration 계획을 먼저 세운다.

## 안전 해석 규칙

- category는 “이번 변경이 downstream 프로젝트에 요구하는 판단 비용”을 뜻한다.
- category가 낮아도 localized 파일이 많으면 실제 작업 비용은 커질 수 있다.
- category가 높아도 영향을 받는 bundle 자산이 적으면 실제 수정 파일 수는 적을 수 있다.
- 따라서 category는 파일 수가 아니라 manual decision 필요성과 breaking 가능성을 기준으로 읽는다.

## 현재 한계

- 이 문서는 semver를 강제하지 않는다.
- 이 문서는 자동 merge 여부를 판정하지 않는다.
- framework별 semantic migration까지 분류하지는 않는다.
- 이후 추가될 upgrade guide나 diff review checklist가 나오면 이 category를 더 구체적인 절차와 연결할 수 있다.
