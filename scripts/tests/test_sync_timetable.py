"""Checks for the public timetable import and marked HTML replacement."""

import csv
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


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
            self.assertIn("행 9개 / 발표 3편 / 변경 있음", result.stdout)
            rendered = output.read_bytes()
            self.assertEqual(outside_regions(rendered), outside_regions(self.original_page))
            self.assertEqual(PAGE.read_bytes(), self.original_page)
            text = rendered.decode("utf-8")
            self.assertIn('<span class="value">발표 3편</span>', text)
            self.assertIn('<span class="type-badge badge-open">등록</span>', text)
            self.assertIn('<span class="type-badge badge-break">휴식</span>', text)
            self.assertIn('<span class="type-badge badge-break">만찬</span>', text)
            self.assertIn('<span class="type-badge badge-discussion">토론</span>', text)
            self.assertIn('<span class="type-badge badge-discussion">랩투어</span>', text)
            self.assertIn('<span class="type-badge badge-talk">발표 3</span>', text)
            self.assertEqual(text.count('<div class="speaker-card confirmed">'), 3)
            self.assertIn('<div class="talk-title"><em>Example Talk Title</em></div>', text)
            self.assertIn('<td class="time-cell">13:00–13:10</td>', text)
            self.assertIn('<td class="time-cell">14:00</td>', text)
            self.assertIn('<td class="time-cell tbd">미정</td>', text)
            self.assertIn('<div class="sc-title tbd-title">발표 주제 추후 공지</div>', text)

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
