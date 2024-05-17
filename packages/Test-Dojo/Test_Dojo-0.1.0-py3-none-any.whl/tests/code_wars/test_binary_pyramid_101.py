def binary_pyramid(m: int, n: int) -> str:
    total = sum([int(bin(i)[2:]) for i in range(m, n + 1)])

    return bin(total)[2:]


def test_1():
    assert binary_pyramid(0, 1) == "1"


def test_2():
    assert binary_pyramid(1, 2) == "1011"


def test_4():
    assert binary_pyramid(1, 4) == "1111010"
