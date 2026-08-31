# 내부 관리 문서 (MAINTAINERS)

이 문서는 로봇학습연구회 웹사이트를 **관리하는 사람(내부자)을 위한** 운영 안내서입니다.
사이트 소개는 `README.md` 에 있고, 실제 수정 절차는 전부 이 문서에 모여 있습니다.
클로드 코드로 작업할 때도 이 문서를 기준으로 삼으면 됩니다 (`CLAUDE.md` 가 이 문서를 가리킵니다).

> ⚠️ 현재 레포는 **비공개**입니다. 공개로 전환하면 이 문서도 함께 공개되므로,
> 공개 전에 아래 [공개 전 체크리스트](#공개-전-체크리스트)를 확인하세요.

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

## 가입신청 폼 연결 (`join/index.html`)

1. 구글 폼을 만들고, 폼의 **응답 탭 → 스프레드시트에 연결**에서 아래 회원 명단 시트를 응답 대상으로 지정합니다.
   그러면 가입신청 응답이 시트에 자동으로 쌓입니다.
2. 폼의 **[보내기] → [`<>` 임베드]** 에서 임베드 주소(`.../viewform?embedded=true`)를 복사합니다.
3. `join/index.html` 의 플레이스홀더 `GOOGLE_FORM_URL_HERE` **두 곳**을 교체합니다.
   - 주석 처리된 폼 임베드 블록(`.form-embed`) 안 `<iframe>` 의 `src` → 임베드 주소
   - `새 창에서 열기` 버튼의 `href` → 일반 폼 주소(`.../viewform`)
4. `가입신청 폼 준비 중` 안내 박스(`.form-placeholder`)를 주석 처리하고 임베드 블록의 주석을 해제합니다.
   자바스크립트 없이 주석 전환만으로 동작합니다.

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

## 공개 전 체크리스트

디버그가 끝나면 공개합니다. **비공개 레포에서는 Pages 를 켤 수 없다는 것을 확인했으므로**(무료 조직 요금제),
공개 전환이 곧 배포 시점입니다.

1. 네 페이지를 로컬에서 열어 내용·링크·오탈자를 최종 확인합니다.
2. 이 문서(`MAINTAINERS.md`)도 함께 공개된다는 점을 결정합니다.
   시트 링크는 구글 권한이 없으면 열리지 않지만, 문서 ID 노출이 싫으면 이 문서를 레포 밖으로 옮깁니다.
3. 기본 브랜치를 `main` 으로 만듭니다: `git push origin init-site:main` 후
   GitHub **Settings → General → Default branch** 를 `main` 으로 변경합니다.
4. 레포를 공개로 전환합니다: **Settings → General → Danger Zone → Change visibility → Public**
   (또는 `gh repo edit gist-ailab/kros-rlr --visibility public`)
5. Pages 를 켭니다: **Settings → Pages → Deploy from a branch → `main` / `/ (root)`**
6. 몇 분 뒤 https://gist-ailab.github.io/kros-rlr/ 에서 사이트를 확인합니다.
