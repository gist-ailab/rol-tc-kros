# 로봇학습연구회 (Robot Learning Research Society) 워크샵 웹사이트

한국로봇학회(KROS) 산하 **로봇학습연구회**의 워크샵 및 연구회 안내 웹사이트입니다.
빌드 도구 없이 순수 HTML/CSS/바닐라 JS 로 구성했으며, GitHub Pages 로 배포됩니다.

- 배포 주소: https://gist-ailab.github.io/rol-tc-kros/
- 원격 저장소: gist-ailab/rol-tc-kros (공개)
- 브랜드: RoL-TC · 대표색 `#DB2416`

## 사이트 구조

```
.
├── index.html                      # 홈 — 다가오는 워크샵 (2026 제3회)
├── workshops/
│   ├── index.html                  # 이전 워크샵 아카이브 (회차 목록)
│   └── 2026/2nd/index.html         # 회차 상세 (프로그램·발표자·사진·행사정보)
├── photos/index.html               # Photos — 회차별 서브탭 사진 갤러리
├── join/index.html                 # Membership — 가입신청 (구글 폼 임베드)
├── assets/
│   ├── style.css                   # 다섯 페이지 공통 스타일 (토큰·헤더·탭·히어로·카드·푸터)
│   ├── calendar-popup.js           # 일시 칩의 일정 추가 팝업 토글
│   ├── icons/                      # 서비스 아이콘 (구글캘린더·Outlook·네이버지도·TMAP·일정추가)
│   └── logos/                      # RoL-TC 로고 (원본 SVG, 배포용 PNG·AI, 파비콘)
├── events/                         # 회차별 일정 파일 (.ics)
├── favicon.ico
├── .nojekyll                       # GitHub Pages 의 Jekyll 처리 비활성화
├── README.md                       # 이 문서 — 사이트 소개
├── STATUS.md                       # 진행 상황 · 결정 사항 · 남은 일
├── MAINTAINERS.md                  # 운영 안내서 — 사진 게시·내용 수정·배포 절차
└── CLAUDE.md                       # 클로드 코드 세션용 작업 규칙
```

모든 페이지 상단에 공통 탭 내비게이션(`Home` / `Workshops` / `Photos` / `Membership`)이 있습니다.
프로젝트 페이지(`/rol-tc-kros/` 하위 경로)로 배포되므로 **모든 내부 링크는 상대 경로**입니다.

## 문서 안내

| 문서 | 읽어야 할 때 |
|---|---|
| [`STATUS.md`](STATUS.md) | 지금 무엇이 되어 있고 무엇이 남았는지 파악할 때. **새로 합류하면 여기부터** |
| [`MAINTAINERS.md`](MAINTAINERS.md) | 사진 게시, 내용 수정, 회차 추가, 폼 연결, 배포 등 실제 작업을 할 때 |
| [`CLAUDE.md`](CLAUDE.md) | 클로드 코드로 이 저장소를 수정할 때 지켜야 할 규칙 |

## 참고

- 폰트는 구글 폰트(Noto Sans KR + JetBrains Mono)를 사용합니다. 로고는 Archivo + IBM Plex Mono 입니다.
- 디자인 참고용 원본은 `_reference/` 에 있으며 `.gitignore` 로 커밋·배포 대상에서 제외됩니다.
