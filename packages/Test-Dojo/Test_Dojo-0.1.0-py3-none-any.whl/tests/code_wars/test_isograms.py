def is_isogram(string: str) -> bool:
    string = string.lower()
    for i in string:
        if string.count(i) > 1:
            return False
    return True


def test_one():
    assert is_isogram("") == True


def test_two():
    assert is_isogram("aba") == False


def test_three():
    assert is_isogram("Aba") == False


def test_four():
    assert is_isogram("LaSfPnrSEOdqYuiJVJ") == False
