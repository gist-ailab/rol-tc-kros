# 내부 관리 문서 (MAINTAINERS)

이 문서는 로봇학습연구회 웹사이트를 **관리하는 사람(내부자)을 위한** 운영 안내서입니다.
사이트 소개는 `README.md` 에 있고, 실제 수정 절차는 전부 이 문서에 모여 있습니다.
클로드 코드로 작업할 때도 이 문서를 기준으로 삼으면 됩니다 (`CLAUDE.md` 가 이 문서를 가리킵니다).
지금 무엇이 되어 있고 무엇이 미정인지는 `STATUS.md` 에 정리해 두었습니다.

> ℹ️ 이 레포는 **공개** 상태이며 사이트가 https://gist-ailab.github.io/rol-tc-kros/ 에서 서비스 중입니다.
> 이 문서도 함께 공개되어 있으니, 개인정보나 비공개 자료를 적지 마세요.
> `main` 에 푸시하면 1분 내외로 사이트에 반영됩니다.

## 사진 올리는 법 — 회차별 서브탭 운영

행사 사진은 `photos/` 페이지에 **워크샵 회차별 서브탭**으로 게시합니다.
회차마다 탭 하나와 패널 하나가 짝을 이루고, **가장 최근 회차를 맨 앞에** 둡니다. 맨 앞 탭이 처음 열립니다.
각 패널에는 구글 포토 슬라이드쇼(publicalbum 위젯)와 `구글 포토 앨범에서 보기` 버튼이 들어갑니다.

**운영 방식 (인수인계 핵심):** 관리자가 구글 포토 **공유 앨범 주소**를 전달합니다.
`https://photos.app.goo.gl/...` 와 `https://photos.google.com/share/...?key=...` 둘 다 됩니다(링크 공유가 켜져 있어야 함).

**새 회차 탭 추가 (예: 2026 제3회, 2026-10-27 적용):**

1. 사진 주소를 뽑습니다. 사진 수 제한은 없고 앨범 전체를 넣습니다.
   ```bash
   python3 scripts/album_urls.py "<공유 주소>" --objects    # 마지막 줄에 "사진 N장" 이 나옵니다
   ```
2. `photos/index.html` 에서 가장 최근 회차의 버튼(`.subtab-btn`)과 패널(`.subtab-panel`)을 **통째로 복사해 그 앞에** 붙입니다.
3. 복사본에서 바꿀 값:
   - `data-subtab` / `data-panel`: 같은 문자열로 (`2026-3rd` 형식)
   - 탭 라벨: `2026 제3회` 형식
   - `<h3>`, `aria-label`, 위젯의 `data-title`: **`20XX년 제 X회 로봇학습연구회 워크샵`** 형식
   - 위젯의 `data-link` 와 버튼의 `href`: 공유 주소
   - 위젯 안의 `<object>` 줄: 1단계 출력으로 전부 교체
4. 로컬 미리보기(`bash scripts/preview.sh`)에서 탭 전환과 슬라이드쇼 재생을 확인하고 푸시합니다.

**앨범을 고쳤을 때 (사진 추가·삭제):** 위젯은 앨범을 자동으로 따라가지 않습니다. 1단계를 다시 실행해
그 회차 위젯의 `<object>` 줄만 통째로 바꿉니다. 지운 사진의 옛 주소도 한동안 열리므로, 빼는 기준은
"새 목록에 없는 주소"입니다(2026-10-27 제3회 40장 → 30장 사례).

회차 상세 페이지(`workshops/<연도>/<회차>/`)의 사진 섹션도 같은 주소에 `=w800` 을 붙인 `<img>` 로 만듭니다(`workshops/2026/2nd/` 참고).

## 내용 수정하는 법

### 홈 — 워크샵 정보 채우기 (`index.html`)

홈은 **다가오는 한 회차**만 보여 줍니다. 회차마다 바뀌는 값의 위치는 아래 "회차가 끝난 뒤" 절의 표에 모아 두었습니다.
값이 아직 정해지지 않았으면 `추후 공지` 표기와 `tbd` 스타일을 씁니다.

홈에는 발표자 카드 섹션이 없습니다. 프로그램 표와 내용이 완전히 겹쳐서 2026-10-06에 뺐습니다.
발표자 정보는 프로그램 표의 발표 행에만 적습니다. (회차 상세 페이지의 발표자 카드는 그대로 둡니다.)

### 시간표 반영 (시트 → 로컬 확인 → 배포)

홈의 프로그램 표 본문과 히어로 발표 칩은 `index.html` 의 `timetable:` 주석 표지 안에서
`scripts/sync_timetable.py` 가 생성합니다. 발표자 카드 표지(`timetable:speakers`)는 선택 사항이라, 표지가 없으면 건너뜁니다. 시트는 공개 사이트에서 직접 읽지 않습니다.
`scripts/timetable.config.json` 의 `csv_url` 에는 **`웹_시간표` 탭 하나만 웹에 게시한 CSV 주소**를 넣습니다.
파일 전체 게시 주소나 개인정보가 든 CSV는 쓰지 마세요. 기본 워크샵ID는 `timetable.config.json` 의 `wsid` 입니다(지금 `26-3차`).
CSV 머리글은 `워크샵ID,시작,종료,내용,발표자/진행` 이고, 메인 발표와 따로 세고 싶은 발표(교류세션 등)는 여섯째 열 `세션` 에 세션 이름을 적습니다.
히어로 칩은 "메인세션 N편 · <세션 이름> M편" 으로 바뀝니다. 발표 제목 칸이 `TBD` 면 "발표 제목 추후 공지" 로 나옵니다.
`csv_url` 이 비어 있는 동안(2026-10 현재)은 시트에서 받은 CSV를 `--csv` 로 넣었습니다. 26-3차 CSV 사본은 간사 작업 폴더(`~/로학연-간사/웹시간표/`)에 있습니다.

1. 시트의 `WS_<워크샵ID>` 탭에 시간표를 작성하고 메뉴 **시간표 → 웹 게시용 탭 갱신**을 실행합니다.
2. `python3 scripts/sync_timetable.py --check` 로 바뀔 내용을 확인합니다.
3. `python3 scripts/sync_timetable.py` 로 `index.html` 을 갱신합니다.
4. `bash scripts/preview.sh` 로 띄운 `http://localhost:8000/` (포트가 사용 중이면 8001)을 로컬 브라우저에서 확인합니다.
5. 이상이 없으면 커밋 후 `main` 에 푸시하여 공개 배포합니다. **로컬 확인 전에는 `main` 에 푸시하지 않습니다.**

게시 주소를 설정하기 전에는 `--csv <파일>` 로 로컬 CSV를 지정해 같은 절차를 시험할 수 있습니다.
`--out <경로>` 는 원본을 그대로 두고 별도 HTML을 만들며, `--check` 는 파일을 쓰지 않습니다.
검증은 `python3 -m unittest discover -s scripts/tests -v` 로 실행합니다.

### 이전 워크샵 회차 추가 (`workshops/`)

바로 아래 "회차가 끝난 뒤" 절의 A 항목을 따릅니다. 완성 예시는 `workshops/2026/2nd/index.html` 입니다.

### 회차가 끝난 뒤 — 아카이브 만들고 홈을 다음 회차로 바꾸기

같은 디자인을 그대로 이어 쓰는 절차입니다. 새 마크업을 짜지 말고 **기존 페이지를 복사해 값만 바꿉니다.**

**A. 끝난 회차를 아카이브로 (예: 2026 제3회)**
1. `workshops/2026/2nd/` 폴더를 `workshops/2026/3rd/` 로 복사합니다. 경로 깊이가 같으므로 `../../../` 상대 경로는 그대로 둡니다.
2. 복사본의 `<title>`, 히어로 제목(`2026년 제 3회<br>로봇학습연구회 <em>워크샵</em>`), 일시·장소 칩, 캘린더 링크(`events/2026-3rd.ics`),
   프로그램 표, 발표자 카드, 행사 정보, 사진 섹션을 끝난 회차 값으로 채웁니다.
   프로그램 표는 홈의 `timetable:program` 표지 안 내용을 그대로 옮기면 됩니다(행사 직전 최종본).
3. `workshops/index.html` 의 `2026 · 2nd` 카드를 복사해 **그 앞에** 붙이고 `href`·회차·날짜·장소를 바꿉니다.
4. `photos/index.html` 에 그 회차 탭이 없으면 위 "사진 올리는 법" 으로 추가합니다.

**B. 홈(`index.html`)을 다음 회차로**

| 바꿀 것 | 위치 |
|---|---|
| 페이지 제목 | `<title>`, `.hero-eyebrow` (`2026년도 제3회 워크샵`) |
| 일시 | 첫 `.meta-chip` 의 `.value` |
| 캘린더 | 같은 칩의 `.cal-add-item` 네 개: Outlook 두 개(오프셋 포함 ISO), 구글(UTC), `.ics` 경로 |
| `.ics` 파일 | `events/2026-3rd.ics` 를 복사해 `events/<연도>-<회차>.ics` 로. UID·SUMMARY·LOCATION·DTSTART/DTEND(UTC)를 바꿉니다 |
| 장소 | 둘째 `.meta-chip` 의 `.value`, 네이버지도(`naver.me` 공유 주소), TMAP(좌표) |
| 발표 수 | `timetable:talkcount` 표지 (시간표 동기화가 씁니다) |
| 참석 등록 버튼 | 히어로의 `워크숍 참석 등록하기 ↗` `href` (참석 조사 구글 폼. 폼을 새로 만들지 않고 제목만 바꿔 쓰면 주소가 같습니다) |
| 프로그램 | `timetable:program` 표지 (시간표 동기화) |
| 행사 정보 | `행사 정보` 절의 일시·장소·주소·주관·등록(KROS 등록 페이지 링크)·발표 신청·문의 |
| 시간표 설정 | `scripts/timetable.config.json` 의 `wsid` 를 새 워크샵ID(`27-1차` 등)로 |

다음 회차 정보가 아직 없으면 위 값을 `추후 공지` 로 비워 둡니다. 지난 회차 값을 남겨 두지 않습니다.

**C. 마무리**: 로컬 미리보기로 다섯 페이지 탭 이동과 칩 팝업을 확인하고, `python3 -m unittest discover -s scripts/tests` 통과 후 푸시합니다.
`STATUS.md` 의 회차 행도 갱신합니다. 사진·카드·아카이브는 모두 **가장 최근 회차가 맨 앞**입니다.

### 공통 디자인 수정 (`assets/style.css`)

색·폰트·헤더·탭·푸터는 네 페이지가 `assets/style.css` 하나를 공유합니다.
색상을 바꾸려면 파일 상단 `:root` 의 CSS 변수만 수정하면 전체에 적용됩니다.
링크는 반드시 **상대 경로**로 작성합니다 (`/` 로 시작하는 절대 경로 금지 — 프로젝트 페이지 하위 경로에서 깨집니다).

## 스타일·스크립트를 고친 뒤 (캐시 무효화) — 빠뜨리기 쉬움

`assets/style.css` 나 `assets/calendar-popup.js` 를 고쳤다면, **다섯 페이지의 버전 표시를 함께 올려야 합니다.**

각 페이지 `<head>` 와 하단에 다음처럼 버전이 붙어 있습니다.

```html
<link rel="stylesheet" href="assets/style.css?v=20260831b">
<script src="assets/calendar-popup.js?v=20260831b"></script>
```

`?v=` 뒤의 값을 오늘 날짜 기준으로 바꾸고(예: `20260901a`), **다섯 페이지 모두 같은 값**으로 맞춥니다.

```bash
cd /mnt/HDD1/Workspace/src/Project/RobotLearningResearch
grep -rl "?v=20260831b" --include="*.html" . | xargs sed -i 's/?v=20260831b/?v=20260901a/g'
grep -rho "?v=[0-9a-z]*" --include="*.html" . | sort -u   # 하나로 통일됐는지 확인
```

**왜 필요한가**: 브라우저는 스타일 파일을 한동안 저장해 두고 재사용합니다. 주소가 그대로면 새 파일을
받아가지 않아서, 새 HTML 에 옛 스타일이 입혀진 채로 보입니다. 실제로 일정 추가 팝업이 스타일 없이
아이콘만 거대하게 뜨는 사고가 있었습니다. 로컬에서는 멀쩡하고 배포본만 이상하면 대개 이 문제입니다.

## 히어로 사선 마감을 건드릴 때

히어로 하단의 사선은 `.hero::after` 가 배경색 삼각형을 덮어 그리는 방식입니다.
**`.hero` 에 `clip-path` 를 걸지 마세요.** 히어로 밖으로 나오는 자식 요소(일정 추가 팝업 등)까지 잘려서,
팝업이 첫 줄만 보이는 문제가 생깁니다.

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
- 네이버지도: 정확한 장소 공유 링크(`naver.me/...`)가 있으면 그것을 쓰고, 없으면 `https://map.naver.com/v5/search/<장소>`
- TMAP: 좌표를 알면 `tmap://route?goalname=<장소>&goalx=<경도>&goaly=<위도>` 로 바로 길안내(제3회 홈이 이 방식), 모르면 `tmap://search?name=<장소>` — **앱이 설치된 모바일에서만 열립니다.** 데스크톱에서 눌러도 반응이 없는 것이 정상입니다.

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
   `python3 scripts/album_urls.py "<공유 주소>"` 가 사진 항목만 앨범 순서대로 뽑습니다(`--objects` 를 주면 붙여 넣을 마크업으로 출력).
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
- 2026 제3회부터: 회원 명단 시트의 `WS_<워크샵ID>` 탭(시간표·정산). 회차별 운영 시트를 따로 만들지 않습니다.
- 홈에 마지막으로 게시한 프로그램 표(`timetable:program` 표지 안)가 가장 정확한 최종본입니다. 아카이브는 이것을 옮깁니다.
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

## 명단·참석기록 관리 스크립트 (이 저장소 바깥)

회원 명단과 참석기록을 다루는 구글 시트 Apps Script 는 개인정보가 오가는 코드라 이 공개 저장소에 두지 않습니다.

- 위치: 간사 작업 폴더 `~/로학연-간사/` (연구실 워크스테이션 로컬). 정본은 `시트운영/통합/Code.gs` 이고 시트에 붙은 Apps Script 프로젝트에 올라가 있습니다.
- 시트 사용법·회원 등록·회차 열기·드라이브 폴더 구조·참가확인서 발급은 그 폴더의 `README.md`(간사 인수인계)에 있습니다.
- 옛 경로 `/mnt/HDD1/Workspace/src/Project/rlr-sheets-ops/` 는 `~/로학연-간사/시트운영/` 을 가리키는 심링크입니다.
- 기능: 가입접수 반영, 폼 응답을 참석기록으로 이관, 소속·직위 스냅샷 채우기, 워크샵 운영 탭 생성, 수식 복구

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
