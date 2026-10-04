"""Checks for the public timetable import and marked HTML replacement."""

import csv
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import sync_timetable


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/sync_timetable.py"
SAMPLE = ROOT / "scripts/tests/sample_timetable.csv"
PAGE = ROOT / "index.html"
REGION = re.compile(
    rb"(<!-- timetable:(program|speakers|talkcount):begin -->).*?(<!-- timetable:\2:end -->)",
    re.DOTALL,
)


def run_sync(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *map(str, args)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )


def outside_regions(data):
    return REGION.sub(lambda match: match.group(1) + b"<generated>" + match.group(3), data)


class TimetableSyncTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_page = PAGE.read_bytes()

    @classmethod
    def tearDownClass(cls):
        assert PAGE.read_bytes() == cls.original_page, "테스트가 실제 index.html을 변경했습니다"

    def test_out_preserves_every_byte_outside_markers_and_renders_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "preview.html"
            result = run_sync("--csv", SAMPLE, "--out", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("행 12개 / 발표 5편 / 변경 있음", result.stdout)
            rendered = output.read_bytes()
            self.assertEqual(outside_regions(rendered), outside_regions(self.original_page))
            self.assertEqual(PAGE.read_bytes(), self.original_page)
            text = rendered.decode("utf-8")
            self.assertIn('<span class="value">발표 5편</span>', text)
            self.assertIn('<span class="type-badge badge-open">등록</span>', text)
            self.assertIn('<span class="type-badge badge-break">휴식</span>', text)
            self.assertIn('<span class="type-badge badge-break">만찬</span>', text)
            self.assertIn('<span class="type-badge badge-discussion">토론</span>', text)
            self.assertIn('<span class="type-badge badge-discussion">랩투어</span>', text)
            self.assertIn('<span class="type-badge badge-discussion">교류</span>', text)
            self.assertIn('<span class="type-badge badge-talk">발표 5</span>', text)
            self.assertEqual(text.count('<div class="speaker-card confirmed">'), 4)
            self.assertEqual(text.count('<div class="speaker-card tbd-card">'), 1)
            self.assertIn('<div class="talk-title"><em>Example Talk Title</em></div>', text)
            self.assertIn('<td class="time-cell">13:00–13:10</td>', text)
            self.assertIn('<td class="time-cell">14:00</td>', text)
            self.assertIn('<td class="time-cell tbd">미정</td>', text)
            self.assertIn('<div class="sc-title tbd-title">발표 주제 추후 공지</div>', text)

    def test_clean_value_collapses_whitespace_and_undecided_values(self):
        self.assertEqual(sync_timetable.clean_value("  예시발표자A  박사과정  "), "예시발표자A 박사과정")
        for value in ("TBD", "tBa", "미정", "추후", "추후   공지", "-"):
            with self.subTest(value=value):
                self.assertEqual(sync_timetable.clean_value(f"  {value}  "), "")
        self.assertEqual(sync_timetable.clean_value("TBD 발표"), "TBD 발표")

    def test_classification_uses_keywords_then_defaults_to_talk(self):
        for title, badge, label in (
            ("교류세션 및 토론", "badge-discussion", "교류"),
            ("세션", "badge-discussion", "교류"),
            ("패널 토론", "badge-discussion", "토론"),
            ("LaB ToUr", "badge-discussion", "랩투어"),
        ):
            with self.subTest(title=title):
                self.assertEqual(sync_timetable.classify(title, "", 1), (badge, label, False))
        self.assertEqual(sync_timetable.classify("Toward Smooth Motion", "", 2),
                         ("badge-talk", "발표 2", True))
        self.assertEqual(sync_timetable.classify("", "예시발표자", 3),
                         ("badge-talk", "발표 3", True))

    def test_sample_skips_row_with_undecided_title_and_speaker(self):
        rows = sync_timetable.parse_csv(SAMPLE.read_bytes(), "26-3차")
        self.assertEqual(len(rows), 12)
        self.assertEqual(sum(not row["내용"] for row in rows), 1)
        self.assertEqual(sum(not row["발표자/진행"] for row in rows), 8)
        only_undecided = "워크샵ID,시작,종료,내용,발표자/진행\n26-3차,13:00,13:10,TBD,미정\n"
        self.assertEqual(sync_timetable.parse_csv(only_undecided.encode(), "26-3차"), [])

    def test_speaker_formats_and_missing_values_render(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "preview.html"
            result = run_sync("--csv", SAMPLE, "--out", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            text = output.read_text(encoding="utf-8")
            self.assertIn('<div class="talk-speaker"><strong>예시발표자A</strong> · 예시직위 · 예시소속A</div>', text)
            self.assertIn('<div class="sc-name">예시발표자A</div>', text)
            self.assertIn('<div class="sc-affil">예시직위 · 예시소속A</div>', text)
            self.assertIn('<div class="talk-speaker"><strong>예시발표자B</strong> · 박사과정 · 예시소속</div>', text)
            self.assertIn('<div class="sc-affil">박사과정 · 예시소속</div>', text)
            self.assertIn('<div class="talk-speaker"><strong>예시발표자C</strong></div>', text)
            self.assertIn('<div class="talk-speaker"><strong>예시발표자D</strong> · 예시소속</div>', text)
            self.assertIn('<div class="sc-affil">예시소속</div>', text)
            self.assertIn('<div class="talk-title tbd">발표 제목 추후 공지</div>', text)
            self.assertIn('<div class="talk-speaker tbd">발표자 추후 공지</div>', text)
            self.assertIn('<span class="sc-status status-expected">예정</span>', text)
            self.assertIn('<div class="sc-name tbd">발표자 추후 공지</div>', text)
            self.assertIn('<div class="sc-affil tbd">소속 미정</div>', text)
            self.assertNotIn('<span class="type-badge badge-open">Toward</span>', text)
            self.assertEqual(text.count('<div class="talk-speaker'), 5)
            self.assertEqual(text.count('<div class="talk-speaker tbd">'), 1)

    def test_second_run_is_identical(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.html"
            second = Path(directory) / "second.html"
            self.assertEqual(run_sync("--csv", SAMPLE, "--out", first).returncode, 0)
            result = run_sync("--csv", SAMPLE, "--page", first, "--out", second)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertIn("변경 없음", result.stdout)

    def test_private_header_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_file = Path(directory) / "private.csv"
            output = Path(directory) / "output.html"
            csv_file.write_text(SAMPLE.read_text(encoding="utf-8").replace(
                "발표자/진행\n", "발표자/진행,이메일\n", 1), encoding="utf-8")
            result = run_sync("--csv", csv_file, "--out", output)
            self.assertEqual(result.returncode, 2)
            self.assertIn("1행", result.stderr)
            self.assertFalse(output.exists())

    def test_private_cells_rejected_without_output(self):
        for private_value in ("test@example.invalid", "010-1234-5678"):
            with self.subTest(private_value=private_value), tempfile.TemporaryDirectory() as directory:
                csv_file = Path(directory) / "private.csv"
                output = Path(directory) / "output.html"
                with csv_file.open("w", encoding="utf-8", newline="") as stream:
                    writer = csv.writer(stream)
                    writer.writerow(("워크샵ID", "시작", "종료", "내용", "발표자/진행"))
                    writer.writerow(("26-3차", "13:00", "13:10", "예시 내용", private_value))
                result = run_sync("--csv", csv_file, "--out", output)
                self.assertEqual(result.returncode, 2)
                self.assertIn("2행", result.stderr)
                self.assertFalse(output.exists())

    def test_private_cell_in_other_workshop_is_also_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_file = Path(directory) / "private.csv"
            output = Path(directory) / "output.html"
            with csv_file.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow(("워크샵ID", "시작", "종료", "내용", "발표자/진행"))
                writer.writerow(("26-3차", "13:00", "13:10", "등록", ""))
                writer.writerow(("다른-회차", "13:10", "13:20", "예시 내용", "test@example.invalid"))
            result = run_sync("--csv", csv_file, "--out", output)
            self.assertEqual(result.returncode, 2)
            self.assertIn("3행", result.stderr)
            self.assertFalse(output.exists())

    def test_unmatched_wsid_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output.html"
            result = run_sync("--csv", SAMPLE, "--wsid", "없는-회차", "--out", output)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(output.exists())

    def test_zero_talks_keep_recruiting_chip(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_file = Path(directory) / "no_talks.csv"
            output = Path(directory) / "output.html"
            csv_file.write_text("워크샵ID,시작,종료,내용,발표자/진행\n26-3차,13:00,13:10,개회,\n", encoding="utf-8")
            result = run_sync("--csv", csv_file, "--out", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("발표 0편", result.stdout)
            self.assertIn('<span class="value tbd">모집 예정</span>', output.read_text(encoding="utf-8"))

    def test_csv_text_is_html_escaped(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_file = Path(directory) / "escaped.csv"
            output = Path(directory) / "output.html"
            with csv_file.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow(("워크샵ID", "시작", "종료", "내용", "발표자/진행"))
                writer.writerow(("26-3차", "13:00", "13:10", "Example <script> & Talk", "예시 발표자 A · 예시 <소속>"))
            result = run_sync("--csv", csv_file, "--out", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            rendered = output.read_text(encoding="utf-8")
            self.assertIn("<em>Example &lt;script&gt; &amp; Talk</em>", rendered)
            self.assertIn("예시 &lt;소속&gt;", rendered)
            self.assertNotIn("<script>", rendered)

    def test_check_prints_diff_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output.html"
            result = run_sync("--csv", SAMPLE, "--out", output, "--check")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("--- index.html", result.stdout)
            self.assertIn("+++ ", result.stdout)
            self.assertFalse(output.exists())
            self.assertEqual(PAGE.read_bytes(), self.original_page)


if __name__ == "__main__":
    unittest.main()
