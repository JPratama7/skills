#!/usr/bin/env python3
"""Validate a docs-styler output file against the delivery contract.

Usage: python3 check_html.py <file.html>
Exit 0 and print nothing on success; exit 1 with one problem per line.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class DocScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.ids = set()
        self.anchors = []
        self.external = []
        self.title_text = []
        self._in_title = False
        self._in_style = False
        self.style_text = []
        self.html_attrs = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if tag == "html":
            self.html_attrs = a
        if "id" in a:
            self.ids.add(a["id"])
        for attr in ("href", "src", "action", "data", "poster"):
            v = a.get(attr, "")
            if attr == "href" and v.startswith("#"):
                self.anchors.append(v[1:])
            elif re.match(r"(https?:)?//", v) or v.startswith("http"):
                self.external.append(f"<{tag} {attr}={v!r}>")
        if tag == "title":
            self._in_title = True
        if tag == "style":
            self._in_style = True

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_title:
            self.title_text.append(data)
        if self._in_style:
            self.style_text.append(data)


def check(path: Path):
    problems = []
    text = path.read_text(encoding="utf-8", errors="replace")

    if not re.search(r"<!doctype\s+html", text, re.I):
        problems.append("missing <!DOCTYPE html>")

    scan = DocScan()
    scan.feed(text)
    css = "\n".join(scan.style_text)

    if "style" not in scan.tags:
        problems.append("no <style> element — CSS must be inlined")
    elif not css.strip():
        problems.append("<style> element is empty")
    if scan.tags.count("style") > 1:
        problems.append("more than one <style> element — keep CSS in a single block")

    if "@media print" not in css:
        problems.append("no @media print rules — document is not print-ready")
    if "@import" in css:
        problems.append("CSS contains @import — external resources are not allowed")
    for m in re.finditer(r"url\(\s*['\"]?(https?:)?//", css):
        problems.append(f"CSS url() points outside the file near offset {m.start()}")

    if "link" in scan.tags:
        problems.append("<link> element found — no external resources allowed")
    if "script" in scan.tags:
        problems.append("<script> element found — documents ship without JavaScript")

    for ref in scan.external:
        problems.append(f"external resource reference: {ref}")

    if not "".join(scan.title_text).strip():
        problems.append("missing or empty <title>")
    if "lang" not in scan.html_attrs:
        problems.append("<html> missing lang attribute")

    meta = "meta" in scan.tags
    if not (meta and re.search(r'<meta[^>]+charset', text, re.I)):
        problems.append("missing <meta charset>")
    if not re.search(r'<meta[^>]+name=["\']viewport', text, re.I):
        problems.append("missing viewport <meta>")

    for anchor in scan.anchors:
        if anchor and anchor not in scan.ids:
            problems.append(f'dead anchor: href="#{anchor}" has no matching id')

    return problems


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"not a file: {path}", file=sys.stderr)
        sys.exit(2)
    problems = check(path)
    if problems:
        for p in problems:
            print(p)
        sys.exit(1)


if __name__ == "__main__":
    main()
