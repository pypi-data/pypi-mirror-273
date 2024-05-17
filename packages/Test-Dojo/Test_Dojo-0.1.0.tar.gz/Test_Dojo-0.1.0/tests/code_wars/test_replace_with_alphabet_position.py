def alphabet_position(text: str) -> str:
    lst = []
    for i in range(len(text)):
        if 96 < ord(text[i].lower()) < 123:
            lst.append(ord(text[i].lower()) - 96)
    return " ".join(str(e) for e in lst)


def test_empty():
    assert alphabet_position("") == ""


def test_a():
    assert alphabet_position("a") == "1"


def test_aa():
    assert alphabet_position("aa") == "1 1"
