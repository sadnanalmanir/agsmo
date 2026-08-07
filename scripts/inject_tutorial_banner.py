#!/usr/bin/env python3
"""Inject a tutorial link banner into WIDOCO index HTML files under site/."""

from __future__ import annotations

from pathlib import Path

BANNER = (
    '<div style="margin:0;padding:0.85rem 1rem;background:#1f6feb;color:#fff;'
    'font-family:system-ui,sans-serif;font-size:0.95rem;text-align:center">'
    "<strong>New here?</strong> Start with the "
    '<a href="tutorial/" style="color:#fff;font-weight:700;text-decoration:underline">'
    "progressive HTML tutorial</a> "
    "(goals → plans → actions → failure), then return for the full specification."
    "</div>\n"
)


def inject(path: Path) -> bool:
    if not path.is_file():
        return False
    html = path.read_text(encoding="utf-8")
    if "progressive HTML tutorial" in html:
        return False
    lower = html.lower()
    i = lower.find("<body")
    if i == -1:
        return False
    j = html.find(">", i)
    if j == -1:
        return False
    path.write_text(html[: j + 1] + "\n" + BANNER + html[j + 1 :], encoding="utf-8")
    return True


def main() -> None:
    site = Path("site")
    for name in ("index.html", "index-en.html"):
        p = site / name
        if inject(p):
            print(f"banner injected into {name}")
        elif p.is_file():
            print(f"skip {name} (missing body or already injected)")


if __name__ == "__main__":
    main()
