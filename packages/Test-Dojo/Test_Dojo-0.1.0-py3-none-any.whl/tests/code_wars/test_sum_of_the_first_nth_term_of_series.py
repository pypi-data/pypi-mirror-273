def series_sum(n):
    lst = [1.00]
    divisor = 4
    if n > 0:
        for i in range(1, n):
            lst.append(1 / divisor)
            divisor += 3
        if len(str(round(sum(lst), 2))) == 3:
            return str(round(sum(lst), 2)) + "0"
        return str(round(sum(lst), 2))
    return "0.00"


def test_():
    assert series_sum(1) == "1.00"
