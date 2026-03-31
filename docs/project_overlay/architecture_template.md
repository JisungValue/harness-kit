# Architecture

## 목적

이 문서는 프로젝트의 실제 레이어 구조와 의존성 방향을 정의한다.

## 레이어 구조

- core
- application
- adapter
- entrypoint
- bootstrap

프로젝트에 맞는 실제 명칭과 패키지 구조를 위 항목에 맞춰 정리한다.

## 의존성 원칙

- 안쪽 레이어는 바깥 레이어를 직접 알지 않는다.
- 외부 모델, 저장 구조, transport 구조는 경계에서 번역한다.
- 실제 조립과 환경 설정은 bootstrap 또는 이에 준하는 레이어에 둔다.
