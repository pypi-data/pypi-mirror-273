def get_middle(s):
    if (len(s) % 2) != 0:
        return s[len(s) // 2]
    return s[len(s) // 2 - 1] + s[len(s) // 2]


def test_1():
    assert get_middle("table") == "b"


def test_2():
    assert get_middle("book") == "oo"
