def xo(s: str) -> bool:
    return (s.lower()).count("x") == (s.lower()).count("o")


def test_1():
    assert xo("x") == False


def test_2():
    assert xo("xo") == True


def test_3():
    assert xo("xxoooohfhf") == False


def test_4():
    assert xo("fhsgsgs") == True


def test_5():
    assert xo("XO") == True


def test_6():
    assert xo("xxXooo") == True
