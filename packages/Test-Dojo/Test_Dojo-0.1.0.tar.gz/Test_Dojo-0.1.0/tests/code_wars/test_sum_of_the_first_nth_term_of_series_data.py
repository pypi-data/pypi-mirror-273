def series_sum(n):
    numbers = []
    i = 1
    if n == 0:
        return "0.00"
    elif n == 1:
        return "1.00"
    else:
        while len(numbers) < n:
            numbers.append(1 / (1 + (i - 1) * 3))
            i = i + 1
        if len(str(round(sum(numbers), 2))) < 4:
            return str(round(sum(numbers), 2)) + "0"
        return str(round(sum(numbers), 2))


def test_series_sum():
    assert series_sum(0) == 0.00
    assert series_sum(1) == 1.00
    assert series_sum(2) == 1.25
    assert series_sum(3) == 1.39
