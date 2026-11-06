#!/usr/bin/env python3
"""Export the whole HTML report as one PDF.

Usage:
    python3 -I export_pdf.py <outside-in-review-dir> [--output NAME.pdf]

1. Assembles every page into a single <dir>/print.html: cover + contents,
   then index, architecture, flow-*, backlog, code-quality (and any other
   page), each starting on a new sheet. Ids are prefixed per page and links
   between pages are rewritten to in-document anchors, so they stay
   clickable in the PDF.
2. Checks with headless Chrome that every diagram renders in print.html.
3. Prints it to <dir>/outside-in-review.pdf (A4, print stylesheet of
   assets/report.css), with the same browser as validate_diagrams.py.

Exit code: 0 PDF written, 1 failure, 2 no headless browser found.
"""
from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_diagrams import find_browser, render_page  # noqa: E402

ORDER = ["index.html", "architecture.html", "flow-*.html", "backlog.html", "code-quality.html"]
PRINT_PAGE = "print.html"
HERO = r'<div class="hero">(.*?)</div>'


def ordered_pages(root: Path) -> list[Path]:
    pages: list[Path] = []
    for pattern in ORDER:
        pages += [p for p in sorted(root.glob(pattern)) if p not in pages]
    pages += [p for p in sorted(root.glob("*.html")) if p not in pages and p.name != PRINT_PAGE]
    return pages


def grab(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.S)
    return m.group(1).strip() if m else ""


def rewrite(fragment: str, slug: str, slugs: dict[str, str]) -> str:
    """Prefix ids with the page slug and turn cross-page links into anchors."""
    fragment = re.sub(r'\b(id|aria-labelledby|aria-describedby)="([^"]+)"',
                      lambda m: f'{m.group(1)}="' + " ".join(f"{slug}--{v}" for v in m.group(2).split()) + '"',
                      fragment)

    def href(m: re.Match) -> str:
        target = m.group(1)
        if re.match(r"^[a-z]+:", target):            # http:, mailto:, …
            return m.group(0)
        page, _, anchor = target.partition("#")
        page_slug = slug if page == "" else slugs.get(page)
        if page_slug is None:                         # asset or unknown file: keep
            return m.group(0)
        return f'href="#{page_slug}--{anchor}"' if anchor else f'href="#page-{page_slug}"'

    return re.sub(r'href="([^"]*)"', href, fragment)


def build_print_html(root: Path, pages: list[Path]) -> Path:
    slugs = {p.name: p.stem for p in pages}
    first = pages[0].read_text(encoding="utf-8")
    title = html.unescape(re.sub(r"<[^>]+>", "", grab(r"<title>(.*?)</title>", first)))
    repo = title.rsplit("—", 1)[-1].strip() or root.resolve().parent.name
    cover_hero = grab(HERO, first)

    contents, sections = [], []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        slug = slugs[page.name]
        # Contents label: first part of "<Page> — Outside-In Review — <repo>".
        label = html.unescape(grab(r"<title>(.*?)</title>", text)).split(" — ")[0].strip()
        h1 = html.escape(label or page.stem)
        hero = "" if page == pages[0] else '<div class="hero">' + grab(HERO, text) + "</div>"
        main = grab(r'<main id="main">(.*?)</main>', text)
        contents.append(f'<li><a href="#page-{slug}">{h1}</a></li>')
        sections.append(
            f'<section class="print-page" id="page-{slug}" aria-label="{html.escape(h1)}">\n'
            f'{hero}\n<div class="layout">{rewrite(main, slug, slugs)}</div>\n</section>')

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Outside-In Review — {html.escape(repo)}</title>
  <link rel="stylesheet" href="assets/report.css">
  <script src="assets/vendor/mermaid.min.js" defer></script>
  <script src="assets/diagrams.js" defer></script>
</head>
<body>
<main id="main" class="container">
  <section class="print-page print-cover" aria-label="Cover">
    <div class="hero">{cover_hero}</div>
    <nav class="print-contents" aria-label="Contents">
      <p class="toc__title">Contents</p>
      <ol>{''.join(contents)}</ol>
    </nav>
  </section>
{chr(10).join(sections)}
</main>
</body>
</html>
"""
    out = root / PRINT_PAGE
    out.write_text(doc, encoding="utf-8")
    return out


def print_pdf(browser: str, page: Path, pdf: Path) -> str | None:
    with tempfile.TemporaryDirectory() as profile:
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-first-run",
               "--no-default-browser-check", "--disable-extensions",
               f"--user-data-dir={profile}", "--allow-file-access-from-files",
               "--run-all-compositor-stages-before-draw", "--virtual-time-budget=60000",
               "--no-pdf-header-footer", f"--print-to-pdf={pdf.resolve()}",
               page.resolve().as_uri()]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        except subprocess.TimeoutExpired:
            return "headless browser timed out"
    if not pdf.exists() or pdf.stat().st_size == 0:
        return (proc.stderr.strip().splitlines() or ["PDF not written"])[-1]
    return None


def main() -> int:
    args = sys.argv[1:]
    output = "outside-in-review.pdf"
    if "--output" in args:
        i = args.index("--output")
        output = args[i + 1]
        del args[i:i + 2]
    root = Path(args[0] if args else "outside-in-review")
    pages = ordered_pages(root)
    if not pages:
        print(f"No HTML pages in {root}", file=sys.stderr)
        return 1

    browser = find_browser()
    if browser is None:
        print("No headless Chromium-based browser found (set CHROME_PATH)", file=sys.stderr)
        return 2

    printable = build_print_html(root, pages)
    print(f"assembled {printable} from {len(pages)} pages: {', '.join(p.name for p in pages)}")

    rendered = render_page(browser, printable)
    if isinstance(rendered, str):
        print(f"FAIL {rendered}", file=sys.stderr)
        return 1
    figures = rendered.figures
    failed = [f for f in figures if f.get("data-render") != "ok"]
    if rendered.page.get("data-diagrams") is None or failed:
        for f in failed:
            print(f"FAIL diagram {f.get('id')}: {f.get('data-render-error', 'not rendered')}", file=sys.stderr)
        print("FAIL diagrams do not all render in print.html: fix them before exporting", file=sys.stderr)
        return 1
    print(f"diagrams: {len(figures)}/{len(figures)} rendered")

    pdf = root / output
    error = print_pdf(browser, printable, pdf)
    if error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1
    data = pdf.read_bytes()
    pages_count = len(re.findall(rb"/Type\s*/Page(?!s)", data))
    print(f"OK   {pdf} ({pages_count} pages, {len(data) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
