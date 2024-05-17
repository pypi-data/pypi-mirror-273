# https://codingdojo.org/kata/Bowling/


def bowling(pins: list) -> int:
    total = []
    check = 1
    for i, pin in enumerate(pins):
        if (
            i == len(pins) - 1
            and pins[-2] + pins[-3] == 10
            or i == len(pins) - 1
            and pins[-3] == 10
            or i == len(pins) - 2
            and pins[-3] == 10
        ):
            pass
        else:
            total.append(pin)

            if i % 2 == check and pin + pins[i - 1] == 10:
                total.append(pins[i + 1])

            if pin == 10:
                total.append(pins[i + 1] + pins[i + 2])
                if check == 1:
                    check = 0
                else:
                    check = 1

    return sum(total)


def test_bonus_after_strike():
    assert (
        bowling([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 1, 1]) == 12
    )


def test_mix():
    assert bowling([10, 5, 4, 10, 6, 4, 0, 8, 1, 2, 0, 0, 7, 3, 10, 10, 8, 2]) == 137


def test_mix_vol2():
    assert bowling([10, 5, 4, 10, 6, 4, 0, 8, 1, 2, 0, 0, 7, 3, 10, 10, 8, 1]) == 136


def test_all_spare():
    assert (
        bowling([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]) == 150
    )


def test_bonus_after_spare():
    assert (
        bowling([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 1]) == 11
    )


def test_spare_after_odd_number_of_strikes():
    assert bowling([10, 10, 10, 9, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 91


def test_all_miss():
    assert bowling([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0


def test_one_miss_in_each_frame():
    assert bowling([9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0]) == 90


def test_one_score():
    assert bowling([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1


def test_four_spare():
    assert bowling([9, 1, 1, 0] * 5) == 60


def test_one_spare():
    assert bowling([1, 9, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 12
    assert bowling([0, 0, 0, 0, 1, 9, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 12


def test_one_strike():
    assert bowling([10, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 14


def test_nine_strikes():
    assert bowling([10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0]) == 240


def test_bonus_strike_after_spare():
    assert (
        bowling([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 10]) == 20
    )


def test_bonus_strike_after_strike():
    assert (
        bowling([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10])
        == 30
    )


def test_all_strikes():
    assert bowling([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]) == 300
