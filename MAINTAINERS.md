# 내부 관리 문서 (MAINTAINERS)

이 문서는 로봇학습연구회 웹사이트를 **관리하는 사람(내부자)을 위한** 운영 안내서입니다.
사이트 소개는 `README.md` 에 있고, 실제 수정 절차는 전부 이 문서에 모여 있습니다.
클로드 코드로 작업할 때도 이 문서를 기준으로 삼으면 됩니다 (`CLAUDE.md` 가 이 문서를 가리킵니다).

> ⚠️ 현재 레포는 **비공개**입니다. 공개로 전환하면 이 문서도 함께 공개되므로,
> 공개 전에 아래 [공개 전 체크리스트](#공개-전-체크리스트)를 확인하세요.

## 사진 올리는 법

행사 사진은 `photos/` 페이지에 게시합니다.

1. 이미지 파일을 `photos/img/` 폴더에 넣습니다. 파일명은 `<연도>-<회차>-<번호>.jpg` 관례를 따릅니다.
   (예: `photos/img/2026-1st-01.jpg`)
2. `photos/index.html` 을 엽니다. 파일 안에 주석으로 갤러리 마크업 템플릿이 준비되어 있습니다.
3. 첫 사진을 올릴 때는 `아직 게시된 사진이 없습니다` 빈 상태 박스(`.empty-state`)를 지우거나 주석 처리하고,
   주석 처리된 `.gallery-grid` 블록의 주석을 해제합니다.
4. `<figure>` 블록을 사진 수만큼 복사해서 `src`(파일 경로), `alt`(설명), `<figcaption>`(캡션)을 채웁니다.
5. 로컬 브라우저로 `photos/index.html` 을 열어 확인한 뒤 커밋합니다.

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
