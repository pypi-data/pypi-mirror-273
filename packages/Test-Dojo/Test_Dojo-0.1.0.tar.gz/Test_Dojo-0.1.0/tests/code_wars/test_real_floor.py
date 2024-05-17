def get_real_floor(n):
    if n <= 0:
        return n
    elif n <= 12:
        return n - 1
    return n - 2


def test_get_real_floor():
    assert get_real_floor(0) == 0
    assert get_real_floor(1) == 0
    assert get_real_floor(2) == 1
    assert get_real_floor(15) == 13
