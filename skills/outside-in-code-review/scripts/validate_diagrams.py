#!/usr/bin/env python3
"""Validate that every Mermaid diagram of the generated HTML report renders.

Usage:
    python3 -I validate_diagrams.py <outside-in-review-dir> [--json]

No download, no npm: pages are rendered by a locally installed Chromium-based
browser in headless mode (Chrome, Chromium, Edge or Brave; override with
$CHROME_PATH), using the Mermaid bundle embedded in assets/vendor/. This is
exactly what a reader sees when opening the report.

Checks:
  1. static  - each <pre class="mermaid"> is extracted as the browser reads it
               (textContent); raw HTML tags inside a block are reported
               (write &lt; &gt; instead); pages with diagrams must load
               assets/vendor/mermaid.min.js and assets/diagrams.js.
  2. render  - `chrome --headless --dump-dom` loads each page; diagrams.js
               writes data-render="ok|error" on every figure, read back here.
  3. coverage - architecture.html holds C4Context, C4Container, C4Component and
               classDiagram; each flow-*.html holds a sequenceDiagram.

Exit code: 0 all good, 1 at least one failure, 2 no headless browser found.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

REQUIRED = {
    "architecture.html": ["C4Context", "C4Container", "C4Component", "classDiagram"],
    "flow-*.html": ["sequenceDiagram"],
}
BROWSERS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
    "microsoft-edge", "brave-browser", "chrome",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


class SourceParser(HTMLParser):
    """Collects mermaid blocks (as textContent) and script srcs."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[dict] = []
        self.scripts: list[str] = []
        self._depth = 0
        self._buf: list[str] = []
        self._tags: list[str] = []
        self._line = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and a.get("src"):
            self.scripts.append(a["src"])
        if self._depth:
            self._tags.append(tag)
            if tag == "pre":
                self._depth += 1
            return
        if tag == "pre" and "mermaid" in (a.get("class") or "").split():
            self._depth, self._buf, self._tags = 1, [], []
            self._line = self.getpos()[0]

    def handle_endtag(self, tag):
        if self._depth and tag == "pre":
            self._depth -= 1
            if not self._depth:
                src = "".join(self._buf).strip()
                self.blocks.append({"line": self._line, "type": diagram_type(src),
                                    "stray_tags": sorted(set(self._tags))})

    def handle_data(self, data):
        if self._depth:
            self._buf.append(data)


class RenderedParser(HTMLParser):
    """Reads the data-render* attributes written by diagrams.js."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.page: dict = {}
        self.figures: list[dict] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.page = a
        if "data-render" in a:
            self.figures.append(a)


def diagram_type(source: str) -> str:
    for raw in source.splitlines():
        line = raw.strip()
        if line and not line.startswith("%%") and line != "---":
            return line.split()[0]
    return "empty"


def find_browser() -> str | None:
    for cand in [os.environ.get("CHROME_PATH"), *BROWSERS]:
        if not cand:
            continue
        path = cand if os.path.isabs(cand) else shutil.which(cand)
        if path and os.path.exists(path):
            return path
    return None


def render_page(browser: str, page: Path) -> RenderedParser | str:
    with tempfile.TemporaryDirectory() as profile:
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-first-run",
               "--no-default-browser-check", "--disable-extensions",
               f"--user-data-dir={profile}", "--allow-file-access-from-files",
               "--virtual-time-budget=60000", "--dump-dom", page.resolve().as_uri()]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            return "headless browser timed out"
    if proc.returncode != 0 and not proc.stdout:
        return (proc.stderr.strip().splitlines() or ["browser failed"])[-1]
    parsed = RenderedParser()
    parsed.feed(proc.stdout)
    return parsed


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    root = Path(args[0] if args else "outside-in-review")
    # print.html is assembled from the other pages by export_pdf.py: skip it.
    pages = sorted(p for p in root.glob("*.html") if p.name != "print.html")
    if not pages:
        print(f"No HTML pages in {root}", file=sys.stderr)
        return 1

    browser = find_browser()
    results: list[dict] = []
    problems: list[str] = []
    types_by_page: dict[str, list[str]] = {}

    if not (root / "assets/vendor/mermaid.min.js").exists():
        problems.append("assets/vendor/mermaid.min.js missing: copy <SKILL_DIR>/assets/vendor/")

    for page in pages:
        src = SourceParser()
        src.feed(page.read_text(encoding="utf-8"))
        types_by_page[page.name] = [b["type"] for b in src.blocks]
        if not src.blocks:
            continue
        for needed in ("assets/vendor/mermaid.min.js", "assets/diagrams.js"):
            if needed not in src.scripts:
                problems.append(f"{page.name}: missing <script src=\"{needed}\" defer>")

        rendered = render_page(browser, page) if browser else None
        if isinstance(rendered, str):
            problems.append(f"{page.name}: {rendered}")
            rendered = None
        elif rendered is not None and "data-diagrams" not in rendered.page:
            problems.append(f"{page.name}: diagrams.js did not finish (check the script tags)")

        for i, block in enumerate(src.blocks):
            entry = {"file": page.name, "line": block["line"], "type": block["type"]}
            fig = rendered.figures[i] if rendered and i < len(rendered.figures) else None
            if block["stray_tags"]:
                entry.update(ok=False, detail="raw HTML tag(s) inside mermaid block: "
                             + ", ".join(f"<{t}>" for t in block["stray_tags"])
                             + " (escape as &lt; &gt;)")
            elif browser is None:
                entry.update(ok=None, detail="no headless browser found: not validated")
            elif fig is None:
                entry.update(ok=False, detail="not rendered")
            elif fig.get("data-render") == "ok":
                entry.update(ok=True, detail="rendered")
            else:
                entry.update(ok=False, detail=fig.get("data-render-error") or "render error")
            results.append(entry)

    for pattern, needed in REQUIRED.items():
        matches = [p.name for p in pages if p.match(pattern)]
        if not matches:
            problems.append(f"coverage: no page matching {pattern}")
        for name in matches:
            missing = [t for t in needed if t not in types_by_page.get(name, [])]
            if missing:
                problems.append(f"coverage: {name} lacks {', '.join(missing)}")

    if as_json:
        print(json.dumps({"browser": browser, "diagrams": results, "problems": problems}, indent=2))
    else:
        print(f"browser: {browser or 'none found (set CHROME_PATH)'}")
        for r in results:
            mark = {True: "OK  ", False: "FAIL", None: "SKIP"}[r["ok"]]
            print(f"{mark} {r['file']}:{r['line']} [{r['type']}] {r['detail']}")
        for p in problems:
            print(f"FAIL {p}")
        ok = sum(r["ok"] is True for r in results)
        print(f"\n{ok}/{len(results)} diagrams rendered, {len(problems)} other problem(s)")

    if any(r["ok"] is False for r in results) or problems:
        return 1
    return 2 if browser is None else 0


if __name__ == "__main__":
    sys.exit(main())
