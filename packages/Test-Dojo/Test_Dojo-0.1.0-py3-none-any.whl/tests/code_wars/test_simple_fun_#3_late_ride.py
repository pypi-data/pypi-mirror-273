def late_ride(n: int) -> int:
    h1, h2, m1, m2 = [0, 0, 0, 0]
    if n % 60 > 9:
        m1 = (n % 60 - n % 10) / 10
        m2 = n % 60 - n // 10 * 10
    else:
        m2 = n % 60
    return h1 + h2 + m1 + m2


def test_zero():
    assert late_ride(0) == 0


def test_8_minutes():
    # 00:08 (0+0+0+8=8)
    assert late_ride(8) == 8


def test_23_minutes():
    assert late_ride(23) == 5


def test_204_minutes():
    assert late_ride(204) == 4
