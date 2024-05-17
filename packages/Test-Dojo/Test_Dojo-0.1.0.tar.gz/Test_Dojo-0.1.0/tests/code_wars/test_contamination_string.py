def contamination(text, char) -> str:
    return len(text) * str(char)


def test_empty_text():
    assert contamination("", "z") == ""


def test_empty_char():
    assert contamination("z", "") == ""


def test_empty_contamination():
    assert contamination("abc", "z") == "zzz"
