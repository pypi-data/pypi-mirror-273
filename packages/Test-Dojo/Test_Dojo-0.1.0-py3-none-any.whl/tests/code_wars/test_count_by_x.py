def count_by(x, n):
    return [i * x for i in range(1, n + 1)]


def test_count_by():
    assert count_by(1, 5) == [1, 2, 3, 4, 5]
    assert count_by(2, 4) == [2, 4, 6, 8]
