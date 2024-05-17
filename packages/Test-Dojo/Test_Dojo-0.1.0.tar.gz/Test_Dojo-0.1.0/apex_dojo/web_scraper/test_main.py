import os

from apex_dojo.web_scraper.main import scrape_website_data


def test_valid_input() -> None:
    url = "http://example.com"
    output_file = "test_output/output.json"
    assert scrape_website_data(url, output_file) is not None
    assert os.path.exists(output_file)


def test_invalid_input() -> None:
    url = "invalid_url"
    output_file = "test_output/output.json"
    assert scrape_website_data(url, output_file) is False


def test_empty_input() -> None:
    url = ""
    output_file = "test_output/output.json"
    assert scrape_website_data(url, output_file) is False


def test_data_type() -> None:
    url = "http://example.com"
    output_file = "test_output/output.json"
    assert type(scrape_website_data(url, output_file)) == str
