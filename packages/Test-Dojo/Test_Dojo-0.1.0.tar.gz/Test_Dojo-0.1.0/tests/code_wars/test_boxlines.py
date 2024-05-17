def f(x, y, z):
    # return x * (y + 1) * (z + 1) + (x + 1) * y * (z + 1) + (x + 1) * (y + 1) * z
    return 3 * (x * y * z) + 2 * (x * y + x * z + y * z) + (x + y + z)


def test_one_on_one():
    assert f(1, 1, 1) == 12


def test_only_x():
    assert f(2, 1, 1) == 20
    assert f(4, 1, 1) == 36
    assert f(6, 1, 1) == 52


def test_only_y():
    assert f(1, 2, 1) == 20
    assert f(1, 4, 1) == 36
    assert f(1, 6, 1) == 52


def test_only_z():
    assert f(1, 1, 2) == 20
    assert f(1, 1, 4) == 36
    assert f(1, 1, 6) == 52

    # def test_x_and_y():
    #     assert f(2, 2, 1) == 32
    assert f(1, 2, 3) == 46
    assert f(2, 2, 2) == 54
