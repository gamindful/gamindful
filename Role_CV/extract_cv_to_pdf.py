"""Extract multilingual CV HTML to PDF by language."""

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os
import tempfile


def extract_cv_to_pdf(language: str, output_path: str = None) -> str:
    """
    Extract CV information in specified language and convert to PDF.
    
    Args:
        language: Language code - "en", "de", or "es"
        output_path: Optional path for output PDF. Defaults to gama_cv_{language}.pdf
    
    Returns:
        Path to the generated PDF file
    
    Raises:
        ValueError: If language is not in ["en", "de", "es"]
        FileNotFoundError: If gama_cv.html is not found
    """
    if language not in ["en", "de", "es"]:
        raise ValueError(f"Language must be 'en', 'de', or 'es', got '{language}'")
    
    htmlfile = "gama_cv_MLE"
    html_path = f"{htmlfile}.html"
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"{html_path} not found in current directory")
    
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    data_attr = f"data-{language}"
    
    for element in soup.find_all(True):
        if element.has_attr(data_attr):
            element.string = element[data_attr]
    
    for tag in soup.find_all(["script"]):
        tag.decompose()
    
    language_toggle = soup.find(class_="language-toggle")
    if language_toggle:
        language_toggle.decompose()
    
    # Convert relative image paths to absolute file:// URLs
    base_dir = os.path.abspath(os.path.dirname(html_path))
    for img in soup.find_all("img"):
        if img.has_attr("src"):
            src = img["src"]
            if not src.startswith("http") and not src.startswith("file://"):
                img["src"] = f"file://{os.path.join(base_dir, src)}"
    
    # Use the container's 40px padding as the page margin so every PDF page
    # gets the same whitespace as the container in the HTML version
    style_tag = soup.find("style")
    if style_tag:
        margin_css = """
        @page {
            margin: 40px;
        }
        body {
            margin: 0 !important;
            padding: 0 !important;
        }
        .container {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        """
        style_tag.append(margin_css)
    
    cleaned_html = soup.prettify()
    
    if output_path is None:
        output_path = f"{htmlfile}_{language}.pdf"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
        tmp.write(cleaned_html)
        tmp_path = tmp.name
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{os.path.abspath(tmp_path)}", wait_until="networkidle")
            # Wait for web fonts (Font Awesome icons) so the mail/ORCID/
            # LinkedIn/GitHub logos render in the PDF instead of blank boxes
            page.evaluate("document.fonts.ready")
            page.pdf(path=output_path, format="Letter", margin={"top": "40px", "bottom": "40px", "left": "40px", "right": "40px"})
            browser.close()
    finally:
        os.unlink(tmp_path)
    
    return output_path


if __name__ == "__main__":
    for lang in ["en", "de", "es"]:
#def main(lang: str):
        try:
            pdf_path = extract_cv_to_pdf(lang)
            print(f"✓ Generated {pdf_path}")
        except Exception as e:
            print(f"✗ Error generating {lang} PDF: {e}")
