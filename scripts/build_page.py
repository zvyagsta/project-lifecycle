"""Build a self-contained reading page (plan, review) from a draft that uses the report style.

Usage:
    python scripts/build_page.py DRAFT.html OUT.html [--md SOURCE.md] [--layout SHOTS_DIR] [--assets DIR]

The draft keeps `@import url("design.css");` and `@import url("plan.css");` in its <style>, so it
also opens beside the style files. The build replaces every such import with the file's content from
the assets folder (default: assets/report-style of this skill), embeds the fonts as data URIs and
drops HTML comments (template notes), so the result works offline as one file.

Checks (exit code 1 on failure):
  * no unfilled {{PLACEHOLDER}} remains;
  * every local link resolves relative to OUT.html;
  * --md: lists words found only in the page or only in the Markdown source, for a human check;
  * --layout: renders 1280 px and 400 px screenshots with Playwright and fails on horizontal scroll.
    Skipped with a message when Playwright or a browser is not available.

Local files only; no network access.
"""

from __future__ import annotations

import argparse
import base64
import html
import re
import sys
from pathlib import Path

from audit import missing_target

SKILL = Path(__file__).resolve().parents[1]
DEFAULT_ASSETS = SKILL / "assets" / "report-style"
IMPORT = re.compile(r'@import\s+url\(\s*["\']?([^"\')]+)["\']?\s*\)\s*;')
COMMENT = re.compile(r"<!--.*?-->\n?", re.S)


def inline_css(name: str, assets: Path) -> str:
    path = assets / name
    if not path.is_file():
        raise SystemExit(f"FAIL: style file not found: {path}")

    def embed(match: re.Match[str]) -> str:
        data = base64.b64encode((assets / match.group(1)).read_bytes()).decode("ascii")
        return f"url(data:font/woff2;base64,{data})"

    return re.sub(r"url\((fonts/[^)]+\.woff2)\)", embed, path.read_text(encoding="utf-8"))


def words(text: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[0-9A-Za-zА-Яа-яЁё]+", text)}


def page_text(page: str) -> str:
    page = re.sub(r"<style.*?</style>|<title>.*?</title>", " ", page, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", page))


def markdown_text(source: str) -> str:
    source = re.sub(r"\]\([^)]*\)", "]", source)
    return re.sub(r"[#*`|>\[\]_-]", " ", source)


def broken_links(page: str, base: Path) -> list[str]:
    return [href for href in re.findall(r'href="([^"]+)"', page) if missing_target(base, href)]


def check_layout(out: Path, shots: Path) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("SKIP layout: Playwright is not installed")
        return True
    shots.mkdir(parents=True, exist_ok=True)
    ok = True
    with sync_playwright() as p:
        browser = None
        for channel in ("chrome", "msedge", None):
            try:
                browser = p.chromium.launch(channel=channel) if channel else p.chromium.launch()
                break
            except Exception:
                continue
        if browser is None:
            print("SKIP layout: no browser found")
            return True
        page = browser.new_page()
        for width in (1280, 400):
            page.set_viewport_size({"width": width, "height": 900})
            page.goto(out.resolve().as_uri())
            page.evaluate("document.fonts.ready")
            scroll = page.evaluate("document.documentElement.scrollWidth")
            page.screenshot(path=str(shots / f"{out.stem}_{width}.png"), full_page=True)
            ok &= scroll <= width
            print(f"{'PASS' if scroll <= width else 'FAIL'} layout {width}px: page is {scroll}px wide")
        browser.close()
    print(f"screenshots: {shots}")
    return ok


def build(draft: Path, out: Path, assets: Path) -> str:
    page, imports = IMPORT.subn(lambda m: inline_css(m.group(1), assets), draft.read_text(encoding="utf-8"))
    if not imports:
        raise SystemExit('FAIL: the draft has no @import url("design.css") to inline')
    page = COMMENT.sub("", page)
    out.write_text(page, encoding="utf-8")
    return page


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("draft", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--md", type=Path, help="Markdown source to compare words with")
    parser.add_argument("--layout", type=Path, help="folder for 1280/400 px screenshots")
    parser.add_argument("--assets", type=Path, default=DEFAULT_ASSETS, help="folder with design.css, plan.css, fonts/")
    args = parser.parse_args()

    page = build(args.draft, args.out, args.assets)
    print(f"built: {args.out} ({round(len(page.encode('utf-8')) / 1024)} KB)")
    ok = True

    left = sorted(set(re.findall(r"\{\{[^}]*\}\}", page)))
    if left:
        ok = False
        print(f"FAIL placeholders: {left[:10]}")

    broken = broken_links(page, args.out.parent)
    ok &= not broken
    print(f"FAIL links: {broken}" if broken else "PASS links")

    if args.md:
        in_page = words(page_text(page))
        in_md = words(markdown_text(args.md.read_text(encoding="utf-8")))
        print(f"words only in page ({len(in_page - in_md)}): {sorted(in_page - in_md)[:40]}")
        print(f"words only in Markdown ({len(in_md - in_page)}): {sorted(in_md - in_page)[:40]}")
        print("Review: labels may differ; lost meaning may not.")

    if args.layout:
        ok &= check_layout(args.out, args.layout)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
