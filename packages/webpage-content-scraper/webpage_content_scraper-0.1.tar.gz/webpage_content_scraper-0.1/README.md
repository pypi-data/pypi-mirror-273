# Webpage Content Scraper

[![PyPI](https://img.shields.io/pypi/v/python-webpage-content-scraper.svg)](https://pypi.org/project/python-webpage-content-scraper/)
[![Tests](https://github.com/ryan-blunden/python-webpage-content-scraper/actions/workflows/test.yml/badge.svg)](https://github.com/ryan-blunden/python-webpage-content-scraper/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/ryan-blunden/python-webpage-content-scraper?include_prereleases&label=changelog)](https://github.com/ryan-blunden/python-webpage-content-scraper/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ryan-blunden/python-webpage-content-scraper/blob/main/LICENSE)

Scrape only the content from a webpage using Firefox's reader view.

## Installation

Install this library using `pip`:
```bash
pip install webpage-content-scraper
```

Then install the Firefox browser for Playwright:

```bash
playwright install firefox
```

## Usage

Simply supply a URL and optionally, a format and timeout.

```python
from webpage_content_scraper import fetch_page_content, Formats

url = 'https://microsoft.github.io/autogen/blog/2023/10/18/RetrieveChat/'

html_content = fetch_page_content(url)
markdown_content = fetch_page_content(url, Formats.MARKDOWN)
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd python-webpage-content-scraper
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
