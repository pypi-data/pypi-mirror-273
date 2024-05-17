def seats_in_theater(tot_cols: int, tot_rows: int, col: int, row: int) -> int:
    return (tot_cols - (col - 1)) * (tot_rows - row)


def test_one_on_one():
    assert seats_in_theater(1, 1, 1, 1) == 0


def test():
    assert seats_in_theater(16, 11, 5, 3) == 96
