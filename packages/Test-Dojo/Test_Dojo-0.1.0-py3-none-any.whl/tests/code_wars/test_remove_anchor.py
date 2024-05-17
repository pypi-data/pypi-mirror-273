def remove_url_anchor(url: str) -> str:
    return url.split("#")[0]


def test_():
    assert remove_url_anchor("www.example.com#123") == "www.example.com"
