from apex_dojo.triangular_treasure import triangular


def test_triangula():
    assert triangular(1) == 1
    assert triangular(2) == 3
    assert triangular(3) == 6
    assert triangular(4) == 10
    assert triangular(5) == 15
    assert triangular(6) == 21
    assert triangular(7) == 28
    assert triangular(8) == 36
    assert triangular(9) == 45
    assert triangular(10) == 55
    assert triangular(-9) == 0
