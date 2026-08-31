# 로봇학습연구회 (Robot Learning Research Society) 워크샵 웹사이트

한국로봇학회(KROS) 산하 **로봇학습연구회**의 워크샵 및 연구회 안내 웹사이트입니다.
빌드 도구 없이 순수 HTML/CSS 만으로 구성했으며, GitHub Pages 로 배포됩니다.

- 배포 주소: https://gist-ailab.github.io/rol-tc-kros/
- 원격 저장소: gist-ailab/rol-tc-kros

## 사이트 구조

```
.
├── index.html              # 홈 — 다가오는 워크샵 안내
├── workshops/index.html    # 이전 워크샵 아카이브 (회차 목록)
├── photos/index.html       # Photo — 행사 사진 갤러리
├── join/index.html         # 가입신청 — 구글 폼 임베드
├── assets/style.css        # 네 페이지가 공유하는 공통 스타일 (토큰·헤더·탭·푸터)
├── .nojekyll               # GitHub Pages 의 Jekyll 처리 비활성화
├── README.md               # 이 문서 — 사이트 소개
├── MAINTAINERS.md          # 내부 관리 문서 — 사진 게시·내용 수정·배포 절차
└── CLAUDE.md               # 클로드 코드 세션용 작업 안내
```

모든 페이지 상단에는 공통 탭 내비게이션(`홈` / `이전 워크샵` / `Photo` / `가입신청`)이 있습니다.
프로젝트 페이지(`/rol-tc-kros/` 하위 경로)로 배포되므로 모든 링크는 상대 경로로 작성되어 있습니다.

## 사이트 관리

사진을 올리는 방법, 워크샵 정보와 페이지 내용을 수정하는 방법, 가입신청 폼 연결과
배포(공개) 절차는 전부 **[`MAINTAINERS.md`](MAINTAINERS.md)** 에 정리되어 있습니다.
사이트를 관리하는 사람과 클로드 코드 모두 그 문서를 기준으로 작업합니다.

## 참고

- 폰트는 구글 폰트(Noto Sans KR + JetBrains Mono)를 사용합니다.
- 디자인 참고용 원본 파일은 `_reference/` 폴더에 있으며, `.gitignore` 로 커밋·배포 대상에서 제외됩니다.
