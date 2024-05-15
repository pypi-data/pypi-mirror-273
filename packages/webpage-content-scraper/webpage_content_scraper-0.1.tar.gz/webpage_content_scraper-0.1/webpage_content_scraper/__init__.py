import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from markdownify import MarkdownConverter


class Formats:
    MARKDOWN = "markdown"
    HTML = "html"


def _get_reader_content(html):
    soup = BeautifulSoup(html, "html.parser")
    reader_content = soup.find(class_="moz-reader-content")

    if reader_content and reader_content.find():
        return reader_content

    return None


def fetch_page_content(url, format=Formats.HTML, timeout=30):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        page.goto(f"about:reader?url={url}")

        start_time = time.time()
        reader_content = None

        while time.time() - start_time < timeout:
            html = page.content()
            reader_content = _get_reader_content(html)

            if reader_content:
                break

            time.sleep(1)

        browser.close()

        if format == Formats.MARKDOWN:
            return MarkdownConverter(heading_style="ATX", heading_level=2).convert_soup(
                reader_content
            )

        return str(reader_content)
