def tribonacci(signature, n):
    if n <= 3:
        return signature[:n]
    for i in range(n - len(signature)):
        signature.append(sum(signature[-3:]))
    return signature


def test_tribonacci():
    assert tribonacci([1, 2, 3], 0) == []
    assert tribonacci([1, 1, 1], 3) == [1, 1, 1]
    assert tribonacci([1, 1, 1], 4) == [1, 1, 1, 3]
    assert tribonacci([1, 1, 1], 5) == [1, 1, 1, 3, 5]
    assert tribonacci([0, 0, 1], 10) == [0, 0, 1, 1, 2, 4, 7, 13, 24, 44]
