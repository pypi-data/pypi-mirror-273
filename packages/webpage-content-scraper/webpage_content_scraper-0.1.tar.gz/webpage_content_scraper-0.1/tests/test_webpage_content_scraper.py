import pytest
from bs4 import BeautifulSoup
from unittest.mock import MagicMock, patch
from webpage_content_scraper import _get_reader_content, fetch_page_content, Formats


def _generate_reader_content_html(content):
    return f"""<!DOCTYPE html><html platform="macosx" lang="en-US" dir="ltr"><head>
    <title id="reader-title"></title>
    <meta http-equiv="Content-Security-Policy" content="default-src chrome:; img-src data: *; media-src *; object-src 'none'">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type">
    <meta name="viewport" content="width=device-width; user-scalable=0">
    <link rel="stylesheet" href="chrome://global/skin/aboutReader.css" type="text/css">
    <link rel="localization" href="toolkit/about/aboutReader.ftl">
    <link rel="localization" href="toolkit/branding/brandings.ftl">
  <link rel="stylesheet" href="chrome://global/skin/narrate.css"></head>

  <body class="light sans-serif" style="--font-size: 20px; --content-width: 30em;">
    <div class="top-anchor"></div>

    <div id="toolbar" class="toolbar-container">
      <div class="toolbar reader-toolbar">
        <div class="reader-controls">
          <button class="close-button toolbar-button" aria-labelledby="toolbar-close" data-telemetry-id="reader-close">
            <span class="hover-label" id="toolbar-close" data-l10n-id="about-reader-toolbar-close">Close Reader View</span>
          </button>
          <ul class="dropdown style-dropdown">
            <li>
              <button class="dropdown-toggle toolbar-button style-button" aria-labelledby="toolbar-type-controls" data-telemetry-id="reader-type-controls">
                <span class="hover-label" id="toolbar-type-controls" data-l10n-id="about-reader-toolbar-type-controls">Type controls</span>
              </button>
            </li>
            <li class="dropdown-popup">
              <div class="dropdown-arrow"></div>
              <div class="font-type-buttons radiorow"><input id="radio-itemsans-serif-button" type="radio" class="radio-button" name="font-type"><label for="radio-itemsans-serif-button" class="sans-serif-button" data-l10n-id="about-reader-font-type-sans-serif" checked="true">Sans-serif</label><input id="radio-itemserif-button" type="radio" class="radio-button" name="font-type"><label for="radio-itemserif-button" class="serif-button" data-l10n-id="about-reader-font-type-serif">Serif</label></div>
              <div class="font-size-buttons buttonrow">
                <button class="minus-button" data-l10n-id="about-reader-toolbar-minus" title="Decrease Font Size"></button>
                <span class="font-size-value">5</span>
                <button class="plus-button" data-l10n-id="about-reader-toolbar-plus" title="Increase Font Size"></button>
              </div>
              <div class="content-width-buttons buttonrow">
                <button class="content-width-minus-button" data-l10n-id="about-reader-toolbar-contentwidthminus" title="Decrease Content Width"></button>
                <span class="content-width-value">3</span>
                <button class="content-width-plus-button" data-l10n-id="about-reader-toolbar-contentwidthplus" title="Increase Content Width"></button>
              </div>
              <div class="line-height-buttons buttonrow">
                <button class="line-height-minus-button" data-l10n-id="about-reader-toolbar-lineheightminus" title="Decrease Line Height"></button>
                <span class="line-height-value">4</span>
                <button class="line-height-plus-button" data-l10n-id="about-reader-toolbar-lineheightplus" title="Increase Line Height"></button>
              </div>
              <div class="color-scheme-buttons radiorow"><input id="radio-itemlight-button" type="radio" class="radio-button" name="color-scheme"><label for="radio-itemlight-button" class="light-button" data-l10n-id="about-reader-color-scheme-light" title="Color Scheme Light">Light</label><input id="radio-itemdark-button" type="radio" class="radio-button" name="color-scheme"><label for="radio-itemdark-button" class="dark-button" data-l10n-id="about-reader-color-scheme-dark" title="Color Scheme Dark">Dark</label><input id="radio-itemsepia-button" type="radio" class="radio-button" name="color-scheme"><label for="radio-itemsepia-button" class="sepia-button" data-l10n-id="about-reader-color-scheme-sepia" title="Color Scheme Sepia">Sepia</label><input id="radio-itemauto-button" type="radio" class="radio-button" name="color-scheme"><label for="radio-itemauto-button" class="auto-button" data-l10n-id="about-reader-color-scheme-auto" checked="true" title="Color Scheme Auto">Auto</label></div>
            </li>
          </ul>
        <ul class="dropdown narrate-dropdown"><li><button class="dropdown-toggle toolbar-button narrate-toggle" data-telemetry-id="reader-listen" aria-label="Listen (N)" hidden=""><span class="hover-label">Listen (N)</span></button></li><li class="dropdown-popup"><div class="narrate-row narrate-control"><button class="narrate-skip-previous" disabled="" title="Back"></button><button class="narrate-start-stop" title="Start (N)"></button><button class="narrate-skip-next" disabled="" title="Forward"></button></div><div class="narrate-row narrate-rate"><input class="narrate-rate-input" value="0" step="5" max="100" min="-100" type="range" title="Speed"></div><div class="narrate-row narrate-voices"><div class="voiceselect voice-select"><button class="select-toggle" aria-controls="voice-options">
      <span class="label">Voice:</span> <span class="current-voice"></span>
    </button>
    <div class="options" id="voice-options" role="listbox"></div></div></div><div class="dropdown-arrow"></div></li></ul></div>
      </div>
    </div>

    <div class="container" style="--line-height: 1.6em;">
      <div class="header reader-header">
        <a class="domain reader-domain"></a>
        <div class="domain-border"></div>
        <h1 class="reader-title"></h1>
        <div class="credits reader-credits"></div>
        <div class="meta-data">
          <div class="reader-estimated-time"></div>
        </div>
      </div>

      <hr>

      <div class="content">
        <div class="moz-reader-content">{content}</div>
      </div>

      <div>
        <div class="reader-message"></div>
      </div>
      <div aria-owns="toolbar"></div>
    </div>
  

</body></html>
"""

# Test _get_reader_content function
def test_get_reader_content_with_reader_content():
    html = _generate_reader_content_html("<h1>Test content</h1>")
    reader_content = _get_reader_content(html)
    assert reader_content is not None
    assert reader_content.find().text == "Test content"


def test_get_reader_content_without_reader_content():
    html = _generate_reader_content_html('')
    reader_content = _get_reader_content(html)
    assert reader_content is None


# Test fetch_page_content function
@patch("webpage_content_scraper.sync_playwright")
@patch("webpage_content_scraper._get_reader_content")
def test_fetch_page_content_html(mock_get_reader_content, mock_sync_playwright):
    # Mock the Playwright context
    mock_browser = MagicMock()
    mock_page = MagicMock()
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_context
    mock_sync_playwright.return_value.__enter__.return_value = mock_context
    mock_context.firefox.launch.return_value = mock_browser
    mock_browser.new_page.return_value = mock_page

    mock_page.content.return_value = (
        _generate_reader_content_html('<article><h1>Test content</h1></article>')
    )
    mock_get_reader_content.return_value = BeautifulSoup(
        mock_page.content.return_value, "html.parser"
    )

    url = "http://example.com"
    result = fetch_page_content(url, format=Formats.HTML)

    assert '<article><h1>Test content</h1></article>' in result


@patch("webpage_content_scraper.sync_playwright")
@patch("webpage_content_scraper._get_reader_content")
def test_fetch_page_content_markdown(mock_get_reader_content, mock_sync_playwright):
    # Mock the Playwright context
    mock_browser = MagicMock()
    mock_page = MagicMock()
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_context
    mock_sync_playwright.return_value.__enter__.return_value = mock_context
    mock_context.firefox.launch.return_value = mock_browser
    mock_browser.new_page.return_value = mock_page

    mock_page.content.return_value = (
       _generate_reader_content_html('<article><h1>Test Title</h1><p>Test content.</p></article>')
    )
    mock_get_reader_content.return_value = BeautifulSoup(
        mock_page.content.return_value, "html.parser"
    )

    url = "http://example.com"
    result = fetch_page_content(url, format=Formats.MARKDOWN)

    assert "# Test Title\n\nTest content" in result


if __name__ == "__main__":
    pytest.main()
