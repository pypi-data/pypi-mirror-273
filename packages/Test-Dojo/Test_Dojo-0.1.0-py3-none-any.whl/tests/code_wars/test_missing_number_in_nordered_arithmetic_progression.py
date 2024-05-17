def find(an: [int]) -> int:
    progression = sorted(an)
    d = progression[1] - progression[0]
    if d == 0:
        return progression[0]

    for i in range(1, len(progression)):
        if progression[i] - progression[i - 1] != d:
            return progression[i - 1] + d

def test_1():
    assert find([1, 1, 1, 1] ) == 1

def test_2():
    assert find([1, 2, 4, 5]) == 3

def test_3():
    assert find([1, 4, 5, 2]) == 3

def test_4():
    assert find([5, -1, 0, 3, 4, -3, 2, -2]) == 1

def test_5():
    assert find([2, -2, 8, -8, 4, -4, 6, -6]) == 0

