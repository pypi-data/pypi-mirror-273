def row_sum_odd_numbers(n):
    return n**3


def test_row_sum_odd_numbers():
    assert row_sum_odd_numbers(1) == 1
    assert row_sum_odd_numbers(2) == 8
    assert row_sum_odd_numbers(3) == 27
    assert row_sum_odd_numbers(4) == 64
