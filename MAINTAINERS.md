# 내부 관리 문서 (MAINTAINERS)

이 문서는 로봇학습연구회 웹사이트를 **관리하는 사람(내부자)을 위한** 운영 안내서입니다.
사이트 소개는 `README.md` 에 있고, 실제 수정 절차는 전부 이 문서에 모여 있습니다.
클로드 코드로 작업할 때도 이 문서를 기준으로 삼으면 됩니다 (`CLAUDE.md` 가 이 문서를 가리킵니다).

> ℹ️ 이 레포는 **공개** 상태이며 사이트가 https://gist-ailab.github.io/rol-tc-kros/ 에서 서비스 중입니다.
> 이 문서도 함께 공개되어 있으니, 개인정보나 비공개 자료를 적지 마세요.
> `main` 에 푸시하면 1분 내외로 사이트에 반영됩니다.

## 사진 올리는 법 — 회차별 서브탭 운영

행사 사진은 `photos/` 페이지에 **워크샵 회차별 서브탭**으로 게시합니다.
회차마다 탭이 하나씩 생기고, 탭을 누르면 그 회차의 사진 패널이 보입니다.

**운영 방식 (인수인계 핵심):**
사진 업데이트가 필요할 때마다 **관리자가 구글 포토 공유 주소를 전달합니다**
(형식 예: `https://photos.app.goo.gl/bgozVhoFPnv25eqN9`).
주소를 받은 사람(또는 클로드 코드)은 그 주소로 해당 회차의 서브탭을 추가·갱신합니다.
구글 포토는 iframe 임베드를 막고 있으므로, 앨범은 페이지에 끼워 넣지 않고
`구글 포토 앨범에서 보기` 외부 링크 버튼으로 연결합니다.

**회차 서브탭 추가 절차:**

1. `photos/index.html` 안에 주석으로 남겨 둔 서브탭 템플릿(`.subtab-bar` + `.subtab-panel` 한 쌍)을 복사해
   `아직 게시된 사진이 없습니다` 빈 상태 박스(`.empty-state`)를 대체합니다. (첫 회차 추가 시에만 빈 상태 제거)
2. 다음 네 값을 채웁니다.
   - 탭 라벨 (`.subtab-btn` 텍스트): 간결하게 `2026 제1회` 형식
   - 패널 제목 (`<h3>`): **반드시 `20XX년 제 X회 로봇학습연구회 워크샵` 형식** (예: `2026년 제 1회 로봇학습연구회 워크샵`)
   - 앨범 주소 (`.subtab-album` 버튼의 `href`): 전달받은 `https://photos.app.goo.gl/...` 주소로
     `GOOGLE_PHOTOS_ALBUM_URL_HERE` 플레이스홀더를 교체
   - 이미지 (`<figure>` 블록들): 레포에 직접 올릴 사진이 있으면 `photos/img/<연도>-<회차>/` 폴더에 넣고
     (예: `photos/img/2026-1st/01.jpg`) `src`·`alt`·`figcaption` 을 채웁니다. 앨범 링크만 걸 때는 그리드를 비워 둡니다.
3. 회차가 둘 이상이면 `.subtab-btn` 과 `.subtab-panel` 을 한 쌍씩 추가하되, 두 요소의
   `data-subtab` · `data-panel` 값을 같은 문자열로 맞춥니다. 탭 전환은 페이지 하단 스크립트가
   자동 처리하며 첫 번째 탭이 기본 선택됩니다.
4. 로컬 브라우저로 `photos/index.html` 을 열어 탭 전환과 앨범 버튼을 확인한 뒤 커밋합니다.

홈(`index.html`) 하단에 대표 사진 한 장을 노출하고 싶으면, 참고용 원본(`_reference/page.html`)의
Gallery 섹션 구조를 따라 섹션을 추가하면 됩니다.

## 내용 수정하는 법

### 홈 — 워크샵 정보 채우기 (`index.html`)

현재 미정으로 표기된 항목과 위치:

| 항목 | 위치 |
|---|---|
| 일시·장소 | 히어로의 메타 칩(`.meta-chip`) 두 개 — `추후 공지` 를 실제 값으로 교체 |
| 프로그램 시간·발표 | 프로그램 테이블(`.program-table`)의 `미정` 시간 셀과 `발표 모집 예정` 행 |
| 발표자 | 발표자 카드(`.speaker-card`) — `모집 예정` 자리표시 카드를 실제 발표자로 교체 |
| 행사 정보 | `info-grid` 네 박스의 `추후 안내` 항목 |
| 문의처 | 푸터의 `문의처 추후 안내` (네 페이지 공통이므로 함께 수정) |

발표자가 확정되면 프로그램 테이블 행과 발표자 카드를 한 쌍으로 같이 채웁니다.
확정 상태 배지는 `status-confirmed`(확정) / `status-expected`(예정) 클래스를 씁니다.

### 이전 워크샵 회차 추가 (`workshops/`)

워크샵이 끝나면 아카이브에 회차를 추가합니다.

1. 상세 페이지를 `workshops/<연도>/<회차>/index.html` 경로에 만듭니다. (예: `workshops/2026/1st/index.html`)
   홈 `index.html` 의 구조를 복사해 실제 내용으로 채우면 되고,
   공통 스타일은 `../../../assets/style.css` 로 링크합니다.
2. `workshops/index.html` 안에 주석으로 남겨 둔 연도 블록(`.year-block`)·워크샵 카드(`.workshop-card`)
   템플릿을 복사해 목록에 항목을 추가합니다.
3. 첫 회차를 추가할 때 `아직 개최된 워크샵이 없습니다` 빈 상태 안내를 제거합니다.

### 공통 디자인 수정 (`assets/style.css`)

색·폰트·헤더·탭·푸터는 네 페이지가 `assets/style.css` 하나를 공유합니다.
색상을 바꾸려면 파일 상단 `:root` 의 CSS 변수만 수정하면 전체에 적용됩니다.
링크는 반드시 **상대 경로**로 작성합니다 (`/` 로 시작하는 절대 경로 금지 — 프로젝트 페이지 하위 경로에서 깨집니다).

## 히어로 칩의 일정·지도 바로가기

워크샵 페이지(홈, 회차 상세)의 일시·장소 칩에는 바로가기 아이콘이 붙습니다.
아이콘 SVG는 `assets/icons/` 에 있습니다 (`gcal.svg`, `outlook.svg`, `navermap.svg`, `tmap.svg`).

새 회차를 만들 때는 기존 페이지의 칩 마크업을 복사하고 아래 값만 바꿉니다.

- 구글 캘린더: `...render?action=TEMPLATE&text=<제목>&dates=<시작>/<종료>&location=<장소>`
  날짜는 **UTC** `YYYYMMDDTHHMMSSZ` 형식입니다. 한국시간 13:00~18:00 은 UTC 로 `T040000Z/T090000Z` 입니다.
- Outlook·기타 캘린더 앱: `events/<연도>-<회차>.ics` 파일을 만들고 `download` 속성으로 연결합니다.
  (예: `<a href="events/2026-3rd.ics" download>`) `.ics` 안의 `DTSTART`/`DTEND` 도 **UTC** 형식이므로,
  기존 파일을 복사해 UID·제목·장소·시간만 바꾸면 됩니다.

  > `outlook.live.com/.../deeplink/compose` 방식은 쓰지 마세요. 개인 Microsoft 계정으로 로그인한
  > 상태가 아니면 일정 추가 화면 대신 마이크로소프트 홍보 페이지로 넘어갑니다(2026-08-31 확인).
  > `.ics` 파일은 Outlook 데스크톱·웹, 애플 캘린더, 썬더버드 어디서나 열립니다.
- 네이버지도: `https://map.naver.com/v5/search/<장소>`
- TMAP: `tmap://search?name=<장소>` — **앱이 설치된 모바일에서만 열립니다.** 데스크톱에서 눌러도 반응이 없는 것이 정상입니다.

한글·공백이 들어가는 값은 모두 URL 인코딩해서 넣습니다.

## 가입신청 폼 연결 (`join/index.html`)

**현재 연결된 폼:** 로봇학습연구회 가입신청서 — https://forms.gle/DqxCF2C8xMzz9PPXA
(임베드 주소: `https://docs.google.com/forms/d/e/1FAIpQLSe77x9Evk3FwBoDBab00H5fv1EEA9MVfLVh-gFh6SEnPeAQ6A/viewform?embedded=true`)

**상태:** 2026-08-31 확인 기준으로 로그인 없이 열리며, 임베드 안에 신청 양식이 바로 표시됩니다.
(초기에는 로그인 제한이 걸려 있었으나 해제되었습니다.)

> 폼이 임베드 안에서 "Google 계정에 로그인하십시오" 로 보인다면 폼 설정이 다시 제한된 것입니다.
> 폼 편집 화면의 **설정 → 응답 → 응답자 제한 / 이메일 주소 수집** 을 확인하세요.
> 터미널에서 `curl -sL -o /dev/null -w "%{http_code}\n" "<임베드 주소>"` 가 200 이면 공개 상태입니다.

폼을 교체할 때는 `join/index.html` 의 **두 곳**을 함께 바꿉니다.

1. 새 폼의 **응답 탭 → 스프레드시트에 연결**에서 회원 명단 시트를 응답 대상으로 지정합니다.
2. 폼의 **[보내기] → [`<>` 임베드]** 에서 임베드 주소(`.../viewform?embedded=true`)를 복사합니다.
3. `.form-embed` 안 `<iframe>` 의 `src` → 임베드 주소, `새 창에서 열기` 버튼의 `href` → 공유용 주소로 교체합니다.

## 구글 포토 슬라이드쇼 임베드 (검증 완료)

구글 포토는 공식 임베드를 제공하지 않지만, 다음 우회 방법이 실제 렌더링 검증을 거쳐 적용되어 있습니다
(적용 예: `photos/index.html` 의 2026 제2회 서브탭).

1. 공유 앨범 페이지(`photos.app.goo.gl` 주소를 브라우저로 연 뒤의 페이지) HTML에서
   `https://lh3.googleusercontent.com/pw/...` 형태의 이미지 원본 주소를 추출합니다.
   터미널에서는 다음 한 줄로 뽑을 수 있습니다.
   ```bash
   curl -sL "<공유 주소>" | grep -oE 'https://lh3\.googleusercontent\.com/pw/[A-Za-z0-9_-]+' | awk '!seen[$0]++'
   ```
2. `pa-gallery-player-widget` 블록(publicalbum.org 위젯)에 이미지 주소들을 `<object data="...=w1920">` 로
   나열하고, 스크립트 `https://cdn.jsdelivr.net/npm/publicalbum@latest/embed-ui.min.js` 를 페이지에 한 번 로드합니다.
   정확한 마크업은 `photos/index.html` 의 기존 블록이나 `_reference/embed-verified-sample.html` 을 복사해서 씁니다.
3. 정적 썸네일이 필요하면 같은 주소에 `=w800` 접미사를 붙여 일반 `<img>` 로 씁니다
   (적용 예: `workshops/2026/2nd/index.html` 의 사진 섹션).

**한계:** 앨범 공유를 중단하면 이미지 주소가 무효화되고, 앨범에 사진을 추가해도 자동 반영되지 않으므로
주소를 다시 추출해 갱신해야 합니다.

## 이전 워크샵 페이지 만들기 — 데이터 출처

지난 워크샵의 프로그램·운영 기록은 회차별 구글 시트에서 관리합니다.

- 2026 제2회 워크샵 정보 시트: https://docs.google.com/spreadsheets/d/1fiAD_RtIqXVoIp2vGmMvG_6h8eJor1jfj7EhmKRswG0/edit
  (탭: Form Responses 1 = 참가 신청 응답, 시간표, 출장계, 결산)
- 공식 공지는 한국로봇학회(KROS) 학술행사 게시판에 올라갑니다.

**⚠️ 개인정보 규칙:** 참가 응답·결산·출장계 탭에는 전화번호·이메일 등 개인정보가 있습니다.
웹사이트에는 **시간표(발표자 이름·소속·발표 제목)와 날짜·장소 같은 행사 사실 정보만** 옮기고,
연락처·결제 정보는 어떤 페이지에도 싣지 않습니다.

상세 페이지 작성 절차는 [이전 워크샵 회차 추가](#이전-워크샵-회차-추가-workshops)를 따르되,
완성 예시는 `workshops/2026/2nd/index.html` 을 참고하면 됩니다.

## 로고 자산 (assets/logos/)

원본은 `assets/logos/logo-download/` 의 SVG 6종(1a/2a/가로형 × positive/reverse)이며,
여기서 파생본을 만들어 두었습니다. **positive = 흰 배경용, reverse = 어두운 배경용.**

| 폴더 | 형식 | 용도 |
|---|---|---|
| `assets/logos/png/` | 투명 배경 PNG (원본의 4배 해상도) | PPT에 바로 붙여넣기, 웹 |
| `assets/logos/ai/` | .ai (PDF 기반 벡터) | Illustrator에서 바로 열기 |
| `assets/logos/favicon/` + 루트 `favicon.ico` | 512/180/32/16 PNG + ico | 브라우저 탭 아이콘 |

- 홈페이지 헤더 로고: `RoL-TC_1a_positive` (다섯 페이지 공통, `.logo img` 높이 46px)
- 파비콘: `RoL-TC_2a_positive` 의 타일+빨간 점 영역을 정사각 크롭한 것
- 로고 폰트: Archivo(900/800), IBM Plex Mono(500). 이 머신에는 `~/.local/share/fonts/rlr-logo/` 에 설치되어 있습니다.
- 파생본 재생성 방법: 원본 SVG를 수정한 뒤, 헤드리스 크롬으로 PNG(`--screenshot` + `--force-device-scale-factor=4` + `--default-background-color=00000000`)와 .ai(`--print-to-pdf`, .ai는 PDF 기반이라 확장자만 .ai로 저장)를 뽑습니다. 원본 SVG는 텍스트가 폰트를 참조하므로 위 폰트가 설치된 환경에서 변환해야 글자가 정확히 나옵니다.

## 회원 명단 관리

회원 명단은 아래 구글 시트에서 관리합니다. (구글 계정 권한이 있어야 열립니다.)

- 회원 명단 시트: https://docs.google.com/spreadsheets/d/1JMILObRebTsnhCfi1an9dCn7NACX7ZlrtWx05LlOUWw/edit?gid=1224316441

## 로컬에서 확인하는 법

빌드 과정이 없으므로 파일을 브라우저로 바로 열면 됩니다.

```bash
# 브라우저에서 직접 열기
file:///mnt/HDD1/Workspace/src/Project/RobotLearningResearch/index.html

# 또는 간이 서버 (탭 이동까지 실제 배포와 같은 조건)
cd /mnt/HDD1/Workspace/src/Project/RobotLearningResearch && python3 -m http.server 8000
```

## 배포 (이미 공개됨)

사이트는 GitHub Pages 로 서비스 중입니다.

- 공개 주소: https://gist-ailab.github.io/rol-tc-kros/
- 소스: `gist-ailab/rol-tc-kros` 레포의 `main` 브랜치 루트
- **`main` 에 푸시하면 자동으로 다시 빌드됩니다.** 보통 1분 안에 반영됩니다.

반영이 안 되면 GitHub 레포의 **Actions** 탭에서 `pages build and deployment` 워크플로가
실패하지 않았는지 확인하세요. 배포 상태는 터미널에서도 볼 수 있습니다.

```bash
gh api repos/gist-ailab/rol-tc-kros/pages/builds/latest --jq '{status:.status, error:.error.message}'
curl -sL -o /dev/null -w "%{http_code}\n" https://gist-ailab.github.io/rol-tc-kros/
```

> 레포 이름을 다시 바꾸면 공개 주소도 함께 바뀝니다. 옛 주소는 한동안 새 주소로 자동 연결되지만,
> 이 문서와 `README.md` 의 주소 표기도 같이 고쳐 주세요.
