def prime_ant(n):
    lst = [2]
    coordinate = 0
    p = 2
    i = 0

    while i < n:
        if is_prime(lst[coordinate]):
            p += 1
            lst.append(p)
            coordinate += 1
            i += 1
        else:
            divisor = smallest_divisor(lst[coordinate])
            lst[coordinate] //= divisor
            lst[coordinate - 1] += divisor
            coordinate -= 1
            i += 1
    return coordinate


def is_prime(p):
    if p > 1:
        return all(p % i != 0 for i in range(2, int(p / 2) + 1))
    return False


def smallest_divisor(p):
    a = [i for i in range(2, p + 1) if p % i == 0]
    a.sort()
    return a[0]


def test_():
    assert prime_ant(2) == 2
    assert prime_ant(11) == 5
    assert prime_ant(19) == 5
