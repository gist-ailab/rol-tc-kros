#!/usr/bin/env python3
"""구글 포토 공유 앨범에서 슬라이드쇼용 이미지 주소를 뽑는다.

앨범 페이지 HTML에 든 사진 항목(사진 ID + lh3 주소 + 가로·세로)만 골라 앨범 순서대로 출력한다.
앨범 표지·프로필 사진처럼 사진 항목이 아닌 주소는 섞이지 않는다.

    python3 scripts/album_urls.py "<공유 주소>"            # 주소 목록
    python3 scripts/album_urls.py "<공유 주소>" --objects  # photos/index.html 에 붙일 <object> 줄

공유 주소는 photos.app.goo.gl/... 와 photos.google.com/share/...?key=... 둘 다 된다.
"""
import argparse
import re
import sys
import urllib.request

ITEM = re.compile(
    r'\["(AF1Qip[A-Za-z0-9_-]+)",\["(https://lh3\.googleusercontent\.com/pw/[A-Za-z0-9_-]+)",(\d+),(\d+)'
)


def album_photos(url: str) -> list[str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", "replace")
    seen, urls = set(), []
    for photo_id, src, _w, _h in ITEM.findall(html):
        if photo_id in seen:
            continue
        seen.add(photo_id)
        urls.append(src)
    return urls


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("url", help="구글 포토 공유 앨범 주소")
    ap.add_argument("--objects", action="store_true", help="<object> 마크업으로 출력")
    args = ap.parse_args()
    urls = album_photos(args.url)
    if not urls:
        print("사진을 찾지 못했습니다. 링크 공유가 켜져 있는지 확인하세요.", file=sys.stderr)
        return 1
    for u in urls:
        if args.objects:
            print(f'        <object data="{u}=w1920" aria-label="사진"></object>')
        else:
            print(u)
    print(f"사진 {len(urls)}장", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
