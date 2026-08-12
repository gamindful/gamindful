"""Render the email-signature logos to transparent PNGs.

Font Awesome supplies ORCID / LinkedIn / GitHub; Font Awesome has no Databricks
icon, so that one comes from the local databricks.svg (Simple Icons).

Edit COLORS and re-run to recolor the set. Output is 112px (4x) so the icons
stay crisp on retina displays when shown at 24px in a mail client.
"""

import os
import re
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SIZE = 112       # PNG canvas, px
GLYPH = 96       # glyph size within the canvas, px

# Each logo in its own brand colour: black, green, blue, red.
COLORS = {
    "github":     "#181717",
    "orcid":      "#A6CE39",
    "linkedin":   "#0A66C2",
    "databricks": "#FF3621",
}

FA_CLASS = {
    "github":   "fab fa-github",
    "orcid":    "fab fa-orcid",
    "linkedin": "fab fa-linkedin",
}


def databricks_svg(color):
    """Inline the Simple Icons Databricks path, recoloured."""
    svg = open(os.path.join(HERE, "databricks.svg"), encoding="utf-8").read()
    path = re.search(r'<path\s+d="([^"]+)"', svg).group(1)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
            f'width="{GLYPH}" height="{GLYPH}" fill="{color}">'
            f'<path d="{path}"/></svg>')


def build_page():
    boxes = []
    for name, color in COLORS.items():
        inner = (databricks_svg(color) if name == "databricks"
                 else f'<i class="{FA_CLASS[name]}" style="color:{color}"></i>')
        boxes.append(f'<div class="box" id="{name}">{inner}</div>')
    return f"""<!doctype html><html><head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
body {{ margin:0; background:transparent }}
.box {{ width:{SIZE}px; height:{SIZE}px; display:flex; align-items:center; justify-content:center }}
i {{ font-size:{GLYPH}px; line-height:1 }}
</style></head><body>{''.join(boxes)}</body></html>"""


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(build_page(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        for name, color in COLORS.items():
            out = os.path.join(HERE, f"{name}.png")
            page.locator(f"#{name}").screenshot(path=out, omit_background=True)
            print(f"OK  {name}.png  {color}")
        browser.close()
