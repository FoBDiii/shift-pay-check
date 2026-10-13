#!/usr/bin/env python3
"""Turn web/shift-pay-check.html (the Claude artifact page) into the Android app's
offline index.html: wraps it in a full document and swaps CDN/Google Fonts links
for the copies bundled in app/src/main/assets."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "web" / "shift-pay-check.html"
OUT = ROOT / "app" / "src" / "main" / "assets" / "index.html"
FONTS_CSS = ROOT / "app" / "src" / "main" / "assets" / "fonts" / "fonts.css"

FACES = [
    ("Bricolage Grotesque", 600, "bricolage-grotesque-latin-600-normal.woff2"),
    ("Bricolage Grotesque", 800, "bricolage-grotesque-latin-800-normal.woff2"),
    ("Atkinson Hyperlegible", 400, "atkinson-hyperlegible-latin-400-normal.woff2"),
    ("Atkinson Hyperlegible", 700, "atkinson-hyperlegible-latin-700-normal.woff2"),
    ("JetBrains Mono", 500, "jetbrains-mono-latin-500-normal.woff2"),
    ("JetBrains Mono", 700, "jetbrains-mono-latin-700-normal.woff2"),
]

HEAD = """<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px system-ui,-apple-system,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head><body>
"""


def main() -> None:
    html = SRC.read_text(encoding="utf-8")
    html = re.sub(r'<link rel="preconnect"[^>]*>\s*', "", html)
    html = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*">',
                  '<link rel="stylesheet" href="fonts/fonts.css">', html)
    html = html.replace("https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js", "lib/jspdf.umd.min.js")
    html = html.replace("https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js",
                        "lib/jspdf.plugin.autotable.min.js")
    assert "cdnjs.cloudflare.com" not in html and "fonts.googleapis.com" not in html, "unbundled remote resource left"
    OUT.write_text(HEAD + html + "\n</body></html>\n", encoding="utf-8")

    css = "".join(
        f'@font-face{{font-family:"{fam}";font-style:normal;font-weight:{w};font-display:swap;src:url("{f}") format("woff2")}}\n'
        for fam, w, f in FACES
    )
    FONTS_CSS.write_text(css, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} and {FONTS_CSS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
