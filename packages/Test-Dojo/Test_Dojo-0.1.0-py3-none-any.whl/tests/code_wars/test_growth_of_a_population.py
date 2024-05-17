def nb_year(p0: int, percent: float, aug: int, p: int) -> int:
    years_left = 0
    while p0 < p:
        p0 = int(p0 + p0 * (percent / 100)) + aug
        years_left += 1

    return years_left


def test_nb_year():
    assert nb_year(1500, 5, 100, 5000) == 15
    assert nb_year(1500000, 2.5, 10000, 2000000) == 10
    assert nb_year(1500000, 0.25, 1000, 2000000) == 94
    assert nb_year(0, 0, 1, 4) == 4
