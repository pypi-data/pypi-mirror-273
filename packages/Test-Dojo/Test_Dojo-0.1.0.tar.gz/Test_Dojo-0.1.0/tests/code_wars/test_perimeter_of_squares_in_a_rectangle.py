def perimeter(n: int) -> int:
    accum = [1, 1]
    for i in range(2, n + 1):
        accum.append(accum[i - 1] + accum[i - 2])

    return sum(accum) * 4


def test_perimeter():
    assert perimeter(5) == 80
    assert perimeter(7) == 216
