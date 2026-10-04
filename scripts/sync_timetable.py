#!/usr/bin/env python3
"""Render the published, public-only timetable CSV into marked home-page regions."""

import argparse
import csv
import difflib
import html
import io
import json
import re
import sys
from pathlib import Path
from urllib.request import urlopen


CONFIG = Path(__file__).with_name("timetable.config.json")
COLUMNS = ("워크샵ID", "시작", "종료", "내용", "발표자/진행")
PRIVATE_HEADERS = ("연락처", "전화", "휴대", "이메일", "메일", "email", "phone", "등록비", "입금")
PHONE = re.compile(r"(?<!\d)01\d-?\d{3,4}-?\d{4}(?!\d)")
HANGUL = re.compile(r"[가-힣]")
UNDECIDED = {"tbd", "tba", "미정", "추후", "추후 공지", "-"}


class SyncError(Exception):
    def __init__(self, message, code=1):
        super().__init__(message)
        self.code = code


def clean_value(value):
    value = " ".join(value.split())
    return "" if value.casefold() in UNDECIDED else value


def parse_csv(data, wsid):
    try:
        reader = csv.reader(io.StringIO(data.decode("utf-8-sig"), newline=""), strict=True)
        header = next(reader)
    except StopIteration:
        raise SyncError("CSV에 머리글이 없습니다.")
    except (UnicodeDecodeError, csv.Error) as exc:
        raise SyncError(f"CSV를 읽을 수 없습니다: {exc}") from exc

    for column in header:
        if any(word in column.casefold() for word in PRIVATE_HEADERS):
            raise SyncError(f"개인정보 열이 있습니다 (1행: {column}).", 2)
    raw_rows = []
    try:
        for row in reader:
            row_number = reader.line_num
            for cell in row:
                if "@" in cell:
                    raise SyncError(f"개인정보 형태의 이메일이 있습니다 ({row_number}행).", 2)
                if PHONE.search(cell):
                    raise SyncError(f"개인정보 형태의 휴대전화가 있습니다 ({row_number}행).", 2)
            if row:
                raw_rows.append((row_number, row))
    except csv.Error as exc:
        raise SyncError(f"CSV를 읽을 수 없습니다 ({reader.line_num}행): {exc}") from exc

    if tuple(header) != COLUMNS:
        raise SyncError("CSV 머리글은 워크샵ID, 시작, 종료, 내용, 발표자/진행 순서여야 합니다.")
    selected = []
    matched = False
    for row_number, row in raw_rows:
        if len(row) != len(COLUMNS):
            raise SyncError(f"열 개수가 맞지 않습니다 ({row_number}행).")
        values = dict(zip(COLUMNS, (clean_value(cell) for cell in row)))
        if values["워크샵ID"] == wsid:
            matched = True
            if values["내용"] or values["발표자/진행"]:
                selected.append(values)
    if not matched:
        raise SyncError(f"워크샵ID {wsid!r}에 맞는 행이 없습니다.")
    return selected


def classify(title, speaker, talk_number):
    lowered = title.casefold()
    for words, badge_class, label in (
        (("등록",), "badge-open", "등록"),
        (("개회",), "badge-open", "개회"),
        (("폐회",), "badge-open", "폐회"),
        (("휴식", "coffee", "break", "브레이크"), "badge-break", "휴식"),
        (("석식", "만찬", "저녁", "dinner"), "badge-break", "만찬"),
        (("교류", "세션"), "badge-discussion", "교류"),
        (("토론", "질의", "q&a", "패널", "네트워킹"), "badge-discussion", "토론"),
        (("랩투어", "투어", "tour"), "badge-discussion", "랩투어"),
    ):
        if any(word in lowered for word in words):
            return badge_class, label, False
    return "badge-talk", f"발표 {talk_number}", True


def speaker_parts(value):
    if "/" in value:
        affiliation, person = (part.strip() for part in value.split("/", 1))
        name, _, position = person.partition(" ")
        return name, " · ".join(part for part in (position, affiliation) if part)
    parts = [part.strip() for part in value.split("·")]
    return parts[0], " · ".join(part for part in parts[1:] if part)


def render(rows):
    program = []
    speakers = []
    talk_count = 0
    for row in rows:
        title, speaker = row["내용"], row["발표자/진행"]
        badge_class, badge, is_talk = classify(title, speaker, talk_count + 1)
        if is_talk:
            talk_count += 1

        start, end = row["시작"], row["종료"]
        time_cell = (f'<td class="time-cell">{html.escape(start + ("–" + end if end else ""))}</td>'
                     if start else '<td class="time-cell tbd">미정</td>')
        if title:
            escaped_title = html.escape(title)
            if not HANGUL.search(title):
                escaped_title = f"<em>{escaped_title}</em>"
            title_cell = f'<div class="talk-title">{escaped_title}</div>'
        else:
            title_cell = '<div class="talk-title tbd">발표 제목 추후 공지</div>'

        program.extend((
            "        <tr>",
            f"          {time_cell}",
            "          <td>",
            f'            <span class="type-badge {badge_class}">{html.escape(badge)}</span>',
            f"            {title_cell}",
        ))
        if speaker:
            name, affiliation = speaker_parts(speaker)
            program.append(f'            <div class="talk-speaker"><strong>{html.escape(name)}</strong>'
                           + (" · " + html.escape(affiliation) if affiliation else "") + "</div>")
        elif is_talk:
            program.append('            <div class="talk-speaker tbd">발표자 추후 공지</div>')
        program.extend(("          </td>", "        </tr>"))

        if is_talk:
            if speakers:
                speakers.append("")
            if speaker:
                name, affiliation = speaker_parts(speaker)
                speakers.extend((
                    '      <div class="speaker-card confirmed">',
                    f'        <div class="sc-top"><span class="sc-num">{talk_count:02d}</span><span class="sc-status status-confirmed">확정</span></div>',
                    f'        <div class="sc-name">{html.escape(name)}</div>',
                    f'        <div class="sc-affil">{html.escape(affiliation)}</div>',
                ))
            else:
                speakers.extend((
                    '      <div class="speaker-card tbd-card">',
                    f'        <div class="sc-top"><span class="sc-num">{talk_count:02d}</span><span class="sc-status status-expected">예정</span></div>',
                    '        <div class="sc-name tbd">발표자 추후 공지</div>',
                    '        <div class="sc-affil tbd">소속 미정</div>',
                ))
            speakers.extend((
                (f'        <div class="sc-title">{html.escape(title)}</div>' if title
                 else '        <div class="sc-title tbd-title">발표 주제 추후 공지</div>'),
                "      </div>",
            ))

    count_chip = (f'<span class="value">발표 {talk_count}편</span>' if talk_count
                  else '<span class="value tbd">모집 예정</span>')
    return {"program": program, "speakers": speakers, "talkcount": ["          " + count_chip]}, talk_count


def replace_regions(source, regions):
    newline = "\r\n" if "\r\n" in source else "\n"
    result = source
    for name, lines in regions.items():
        begin = f"<!-- timetable:{name}:begin -->"
        end = f"<!-- timetable:{name}:end -->"
        if result.count(begin) != 1 or result.count(end) != 1:
            raise SyncError(f"{name} 생성 구역 표지가 정확히 한 쌍이어야 합니다.")
        body_start = result.index(begin) + len(begin)
        body_end = result.index(end)
        if body_end <= body_start:
            raise SyncError(f"{name} 생성 구역 표지 순서가 잘못되었습니다.")
        indent = {"program": "        ", "speakers": "      ", "talkcount": "          "}[name]
        body = newline + newline.join(lines) + newline + indent
        result = result[:body_start] + body + result[body_end:]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--csv", type=Path, help="게시 CSV의 로컬 파일")
    source.add_argument("--url", help="웹_시간표 탭의 게시 CSV 주소")
    parser.add_argument("--wsid", help="대상 워크샵ID")
    parser.add_argument("--page", type=Path, default=Path("index.html"))
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        wsid = args.wsid or config["wsid"]
        url = args.url or (None if args.csv else config["csv_url"])
        if not args.csv and not url:
            raise SyncError("CSV 주소가 비어 있습니다. scripts/timetable.config.json의 csv_url을 채우거나 --csv/--url을 지정하세요.")
        if args.out and args.out.resolve() == args.page.resolve():
            raise SyncError("--out은 --page와 다른 경로여야 합니다.")
        data = args.csv.read_bytes() if args.csv else urlopen(url, timeout=30).read()
        rows = parse_csv(data, wsid)
        original = args.page.read_bytes()
        page = original.decode("utf-8")
        regions, talk_count = render(rows)
        updated = replace_regions(page, regions).encode("utf-8")
        changed = updated != original
        if args.check:
            diff = difflib.unified_diff(
                page.splitlines(keepends=True), updated.decode("utf-8").splitlines(keepends=True),
                fromfile=str(args.page), tofile=str(args.out or args.page),
            )
            sys.stdout.writelines(diff)
        elif args.out:
            args.out.write_bytes(updated)
        elif changed:
            args.page.write_bytes(updated)
        print(f"행 {len(rows)}개 / 발표 {talk_count}편 / 변경 {'있음' if changed else '없음'}")
        return 0
    except SyncError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return exc.code
    except (OSError, UnicodeError, ValueError, KeyError) as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
