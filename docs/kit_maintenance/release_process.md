# Release Process

이 문서는 `harness-kit` maintainer가 버전 릴리스를 준비하고 배포할 때 따르는 기본 절차를 정의한다.

## 목적

- 릴리스 가능 상태를 maintainer마다 다르게 해석하지 않게 한다.
- release gate, release note, tag, GitHub Release 생성을 같은 순서로 수행하게 한다.
- 문서/스크립트/validator 중심 저장소에 맞는 배포 절차를 명시한다.

## 적용 범위

- `harness-kit` core 릴리스
- Git tag 생성
- GitHub Release 생성
- 릴리스 노트 작성과 검토

## 릴리스 전 확인

릴리스를 시작하기 전에 아래를 모두 확인한다.

1. 로컬 `main`이 깨끗하고 `origin/main`과 동기화돼 있다.
2. milestone과 must-have / optional 라벨을 운영 중이면, 대상 milestone의 must-have issue가 모두 종료됐다.
3. release gate issue를 운영 중이면, gate issue가 현재 상태를 반영하고 있다.
4. 의미 있는 core 변경은 모두 `harness.log`에 기록돼 있다.
5. representative changed-parts / whole-harness audit 기록이 남아 있다.
6. 릴리스에 포함될 사용자 진입 문서와 도구 설명이 현재 동작과 맞는다.
7. downstream bundle artifact를 함께 배포하는 릴리스라면, 포함/제외 기준이 `docs/kit_maintenance/downstream_bundle_boundary.md`와 일치한다.
8. downstream bundle artifact를 함께 배포하는 릴리스라면, generated bundle 기준 install/adoption smoke test가 최근 기준선에서 통과한다.

## Release Gate 정리

- release gate issue를 운영 중이면, 단순 진행 메모가 아니라 실제 배포 가능 여부를 판정하는 마지막 체크리스트로 사용한다.
- milestone과 must-have / optional 라벨을 운영 중이면, must-have 구현이 끝날 때 gate issue의 체크박스를 현재 상태에 맞게 갱신한다.
- optional issue는 완료 여부를 별도로 적되, must-have와 섞어 배포 판단을 흐리지 않는다.
- release gate issue를 운영 중인데 stale하면 tag를 만들지 않는다.

## Release Note 작성 기준

릴리스 노트는 최소한 아래 섹션을 포함한다.

- 릴리스 한 줄 요약
- highlights
- 이번 버전에 포함된 기능
- 지원 범위
- 아직 지원하지 않는 범위
- getting started 또는 진입 문서
- known limitations

## Release Note 작성 원칙

- 이번 버전에 실제로 들어간 기능만 적는다.
- 다음 milestone 범위 기능을 과장해 섞지 않는다.
- greenfield / brownfield 지원 수준을 구분해 적는다.
- 자동 merge, interactive, agent-assisted 같이 아직 없는 기능을 있는 것처럼 쓰지 않는다.
- project-facing 진입 문서 경로를 함께 적는다.

## Release Note 파일 준비

- release note 초안은 repo를 더럽히지 않도록 임시 파일이나 maintainer 로컬 파일로 준비한다.
- 예: `/tmp/harness-kit-v0.1.0-notes.md`
- release note 파일을 저장소 안에 두기로 한 별도 운영 규칙이 없다면, 릴리스 준비용 메모 파일을 새 tracked 파일로 커밋하지 않는다.

## Tag 와 GitHub Release 절차

예시 버전이 `v0.1.0`이고 release note 초안을 `/tmp/harness-kit-v0.1.0-notes.md`에 준비했다면 아래 순서로 진행한다.

```bash
git switch main
git pull --ff-only origin main
git tag -a v0.1.0 -m "release v0.1.0"
git push origin v0.1.0
gh release create v0.1.0 --title "harness-kit v0.1.0" --notes-file "/tmp/harness-kit-v0.1.0-notes.md"
```

downstream bundle artifact도 함께 배포한다면, canonical directory artifact를 다시 생성한 뒤 파생 archive를 만들어 release asset으로 업로드한다.

```bash
python3 scripts/generate_downstream_bundle.py --force
python3 scripts/validate_downstream_bundle.py
python3 -m unittest tests.test_downstream_bundle_smoke
tar -czf "/tmp/harness-kit-project-bundle-v0.1.0.tar.gz" -C dist harness-kit-project-bundle
gh release create v0.1.0 --title "harness-kit v0.1.0" --notes-file "/tmp/harness-kit-v0.1.0-notes.md" "/tmp/harness-kit-project-bundle-v0.1.0.tar.gz#harness-kit-project-bundle-v0.1.0.tar.gz"
```

## 권장 실행 순서

1. release gate issue를 운영 중이면 최신화한다.
2. release note 초안을 작성한다.
3. `main` 최신화와 worktree clean 상태를 확인한다.
4. downstream bundle artifact를 함께 배포하는 릴리스라면 `python3 scripts/generate_downstream_bundle.py --force`로 canonical directory artifact를 다시 생성한다.
5. `python3 scripts/validate_downstream_bundle.py`로 bundle의 `README.md`, `bundle_manifest.json`, 포함/제외 경계, copied file 내용이 `docs/kit_maintenance/downstream_bundle_boundary.md`와 일치하는지 확인한다.
6. bundle artifact를 함께 배포한다면 `python3 -m unittest tests.test_downstream_bundle_smoke`로 generated bundle을 vendored dependency처럼 사용했을 때 greenfield/brownfield 기본 경로가 실제로 동작하는지 확인한다.
   관련 시나리오와 기대 결과 예시는 `docs/kit_maintenance/downstream_bundle_smoke_validation.md`를 따른다.
7. bundle artifact를 함께 배포한다면 `dist/harness-kit-project-bundle/`에서 release asset용 archive를 만든다.
8. annotated tag를 만든다.
9. tag를 remote에 push한다.
10. GitHub Release를 생성하고, bundle archive를 함께 release asset으로 붙인다.
11. 생성된 release 본문, tag, release asset 이름이 의도한 버전과 일치하는지 확인한다.

## 주의점

- 릴리스 전에 release gate와 release note의 지원 범위가 서로 다르면 먼저 문서를 맞춘다.
- `harness.log` 누락 상태에서 릴리스를 만들지 않는다.
- release note에서 `0.1.0` 지원 범위와 이후 버전 계획을 구분한다.
- patch/minor release라도 배포 당시 진입 문서가 실제 현재 동작과 맞는지 다시 확인한다.
- downstream bundle artifact를 배포하기 시작한 이후에는, bundle 생성 결과가 boundary 문서와 어긋난 상태로 릴리스하지 않는다.
- downstream bundle artifact를 배포한다면, bundle structure/content validation만 통과한 상태로 바로 릴리스하지 말고 generated bundle consumer smoke test까지 확인한다.
- downstream bundle artifact의 canonical input은 `dist/harness-kit-project-bundle/` directory와 `bundle_manifest.json`이다. zip/tarball은 필요 시 이 결과에서 파생한다.

## 배포 이후

- release URL과 tag를 확인한다.
- 필요하면 release gate issue를 종료하거나, 다음 milestone gate로 연결한다.
- 다음 버전에서 이어질 optional 또는 deferred issue를 milestone 기준으로 다시 정리한다.
