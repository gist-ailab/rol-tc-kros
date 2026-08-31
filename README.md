# 로봇학습연구회 (Robot Learning Research Society) 워크샵 웹사이트

한국로봇학회(KROS) 산하 **로봇학습연구회**의 워크샵 및 연구회 안내 웹사이트입니다.
빌드 도구 없이 순수 HTML/CSS 만으로 구성했으며, GitHub Pages 로 배포됩니다.

- 배포 주소: https://gist-ailab.github.io/kros-rlr/
- 원격 저장소: gist-ailab/kros-rlr

## 사이트 구조

```
.
├── index.html              # 홈 — 다가오는 워크샵 안내
├── workshops/index.html    # 이전 워크샵 아카이브 (회차 목록)
├── photos/index.html       # Photo — 행사 사진 갤러리
├── join/index.html         # 가입신청 — 구글 폼 임베드
├── assets/style.css        # 네 페이지가 공유하는 공통 스타일 (토큰·헤더·탭·푸터)
├── .nojekyll               # GitHub Pages 의 Jekyll 처리 비활성화
└── README.md
```

모든 페이지 상단에는 공통 탭 내비게이션(`홈` / `이전 워크샵` / `Photo` / `가입신청`)이 있습니다.
프로젝트 페이지(`/kros-rlr/` 하위 경로)로 배포되므로 모든 링크는 상대 경로로 작성되어 있습니다.
하위 폴더 페이지에서는 `../` 를 사용합니다.

## GitHub Pages 활성화 방법

1. 이 저장소를 `gist-ailab/kros-rlr` 로 푸시합니다.
2. GitHub 저장소의 **Settings → Pages** 로 이동합니다.
3. **Source** 를 `Deploy from a branch` 로 두고, 브랜치는 `main`, 폴더는 `/ (root)` 를 선택합니다.
4. 저장하면 잠시 후 https://gist-ailab.github.io/kros-rlr/ 에서 사이트가 열립니다.

## 구글 폼 URL 교체 방법

가입신청 폼은 `join/index.html` 에 구글 폼 임베드 자리로 준비되어 있습니다.
폼 주소가 정해지면 `GOOGLE_FORM_URL_HERE` 라는 플레이스홀더 문자열 **두 곳**을 실제 주소로 교체합니다.

1. 구글 폼을 만들고 **[보내기] → [`<>` 임베드]** 에서 iframe 주소를 복사합니다.
   (임베드 주소는 대개 `.../viewform?embedded=true` 형태입니다.)
2. `join/index.html` 을 열어 다음을 수정합니다.
   - 주석 처리된 **폼 임베드 블록**(`.form-embed`) 안 `<iframe>` 의 `src` → 임베드 주소
   - **새 창에서 열기** 버튼의 `href` → 일반 폼 주소(`.../viewform`)
3. `가입신청 폼 준비 중` 안내 박스(`.form-placeholder`)를 주석 처리하고,
   폼 임베드 블록의 주석을 해제합니다. (자바스크립트 없이 주석 전환만으로 동작합니다.)

## 회원 명단 관리

회원 명단은 아래 구글 시트에서 관리합니다.

- 회원 명단 시트: https://docs.google.com/spreadsheets/d/1JMILObRebTsnhCfi1an9dCn7NACX7ZlrtWx05LlOUWw/edit?gid=1224316441

구글 폼의 **응답** 탭에서 이 시트를 응답 대상으로 연결하면, 가입신청 응답이 시트에 자동으로 쌓입니다.

## 새 워크샵 회차 추가 방법

각 회차의 상세 페이지는 `workshops/<연도>/<회차>/index.html` 관례로 만듭니다.
(예: `workshops/2026/1st/index.html`)

1. `assets/style.css` 를 함께 불러오는 새 상세 페이지를 위 경로에 만듭니다.
   (홈 `index.html` 의 프로그램·발표자·행사 정보 구조를 실제 내용으로 채우면 됩니다.
   상세 페이지에서 공통 스타일은 `../../../assets/style.css` 로 링크합니다.)
2. `workshops/index.html` 을 열어, 파일에 주석으로 남겨 둔 연도 블록(`.year-block`)과
   워크샵 카드(`.workshop-card`) 템플릿을 참고해 목록에 항목을 추가합니다.
   (첫 회차를 추가할 때 `아직 개최된 워크샵이 없습니다` 빈 상태 안내를 제거합니다.)
3. 행사 사진은 `photos/img/` 에 넣고, `photos/index.html` 의 `<figure>` 블록 템플릿을 복사해 게시합니다.

## 참고

- 디자인 참고용 원본 파일은 `_reference/` 폴더에 있으며, `.gitignore` 로 커밋·배포 대상에서 제외됩니다.
- 폰트는 구글 폰트(Noto Sans KR + JetBrains Mono)를 사용합니다.
