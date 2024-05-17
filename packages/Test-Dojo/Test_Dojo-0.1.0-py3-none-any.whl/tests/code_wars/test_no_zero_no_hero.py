def no_boring_zeros(n):
    if n == 0:
        return 0

    while n % 10 == 0:
        n //= 10

    return n


def test_no_boring_zeros():
    assert no_boring_zeros(0) == 0
    assert no_boring_zeros(9600) == 96
    assert no_boring_zeros(90600) == 906
