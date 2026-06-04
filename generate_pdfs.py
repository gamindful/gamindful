#!/usr/bin/env python3
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

LANG_MAP = {
    'en': '🇬🇧',
    'de': '🇩🇪',
    'es': '🇲🇽',
}

HTML_GLOB = 'gama_cv*.html'

async def make_pdfs():
    root = Path(__file__).parent.resolve()
    html_files = sorted(root.glob(HTML_GLOB))
    if not html_files:
        print('No HTML files matching', HTML_GLOB)
        return

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        context = await browser.new_context()

        for html in html_files:
            url = html.as_uri()
            for lang, flag in LANG_MAP.items():
                page = await context.new_page()
                await page.goto(url)
                await page.wait_for_load_state('networkidle')

                # Try to call the page's language switcher; fallback to attribute copy
                try:
                    await page.evaluate(f"if(typeof switchLanguage === 'function') switchLanguage('{lang}');")
                except Exception:
                    await page.evaluate(f"document.querySelectorAll('[data-en]').forEach(el=>{{const a='data-{lang}'; if(el.hasAttribute(a)) el.textContent = el.getAttribute(a);}}); document.documentElement.lang='{lang}';")

                # Insert visible flag badge
                badge_text = f"{flag} {lang.upper()}"
                await page.evaluate("(badgeText) => {\n                    let ex = document.getElementById('pdf-export-flag');\n                    if (ex) ex.remove();\n                    const d = document.createElement('div');\n                    d.id = 'pdf-export-flag';\n                    d.textContent = badgeText;\n                    d.style.position = 'fixed';\n                    d.style.top = '12px';\n                    d.style.left = '12px';\n                    d.style.fontSize = '18px';\n                    d.style.background = 'white';\n                    d.style.padding = '6px 10px';\n                    d.style.borderRadius = '8px';\n                    d.style.boxShadow = '0 2px 8px rgba(0,0,0,0.12)';\n                    d.style.zIndex = 999999;\n                    document.body.appendChild(d);\n                }", badge_text)

                await page.wait_for_timeout(150)
                out_name = f"{html.stem}_{lang}.pdf"
                out_path = root / out_name
                await page.pdf(path=str(out_path), format='A4', print_background=True)
                print('Wrote', out_path)
                await page.close()

        await browser.close()

if __name__ == '__main__':
    asyncio.run(make_pdfs())
