import os
import requests
from bs4 import BeautifulSoup
import validators
import json

TEST_OUTPUT_DIR = "test_output"


def setup_module():
    if not os.path.exists(TEST_OUTPUT_DIR):
        os.makedirs(TEST_OUTPUT_DIR)


def teardown_module():
    for filename in os.listdir(TEST_OUTPUT_DIR):
        file_path = os.path.join(TEST_OUTPUT_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def scrape_website_data(url, output_file):
    if not validators.url(url):
        return False

    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.RequestException:
        return False

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.text if soup.title else None
    paragraphs = [p.text for p in soup.find_all("p")]
    links = [a["href"] for a in soup.find_all("a", href=True)]

    data = {"title": title, "paragraphs": paragraphs, "links": links}
    with open(output_file, "w") as json_file:
        json.dump(data, json_file, indent=4)

    return data


if __name__ == "__main__":
    url = "https://www.youtube.com/"
    output_file = os.path.join(TEST_OUTPUT_DIR, "output.json")

    scrape_website_data(url, output_file)
    print("Information scraped and saved to", output_file)
