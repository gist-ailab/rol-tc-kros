# 클로드 코드 작업 안내 — rol-tc-kros (로봇학습연구회 웹사이트)

이 레포는 로봇학습연구회 워크샵 웹사이트다. 순수 HTML/CSS/바닐라 JS 정적 사이트이며 빌드 과정이 없다.
공개 저장소이고 `main` 푸시가 곧 배포다 (https://gist-ailab.github.io/rol-tc-kros/).

**작업 전에 반드시 읽어라.**
- `STATUS.md` — 지금 무엇이 되어 있고 무엇이 미정인지, 이미 내려진 결정은 무엇인지
- `MAINTAINERS.md` — 사진 게시, 내용 수정, 회차 추가, 폼 연결, 배포의 실제 절차

## 페이지 구성

`index.html`(홈·다가오는 회차), `workshops/index.html`(아카이브 목록),
`workshops/<연도>/<회차>/index.html`(회차 상세), `photos/index.html`(회차별 서브탭 갤러리),
`join/index.html`(가입신청). 상단 탭은 다섯 페이지 공통이며 라벨은 영문
`Home` / `Workshops` / `Photos` / `Membership` 이다.

## 반드시 지킬 것

- **링크는 전부 상대 경로.** `/` 로 시작하는 절대 경로는 프로젝트 페이지(`/rol-tc-kros/`) 배포에서 깨진다.
  하위 폴더 깊이에 맞게 `../` 를 붙인다.
- **공통 스타일은 `assets/style.css` 하나다.** 페이지별 `<style>` 블록을 새로 만들지 말고 공통 파일을 고친다.
  색은 `:root` 의 토큰(`--accent`, `--hero-*`, `--bg*`)을 쓰고 값을 직접 박지 않는다.
- **`assets/style.css` 나 `assets/calendar-popup.js` 를 고치면 캐시 무효화 값을 올린다.**
  다섯 페이지의 `?v=YYYYMMDDx` 를 같은 값으로 바꾼다. 이걸 빼먹으면 방문자 브라우저가 옛 CSS 를 계속 써서
  새 마크업에 옛 스타일이 입혀진다(실제로 팝업이 깨져 보이는 사고가 났다).
- **확정되지 않은 정보를 지어내지 않는다.** 일시·장소·발표자·이메일이 미정이면 `추후 공지` 표기와 `tbd` 스타일을 쓴다.
- **개인정보를 넣지 않는다.** 공개 저장소다. 연락처·이메일·참가자 명단은 사이트에도 문서에도 두지 않는다.
- **`_reference/` 는 디자인 참고용 원본이므로 수정하지 않는다** (`.gitignore` 로 제외되어 있다).

## 이 저장소의 함정 (실제로 사고가 났던 것)

- **`.hero` 에 `clip-path` 를 걸지 마라.** 하단 사선 마감을 `clip-path` 로 처리하면 히어로 밖으로 나오는
  자식 요소(일정 추가 팝업 등)까지 잘린다. 지금은 `.hero::after` 로 배경색 삼각형을 덮어 그리고,
  `.hero` 에는 `position: relative; z-index: 1` 만 준다.
- **구글 포토는 iframe 임베드가 막혀 있다.** `photos/index.html` 은 publicalbum.org 위젯으로 우회한다.
  마크업을 새로 짜지 말고 기존 블록을 복사해서 쓴다.
- **Outlook 일정 링크는 계정 종류에 따라 주소가 다르다.** 개인은 `outlook.live.com`,
  회사·학교는 `outlook.office.com`. 한쪽만 걸면 로그인 안 된 사용자는 홍보 페이지로 튕긴다.
  일시 칩의 팝업(`assets/calendar-popup.js`)에서 둘 다 제공하고 `.ics`(`events/`)도 함께 둔다.
- **캘린더 링크의 시간 표기.** 구글 캘린더는 UTC(`YYYYMMDDTHHMMSSZ`), Outlook 은 오프셋 포함
  ISO(`2026-10-23T13:00:00+09:00`) 를 쓴다. 한국시간 13:00~18:00 은 UTC 로 `T040000Z/T090000Z` 다.

## 확인 방법

빌드가 없으므로 파일을 브라우저로 바로 열면 된다.
배포본을 확인할 때는 브라우저 캐시 때문에 로컬과 다르게 보일 수 있으니 캐시를 비운 상태로 봐야 한다.

## 이 저장소 바깥

회원 명단·참석기록을 다루는 구글 시트 Apps Script 는 개인정보 때문에 여기 두지 않는다.
`/mnt/HDD1/Workspace/src/Project/rlr-sheets-ops/` 에 있다.
