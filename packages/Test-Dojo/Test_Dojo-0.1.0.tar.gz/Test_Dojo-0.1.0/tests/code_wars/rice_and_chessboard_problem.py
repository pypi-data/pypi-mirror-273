def squares_needed(grains):
    lst = []
    i = 0
    while sum(lst) < grains:
        lst.append(2**i)
        i = i + 1
    return len(lst)


def test_1():
    assert squares_needed(0) == 0


def test_2():
    assert squares_needed(1) == 1


#
def test_3():
    assert squares_needed(2) == 2


def test_4():
    assert squares_needed(3) == 2


def test_5():
    assert squares_needed(4) == 3
