def last_chair(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n >= 3:
        return n - 1


def test_last_chair():
    assert last_chair(1) == 1
    assert last_chair(2) == 2
    assert last_chair(3) == 2
    assert last_chair(4) == 3


def last_chair(n):
    if n < 5:
        return n // 2 + 1
    return n - 1


def test_1():
    assert last_chair(1) == 1


def test_2():
    assert last_chair(2) == 2


def test_3():
    assert last_chair(3) == 2


def test_4():
    assert last_chair(4) == 3


def test_5():
    assert last_chair(5) == 4
