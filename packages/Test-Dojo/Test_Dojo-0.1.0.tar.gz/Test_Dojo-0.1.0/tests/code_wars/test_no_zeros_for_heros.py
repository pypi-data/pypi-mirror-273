def no_boring_zeros(n):
    while n % 10 == 0:
        n = n / 10
    return n


def test_1():
    assert no_boring_zeros(10) == 1


def test_2():
    assert no_boring_zeros(200) == 2
